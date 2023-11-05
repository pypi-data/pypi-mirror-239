import json

import pytest
from rest_framework import serializers

from baserow_dynamic_table.api.rows.serializers import (
    RowSerializer,
    get_example_row_serializer_class,
    get_row_serializer_class,
    remap_serialized_row_to_user_field_names,
)
from baserow_dynamic_table.fields.handler import FieldHandler
from baserow_dynamic_table.fields.models import SelectOption
from baserow_dynamic_table.fields.registries import field_type_registry
from baserow.test_utils.helpers import setup_interesting_test_table


@pytest.mark.django_db
def test_get_table_serializer(data_fixture):
    table = data_fixture.create_database_table(name="Cars")
    text_field = data_fixture.create_text_field(
        table=table, order=0, name="Color", text_default="white"
    )
    data_fixture.create_number_field(table=table, order=1, name="Horsepower")
    data_fixture.create_boolean_field(table=table, order=3, name="For sale")
    data_fixture.create_number_field(
        table=table,
        order=4,
        name="Price",
        number_negative=True,
        number_decimal_places=2,
    )

    model = table.get_model(attribute_names=True)
    serializer_class = get_row_serializer_class(model=model)

    # expect the result to be empty if not provided
    serializer_instance = serializer_class(data={})
    assert serializer_instance.is_valid()
    assert serializer_instance.data == {
        "color": "white",
        "horsepower": None,
        "for_sale": False,
        "price": None,
    }

    # text field
    serializer_instance = serializer_class(data={"color": "Green"})
    assert serializer_instance.is_valid()
    assert serializer_instance.data["color"] == "Green"

    serializer_instance = serializer_class(data={"color": 123})
    assert serializer_instance.is_valid()
    assert serializer_instance.data["color"] == "123"

    serializer_instance = serializer_class(data={"color": None})
    assert serializer_instance.is_valid()
    assert serializer_instance.data["color"] is None

    # number field
    serializer_instance = serializer_class(data={"horsepower": 120})
    assert serializer_instance.is_valid()
    assert serializer_instance.data["horsepower"] == "120"

    serializer_instance = serializer_class(
        data={"horsepower": 99999999999999999999999999999999999999999999999999}
    )
    assert serializer_instance.is_valid()
    assert (
        serializer_instance.data["horsepower"]
        == "99999999999999999999999999999999999999999999999999"
    )

    serializer_instance = serializer_class(
        data={"horsepower": 999999999999999999999999999999999999999999999999999}
    )
    assert not serializer_instance.is_valid()

    serializer_instance = serializer_class(data={"horsepower": None})
    assert serializer_instance.is_valid()
    assert serializer_instance.data["horsepower"] is None

    serializer_instance = serializer_class(data={"horsepower": "abc"})
    assert not serializer_instance.is_valid()
    assert len(serializer_instance.errors["horsepower"]) == 1

    serializer_instance = serializer_class(data={"horsepower": -1})
    assert not serializer_instance.is_valid()
    assert len(serializer_instance.errors["horsepower"]) == 1

    # boolean field
    serializer_instance = serializer_class(data={"for_sale": True})
    assert serializer_instance.is_valid()
    assert serializer_instance.data["for_sale"] is True

    serializer_instance = serializer_class(data={"for_sale": False})
    assert serializer_instance.is_valid()
    assert serializer_instance.data["for_sale"] is False

    serializer_instance = serializer_class(data={"for_sale": None})
    assert not serializer_instance.is_valid()
    assert len(serializer_instance.errors["for_sale"]) == 1

    serializer_instance = serializer_class(data={"for_sale": "abc"})
    assert not serializer_instance.is_valid()
    assert len(serializer_instance.errors["for_sale"]) == 1

    # price field
    serializer_instance = serializer_class(data={"price": 120})
    assert serializer_instance.is_valid()
    assert serializer_instance.data["price"] == "120.00"

    serializer_instance = serializer_class(data={"price": "-10.22"})
    assert serializer_instance.is_valid()
    assert serializer_instance.data["price"] == "-10.22"

    serializer_instance = serializer_class(data={"price": "abc"})
    assert not serializer_instance.is_valid()
    assert len(serializer_instance.errors["price"]) == 1

    serializer_instance = serializer_class(data={"price": None})
    assert serializer_instance.is_valid()
    assert serializer_instance.data["price"] is None

    # not existing value
    serializer_instance = serializer_class(data={"NOT_EXISTING": True})
    assert serializer_instance.is_valid()
    assert serializer_instance.data == {
        "color": "white",
        "horsepower": None,
        "for_sale": False,
        "price": None,
    }

    # all fields
    serializer_instance = serializer_class(
        data={"color": "green", "horsepower": 120, "for_sale": True, "price": 120.22}
    )
    assert serializer_instance.is_valid()
    assert serializer_instance.data == {
        "color": "green",
        "horsepower": "120",
        "for_sale": True,
        "price": "120.22",
    }

    # adding an extra field and only use that one.
    price_field = data_fixture.create_number_field(
        table=table,
        order=0,
        name="Sale price",
        number_decimal_places=3,
        number_negative=True,
    )
    model = table.get_model(fields=[price_field], field_ids=[])
    serializer_class = get_row_serializer_class(model=model)

    serializer_instance = serializer_class(data={f"field_{price_field.id}": 12.22})
    assert serializer_instance.is_valid()
    assert serializer_instance.data == {f"field_{price_field.id}": "12.220"}

    serializer_instance = serializer_class(data={f"field_{price_field.id}": -10.02})
    assert serializer_instance.is_valid()
    assert serializer_instance.data == {f"field_{price_field.id}": "-10.020"}

    serializer_instance = serializer_class(data={f"field_{price_field.id}": "abc"})
    assert not serializer_instance.is_valid()
    assert len(serializer_instance.errors[f"field_{price_field.id}"]) == 1

    model = table.get_model(attribute_names=True)
    serializer_class = get_row_serializer_class(model=model, field_ids=[text_field.id])
    serializer_instance = serializer_class(data={})
    assert serializer_instance.is_valid()
    assert serializer_instance.data == {"color": "white"}

    serializer_class = get_row_serializer_class(
        model=model, field_names_to_include=[text_field.name]
    )
    serializer_instance = serializer_class(data={})
    assert serializer_instance.is_valid()
    assert serializer_instance.data == {"color": "white"}


@pytest.mark.django_db
def test_get_example_row_serializer_class():
    request_serializer = get_example_row_serializer_class(example_type="post")
    response_serializer = get_example_row_serializer_class(example_type="get")

    num_request_fields = len(request_serializer._declared_fields)
    num_response_fields = len(response_serializer._declared_fields)
    num_readonly_fields = len(
        [ftype for ftype in field_type_registry.registry.values() if ftype.read_only]
    )
    num_extra_response_fields = 2  # id + order
    num_difference = num_readonly_fields + num_extra_response_fields

    assert num_request_fields == num_response_fields - num_difference
    assert num_response_fields == (
        len(field_type_registry.registry.values()) + num_extra_response_fields
    )

    assert isinstance(
        response_serializer._declared_fields["id"], serializers.IntegerField
    )

    # This assert depends on TextField to be added first in the
    # `baserow_dynamic_table.config` module.
    assert isinstance(
        response_serializer._declared_fields["field_1"], serializers.CharField
    )


@pytest.mark.django_db
def test_get_row_serializer_with_user_field_names(data_fixture):
    table, user, row, _, context = setup_interesting_test_table(data_fixture)
    model = table.get_model()
    queryset = model.objects.all().enhance_by_fields()
    serializer_class = get_row_serializer_class(
        model, RowSerializer, is_response=True, user_field_names=True
    )
    serializer_instance = serializer_class(queryset, many=True)
    assert json.loads(json.dumps(serializer_instance.data[1])) == json.loads(
        json.dumps(
            {
                "boolean": True,
                "date_eu": "2020-02-01",
                "date_us": "2020-02-01",
                "datetime_eu": "2020-02-01T01:23:00Z",
                "datetime_us": "2020-02-01T01:23:00Z",
                "datetime_eu_tzone_visible": "2020-02-01T01:23:00Z",
                "datetime_eu_tzone_hidden": "2020-02-01T01:23:00Z",
                "last_modified_date_eu": "2021-01-02",
                "last_modified_date_us": "2021-01-02",
                "last_modified_datetime_eu": "2021-01-02T12:00:00Z",
                "last_modified_datetime_us": "2021-01-02T12:00:00Z",
                "last_modified_datetime_eu_tzone": "2021-01-02T12:00:00Z",
                "created_on_date_eu": "2021-01-02",
                "created_on_date_us": "2021-01-02",
                "created_on_datetime_eu": "2021-01-02T12:00:00Z",
                "created_on_datetime_us": "2021-01-02T12:00:00Z",
                "created_on_datetime_eu_tzone": "2021-01-02T12:00:00Z",
                "decimal_link_row": [
                    {"id": 1, "value": "1.234"},
                    {"id": 2, "value": "-123.456"},
                    {"id": 3, "value": ""},
                ],
                "email": "test@example.com",
                "file": [
                    {
                        "image_height": 0,
                        "image_width": 0,
                        "is_image": False,
                        "mime_type": "text/plain",
                        "name": "hashed_name.txt",
                        "size": 0,
                        "thumbnails": None,
                        "uploaded_at": "2020-02-01 01:23",
                        "url": "http://localhost:8000/media/user_files/hashed_name.txt",
                        "visible_name": "a.txt",
                    },
                    {
                        "image_height": 0,
                        "image_width": 0,
                        "is_image": False,
                        "mime_type": "text/plain",
                        "name": "other_name.txt",
                        "size": 0,
                        "thumbnails": None,
                        "uploaded_at": "2020-02-01 01:23",
                        "url": "http://localhost:8000/media/user_files/other_name.txt",
                        "visible_name": "b.txt",
                    },
                ],
                "file_link_row": [
                    {"id": 1, "value": "name.txt"},
                    {"id": 2, "value": ""},
                ],
                "id": 2,
                "link_row": [
                    {"id": 1, "value": "linked_row_1"},
                    {"id": 2, "value": "linked_row_2"},
                    {"id": 3, "value": ""},
                ],
                "self_link_row": [{"id": 1, "value": ""}],
                "link_row_without_related": [
                    {"id": 1, "value": "linked_row_1"},
                    {"id": 2, "value": "linked_row_2"},
                ],
                "long_text": "long_text",
                "negative_decimal": "-1.2",
                "negative_int": "-1",
                "order": "1.00000000000000000000",
                "phone_number": "+4412345678",
                "positive_decimal": "1.2",
                "positive_int": "1",
                "rating": 3,
                "single_select": {
                    "color": "red",
                    "id": SelectOption.objects.get(value="A").id,
                    "value": "A",
                },
                "multiple_collaborators": [
                    {"id": context["user2"].id, "name": context["user2"].first_name},
                    {"id": context["user3"].id, "name": context["user3"].first_name},
                ],
                "multiple_select": [
                    {
                        "color": "yellow",
                        "id": SelectOption.objects.get(value="D").id,
                        "value": "D",
                    },
                    {
                        "color": "orange",
                        "id": SelectOption.objects.get(value="C").id,
                        "value": "C",
                    },
                    {
                        "color": "green",
                        "id": SelectOption.objects.get(value="E").id,
                        "value": "E",
                    },
                ],
                "text": "text",
                "url": "https://www.google.com",
                "formula_bool": True,
                "formula_date": "2020-01-01",
                "formula_dateinterval": "1 day",
                "formula_decimal": "33.3333333333",
                "formula_email": "test@example.com",
                "formula_int": "1",
                "formula_singleselect": {
                    "color": "red",
                    "id": SelectOption.objects.get(value="A").id,
                    "value": "A",
                },
                "formula_text": "test FORMULA",
                "count": "3",
                "rollup": "-122.222",
                "lookup": [
                    {"id": 1, "value": "linked_row_1"},
                    {"id": 2, "value": "linked_row_2"},
                    {"id": 3, "value": None},
                ],
                "formula_link_url_only": {"label": None, "url": "https://google.com"},
                "formula_link_with_label": {
                    "label": "label",
                    "url": "https://google.com",
                },
            }
        )
    )


@pytest.mark.django_db
def test_remap_serialized_row_to_user_field_names(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    table_2 = data_fixture.create_database_table(database=table.database)

    text_field = data_fixture.create_text_field(
        table=table, primary=True, name="Test 1"
    )
    table_2_primary_field = data_fixture.create_text_field(
        table=table_2, name="Primary Field", primary=True
    )

    link_row_field = FieldHandler().create_field(
        user=user,
        table=table,
        type_name="link_row",
        name="Link",
        link_row_table=table_2,
    )

    lookup_model = table_2.get_model()
    i1 = lookup_model.objects.create(
        **{f"field_{table_2_primary_field.id}": "Lookup 1"}
    )

    grid = data_fixture.create_grid_view(table=table)
    data_fixture.create_grid_view_field_option(grid, link_row_field, hidden=False)

    model = table.get_model()
    row = model.objects.create(**{f"field_{text_field.id}": "Test value"})
    getattr(row, f"field_{link_row_field.id}").add(i1.id)

    serialized_row = get_row_serializer_class(
        model,
        RowSerializer,
        is_response=True,
        user_field_names=False,
    )(row).data

    remapped_row = remap_serialized_row_to_user_field_names(serialized_row, model)
    assert remapped_row == {
        "id": 1,
        "order": "1.00000000000000000000",
        "Link": [{"id": 1, "value": "Lookup 1"}],
        "Test 1": "Test value",
    }
