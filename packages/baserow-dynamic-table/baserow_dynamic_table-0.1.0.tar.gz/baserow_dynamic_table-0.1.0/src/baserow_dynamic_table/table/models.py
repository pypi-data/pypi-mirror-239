import csv
import itertools
import re
from collections import defaultdict
from types import MethodType
from typing import Generator, Iterable, List, Optional, Type, TypedDict, Union

from django.apps import apps
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import FieldDoesNotExist as DjangoFieldDoesNotExist
from django.db import models
from django.db.models import Field as DjangoModelFieldClass
from django.db.models import JSONField, QuerySet
from loguru import logger

from baserow_dynamic_table.core.db import MultiFieldPrefetchQuerysetMixin, specific_iterator
from baserow_dynamic_table.core.mixins import HierarchicalModelMixin, CreatedAndUpdatedOnMixin, OrderableMixin
from baserow_dynamic_table.fields.exceptions import (
    FilterFieldNotFound,
    OrderByFieldNotFound,
    OrderByFieldNotPossible,
)
from baserow_dynamic_table.fields.field_filters import (
    FILTER_TYPE_AND,
    FILTER_TYPE_OR,
    FilterBuilder,
)
from baserow_dynamic_table.fields.models import (
    CreatedOnField,
    Field,
    LastModifiedField,
)
from baserow_dynamic_table.fields.registries import FieldType, field_type_registry
from baserow_dynamic_table.table.cache import (
    get_cached_model_field_attrs,
    set_cached_model_field_attrs,
)

extract_filter_sections_regex = re.compile(r"filter__(.+)__(.+)$")
field_id_regex = re.compile(r"field_(\d+)$")

USER_TABLE_DATABASE_NAME_PREFIX = "database_table_"


def split_comma_separated_string(comma_separated_string: str) -> List[str]:
    r"""
    Correctly splits a comma separated string which can contain quoted values to include
    commas in individual items like so: 'A,"B , C",D' -> ['A', 'B , C', 'D'] or using
    backslashes to escape double quotes like so: 'A,\"B,C' -> ['A', '"B', 'C'].

    :param comma_separated_string: The string to split
    :return: A list of split items from the provided string.
    """

    # Use python's csv handler as it knows how to handle quoted csv values etc.
    # csv.reader returns an iterator, we use next to get the first split row back.
    return next(
        csv.reader(
            [comma_separated_string], delimiter=",", quotechar='"', escapechar="\\"
        )
    )


class TableModelQuerySet(MultiFieldPrefetchQuerysetMixin, models.QuerySet):

    def enhance_by_fields(self):
        """
        Enhances the queryset based on the `enhance_queryset_in_bulk` for each unique
        field type used in the table. This one will eventually call the
        `enhance_queryset` for reach field in the table. For example the `link_row`
        field adds the `prefetch_related` to prevent N queries per row. This helper
        should only be used when multiple rows are going to be fetched.

        :return: The enhanced queryset.
        :rtype: QuerySet
        """

        by_type = defaultdict(list)
        for field_object in self.model._field_objects.values():
            field_type = field_object["type"]
            by_type[field_type].append(field_object)
        for field_type, field_objects in by_type.items():
            self = field_type.enhance_queryset_in_bulk(self, field_objects)
        return self

    def _get_field_name(self, field: str) -> str:
        """
        Helper method for parsing a field name from a string
        with a possible prefix.

        :param field: The string from which the field name
            should be parsed.
        :type field: str
        :return: The field without prefix.
        :rtype: str
        """

        possible_prefix = field[:1]
        if possible_prefix in {"-", "+"}:
            return field[1:]
        else:
            return field

    def _get_field_id(self, field: str) -> Union[int, None]:
        """
        Helper method for parsing a field ID from a string.

        :param field: The string from which the field id
            should be parsed.
        :type field: str
        :return: The ID of the field or None
        :rtype: int or None
        """

        try:
            field_id = int(re.sub("[^0-9]", "", str(field)))
        except ValueError:
            field_id = None

        return field_id

    def order_by_fields_string(
            self, order_string, user_field_names=False, only_order_by_field_ids=None
    ):
        """
        Orders the query by the given field order string. This string is often
        directly forwarded from a GET, POST or other user provided parameter.
        Multiple fields can be provided by separating the values by a comma. When
        user_field_names is False the order_string must contain a comma separated
        list of field ids. The field id is extracted from the string so it can either
        be provided as field_1, 1, id_1, etc. When user_field_names is True the
        order_string is treated as a comma separated list of the actual field names,
        use quotes to wrap field names containing commas.

        :param order_string: The field ids to order the queryset by separated by a
            comma. For example `field_1,2` which will order by field with id 1 first
            and then by field with id 2 second.
        :type order_string: str
        :param user_field_names: If true then the order_string is instead treated as
        a comma separated list of actual field names and not field ids.
        :type user_field_names: bool
        :param only_order_by_field_ids: Only field ids in this iterable will be
            ordered by. Other fields not in the iterable will be ignored and not be
            filtered.
        :type only_order_by_field_ids: Optional[Iterable[int]]
        :raises OrderByFieldNotFound: when the provided field id is not found in the
            model.
        :raises OrderByFieldNotPossible: when it is not possible to order by the
            field's type.
        :return: The queryset ordered by the provided order_string.
        :rtype: QuerySet
        """

        order_by = split_comma_separated_string(order_string)

        if len(order_by) == 0:
            raise ValueError("At least one field must be provided.")

        if user_field_names:
            field_object_dict = {
                o["field"].name: o for o in self.model._field_objects.values()
            }
        else:
            field_object_dict = self.model._field_objects

        annotations = {}
        for index, order in enumerate(order_by):
            if user_field_names:
                field_name_or_id = self._get_field_name(order)
            else:
                field_name_or_id = self._get_field_id(order)

            if field_name_or_id not in field_object_dict or (
                    only_order_by_field_ids is not None
                    and field_name_or_id not in only_order_by_field_ids
            ):
                raise OrderByFieldNotFound(order)

            order_direction = "DESC" if order[:1] == "-" else "ASC"
            field_object = field_object_dict[field_name_or_id]
            field_type = field_object["type"]
            field_name = field_object["name"]
            field = field_object["field"]
            user_field_name = field_object["field"].name
            error_display_name = user_field_name if user_field_names else field_name

            if not field_object["type"].check_can_order_by(field_object["field"]):
                raise OrderByFieldNotPossible(
                    error_display_name,
                    field_type.type,
                    f"It is not possible to order by field type {field_type.type}.",
                )

            field_annotated_order_by = field_type.get_order(
                field, field_name, order_direction
            )

            if field_annotated_order_by.annotation is not None:
                annotations = {**annotations, **field_annotated_order_by.annotation}
            field_order_by = field_annotated_order_by.order
            order_by[index] = field_order_by

        order_by.append("order")
        order_by.append("id")

        return self.annotate(**annotations).order_by(*order_by)

    def filter_by_fields_object(
            self,
            filter_object,
            filter_type=FILTER_TYPE_AND,
            only_filter_by_field_ids=None,
            user_field_names=False,
    ):
        """
        Filters the query by the provided filters in the filter_object. The following
        format `filter__field_{id}__{view_filter_type}` is expected as key and multiple
        values can be provided as a list containing strings. Only the view filter types
        are allowed.

        Example: {
            'filter__field_{id}__{view_filter_type}': {value}.
        }

        In addition to that, it's also possible to directly filter on the
        `created_on` and `updated_on` fields, even if the CreatedOn and LastModified
        fields are not created. This can be done by providing
        `filter__field_created_on__{view_filter_type}` or
        `filter__field_updated_on__{view_filter_type}` as keys in the `filter_object`.

        :param filter_object: The object containing the field and filter type as key
            and the filter value as value.
        :type filter_object: object
        :param filter_type: Indicates if the provided filters are in an AND or OR
            statement.
        :type filter_type: str
        :param only_filter_by_field_ids: Only field ids in this iterable will be
            filtered by. Other fields not in the iterable will be ignored and not be
            filtered.
        :type only_filter_by_field_ids: Optional[Iterable[int]]
        :param user_field_names: If True, use field names in the filter object
            instead of ids
        :type user_field_names: bool
        :raises ValueError: Raised when the provided filer_type isn't AND or OR.
        :raises FilterFieldNotFound: Raised when the provided field isn't found in
            the model.
        :raises ViewFilterTypeDoesNotExist: when the view filter type doesn't exist.
        :raises ViewFilterTypeNotAllowedForField: when the view filter type isn't
            compatible with field type.
        :return: The filtered queryset.
        :rtype: QuerySet
        """

        if filter_type not in [FILTER_TYPE_AND, FILTER_TYPE_OR]:
            raise ValueError(f"Unknown filter type {filter_type}.")

        filter_builder = FilterBuilder(filter_type=filter_type)

        user_field_name_to_id_mapping = (
            {v["field"].name: k for k, v in self.model._field_objects.items()}
            if user_field_names
            else {}
        )

        fixed_field_instance_mapping = {
            "field_created_on": CreatedOnField(),
            "field_updated_on": LastModifiedField(),
        }

        for key, values in filter_object.items():
            filter_sections = extract_filter_sections_regex.match(key)
            if not filter_sections:
                continue

            field_name_or_id, view_filter_name = filter_sections.groups()

            if user_field_names and field_name_or_id in user_field_name_to_id_mapping:
                field_id = user_field_name_to_id_mapping[field_name_or_id]
            elif field_name_or_id in fixed_field_instance_mapping.keys():
                field_instance = fixed_field_instance_mapping[field_name_or_id]
                field_name = field_name_or_id.replace("field_", "")
            else:
                field_id_match = field_id_regex.match(field_name_or_id)
                if field_id_match:
                    field_id = int(field_id_match.group(1))
                else:
                    continue

            if field_name_or_id not in fixed_field_instance_mapping.keys():
                if field_id not in self.model._field_objects or (
                        only_filter_by_field_ids is not None
                        and field_id not in only_filter_by_field_ids
                ):
                    raise FilterFieldNotFound(
                        field_id, f"Field {field_id} does not exist."
                    )

                field_object = self.model._field_objects[field_id]
                field_instance = field_object["field"]
                field_name = field_object["name"]
                field_type = field_object["type"].type

            model_field = self.model._meta.get_field(field_name)
            view_filter_type = view_filter_type_registry.get(view_filter_name)

            if not view_filter_type.field_is_compatible(field_instance):
                raise ViewFilterTypeNotAllowedForField(
                    view_filter_name,
                    field_type,
                )

            if not isinstance(values, list):
                values = [values]

            for value in values:
                filter_builder.filter(
                    view_filter_type.get_filter(
                        field_name, value, model_field, field_instance
                    )
                )

        return filter_builder.apply_to_queryset(self)


class TableModelTrashAndObjectsManager(models.Manager):
    def get_queryset(self):
        qs = TableModelQuerySet(self.model, using=self._db)
        return qs


class TableModelManager(TableModelTrashAndObjectsManager):
    def get_queryset(self):
        return super().get_queryset().filter(trashed=False)


class FieldObject(TypedDict):
    type: FieldType
    field: Field
    name: str


class GeneratedTableModel(
    # HierarchicalModelMixin,
    models.Model
):
    """
    Mixed into Model classes which have been generated by Baserow.
    Can also be used to identify instances of generated baserow models
    like `isinstance(possible_baserow_model, GeneratedTableModel)`.
    """

    def _do_update(self, base_qs, using, pk_val, values, update_fields, forced_update):
        """
        We override this method to prevent safe and bulk save queries from setting
        TSV field values as they never need to as we want to manage these in a
        background job.
        """

        if update_fields is not None:
            update_fields = [f for f in update_fields if TSV_FIELD_PREFIX not in f]
        else:
            update_fields = None
        return super()._do_update(
            base_qs, using, pk_val, values, update_fields, forced_update
        )

    @classmethod
    def get_parent(cls):
        return cls.baserow_table

    @classmethod
    def get_root(cls):
        return cls.baserow_table.get_root()

    @classmethod
    def fields_requiring_refresh_after_insert(cls):
        return [
            f.attname
            for f in cls._meta.fields
            if getattr(f, "requires_refresh_after_insert", False)
               # There is a bug in Django where db_returning fields do not have their
               # from_db_value function applied after performing and INSERT .. RETURNING
               # Instead for now we force a refresh to ensure these fields are converted
               # from their db representations correctly.
               or isinstance(f, JSONField) and f.db_returning
        ]

    @classmethod
    def fields_requiring_refresh_after_update(cls):
        return [
            f.attname
            for f in cls._meta.fields
            if getattr(f, "requires_refresh_after_update", False)
        ]

    @classmethod
    def get_field_object(cls, field_name: str, include_trash: bool = False):
        field_objects = cls.get_field_objects(include_trash)

        try:
            return next(filter(lambda f: f["name"] == field_name, field_objects))
        except StopIteration:
            raise ValueError(f"Field {field_name} not found.")

    @classmethod
    def get_field_objects(cls, include_trash: bool = False):
        field_objects = cls._field_objects.values()
        if include_trash:
            field_objects = itertools.chain(
                field_objects, cls._trashed_field_objects.values()
            )
        return field_objects

    @classmethod
    def get_field_objects_by_type(cls, field_type: str, include_trash: bool = False):
        field_objects = cls.get_field_objects(include_trash)

        return filter(lambda f: f["type"].type == field_type, field_objects)

    @classmethod
    def get_fields_missing_search_index(cls) -> List[Field]:
        """
        Returns a list of fields which don't yet have a
        corresponding tsvector column.
        """

        return [
            field for field in cls.get_fields() if not field.tsvector_column_created
        ]

    @classmethod
    def get_fields_with_search_index(cls, include_trash=False) -> List[Field]:
        """
        Returns a list of fields which do have a tsvector column.
        """

        return [
            field
            for field in cls.get_fields(include_trash)
            if field.tsvector_column_created
        ]

    @classmethod
    def get_searchable_fields(
            cls,
            include_trash: bool = False,
    ) -> Generator[Field, None, None]:
        """
        Generates all searchable fields in a table. A searchable field is one where
        field_type.is_searchable(field) is true.

        :param include_trash: Whether to include trashed searchable fields in the result
        :return: A generator of Field.
        """

        for field_object in cls.get_field_objects(include_trash):
            field_type = field_object["type"]
            field = field_object["field"]

            if field.tsvector_column_created and field_type.is_searchable(field):
                yield field

    @classmethod
    def get_fields(cls, include_trash=False):
        return [o["field"] for o in cls.get_field_objects(include_trash)]

    class Meta:
        abstract = True


class DefaultAppsProxy:
    """
    A proxy class to the default apps registry.
    This class is needed to make our dynamic models available in the
    options then the relation tree is built.

    This permits to django to find the reverse relation in the _relation_tree.
    Look into django.db.models.options.py - _populate_directed_relation_graph
    for more information.
    """

    def __init__(self, baserow_m2m_models):
        self.baserow_m2m_models = baserow_m2m_models

    def get_models(self, *args, **kwargs):
        # Called by django and must contain ALL the models that have been generated
        # and connected together as django will loop over every model in this list
        # and set cached properties on each. These cached django properties are then
        # used to when looking up fields, so they must include every connected model
        # that could be involved in queries and not just a sub-set of them.
        return apps.get_models(*args, **kwargs) + list(self.baserow_m2m_models.values())

    def __getattr__(self, attr):
        return getattr(apps, attr)


def patch_meta_get_field(_meta):
    original_get_field = _meta.get_field

    def get_field(self, field_name, *args, **kwargs):
        try:
            return original_get_field(field_name, *args, **kwargs)
        except DjangoFieldDoesNotExist as exc:
            try:
                field_object = self.model.get_field_object(
                    field_name, include_trash=True
                )

            except ValueError:
                raise exc

            field_type = field_object["type"]
            logger.debug(
                "Lazy load missing {} of type {} for table {}",
                field_name,
                field_type.type,
                self.model.pk,
            )
            field_type.after_model_generation(
                field_object["field"], self.model, field_object["name"]
            )
            return original_get_field(field_name, *args, **kwargs)

    _meta.get_field = MethodType(get_field, _meta)


class Table(
    HierarchicalModelMixin,
    CreatedAndUpdatedOnMixin,
    OrderableMixin,
    models.Model,
):
    # database = models.ForeignKey("database.Database", on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    row_count = models.PositiveIntegerField(null=True)
    row_count_updated_at = models.DateTimeField(null=True)
    version = models.TextField(default="initial_version")

    # needs_background_update_column_added = models.BooleanField(
    #     default=False,
    #     help_text="Indicates whether the table has had the background_update_needed "
    #               "column added.",
    # )

    class Meta:
        ordering = ("order",)

    @property
    def tsv_id_column_idx_name(self) -> str:
        return f"tsv_id_idx_{self.id}"

    def get_parent(self):
        return self.database

    @classmethod
    def get_last_order(cls):
        queryset = Table.objects.filter()
        return cls.get_highest_order_of_queryset(queryset) + 1

    def get_database_table_name(self):
        return f"{USER_TABLE_DATABASE_NAME_PREFIX}{self.id}"

    def get_model(
            self,
            fields=None,
            field_ids=None,
            field_names=None,
            attribute_names=False,
            manytomany_models=None,
            add_dependencies=True,
            managed=False,
            use_cache=True,
            force_add_tsvectors: bool = False,
    ) -> Type[GeneratedTableModel]:
        """
        Generates a temporary Django model based on available fields that belong to
        this table. Note that the model will not be registered with the apps because
        of the `DatabaseConfig.prevent_generated_model_for_registering` hack. We do
        not want to the model cached because models with the same name can differ.

        :param fields: Extra table field instances that need to be added the model.
        :type fields: list
        :param field_ids: If provided only the fields with the ids in the list will be
            added to the model. This can be done to improve speed if for example only a
            single field needs to be mutated.
        :type field_ids: None or list
        :param field_names: If provided only the fields with the names in the list
            will be added to the model. This can be done to improve speed if for
            example only a single field needs to be mutated.
        :type field_names: None or list
        :param attribute_names: If True, the model attributes will be based on the
            field name instead of the field id.
        :type attribute_names: bool
        :param manytomany_models: In some cases with related fields a model has to be
            generated in order to generate that model. In order to prevent a
            recursion loop we cache the generated models and pass those along.
        :type manytomany_models: dict
        :param add_dependencies: When True will ensure any direct field dependencies
            are included in the model. Otherwise only the exact fields you specify will
            be added to the model.
        :param managed: Whether the created model should be managed by Django or not.
            Only in very specific limited situations should this be enabled as
            generally Baserow itself manages most aspects of returned generated models.
        :type managed: bool
        :param use_cache: Indicates whether a cached model can be used.
        :type use_cache: bool
        :param force_add_tsvectors: gtIndicates that we want to forcibly add the table's
            `tsvector` columns.
        :type force_add_tsvectors: bool
        :return: The generated model.
        :rtype: Model
        """

        logger.debug(
            "Generating model for table {} with fields {}, manytomany_models {}, add_dependencies {}, use_cache {}",
            str(self.pk),
            fields,
            manytomany_models,
            add_dependencies,
            use_cache,
        )

        filtered = field_names is not None or field_ids is not None
        model_name = f"Table{self.pk}Model"

        if fields is None:
            fields = []

        # By default, we create an index on the `order` and `id`
        # columns. If `USE_PG_FULLTEXT_SEARCH` is enabled, which
        # it is by default, we'll include a GIN index on the table's
        # `tsvector` column.
        indexes = [
            models.Index(
                fields=["order", "id"],
                name=self.get_collision_safe_order_id_idx_name(),
            )
        ]

        app_label = "database_table"
        baserow_m2m_models = manytomany_models or {}
        meta = type(
            "Meta",
            (),
            {
                "apps": DefaultAppsProxy(baserow_m2m_models),
                "managed": managed,
                "db_table": self.get_database_table_name(),
                "app_label": app_label,
                "ordering": ["order", "id"],
                "indexes": indexes,
            },
        )

        def __str__(self):
            """
            When the model instance is rendered to a string, then we want to return the
            primary field value in human readable format.
            """

            field = self._field_objects.get(self._primary_field_id, None)

            if not field:
                return f"unnamed row {self.id}"

            return field["type"].get_human_readable_value(
                getattr(self, field["name"]), field
            )

        attrs = {
            "Meta": meta,
            "__module__": "database.models",
            # An indication that the model is a generated table model.
            "_generated_table_model": True,
            "baserow_table": self,
            "baserow_table_id": self.id,
            "baserow_m2m_models": baserow_m2m_models,
            # We are using our own table model manager to implement some queryset
            # helpers.
            "objects": TableModelManager(),
            "objects_and_trash": TableModelTrashAndObjectsManager(),
            "__str__": __str__,
        }

        use_cache = (
                use_cache
                and len(fields) == 0
                and field_ids is None
                and add_dependencies is True
                and attribute_names is False
                and not settings.BASEROW_DISABLE_MODEL_CACHE
        )

        if use_cache:
            logger.debug("Using cached model for table {}", self.pk)
            self.refresh_from_db(fields=["version"])
            field_attrs = get_cached_model_field_attrs(self)
        else:
            field_attrs = None

        if field_attrs is None:
            logger.debug("Generating model field attrs for table {}", self.pk)
            field_attrs = self._fetch_and_generate_field_attrs(
                add_dependencies,
                attribute_names,
                field_ids,
                field_names,
                fields,
                filtered,
            )

            if use_cache:
                set_cached_model_field_attrs(self, field_attrs)
        else:
            # We found cached model fields, they will have a cached creation_counter
            # attribute each used to compare model fields to do django
            # fundamental internal operations like generating SQL to select from this
            # table. Any new model fields added to this table will use a global
            # static counter on the Model class itself. To prevent any possibility
            # of collisions between the model fields that just came out of the cache
            # and these new model fields we are about to init below, we increase
            # this global creation_counter to prevent any possible collision and
            # horrible bugs.
            max_creation_counter_from_cache = DjangoModelFieldClass.creation_counter
            for f in field_attrs.values():
                if isinstance(f, DjangoModelFieldClass) and not f.auto_created:
                    max_creation_counter_from_cache = max(
                        max_creation_counter_from_cache,
                        getattr(f, "creation_counter", max_creation_counter_from_cache),
                    )
            DjangoModelFieldClass.creation_counter = max_creation_counter_from_cache + 1

        # We have to add the order field after reading the potentially cached values
        # as those cached model fields will have a cached creation_counter and we need
        # to ensure any other model fields added to this same model are __init__ed
        # after we've fixed the global DjangoModelFieldClass.creation_counter
        # above.
        field_attrs["order"] = models.DecimalField(
            max_digits=40,
            decimal_places=20,
            editable=False,
            default=1,
        )

        self._add_search_tsvector_fields_to_model(
            field_attrs, indexes, force_add_tsvectors
        )

        if self.needs_background_update_column_added:
            self._add_needs_background_update_column(field_attrs, indexes)

        attrs.update(**field_attrs)

        # Create the model class.
        model = type(
            str(model_name),
            (
                GeneratedTableModel,
                CreatedAndUpdatedOnMixin,
                models.Model,
            ),
            attrs,
        )

        patch_meta_get_field(model._meta)

        if not model.baserow_m2m_models:
            self._after_model_generation(attrs, model)

        return model

    def _add_search_tsvector_fields_to_model(self, field_attrs, indexes, force_add):
        field_objects = field_attrs["_field_objects"]
        trashed_field_objects = field_attrs["_trashed_field_objects"]
        for field_object in itertools.chain(
                field_objects.values(), trashed_field_objects.values()
        ):
            field = field_object["field"]
            if field.tsvector_column_created or force_add:
                field_attrs[field.tsv_db_column] = SearchVectorField(null=True)
                indexes.append(
                    GinIndex(fields=[field.tsv_db_column], name=field.tsv_index_name)
                )

    def _after_model_generation(self, attrs, model):
        # In some situations the field can only be added once the model class has been
        # generated. So for each field we will call the after_model_generation with
        # the generated model as argument in order to do this. This is for example used
        # by the link row field. It can also be used to make other changes to the
        # class.
        all_field_objects = {
            **attrs["_field_objects"],
            **attrs["_trashed_field_objects"],
        }
        for field_object in all_field_objects.values():
            field_object["type"].after_model_generation(
                field_object["field"], model, field_object["name"]
            )

    def _fetch_and_generate_field_attrs(
            self,
            add_dependencies,
            attribute_names,
            field_ids,
            field_names,
            fields,
            filtered,
    ):
        field_attrs = {
            "_primary_field_id": -1,
            # An object containing the table fields, field types and the chosen
            # names with the table field id as key.
            "_field_objects": {},
            # An object containing the trashed table fields, field types and the
            # chosen names with the table field id as key.
            "_trashed_field_objects": {},
        }
        # Construct a query to fetch all the fields of that table. We need to
        # include any trashed fields so the created model still has them present
        # as the column is still actually there. If the model did not have the
        # trashed field attributes then model.objects.create will fail as the
        # trashed columns will be given null values by django triggering not null
        # constraints in the database.
        fields_query = self.field_set(manager="objects_and_trash").all()

        # If the field ids are provided we must only fetch the fields of which the
        # ids are in that list.
        if isinstance(field_ids, list):
            if len(field_ids) == 0:
                fields_query = []
            else:
                fields_query = fields_query.filter(pk__in=field_ids)

        # If the field names are provided we must only fetch the fields of which the
        # user defined name is in that list.
        if isinstance(field_names, list):
            if len(field_names) == 0:
                fields_query = []
            else:
                fields_query = fields_query.filter(name__in=field_names)

        if isinstance(fields_query, QuerySet):
            fields_query = specific_iterator(fields_query)

        # Create a combined list of fields that must be added and belong to the this
        # table.
        fields = list(fields) + [field for field in fields_query]

        # If there are duplicate field names we have to store them in a list so we
        # know later which ones are duplicate.
        duplicate_field_names = []
        already_included_field_names = set([f.name for f in fields])

        # We will have to add each field to with the correct field name and model
        # field to the attribute list in order for the model to work.
        while len(fields) > 0:
            field = fields.pop(0)
            trashed = field.trashed
            field = field.specific
            field_type = field_type_registry.get_by_model(field)
            field_name = field.db_column

            if filtered and add_dependencies:
                from baserow_dynamic_table.fields.dependencies.handler import (
                    FieldDependencyHandler,
                )

                direct_dependencies = (
                    FieldDependencyHandler.get_same_table_dependencies(field)
                )
                for f in direct_dependencies:
                    if f.name not in already_included_field_names:
                        fields.append(f)
                        already_included_field_names.add(f.name)

            # If attribute_names is True we will not use 'field_{id}' as attribute
            # name, but we will rather use a name the user provided.
            if attribute_names:
                field_name = field.model_attribute_name
                if trashed:
                    field_name = f"trashed_{field_name}"
                # If the field name already exists we will append '_field_{id}' to
                # each entry that is a duplicate.
                if field_name in field_attrs:
                    duplicate_field_names.append(field_name)
                    replaced_field_name = (
                        f"{field_name}_{field_attrs[field_name].db_column}"
                    )
                    field_attrs[replaced_field_name] = field_attrs.pop(field_name)
                if field_name in duplicate_field_names:
                    field_name = f"{field_name}_{field.db_column}"

            field_objects_dict = (
                "_trashed_field_objects" if trashed else "_field_objects"
            )
            # Add the generated objects and information to the dict that
            # optionally can be returned. We exclude trashed fields here so they
            # are not displayed by baserow anywhere.
            field_attrs[field_objects_dict][field.id] = {
                "field": field,
                "type": field_type,
                "name": field_name,
            }
            if field.primary:
                field_attrs["_primary_field_id"] = field.id
            # Add the field to the attribute dict that is used to generate the
            # model. All the kwargs that are passed to the `get_model_field`
            # method are going to be passed along to the model field.
            field_attrs[field_name] = field_type.get_model_field(
                field,
                db_column=field.db_column,
                verbose_name=field.name,
            )

        return field_attrs

    # Use our own custom index name as the default models.Index
    # naming scheme causes 5+ collisions on average per 1000 new
    # tables.
    def get_collision_safe_order_id_idx_name(self):
        return f"tbl_order_id_{self.id}_idx"
