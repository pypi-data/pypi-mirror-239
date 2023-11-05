import traceback
from typing import Any, Dict, List, NewType, Optional, Tuple, cast

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import DatabaseError, ProgrammingError
from django.db.models import Q, QuerySet, Sum
from django.utils import timezone, translation
from django.utils.translation import gettext as _

from baserow_dynamic_table.db.schema import safe_django_schema_editor
from baserow_dynamic_table.fields.dependencies.models import FieldDependency
from baserow_dynamic_table.fields.exceptions import (
    InvalidBaserowFieldName,
    MaxFieldLimitExceeded,
    MaxFieldNameLengthExceeded,
    ReservedBaserowFieldNameException,
)
from baserow_dynamic_table.fields.handler import FieldHandler
from baserow_dynamic_table.fields.registries import field_type_registry
from .exceptions import (
    FailedToLockTableDueToConflict,
    InitialTableDataDuplicateName,
    InitialTableDataLimitExceeded,
    InvalidInitialTableData,
    TableDoesNotExist,
    TableNotInDatabase,
)
from .models import Table

BATCH_SIZE = 1024

TableForUpdate = NewType("TableForUpdate", Table)


class TableHandler:
    def get_table(
            self, table_id: int, base_queryset: Optional[QuerySet] = None
    ) -> Table:
        """
        Selects a table with a given id from the database.

        :param table_id: The identifier of the table that must be returned.
        :param base_queryset: The base queryset from where to select the table
            object from. This can for example be used to do a `select_related`.
        :raises TableDoesNotExist: When the table with the provided id does not exist.
        :return: The requested table of the provided id.
        """

        if base_queryset is None:
            base_queryset = Table.objects

        try:
            table = base_queryset.select_related("database__workspace").get(id=table_id)
        except Table.DoesNotExist:
            raise TableDoesNotExist(f"The table with id {table_id} does not exist.")

        return table

    def get_table_for_update(
            self, table_id: int, nowait: bool = False
    ) -> TableForUpdate:
        """
        Provide a type hint for tables that need to be updated.
        :param table_id: The id of the table that needs to be updated.
        :param nowait: Whether to wait to get the lock on the table or raise a
            DatabaseError not able to do so immediately.
        :return: The table that needs to be updated.
        :raises: FailedToLockTableDueToConflict if nowait is True and the table was not
            able to be locked for update immediately.
        """

        try:
            return cast(
                TableForUpdate,
                self.get_table(
                    table_id,
                    base_queryset=Table.objects.select_for_update(
                        of=("self",), nowait=nowait
                    ),
                ),
            )
        except DatabaseError as e:
            if "could not obtain lock on row" in traceback.format_exc():
                raise FailedToLockTableDueToConflict() from e
            else:
                raise e

    def get_tables_order(self, database: Database) -> List[int]:
        """
        Returns the tables in the database ordered by the order field.

        :param database: The database that the tables belong to.
        :return: A list containing the order of the tables in the database.
        """

        return [table.id for table in database.table_set.order_by("order")]

    def create_table(
            self,
            user: AbstractUser,
            name: str,
            data: Optional[List[List[Any]]] = None,
            first_row_header: bool = True,
            fill_example: bool = False,
    ):
        """
        Creates a new table from optionally provided data. If no data is specified,
        and fill_example is True, the new table will contain demo data. If fill_example
        is `False` the table will be empty.
        Send a `table_created` signal at the end of the process.

        :param user: The user on whose behalf the table is created.
        :param database: The database that the table instance belongs to.
        :param name: The name of the table is created.
        :param data: A list containing all the rows that need to be inserted is
            expected. All the values will be inserted in the database.
        :param first_row_header: Indicates if the first row are the fields. The names
            of these rows are going to be used as fields. If `fields` is provided,
            this options is ignored.
        :param fill_example: Fill the table with example field and data.
        :param progress: An optional progress instance if you want to track the progress
            of the task.
        :return: The created table and the error report.
        """

        if data is not None:
            (
                fields,
                data,
            ) = self.normalize_initial_table_data(
                data, first_row_header=first_row_header
            )
        else:
            with translation.override(user.profile.language):
                if fill_example:
                    fields, data = self.get_example_table_field_and_data()
                else:
                    fields, data = self.get_minimal_table_field_and_data()

        table = self.create_table_and_fields(user, name, fields)

        _, error_report = RowHandler().import_rows(
            user, table, data, progress=progress, send_realtime_update=False
        )

        return table, error_report

    def create_table_and_fields(
            self,
            user: AbstractUser,
            name: str,
            fields: List[Tuple[str, str, Dict[str, Any]]],
    ) -> Table:
        """
        Creates a new table with the specified fields. Also creates a default grid view
        for this table.

        :param user: The user on whose behalf the table is created.
        :param database: The database that the table instance belongs to.
        :param name: The name of the table is created.
        :param fields: You specify the field configuration with this parameter. The
            tuples content is the field name, then the field type and the field
            configuration. You can add an optional `field_options` dict for the
            field_options of the created view.
        """

        last_order = Table.get_last_order()
        table = Table.objects.create(
            order=last_order,
            name=name,
            needs_background_update_column_added=True,
        )

        # Let's create the fields before creating the model so that the whole
        # table schema is created right away.
        field_options_dict = {}
        for index, (name, field_type_name, field_config) in enumerate(fields):
            field_options = field_config.pop("field_options", None)
            field_type = field_type_registry.get(field_type_name)
            FieldModel = field_type.model_class

            fields[index] = FieldModel.objects.create(
                table=table,
                order=index,
                primary=index == 0,
                name=name,
                tsvector_column_created=table.tsvectors_are_supported,
                **field_config,
            )
            if field_options:
                field_options_dict[fields[index].id] = field_options

        # Create the table schema in the database.
        with safe_django_schema_editor() as schema_editor:
            # Django only creates indexes when the model is managed.
            model = table.get_model(managed=True)
            schema_editor.create_model(model)

        return table

    def normalize_initial_table_data(
            self, data: List[List[Any]], first_row_header: bool
    ) -> Tuple[List, List]:
        """
        Normalizes the provided initial table data. The amount of columns will be made
        equal for each row. The header and the rows will also be separated.

        :param data: A list containing all the provided rows.
        :param first_row_header: Indicates if the first row is the header. For each
            of these header columns a field is going to be created.
        :raises InvalidInitialTableData: When the data doesn't contain a column or row.
        :raises MaxFieldNameLengthExceeded: When the provided name is too long.
        :raises InitialTableDataDuplicateName: When duplicates exit in field names.
        :raises ReservedBaserowFieldNameException: When the field name is reserved by
            Baserow.
        :raises InvalidBaserowFieldName: When the field name is invalid (empty).
        :return: A list containing the field names with a type and a list containing all
            the rows.
        """

        if len(data) == 0:
            raise InvalidInitialTableData("At least one row should be provided.")

        limit = settings.INITIAL_TABLE_DATA_LIMIT
        if limit and len(data) > limit:
            raise InitialTableDataLimitExceeded(
                f"It is not possible to import more than "
                f"{settings.INITIAL_TABLE_DATA_LIMIT} rows when creating a table."
            )

        largest_column_count = len(max(data, key=len))

        if largest_column_count == 0:
            raise InvalidInitialTableData("At least one column should be provided.")

        fields = data.pop(0) if first_row_header else []

        for i in range(len(fields), largest_column_count):
            fields.append(_("Field %d") % (i + 1,))

        if len(fields) > settings.MAX_FIELD_LIMIT:
            raise MaxFieldLimitExceeded(
                f"Fields count exceeds the limit of {settings.MAX_FIELD_LIMIT}"
            )

        # Stripping whitespace from field names is already done by
        # TableCreateSerializer however we repeat to ensure that non API usages of
        # this method is consistent with api usage.
        field_name_set = {str(name).strip() for name in fields}

        if len(field_name_set) != len(fields):
            raise InitialTableDataDuplicateName()

        max_field_name_length = Field.get_max_name_length()
        long_field_names = [x for x in field_name_set if len(x) > max_field_name_length]

        if len(long_field_names) > 0:
            raise MaxFieldNameLengthExceeded(max_field_name_length)

        if len(field_name_set.intersection(RESERVED_BASEROW_FIELD_NAMES)) > 0:
            raise ReservedBaserowFieldNameException()

        if "" in field_name_set:
            raise InvalidBaserowFieldName()

        fields_with_type = [(field_name, "text", {}) for field_name in fields]
        result = [[str(value) for value in row] for row in data]

        return fields_with_type, result

    def get_example_table_field_and_data(self):
        """
        Generates fields and data with some initial example data.
        """

        fields = [
            (_("Name"), "text", {}),
            (_("Notes"), "long_text", {"field_options": {"width": 400}}),
            (_("Active"), "boolean", {"field_options": {"width": 100}}),
        ]
        data = [["", "", False], ["", "", False]]
        return fields, data

    def get_minimal_table_field_and_data(self):
        """
        Generates fields and data for an empty table.
        """

        fields = [
            (_("Name"), "text", {}),
        ]
        data = []
        return fields, data

    def update_table_by_id(self, user: AbstractUser, table_id: int, name: str) -> Table:
        """
        Updates an existing table instance.

        :param user: The user on whose behalf the table is updated.
        :param table_id: The id of the table that needs to be updated.
        :param name: The name to be updated.
        :raises ValueError: When the provided table is not an instance of Table.
        :return: The updated table instance.
        """

        table = self.get_table_for_update(table_id)
        return self.update_table(user, table, name)

    def update_table(self, user: AbstractUser, table: Table, name: str) -> Table:
        """
        Updates an existing table instance.

        :param user: The user on whose behalf the table is updated.
        :param table: The table instance that needs to be updated.
        :param name: The name to be updated.
        :raises ValueError: When the provided table is not an instance of Table.
        :return: The updated table instance.
        """

        if not isinstance(table, Table):
            raise ValueError("The table is not an instance of Table")

        table.name = name
        table.save()

        return table

    def order_tables(self, user: AbstractUser, order: List[int]):
        """
        Updates the order of the tables in the given database. The order of the views
        that are not in the `order` parameter set to `0`.

        :param user: The user on whose behalf the tables are ordered.
        :param database: The database of which the views must be updated.
        :param order: A list containing the table ids in the desired order.
        :raises TableNotInDatabase: If one of the table ids in the order does not belong
            to the database.
        """

        all_tables = Table.objects.all()

        user_tables = all_tables.filter(user=user)

        table_ids = user_tables.values_list("id", flat=True)

        for table_id in order:
            if table_id not in table_ids:
                raise TableNotInDatabase(table_id)

        Table.order_objects(all_tables, order)

    def find_unused_table_name(self, database: Database, proposed_name: str) -> str:
        """
        Finds an unused name for a table in a database.

        :param database: The database that the table belongs to.
        :param proposed_name: The name that is proposed to be used.
        :return: A unique name to use.
        """

        existing_tables_names = list(database.table_set.values_list("name", flat=True))
        return find_unused_name([proposed_name], existing_tables_names, max_length=255)

    def _create_related_link_fields_in_existing_tables_to_import(
            self, serialized_table: Dict[str, Any], id_mapping: Dict[str, Any]
    ) -> List[Tuple[Table, Dict[str, Any]]]:
        """
        Creates extra serialized field dicts to pass to the table importer so it will
        create the reverse link row fields in any existing tables.

        :param serialized_table: The serialized table.
        :param id_mapping: The id mapping.
        :return : A list of external tables with the link row fields to import into
            them.
        """

        from baserow_dynamic_table.fields.field_types import LinkRowFieldType

        external_fields = []
        for serialized_field in serialized_table["fields"]:
            if serialized_field["type"] != LinkRowFieldType.type:
                continue

            link_row_table_id = serialized_field.get("link_row_table_id", None)
            self_referencing_field = link_row_table_id == serialized_table["id"]
            link_row_table = self.get_table(link_row_table_id)
            has_related_field = serialized_field.get("link_row_related_field_id")
            id_mapping["database_tables"][link_row_table_id] = link_row_table_id

            if self_referencing_field or not has_related_field:
                continue

            related_field_name = FieldHandler().find_next_unused_field_name(
                link_row_table, [serialized_table["name"]]
            )
            # We deliberately want to use a negative ID for the newly created related
            # field because it can't clash with another existing field ID. It doesn't
            # matter that it's negative because it get a new unique when it's
            # imported later on.
            related_field_id = -len(external_fields)
            serialized_field["link_row_related_field_id"] = related_field_id
            serialized_related_link_row_field = {
                "id": related_field_id,
                "name": related_field_name,
                "type": LinkRowFieldType.type,
                "link_row_table_id": serialized_table["id"],
                "link_row_related_field_id": serialized_field["id"],
                "order": Field.get_last_order(link_row_table),
            }
            external_fields.append((link_row_table, serialized_related_link_row_field))

        return external_fields

    def duplicate_table(
            self,
            user: AbstractUser,
            table: Table,
            progress_builder: Optional[ChildProgressBuilder] = None,
    ) -> Table:
        """
        Duplicates an existing table instance.

        :param user: The user on whose behalf the table is duplicated.
        :param table: The table instance that needs to be duplicated.
        :param progress: A progress object that can be used to report progress.
        :raises ValueError: When the provided table is not an instance of Table.
        :return: The duplicated table instance.
        """

        if not isinstance(table, Table):
            raise ValueError("The table is not an instance of Table")

        start_progress, export_progress, import_progress = 10, 30, 60
        progress = ChildProgressBuilder.build(progress_builder, child_total=100)
        progress.increment(by=start_progress)

        database = table.database

        CoreHandler().check_permissions(
            user,
            DuplicateDatabaseTableOperationType.type,
            workspace=database.workspace,
            context=table,
        )

        database_type = application_type_registry.get_by_model(database)

        config = ImportExportConfig(
            include_permission_data=True, reduce_disk_space_usage=False
        )

        serialized_tables = database_type.export_tables_serialized([table], config)

        # Set a unique name for the table to import back as a new one.
        exported_table = serialized_tables[0]
        exported_table["name"] = self.find_unused_table_name(database, table.name)
        exported_table["order"] = Table.get_last_order(database)

        # It can happen that a field, filter, etc has a reference to a field in
        # another table. This can result in an error because that field id is not in
        # the field mapping. Therefore, we're fetching all the related field ids in
        # the table and add those to the mapping. The key and value is the same
        # because those field ids haven't changed.
        all_table_dependency_field_ids = FieldDependency.objects.filter(
            Q(dependant__table_id=table.id) & ~Q(dependency__table_id=table.id)
        ).values_list("dependency_id", flat=True)
        all_table_dependency_field_ids = {
            field_id: field_id for field_id in all_table_dependency_field_ids
        }
        id_mapping: Dict[str, Any] = {
            "database_tables": {},
            "database_fields": all_table_dependency_field_ids,
            # We have to create the `database_field_select_options` because that's
            # otherwise not created later on.
            "database_field_select_options": {},
        }

        link_fields_to_import_to_existing_tables = (
            self._create_related_link_fields_in_existing_tables_to_import(
                exported_table, id_mapping
            )
        )
        progress.increment(by=export_progress)

        imported_tables = database_type.import_tables_serialized(
            database,
            [exported_table],
            id_mapping,
            config,
            external_table_fields_to_import=link_fields_to_import_to_existing_tables,
            progress_builder=progress.create_child_builder(
                represents_progress=import_progress
            ),
        )

        new_table_clone = imported_tables[0]

        table_created.send(self, table=new_table_clone, user=user)

        return new_table_clone

    def delete_table_by_id(self, user: AbstractUser, table_id: int):
        """
        Moves to the trash an existing an existing table instance if the user
        has access to the related workspace.
        The table deleted signals are also fired.

        :param user: The user on whose behalf the table is deleted.
        :param table_id: The table id of the table that needs to be deleted.
        :raises ValueError: When the provided table is not an instance of Table.
        """

        table = self.get_table_for_update(table_id)
        self.delete_table(user, table)

    def delete_table(self, user: AbstractUser, table: Table):
        """
        Moves to the trash an existing table instance if the user has access
        to the related workspace.
        The table deleted signals are also fired.

        :param user: The user on whose behalf the table is deleted.
        :param table: The table instance that needs to be deleted.
        :raises ValueError: When the provided table is not an instance of Table.
        """

        if not isinstance(table, Table):
            raise ValueError("The table is not an instance of Table")

        CoreHandler().check_permissions(
            user,
            DeleteDatabaseTableOperationType.type,
            workspace=table.database.workspace,
            context=table,
        )

        TrashHandler.trash(user, table.database.workspace, table.database, table)

        table_deleted.send(self, table_id=table.id, table=table, user=user)

    @classmethod
    def count_rows(cls) -> int:
        """
        Counts how many rows each user table has and stores the count
        for later reference.
        :returns: The number of tables counted.
        """

        chunk_size = 200
        tables_to_store = []
        time = timezone.now()
        i = 0
        for table in Table.objects.filter(
                database__workspace__template__isnull=True
        ).iterator(chunk_size=chunk_size):
            try:
                count = table.get_model(field_ids=[]).objects.count()
                table.row_count = count
                table.row_count_updated_at = time
                tables_to_store.append(table)
            except ProgrammingError as e:
                if f'"database_table_{table.id}" does not exist' in str(e):
                    logger.warning(f"Error while counting rows {e}")
                else:
                    raise e

            # This makes sure we don't pollute the memory
            if i % chunk_size == 0:
                Table.objects.bulk_update(
                    tables_to_store, ["row_count", "row_count_updated_at"]
                )
                tables_to_store = []
            i += 1

        if len(tables_to_store) > 0:
            Table.objects.bulk_update(
                tables_to_store, ["row_count", "row_count_updated_at"]
            )

        return i

    @classmethod
    def get_total_row_count_of_workspace(cls, workspace_id: int) -> int:
        """
        Returns the total row count of all tables in the given workspace.

        :param workspace_id: The workspace which the total row count needs to be
            calculated.
        :return: The total row count of all tables in the given workspace.
        """

        return (
                Table.objects.filter(database__workspace_id=workspace_id).aggregate(
                    Sum("row_count")
                )["row_count__sum"]
                or 0
        )

    def create_needs_background_update_field(self, table: "Table") -> None:
        """
        Responsible for creating the `ROW_NEEDS_BACKGROUND_UPDATES_RUN_COLUMN_NAME` and
        fields on the `Table`.
        """

        if table.needs_background_update_column_added:
            return

        # Prepare a fresh model we can use to create the columns.
        table.needs_background_update_column_added = True
        model = table.get_model()

        with safe_django_schema_editor(atomic=False) as schema_editor:
            needs_background_update_field = model._meta.get_field(
                ROW_NEEDS_BACKGROUND_UPDATE_COLUMN_NAME
            )
            schema_editor.add_field(model, needs_background_update_field)
            schema_editor.add_index(model, get_row_needs_background_update_index(table))

        table.save(update_fields=("needs_background_update_column_added",))
