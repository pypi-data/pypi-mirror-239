from typing import Optional

from django.db import models
from django.db.models import Field, Value
from django.db.models.expressions import RawSQL
from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor,
    ManyToManyDescriptor,
)
from django.utils.functional import cached_property


class SingleSelectForwardManyToOneDescriptor(ForwardManyToOneDescriptor):
    def get_queryset(self, **hints):
        """
        We specifically want to return a new query set without the provided hints
        because the related table could be in another database and that could fail
        otherwise.
        """

        return self.field.remote_field.model.objects.all()

    def get_object(self, instance):
        """
        Tries to fetch the reference object, but if it fails because it doesn't exist,
        the value will be set to None instead of failing hard.
        """

        try:
            return super().get_object(instance)
        except self.field.remote_field.model.DoesNotExist:
            setattr(instance, self.field.name, None)
            instance.save()
            return None


class SingleSelectForeignKey(models.ForeignKey):
    forward_related_accessor_class = SingleSelectForwardManyToOneDescriptor


class MultipleSelectManyToManyDescriptor(ManyToManyDescriptor):
    """
    This is a slight modification of Djangos default ManyToManyDescriptor for the
    MultipleSelectFieldType. This is needed in order to change the default ordering of
    the select_options that are being returned when accessing those by calling ".all()"
    on the field. The default behavior was that no ordering is applied, which in the
    case for the MultipleSelectFieldType meant that the relations were ordered by
    their ID. To show the relations in the order of how the user added those to
    the field, the `get_queryset` and `get_prefetch_queryset` method was modified by
    applying an order_by. The `order_by` is using the id of the through table.

    Optionally it's also possible to provide a `additional_filters` dict parameter.
    It can contain additional filters that must be applied to the queryset.

    The changes are compatible for a normal and prefetched queryset.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        :param additional_filters: Can contain additional filters that must be
            applied to the queryset. For example `{"id__in": [1, 2]}` makes sure that
            only results where the id is either `1` or `2` is returned.
        """

        self.additional_filters = kwargs.pop("additional_filters", None)
        super().__init__(*args, **kwargs)

    @cached_property
    def related_manager_cls(self):
        additional_filters = self.additional_filters
        manager_class = super().related_manager_cls

        class CustomManager(manager_class):
            def __init__(self, instance=None):
                super().__init__(instance=instance)
                self.additional_filters = additional_filters

                if self.additional_filters:
                    self.core_filters.update(**additional_filters)

            def _apply_rel_ordering(self, queryset):
                return queryset.extra(order_by=[f"{self.through._meta.db_table}.id"])

            def get_queryset(self):
                try:
                    return self.instance._prefetched_objects_cache[
                        self.prefetch_cache_name
                    ]
                except (AttributeError, KeyError):
                    queryset = super().get_queryset()
                    queryset = self._apply_rel_ordering(queryset)
                    return queryset

            def get_prefetch_queryset(self, instances, queryset=None):
                returned_tuple = list(
                    super().get_prefetch_queryset(instances, queryset)
                )

                if self.additional_filters:
                    returned_tuple[0] = returned_tuple[0].filter(**additional_filters)

                returned_tuple[0] = returned_tuple[0].extra(
                    order_by=[f"{self.through._meta.db_table}.id"]
                )

                return tuple(returned_tuple)

        return CustomManager


class MultipleSelectManyToManyField(models.ManyToManyField):
    """
    This is a slight modification of Djangos default ManyToManyField to apply the
    custom `MultipleSelectManyToManyDescriptor` to the class of the model.
    """

    def __init__(self, *args, **kwargs):
        self.additional_filters = kwargs.pop("additional_filters", None)
        self.reversed_additional_filters = kwargs.pop(
            "reversed_additional_filters", None
        )
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(
            cls,
            self.name,
            MultipleSelectManyToManyDescriptor(
                self.remote_field,
                reverse=False,
                additional_filters=self.additional_filters,
            ),
        )

    def contribute_to_related_class(self, cls, related):
        super().contribute_to_related_class(cls, related)
        if (
                not self.remote_field.is_hidden()
                and not related.related_model._meta.swapped
        ):
            setattr(
                cls,
                related.get_accessor_name(),
                MultipleSelectManyToManyDescriptor(
                    self.remote_field,
                    reverse=True,
                    additional_filters=self.reversed_additional_filters,
                ),
            )


class BaserowExpression:
    pass


class BaserowExpressionField(models.Field):
    """
    A Custom Django field which is always set to the value of the provided Baserow
    Expression.
    """

    # Ensure when a model using one of these fields is created that the values of any
    # generated columns are returned using a INSERT ... RETURNING pk, gen_col_1, etc
    # as there is no default and no way of knowing what the expression evaluates to
    db_returning = True
    requires_refresh_after_update = True

    def __init__(
            self,
            expression: Optional[BaserowExpression],
            expression_field: Field,
            requires_refresh_after_insert: bool,
            *args,
            **kwargs,
    ):
        """
        :param expression: The Baserow expression used to calculate this fields value.
        :param expression_field: An instance of a Django field that should be used to
            store the result of the expression in the database.
        """

        self.expression = expression
        self.expression_field = expression_field
        self.requires_refresh_after_insert = requires_refresh_after_insert

        # Add all the various lookups for the underlying Django field so specific
        # filters work on a field of this type. E.g. if expression_field is a DateField
        # then by doing this a model containing this field can then be used like so:
        # Model.objects.filter(expr_field__year='2020')
        for name, lookup in self.expression_field.get_lookups().items():
            self.register_lookup(lookup, lookup_name=name)
        super().__init__(*args, **kwargs)

    def __copy__(self):
        obj = super().__copy__()
        # Un-override the __class__ property below so we dont un-serialize literally as
        # self.expression_field.__class__
        obj.__class__ = BaserowExpressionField
        return obj

    def __reduce__(self):
        reduced_tuple = super().__reduce__()
        if len(reduced_tuple) == 3:
            # Un-override the __class__ property below so we dont un-serialize
            # literally as self.expression_field.__class__
            return reduced_tuple[0], (BaserowExpressionField,), reduced_tuple[2]
        else:
            return reduced_tuple

    @property
    def __class__(self):
        # Pretend to be the expression_field Django model field so Django will let
        # us do filters on a field of this type which are valid for the underlying
        # expression field.
        return self.expression_field.__class__

    def get_transform(self, name):
        # When a model field of this type is pickled and stored in the Baserow model
        # cache, the lookups on the class setup in the __init__ are not persisted.
        # So to ensure when they are accessed on a unserialized version of this model
        # we override this method to delegate to the underlying field type. This means
        # that django lookups and transforms like model.objects.filter(
        # formula_field_1__year=Value(2023)) work out of the box and so view filters
        # work on formula fields.
        return self.expression_field.get_transform(name)

    def get_lookup(self, name):
        # See comment in get_transform as to why we delegate here.
        return self.expression_field.get_lookup(name)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["expression"] = self.expression
        kwargs["expression_field"] = self.expression_field
        kwargs["requires_refresh_after_insert"] = self.requires_refresh_after_insert
        return name, path, args, kwargs

    def db_type(self, connection):
        return self.expression_field.db_type(connection)

    def get_prep_value(self, value):
        return self.expression_field.get_prep_value(value)

    def from_db_value(self, value, expression, connection):
        if hasattr(self.expression_field, "from_db_value"):
            return self.expression_field.from_db_value(value, expression, connection)
        else:
            return value

    def select_format(self, compiler, sql, params):
        return self.expression_field.select_format(compiler, sql, params)

    def pre_save(self, model_instance, add):
        if self.expression is None:
            return Value(None)
        else:
            if add:
                return FormulaHandler.baserow_expression_to_insert_django_expression(
                    self.expression, model_instance
                )
            else:
                return (
                    FormulaHandler.baserow_expression_to_row_update_django_expression(
                        self.expression, model_instance
                    )
                )

    @property
    def valid_for_bulk_update(self):
        # When the expression is None we are in the error state and so shouldn't be
        # included in any BULK UPDATE statement.
        return self.expression is not None


class SerialField(models.Field):
    """
    The serial field works very similar compared to the `AutoField` (primary key field).
    Everytime a new row is created and the value is not set, it will automatically
    increment a sequence and that will be set as value. It's basically an auto
    increment column. The sequence is independent of a transaction to prevent race
    conditions.
    """

    db_returning = True

    def db_type(self, connection):
        return "serial"

    def pre_save(self, model_instance, add):
        if add and not getattr(model_instance, self.name):
            sequence_name = f"{model_instance._meta.db_table}_{self.name}_seq"
            return RawSQL(  # nosec
                f"nextval('{sequence_name}'::regclass)",
                (),
            )
        else:
            return super().pre_save(model_instance, add)


class DurationFieldUsingPostgresFormatting(models.DurationField):
    def to_python(self, value):
        return value

    def select_format(self, compiler, sql, params):
        # We want to use postgres's method of converting intervals to strings instead
        # of pythons timedelta representation. This is so lookups of date intervals
        # which cast the interval to string inside of the database will have the
        # same values as non lookup intervals. The postgres str representation is also
        # more human readable.
        return sql + "::text", params
