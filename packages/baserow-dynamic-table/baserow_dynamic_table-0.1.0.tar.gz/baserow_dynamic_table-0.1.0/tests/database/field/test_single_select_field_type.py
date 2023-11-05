from io import BytesIO

from django.core.exceptions import ValidationError
from django.db import connection
from django.shortcuts import reverse
from django.test.utils import CaptureQueriesContext

import pytest
from faker import Faker
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from baserow_dynamic_table.api.rows.serializers import (
    RowSerializer,
    get_row_serializer_class,
)
from baserow_dynamic_table.fields.deferred_field_fk_updater import (
    DeferredFieldFkUpdater,
)
from baserow_dynamic_table.fields.field_types import SingleSelectFieldType
from baserow_dynamic_table.fields.handler import FieldHandler
from baserow_dynamic_table.fields.models import SelectOption, SingleSelectField
from baserow_dynamic_table.fields.registries import field_type_registry
from baserow_dynamic_table.rows.handler import RowHandler
from baserow_dynamic_table.views.handler import ViewHandler
from baserow.core.handler import CoreHandler
from baserow.core.registries import ImportExportConfig
from baserow.test_utils.helpers import AnyInt


@pytest.mark.django_db
def test_single_select_field_type(data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)

    field_handler = FieldHandler()

    field = field_handler.create_field(
        user=user,
        table=table,
        type_name="single_select",
        name="Single select",
        select_options=[{"value": "Option 1", "color": "blue"}],
    )

    assert SingleSelectField.objects.all().first().id == field.id
    assert SelectOption.objects.all().count() == 1

    select_options = field.select_options.all()
    assert len(select_options) == 1
    assert select_options[0].order == 0
    assert select_options[0].field_id == field.id
    assert select_options[0].value == "Option 1"
    assert select_options[0].color == "blue"

    field = field_handler.update_field(
        user=user,
        table=table,
        field=field,
        select_options=[
            {"value": "Option 2 B", "color": "red 2"},
            {"id": select_options[0].id, "value": "Option 1 B", "color": "blue 2"},
        ],
    )

    assert SelectOption.objects.all().count() == 2
    select_options_2 = field.select_options.all()
    assert len(select_options_2) == 2
    assert select_options_2[0].order == 0
    assert select_options_2[0].field_id == field.id
    assert select_options_2[0].value == "Option 2 B"
    assert select_options_2[0].color == "red 2"
    assert select_options_2[1].id == select_options[0].id
    assert select_options_2[1].order == 1
    assert select_options_2[1].field_id == field.id
    assert select_options_2[1].value == "Option 1 B"
    assert select_options_2[1].color == "blue 2"

    field_handler.delete_field(user=user, field=field)
    assert SelectOption.objects.all().count() == 0

    field = field_handler.create_field(
        user=user,
        table=table,
        type_name="single_select",
        select_options=[],
        name="Another Single Select",
    )
    field_handler.update_field(user=user, field=field, new_type_name="text")


@pytest.mark.django_db
def test_can_convert_a_single_select_option_field_with_dollar_dollar_option(
    data_fixture,
):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)

    field_handler = FieldHandler()
    field = field_handler.create_field(
        user=user,
        table=table,
        type_name="single_select",
        name="Single select",
        select_options=[
            {
                "value": "$$",
                "color": "red",
            }
        ],
    )
    select_option = field.select_options.all()[0]

    row_handler = RowHandler()
    row = row_handler.create_row(user, table, {f"field_{field.id}": select_option.id})

    field_handler.update_field(user=user, field=field, new_type_name="text")

    new_row = row_handler.get_row(user, table, row.id)
    assert getattr(new_row, f"field_{field.id}") == "$$"


@pytest.mark.django_db
def test_cant_use_dollar_end_tag_as_option_name_during_conversion(
    data_fixture,
):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)

    field_handler = FieldHandler()
    field = field_handler.create_field(
        user=user,
        table=table,
        type_name="single_select",
        name="Single select",
        select_options=[
            {
                "value": "some $FUNCTION$ thing",
                "color": "red",
            }
        ],
    )
    select_option = field.select_options.all()[0]

    row_handler = RowHandler()
    row = row_handler.create_row(user, table, {f"field_{field.id}": select_option.id})

    field_handler.update_field(user=user, field=field, new_type_name="text")

    new_row = row_handler.get_row(user, table, row.id)
    assert getattr(new_row, f"field_{field.id}") == "some  thing"


@pytest.mark.django_db
def test_single_select_field_type_rows(data_fixture, django_assert_num_queries):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    other_select_option = data_fixture.create_select_option()

    field_handler = FieldHandler()
    row_handler = RowHandler()

    field = field_handler.create_field(
        user=user,
        table=table,
        name="name",
        type_name="single_select",
        select_options=[
            {"value": "Option 1", "color": "red"},
            {"value": "Option 2", "color": "blue"},
        ],
    )

    with pytest.raises(ValidationError):
        row_handler.create_row(
            user=user, table=table, values={f"field_{field.id}": 999999}
        )

    with pytest.raises(ValidationError):
        row_handler.create_row(
            user=user, table=table, values={f"field_{field.id}": other_select_option.id}
        )

    with pytest.raises(ValidationError):
        row_handler.create_row(
            user=user, table=table, values={f"field_{field.id}": "Missing option value"}
        )

    select_options = field.select_options.all()
    row = row_handler.create_row(
        user=user, table=table, values={f"field_{field.id}": select_options[0].id}
    )

    assert getattr(row, f"field_{field.id}").id == select_options[0].id
    assert getattr(row, f"field_{field.id}").value == select_options[0].value
    assert getattr(row, f"field_{field.id}").color == select_options[0].color
    assert getattr(row, f"field_{field.id}_id") == select_options[0].id

    field = field_handler.update_field(
        user=user,
        field=field,
        select_options=[
            {"value": "Option 3", "color": "orange"},
            {"value": "Option 4", "color": "purple"},
        ],
    )

    select_options = field.select_options.all()
    row_2 = row_handler.create_row(
        user=user, table=table, values={f"field_{field.id}": select_options[0].value}
    )
    assert getattr(row_2, f"field_{field.id}").id == select_options[0].id
    assert getattr(row_2, f"field_{field.id}").value == select_options[0].value
    assert getattr(row_2, f"field_{field.id}").color == select_options[0].color
    assert getattr(row_2, f"field_{field.id}_id") == select_options[0].id

    row_3 = row_handler.create_row(
        user=user, table=table, values={f"field_{field.id}": select_options[1].id}
    )
    assert getattr(row_3, f"field_{field.id}").id == select_options[1].id
    assert getattr(row_3, f"field_{field.id}_id") == select_options[1].id

    row_4 = row_handler.create_row(
        user=user, table=table, values={f"field_{field.id}": select_options[0].id}
    )
    assert getattr(row_4, f"field_{field.id}").id == select_options[0].id
    assert getattr(row_4, f"field_{field.id}_id") == select_options[0].id

    model = table.get_model()
    row_0, row_1, row_2, row_3 = model.objects.all()

    with django_assert_num_queries(2):
        rows = list(model.objects.all().enhance_by_fields())

    assert getattr(row_0, f"field_{field.id}") is None
    assert getattr(row_1, f"field_{field.id}").id == select_options[0].id
    assert getattr(row_2, f"field_{field.id}").id == select_options[1].id
    assert getattr(row_3, f"field_{field.id}").id == select_options[0].id

    row.refresh_from_db()
    assert getattr(row, f"field_{field.id}") is None
    assert getattr(row, f"field_{field.id}_id") is None

    field = field_handler.update_field(user=user, field=field, new_type_name="text")
    assert field.select_options.all().count() == 0
    model = table.get_model()
    row_0, row_1, row_2, row_3 = model.objects.all().enhance_by_fields()
    assert getattr(row_0, f"field_{field.id}") is None
    assert getattr(row_1, f"field_{field.id}") == "Option 3"
    assert getattr(row_2, f"field_{field.id}") == "Option 4"
    assert getattr(row_3, f"field_{field.id}") == "Option 3"

    field = field_handler.update_field(
        user=user,
        field=field,
        new_type_name="single_select",
        select_options=[
            {"value": "Option 2", "color": "blue"},
            {"value": "option 3", "color": "purple"},
        ],
    )
    assert field.select_options.all().count() == 2
    model = table.get_model()
    row_0, row_1, row_2, row_3 = model.objects.all().enhance_by_fields()
    select_options = field.select_options.all()
    assert getattr(row_0, f"field_{field.id}") is None
    assert getattr(row_1, f"field_{field.id}").id == select_options[1].id
    assert getattr(row_2, f"field_{field.id}") is None
    assert getattr(row_3, f"field_{field.id}").id == select_options[1].id

    row_4 = row_handler.update_row_by_id(
        user=user, table=table, row_id=row_4.id, values={f"field_{field.id}": None}
    )
    assert getattr(row_4, f"field_{field.id}") is None
    assert getattr(row_4, f"field_{field.id}_id") is None

    field = field_handler.update_field(user=user, field=field, new_type_name="text")
    assert field.select_options.all().count() == 0
    model = table.get_model()
    row_0, row_1, row_2, row_3 = model.objects.all().enhance_by_fields()
    assert getattr(row_0, f"field_{field.id}") is None
    assert getattr(row_1, f"field_{field.id}") == "option 3"
    assert getattr(row_2, f"field_{field.id}") is None
    assert getattr(row_3, f"field_{field.id}") is None

    field = field_handler.update_field(
        user=user, field=field, new_type_name="single_select"
    )
    assert field.select_options.all().count() == 0
    model = table.get_model()
    row_0, row_1, row_2, row_3 = model.objects.all().enhance_by_fields()
    assert getattr(row_0, f"field_{field.id}") is None
    assert getattr(row_1, f"field_{field.id}") is None
    assert getattr(row_2, f"field_{field.id}") is None
    assert getattr(row_3, f"field_{field.id}") is None

    # Check that we are using the first select option when using text values
    field = field_handler.update_field(
        user=user,
        field=field,
        new_type_name="single_select",
        select_options=[
            {"value": "Option 2", "color": "blue"},
            {"value": "Option 0", "color": "purple"},
            {"value": "option 3", "color": "blue"},
            {"value": "Option 0", "color": "Orange"},
        ],
    )

    select_options = field.select_options.all()
    row_2 = row_handler.create_row(
        user=user, table=table, values={f"field_{field.id}": select_options[1].value}
    )
    assert getattr(row_2, f"field_{field.id}").id == select_options[1].id
    assert getattr(row_2, f"field_{field.id}").value == "Option 0"


@pytest.mark.django_db
@pytest.mark.api_rows
def test_single_select_field_type_multiple_rows(
    data_fixture, django_assert_num_queries
):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)

    field_handler = FieldHandler()

    field = field_handler.create_field(
        user=user,
        table=table,
        name="name",
        type_name="single_select",
        select_options=[
            {"value": "Option 1", "color": "red"},
            {"value": "Option 2", "color": "blue"},
            {"value": "Option 1", "color": "green"},
        ],
    )

    select_options = field.select_options.all()

    RowHandler().create_rows(
        user,
        table,
        rows_values=[
            {f"field_{field.id}": select_options[0].id},
            {f"field_{field.id}": select_options[1].id},
            {f"field_{field.id}": select_options[2].id},
        ],
    )

    model = table.get_model()
    row_0, row_1, row_2 = model.objects.all()

    assert getattr(row_0, f"field_{field.id}").id == select_options[0].id
    assert getattr(row_1, f"field_{field.id}").id == select_options[1].id
    assert getattr(row_2, f"field_{field.id}").id == select_options[2].id

    RowHandler().create_rows(
        user,
        table,
        rows_values=[
            {f"field_{field.id}": select_options[0].value},
            {f"field_{field.id}": select_options[1].value},
            {f"field_{field.id}": select_options[2].value},
        ],
    )

    _, _, _, row_0, row_1, row_2 = model.objects.all()

    assert getattr(row_0, f"field_{field.id}").id == select_options[0].id
    assert getattr(row_1, f"field_{field.id}").id == select_options[1].id
    assert getattr(row_2, f"field_{field.id}").id == select_options[0].id

    # Here we mix value types
    with pytest.raises(ValidationError):
        RowHandler().create_rows(
            user,
            table,
            rows_values=[
                {f"field_{field.id}": select_options[0].id},
                {f"field_{field.id}": "Missing"},
                {f"field_{field.id}": select_options[1].id},
                {f"field_{field.id}": "Missing too"},
                {f"field_{field.id}": select_options[2].value},
                {f"field_{field.id}": 99999999},
            ],
        )

    rows, error_report = RowHandler().create_rows(
        user,
        table,
        rows_values=[
            {f"field_{field.id}": select_options[0].id},
            {f"field_{field.id}": "Missing"},
            {f"field_{field.id}": select_options[1].id},
            {f"field_{field.id}": "Missing too"},
            {f"field_{field.id}": select_options[2].value},
            {f"field_{field.id}": 99999999},
        ],
        generate_error_report=True,
    )

    assert list(error_report.keys()) == [1, 3, 5]
    assert f"field_{field.id}" in error_report[1]
    assert f"field_{field.id}" in error_report[3]
    assert f"field_{field.id}" in error_report[5]

    _, _, _, _, _, _, row_0, row_1, row_2 = model.objects.all()

    assert getattr(row_0, f"field_{field.id}").id == select_options[0].id
    assert getattr(row_1, f"field_{field.id}").id == select_options[1].id
    assert getattr(row_2, f"field_{field.id}").id == select_options[0].id

    RowHandler().update_rows(
        user,
        table,
        [
            {
                "id": row_0.id,
                f"field_{field.id}": select_options[1].id,
            },
            {
                "id": row_1.id,
                f"field_{field.id}": select_options[0].id,
            },
        ],
    )

    row_0.refresh_from_db()
    row_1.refresh_from_db()

    assert getattr(row_0, f"field_{field.id}").id == select_options[1].id
    assert getattr(row_1, f"field_{field.id}").id == select_options[0].id

    RowHandler().update_rows(
        user,
        table,
        [
            {
                "id": row_0.id,
                f"field_{field.id}": select_options[0].value,
            },
            {
                "id": row_1.id,
                f"field_{field.id}": select_options[1].value,
            },
        ],
    )

    row_0.refresh_from_db()
    row_1.refresh_from_db()

    assert getattr(row_0, f"field_{field.id}").id == select_options[0].id
    assert getattr(row_1, f"field_{field.id}").id == select_options[1].id


@pytest.mark.django_db
def test_single_select_field_type_api_views(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1"
    )
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)

    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table.id}),
        {
            "name": "Select 1",
            "type": "single_select",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == "Select 1"
    assert response_json["type"] == "single_select"
    assert response_json["select_options"] == []
    assert SingleSelectField.objects.all().count() == 1
    assert SelectOption.objects.all().count() == 0

    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table.id}),
        {
            "name": "Select 2",
            "type": "single_select",
            "select_options": [{"value": "Option 1", "color": "red"}],
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    field_id = response_json["id"]
    select_options = SelectOption.objects.all()
    assert len(select_options) == 1
    assert select_options[0].field_id == field_id
    assert select_options[0].value == "Option 1"
    assert select_options[0].color == "red"
    assert select_options[0].order == 0
    assert response_json["name"] == "Select 2"
    assert response_json["type"] == "single_select"
    assert response_json["select_options"] == [
        {"id": select_options[0].id, "value": "Option 1", "color": "red"}
    ]
    assert SingleSelectField.objects.all().count() == 2

    response = api_client.patch(
        reverse("api:database:fields:item", kwargs={"field_id": field_id}),
        {"name": "New select 1"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == "New select 1"
    assert response_json["type"] == "single_select"
    assert response_json["select_options"] == [
        {"id": select_options[0].id, "value": "Option 1", "color": "red"}
    ]

    response = api_client.patch(
        reverse("api:database:fields:item", kwargs={"field_id": field_id}),
        {
            "name": "New select 1",
            "select_options": [
                {"id": select_options[0].id, "value": "Option 1 B", "color": "red 2"},
                {"value": "Option 2 B", "color": "blue 2"},
            ],
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    select_options = SelectOption.objects.all()
    assert len(select_options) == 2
    assert response_json["select_options"] == [
        {"id": select_options[0].id, "value": "Option 1 B", "color": "red 2"},
        {"id": select_options[1].id, "value": "Option 2 B", "color": "blue 2"},
    ]

    response = api_client.patch(
        reverse("api:database:fields:item", kwargs={"field_id": field_id}),
        {"name": "New select 1", "select_options": []},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert SelectOption.objects.all().count() == 0
    assert response_json["select_options"] == []

    response = api_client.patch(
        reverse("api:database:fields:item", kwargs={"field_id": field_id}),
        {
            "name": "New select 1",
            "select_options": [
                {"value": "Option 1 B", "color": "red 2"},
                {"value": "Option 2 B", "color": "blue 2"},
            ],
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    select_options = SelectOption.objects.all()
    assert len(select_options) == 2

    response = api_client.delete(
        reverse("api:database:fields:item", kwargs={"field_id": field_id}),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    assert SingleSelectField.objects.all().count() == 1
    assert SelectOption.objects.all().count() == 0


@pytest.mark.django_db
def test_single_select_field_type_api_row_views(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    other_select_option = data_fixture.create_select_option()

    field_handler = FieldHandler()

    field = field_handler.create_field(
        user=user,
        table=table,
        type_name="single_select",
        name="Single select",
        select_options=[
            {"value": "Option 1", "color": "red"},
            {"value": "Option 2", "color": "blue"},
        ],
    )

    select_options = field.select_options.all()

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": table.id}),
        {f"field_{field.id}": []},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert response_json["detail"][f"field_{field.id}"][0]["code"] == "invalid"

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": table.id}),
        {f"field_{field.id}": []},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert response_json["detail"] == {
        field.db_column: [
            {
                "error": "The provided value should be a valid integer or string",
                "code": "invalid",
            }
        ]
    }

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": table.id}),
        {f"field_{field.id}": "Nothing"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert (
        response_json["detail"] == "The provided select option value 'Nothing' is "
        "not a valid select option."
    )

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": table.id}),
        {f"field_{field.id}": 999999},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert (
        response_json["detail"]
        == "The provided select option value '999999' is not a valid select option."
    )

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": table.id}),
        {f"field_{field.id}": other_select_option.id},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert (
        response_json["detail"]
        == f"The provided select option value '{other_select_option.id}' is "
        "not a valid select option."
    )

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": table.id}),
        {f"field_{field.id}": select_options[0].id},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json[f"field_{field.id}"]["id"] == select_options[0].id
    assert response_json[f"field_{field.id}"]["value"] == "Option 1"
    assert response_json[f"field_{field.id}"]["color"] == "red"

    url = reverse(
        "api:database:rows:item",
        kwargs={"table_id": table.id, "row_id": response_json["id"]},
    )
    response = api_client.patch(
        url, {}, format="json", HTTP_AUTHORIZATION=f"JWT {token}"
    )
    assert response.status_code == HTTP_200_OK

    url = reverse(
        "api:database:rows:item",
        kwargs={"table_id": table.id, "row_id": response_json["id"]},
    )
    response = api_client.patch(
        url,
        {f"field_{field.id}": select_options[1].id},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json[f"field_{field.id}"]["id"] == select_options[1].id
    assert response_json[f"field_{field.id}"]["value"] == "Option 2"
    assert response_json[f"field_{field.id}"]["color"] == "blue"

    url = reverse(
        "api:database:rows:item",
        kwargs={"table_id": table.id, "row_id": response_json["id"]},
    )
    response = api_client.patch(
        url,
        {f"field_{field.id}": None},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json[f"field_{field.id}"] is None

    url = reverse(
        "api:database:rows:item",
        kwargs={"table_id": table.id, "row_id": response_json["id"]},
    )
    response = api_client.delete(url, format="json", HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_204_NO_CONTENT
    assert SelectOption.objects.all().count() == 3


@pytest.mark.django_db
def test_single_select_field_type_get_order(data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    field = data_fixture.create_single_select_field(table=table)
    option_c = data_fixture.create_select_option(field=field, value="C", color="blue")
    option_a = data_fixture.create_select_option(field=field, value="A", color="blue")
    option_b = data_fixture.create_select_option(field=field, value="B", color="blue")
    grid_view = data_fixture.create_grid_view(table=table)

    view_handler = ViewHandler()
    row_handler = RowHandler()

    row_1 = row_handler.create_row(
        user=user, table=table, values={f"field_{field.id}": option_b.id}
    )
    row_2 = row_handler.create_row(
        user=user, table=table, values={f"field_{field.id}": option_a.id}
    )
    row_3 = row_handler.create_row(
        user=user, table=table, values={f"field_{field.id}": option_c.id}
    )
    row_4 = row_handler.create_row(
        user=user, table=table, values={f"field_{field.id}": option_b.id}
    )
    row_5 = row_handler.create_row(
        user=user, table=table, values={f"field_{field.id}": None}
    )

    sort = data_fixture.create_view_sort(view=grid_view, field=field, order="ASC")
    model = table.get_model()
    rows = view_handler.apply_sorting(grid_view, model.objects.all())
    row_ids = [row.id for row in rows]
    assert row_ids == [row_5.id, row_2.id, row_1.id, row_4.id, row_3.id]

    sort.order = "DESC"
    sort.save()
    rows = view_handler.apply_sorting(grid_view, model.objects.all())
    row_ids = [row.id for row in rows]
    assert row_ids == [row_3.id, row_1.id, row_4.id, row_2.id, row_5.id]

    option_a.value = "Z"
    option_a.save()
    sort.order = "ASC"
    sort.save()
    model = table.get_model()
    rows = view_handler.apply_sorting(grid_view, model.objects.all())
    row_ids = [row.id for row in rows]
    assert row_ids == [row_5.id, row_1.id, row_4.id, row_3.id, row_2.id]


@pytest.mark.django_db
def test_primary_single_select_field_with_link_row_field(
    api_client, data_fixture, django_assert_num_queries
):
    """
    We expect the relation to a table that has a single select field to work.
    """

    user, token = data_fixture.create_user_and_token()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    example_table = data_fixture.create_database_table(
        name="Example", database=database
    )
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )

    field_handler = FieldHandler()
    row_handler = RowHandler()

    data_fixture.create_text_field(name="Name", table=example_table, primary=True)
    customers_primary = field_handler.create_field(
        user=user,
        table=customers_table,
        name="Single Select",
        type_name="single_select",
        select_options=[
            {"value": "Option 1", "color": "red"},
            {"value": "Option 2", "color": "blue"},
            {"value": "Option 3", "color": "orange"},
        ],
        primary=True,
    )
    link_row_field = field_handler.create_field(
        user=user,
        table=example_table,
        name="Link row",
        type_name="link_row",
        link_row_table=customers_table,
    )
    select_options = customers_primary.select_options.all()

    customers_row_1 = row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary.id}": select_options[0].id},
    )
    customers_row_2 = row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary.id}": select_options[1].id},
    )
    customers_row_3 = row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary.id}": select_options[2].id},
    )
    row_handler.create_row(
        user,
        table=example_table,
        values={f"field_{link_row_field.id}": [customers_row_1.id, customers_row_2.id]},
    )
    row_handler.create_row(
        user,
        table=example_table,
        values={f"field_{link_row_field.id}": [customers_row_1.id]},
    )
    row_handler.create_row(
        user,
        table=example_table,
        values={f"field_{link_row_field.id}": [customers_row_3.id]},
    )

    model = example_table.get_model()
    queryset = model.objects.all().enhance_by_fields()
    serializer_class = get_row_serializer_class(model, RowSerializer, is_response=True)

    with django_assert_num_queries(2):
        serializer = serializer_class(queryset, many=True)
        serializer.data

    response = api_client.get(
        reverse("api:database:rows:list", kwargs={"table_id": example_table.id}),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()

    assert (
        response_json["results"][0][f"field_{link_row_field.id}"][0]["value"]
        == "Option 1"
    )
    assert (
        response_json["results"][0][f"field_{link_row_field.id}"][1]["value"]
        == "Option 2"
    )
    assert (
        response_json["results"][1][f"field_{link_row_field.id}"][0]["value"]
        == "Option 1"
    )
    assert (
        response_json["results"][2][f"field_{link_row_field.id}"][0]["value"]
        == "Option 3"
    )


@pytest.mark.django_db
def test_single_select_field_type_random_value(data_fixture):
    """
    Verify that the random_value function of the single select field type correctly
    returns one option of a given select_options list. If the select_options list is
    empty or the passed field type is not of single select field type by any chance
    it should return None.
    """

    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    field_handler = FieldHandler()
    cache = {}
    fake = Faker()

    field = field_handler.create_field(
        user=user,
        table=table,
        type_name="single_select",
        name="Single select",
        select_options=[
            {"value": "Option 1", "color": "blue"},
            {"value": "Option 2", "color": "red"},
        ],
    )

    select_options = field.select_options.all()
    random_choice = SingleSelectFieldType().random_value(field, fake, cache)
    assert random_choice in select_options
    random_choice = SingleSelectFieldType().random_value(field, fake, cache)
    assert random_choice in select_options

    email_field = field_handler.create_field(
        user=user,
        table=table,
        type_name="email",
        name="E-Mail",
    )
    random_choice_2 = SingleSelectFieldType().random_value(email_field, fake, cache)
    assert random_choice_2 is None


@pytest.mark.django_db
def test_import_export_single_select_field(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    field_handler = FieldHandler()
    field = field_handler.create_field(
        user=user,
        table=table,
        type_name="single_select",
        name="Single select",
        select_options=[{"value": "Option 1", "color": "blue"}],
    )
    select_option = field.select_options.all().first()
    field_type = field_type_registry.get_by_model(field)
    field_serialized = field_type.export_serialized(field)
    id_mapping = {}
    field_imported = field_type.import_serialized(
        table,
        field_serialized,
        ImportExportConfig(include_permission_data=True),
        id_mapping,
        DeferredFieldFkUpdater(),
    )

    assert field_imported.select_options.all().count() == 1
    imported_select_option = field_imported.select_options.all().first()
    assert imported_select_option.id != select_option.id
    assert imported_select_option.value == select_option.value
    assert imported_select_option.color == select_option.color
    assert imported_select_option.order == select_option.order


@pytest.mark.django_db(transaction=True)
def test_get_set_export_serialized_value_single_select_field(data_fixture):
    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)
    imported_workspace = data_fixture.create_workspace(user=user)
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    field = data_fixture.create_single_select_field(table=table)
    option_a = data_fixture.create_select_option(field=field, value="A", color="green")
    option_b = data_fixture.create_select_option(field=field, value="B", color="red")

    core_handler = CoreHandler()

    model = table.get_model()
    model.objects.create()
    model.objects.create(**{f"field_{field.id}_id": option_a.id})
    model.objects.create(**{f"field_{field.id}_id": option_b.id})

    config = ImportExportConfig(include_permission_data=False)
    exported_applications = core_handler.export_workspace_applications(
        workspace, BytesIO(), config
    )
    imported_applications, id_mapping = core_handler.import_applications_to_workspace(
        imported_workspace, exported_applications, BytesIO(), config, None
    )
    imported_database = imported_applications[0]
    imported_table = imported_database.table_set.all()[0]
    imported_field = imported_table.field_set.all().first().specific

    assert imported_table.id != table.id
    assert imported_field.id != field.id

    imported_model = imported_table.get_model()
    all = imported_model.objects.all()
    assert len(all) == 3
    imported_row_1 = all[0]
    imported_row_2 = all[1]
    imported_row_3 = all[2]

    assert getattr(imported_row_1, f"field_{imported_field.id}") is None
    assert getattr(imported_row_2, f"field_{imported_field.id}_id") != option_a.id
    assert getattr(imported_row_2, f"field_{imported_field.id}").value == "A"
    assert getattr(imported_row_2, f"field_{imported_field.id}").color == "green"
    assert getattr(imported_row_3, f"field_{imported_field.id}_id") != option_b.id
    assert getattr(imported_row_3, f"field_{imported_field.id}").value == "B"
    assert getattr(imported_row_3, f"field_{imported_field.id}").color == "red"


@pytest.mark.django_db(transaction=True)
def test_get_set_export_serialized_value_single_select_field_with_deleted_option(
    data_fixture,
):
    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)
    imported_workspace = data_fixture.create_workspace(user=user)
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    field = data_fixture.create_single_select_field(table=table)
    option_a = data_fixture.create_select_option(field=field, value="A", color="green")

    core_handler = CoreHandler()

    model = table.get_model()
    model.objects.create(**{f"field_{field.id}_id": option_a.id})

    # Deleting the option doesn't set the row value to None.
    option_a.delete()

    config = ImportExportConfig(include_permission_data=False)

    exported_applications = core_handler.export_workspace_applications(
        workspace, BytesIO(), config
    )
    imported_applications, id_mapping = core_handler.import_applications_to_workspace(
        imported_workspace, exported_applications, BytesIO(), config, None
    )
    imported_database = imported_applications[0]
    imported_table = imported_database.table_set.all()[0]
    imported_field = imported_table.field_set.all().first().specific

    assert imported_table.id != table.id
    assert imported_field.id != field.id

    imported_model = imported_table.get_model()
    all = imported_model.objects.all()
    assert len(all) == 1
    imported_row_1 = all[0]

    assert getattr(imported_row_1, f"field_{imported_field.id}") is None
    assert getattr(imported_row_1, f"field_{imported_field.id}_id") is None


@pytest.mark.django_db
def test_single_select_adjacent_row(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    grid_view = data_fixture.create_grid_view(user=user, table=table, name="Test")
    single_select_field = data_fixture.create_single_select_field(
        table=table, name="option_field", order=1, primary=True
    )
    option_a = data_fixture.create_select_option(
        field=single_select_field, value="A", color="blue", order=0
    )
    option_b = data_fixture.create_select_option(
        field=single_select_field, value="B", color="red", order=1
    )
    option_c = data_fixture.create_select_option(
        field=single_select_field, value="C", color="green", order=2
    )
    data_fixture.create_view_sort(
        view=grid_view, field=single_select_field, order="ASC"
    )

    handler = RowHandler()
    [row_b, row_c, row_a] = handler.create_rows(
        user=user,
        table=table,
        rows_values=[
            {
                f"field_{single_select_field.id}": option_b.id,
            },
            {
                f"field_{single_select_field.id}": option_c.id,
            },
            {
                f"field_{single_select_field.id}": option_a.id,
            },
        ],
    )

    base_queryset = table.get_model().objects.all()

    previous_row = handler.get_adjacent_row(
        row_b, base_queryset, previous=True, view=grid_view
    )
    next_row = handler.get_adjacent_row(row_b, base_queryset, view=grid_view)

    assert previous_row.id == row_a.id
    assert next_row.id == row_c.id


@pytest.mark.django_db
def test_num_queries_n_number_of_single_select_field_get_rows_query(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    single_select_field = data_fixture.create_single_select_field(
        table=table, name="option_field", order=1, primary=True
    )
    option_a = data_fixture.create_select_option(
        field=single_select_field, value="A", color="blue", order=0
    )
    option_b = data_fixture.create_select_option(
        field=single_select_field, value="B", color="red", order=1
    )

    handler = RowHandler()
    handler.create_rows(
        user=user,
        table=table,
        rows_values=[
            {
                f"field_{single_select_field.id}": option_a.id,
            },
            {
                f"field_{single_select_field.id}": option_b.id,
            },
        ],
    )

    model = table.get_model()

    with CaptureQueriesContext(connection) as query_1:
        result = list(model.objects.all().enhance_by_fields())
        getattr(result[0], f"field_{single_select_field.id}").id
        getattr(result[1], f"field_{single_select_field.id}").id

    single_select_field_2 = data_fixture.create_single_select_field(
        table=table, name="option_field_2", order=2, primary=True
    )
    option_1 = data_fixture.create_select_option(
        field=single_select_field_2, value="1", color="blue", order=0
    )
    option_2 = data_fixture.create_select_option(
        field=single_select_field_2, value="2", color="red", order=1
    )

    model = table.get_model()
    rows = list(model.objects.all())
    setattr(rows[0], f"field_{single_select_field_2.id}_id", option_1.id)
    rows[0].save()
    setattr(rows[1], f"field_{single_select_field_2.id}_id", option_2.id)
    rows[1].save()

    with CaptureQueriesContext(connection) as query_2:
        result = list(model.objects.all().enhance_by_fields())
        print(getattr(result[0], f"field_{single_select_field.id}").id)
        print(getattr(result[0], f"field_{single_select_field_2.id}").id)
        print(getattr(result[1], f"field_{single_select_field.id}").id)
        print(getattr(result[1], f"field_{single_select_field_2.id}").id)

    assert len(query_1.captured_queries) == len(query_2.captured_queries)


@pytest.mark.django_db
@pytest.mark.field_single_select
@pytest.mark.row_history
def test_single_select_serialize_metadata_for_row_history(
    data_fixture, django_assert_num_queries
):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    field_handler = FieldHandler()
    field = field_handler.create_field(
        user=user,
        table=table,
        type_name="single_select",
        name="Single select",
        select_options=[
            {"value": "Option 1", "color": "blue"},
            {"value": "Option 2", "color": "red"},
            {"value": "Option 3", "color": "white"},
            {"value": "Option 4", "color": "green"},
        ],
    )
    model = table.get_model()
    row_handler = RowHandler()
    select_options = field.select_options.all()
    select_option_1_id = select_options[0].id
    select_option_3_id = select_options[2].id
    original_row = row_handler.create_row(
        user=user,
        table=table,
        model=model,
        values={f"field_{field.id}": select_option_1_id},
    )

    updated_row = model.objects.first()
    setattr(updated_row, f"field_{field.id}", select_options[2])

    with django_assert_num_queries(0):
        metadata = SingleSelectFieldType().serialize_metadata_for_row_history(
            field, original_row, None
        )
        metadata = SingleSelectFieldType().serialize_metadata_for_row_history(
            field, updated_row, metadata
        )
        assert metadata == {
            "id": AnyInt(),
            "select_options": {
                select_option_1_id: {
                    "color": "blue",
                    "id": select_option_1_id,
                    "value": "Option 1",
                },
                select_option_3_id: {
                    "color": "white",
                    "id": select_option_3_id,
                    "value": "Option 3",
                },
            },
            "type": "single_select",
        }

    # empty values
    original_row = row_handler.create_row(
        user=user,
        table=table,
        model=model,
        values={f"field_{field.id}": None},
    )

    with django_assert_num_queries(0):
        assert SingleSelectFieldType().serialize_metadata_for_row_history(
            field, original_row, None
        ) == {
            "id": AnyInt(),
            "select_options": {},
            "type": "single_select",
        }
