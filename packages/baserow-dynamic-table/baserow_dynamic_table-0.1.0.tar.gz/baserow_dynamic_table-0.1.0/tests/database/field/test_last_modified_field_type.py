from datetime import datetime
from io import BytesIO

from django.core.exceptions import ValidationError

import pytest
from freezegun import freeze_time
from pytz import timezone

from baserow_dynamic_table.fields.handler import FieldHandler
from baserow_dynamic_table.fields.models import LastModifiedField
from baserow_dynamic_table.rows.handler import RowHandler
from baserow.core.handler import CoreHandler
from baserow.core.registries import ImportExportConfig


@pytest.mark.django_db
def test_last_modified_field_type(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)

    field_handler = FieldHandler()
    row_handler = RowHandler()
    time_to_freeze = "2021-08-10 12:00"

    data_fixture.create_text_field(table=table, name="text_field", primary=True)

    last_modified_field_date = field_handler.create_field(
        user=user,
        table=table,
        type_name="last_modified",
        name="Last Date",
    )
    last_modified_field_datetime = field_handler.create_field(
        user=user,
        table=table,
        type_name="last_modified",
        name="Last Datetime",
        date_include_time=True,
    )
    assert last_modified_field_date.date_include_time is False
    assert last_modified_field_datetime.date_include_time is True
    assert len(LastModifiedField.objects.all()) == 2

    model = table.get_model(attribute_names=True)

    # trying to create a row with values for the last_modified_field
    # set will result in a ValidationError
    with pytest.raises(ValidationError):
        row_handler.create_row(
            user=user, table=table, values={last_modified_field_date.id: "2021-08-09"}
        )

    with pytest.raises(ValidationError):
        row_handler.create_row(
            user=user,
            table=table,
            values={last_modified_field_datetime.id: "2021-08-09T14:14:33.574356Z"},
        )

    with freeze_time(time_to_freeze):
        row = row_handler.create_row(user=user, table=table, values={}, model=model)
    assert row.last_date is not None
    assert row.last_date == row.updated_on
    assert row.last_datetime is not None
    row_last_modified_2 = row.last_datetime
    row_updated_on = row.updated_on
    assert row_last_modified_2 == row_updated_on

    # Trying to update the last_modified field will raise error
    with pytest.raises(ValidationError):
        row_handler.update_row_by_id(
            user=user,
            row_id=row.id,
            table=table,
            values={last_modified_field_date.id: "2021-08-09"},
        )

    with pytest.raises(ValidationError):
        row_handler.update_row_by_id(
            user=user,
            table=table,
            row_id=row.id,
            values={last_modified_field_datetime.id: "2021-08-09T14:14:33.574356Z"},
        )

    # Updating the text field will updated
    # the last_modified datetime field.
    row_last_datetime_before_update = row.last_datetime
    with freeze_time(time_to_freeze):
        row_handler.update_row_by_id(
            user=user,
            table=table,
            row_id=row.id,
            values={
                "text_field": "Hello Test",
            },
            model=model,
        )

    row.refresh_from_db()

    assert row.last_datetime >= row_last_datetime_before_update
    assert row.last_datetime == row.updated_on

    row_last_modified_2_before_alter = row.last_datetime

    # changing the field from LastModified to Datetime should persist the date
    with freeze_time(time_to_freeze):
        field_handler.update_field(
            user=user,
            field=last_modified_field_datetime,
            new_type_name="date",
            date_include_time=True,
        )

    assert len(LastModifiedField.objects.all()) == 1
    row.refresh_from_db()
    assert row.last_datetime == row_last_modified_2_before_alter

    # changing the field from LastModified with Datetime to Text Field should persist
    # the datetime as string
    with freeze_time(time_to_freeze):
        field_handler.update_field(
            user=user,
            field=last_modified_field_datetime,
            new_type_name="last_modified",
            date_include_time=True,
            timezone="Europe/Berlin",
        )
    assert len(LastModifiedField.objects.all()) == 2

    row.refresh_from_db()
    row_last_modified_2_before_alter = row.last_datetime

    field_handler.update_field(
        user=user,
        field=last_modified_field_datetime,
        new_type_name="text",
    )
    row.refresh_from_db()
    assert len(LastModifiedField.objects.all()) == 1
    assert row.last_datetime == row_last_modified_2_before_alter.strftime(
        "%d/%m/%Y %H:%M"
    )

    # deleting the fields
    field_handler.delete_field(user=user, field=last_modified_field_date)

    assert len(LastModifiedField.objects.all()) == 0


@pytest.mark.django_db(transaction=True)
def test_import_export_last_modified_field(data_fixture):
    user = data_fixture.create_user()
    imported_workspace = data_fixture.create_workspace(user=user)
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    field_handler = FieldHandler()
    last_modified_field = field_handler.create_field(
        user=user,
        table=table,
        name="Last modified",
        type_name="last_modified",
    )
    last_modified_field_2 = field_handler.create_field(
        user=user,
        table=table,
        name="Created On 2",
        type_name="created_on",
    )

    row_handler = RowHandler()

    with freeze_time("2020-01-01 12:00"):
        row = row_handler.create_row(
            user=user,
            table=table,
            values={},
        )

    assert getattr(row, f"field_{last_modified_field.id}") == datetime(
        2020, 1, 1, 12, 00, tzinfo=timezone("UTC")
    )
    assert getattr(row, f"field_{last_modified_field_2.id}") == datetime(
        2020, 1, 1, 12, 00, tzinfo=timezone("UTC")
    )

    core_handler = CoreHandler()
    config = ImportExportConfig(include_permission_data=False)

    exported_applications = core_handler.export_workspace_applications(
        database.workspace, BytesIO(), config
    )

    # We manually set this value in the export, because if it's set, then the import
    # will use that value.
    exported_applications[0]["tables"][0]["rows"][0][
        f"field_{last_modified_field_2.id}"
    ] = datetime(2021, 1, 1, 12, 00, tzinfo=timezone("UTC")).isoformat()

    with freeze_time("2020-01-02 12:00"):
        (
            imported_applications,
            id_mapping,
        ) = core_handler.import_applications_to_workspace(
            imported_workspace, exported_applications, BytesIO(), config, None
        )

    imported_database = imported_applications[0]
    imported_tables = imported_database.table_set.all()
    imported_table = imported_tables[0]
    imported_last_modified_field = imported_table.field_set.all().first().specific
    imported_last_modified_field_2 = imported_table.field_set.all().last().specific

    imported_row = row_handler.get_row(user=user, table=imported_table, row_id=row.id)
    assert imported_row.id == row.id
    assert getattr(
        imported_row, f"field_{imported_last_modified_field.id}"
    ) == datetime(2020, 1, 1, 12, 00, tzinfo=timezone("UTC"))
    assert getattr(
        imported_row, f"field_{imported_last_modified_field_2.id}"
    ) == datetime(2021, 1, 1, 12, 00, tzinfo=timezone("UTC"))


@pytest.mark.django_db
def test_last_modified_field_adjacent_row(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    grid_view = data_fixture.create_grid_view(user=user, table=table, name="Test")
    last_modified_field = data_fixture.create_last_modified_field(table=table)

    data_fixture.create_view_sort(
        view=grid_view, field=last_modified_field, order="DESC"
    )

    handler = RowHandler()
    [row_a, row_b, row_c] = handler.create_rows(
        user=user,
        table=table,
        rows_values=[
            {},
            {},
            {},
        ],
    )

    base_queryset = table.get_model().objects.all()

    row_b = base_queryset.get(pk=row_b.id)
    previous_row = handler.get_adjacent_row(
        row_b, base_queryset, previous=True, view=grid_view
    )
    next_row = handler.get_adjacent_row(row_b, base_queryset, view=grid_view)

    assert previous_row.id == row_c.id
    assert next_row.id == row_a.id
