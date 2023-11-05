from io import BytesIO

from django.apps.registry import apps
from django.db import connections
from django.shortcuts import reverse

import pytest
from faker import Faker
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from baserow_dynamic_table.fields.dependencies.exceptions import (
    SelfReferenceFieldDependencyError,
)
from baserow_dynamic_table.fields.exceptions import (
    LinkRowTableNotInSameDatabase,
    LinkRowTableNotProvided,
    SelfReferencingLinkRowCannotHaveRelatedField,
)
from baserow_dynamic_table.fields.field_types import LinkRowFieldType
from baserow_dynamic_table.fields.handler import FieldHandler
from baserow_dynamic_table.fields.models import Field, LinkRowField, TextField
from baserow_dynamic_table.fields.registries import field_type_registry
from baserow_dynamic_table.rows.handler import RowHandler
from baserow_dynamic_table.table.handler import TableHandler
from baserow.core.handler import CoreHandler
from baserow.core.models import TrashEntry
from baserow.core.registries import ImportExportConfig
from baserow.core.trash.handler import TrashHandler
from baserow.test_utils.helpers import AnyInt


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_call_apps_registry_pending_operations(data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )
    field_handler = FieldHandler()
    field_handler.create_field(
        user=user,
        table=table,
        type_name="link_row",
        name="Test",
        link_row_table=customers_table,
    )
    table.get_model()
    # Make sure that there are no pending operations in the app registry. Because a
    # Django ManyToManyField registers pending operations every time a table model is
    # generated, which can causes a memory leak if they are not triggered.
    assert len(apps._pending_operations) == 0


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_link_row_field_type(data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )
    cars_table = data_fixture.create_database_table(name="Cars", database=database)
    unrelated_table_1 = data_fixture.create_database_table(name="Unrelated")

    field_handler = FieldHandler()
    row_handler = RowHandler()

    # Create a primary field and some example data for the customers table.
    customers_primary_field = field_handler.create_field(
        user=user, table=customers_table, type_name="text", name="Name", primary=True
    )
    customers_row_1 = row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary_field.id}": "John"},
    )
    customers_row_2 = row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary_field.id}": "Jane"},
    )

    # Create a primary field and some example data for the cars table.
    cars_primary_field = field_handler.create_field(
        user=user, table=cars_table, type_name="text", name="Name", primary=True
    )
    row_handler.create_row(
        user=user, table=cars_table, values={f"field_{cars_primary_field.id}": "BMW"}
    )
    row_handler.create_row(
        user=user, table=cars_table, values={f"field_{cars_primary_field.id}": "Audi"}
    )

    with pytest.raises(LinkRowTableNotProvided):
        field_handler.create_field(
            user=user, table=table, type_name="link_row", name="Without table"
        )

    with pytest.raises(LinkRowTableNotInSameDatabase):
        field_handler.create_field(
            user=user,
            table=table,
            type_name="link_row",
            name="Unrelated",
            link_row_table=unrelated_table_1,
        )

    link_field_1 = field_handler.create_field(
        user=user,
        table=table,
        type_name="link_row",
        name="Customer",
        link_row_table=customers_table,
    )
    link_field_2 = field_handler.create_field(
        user=user,
        table=table,
        type_name="link_row",
        name="Customer 2",
        link_row_table=customers_table,
    )

    assert link_field_1.link_row_related_field.name == "Example"
    assert link_field_2.link_row_related_field.name == "Example - Customer 2"

    connection = connections["default"]
    tables = connection.introspection.table_names()

    assert (
        link_field_1.through_table_name
        == link_field_1.link_row_related_field.through_table_name
    )
    assert (
        link_field_2.through_table_name
        == link_field_2.link_row_related_field.through_table_name
    )

    assert link_field_1.through_table_name in tables
    assert link_field_2.through_table_name in tables

    model = table.get_model()
    table_row = model.objects.create()

    getattr(table_row, f"field_{link_field_1.id}").add(customers_row_1.id)
    results = getattr(table_row, f"field_{link_field_1.id}").all()
    assert len(results) == 1
    assert getattr(results[0], f"field_{customers_primary_field.id}") == "John"

    getattr(table_row, f"field_{link_field_2.id}").add(
        customers_row_1.id, customers_row_2.id
    )
    results = getattr(table_row, f"field_{link_field_2.id}").all()
    assert len(results) == 2
    assert getattr(results[0], f"field_{customers_primary_field.id}") == "John"
    assert getattr(results[1], f"field_{customers_primary_field.id}") == "Jane"

    table_row_2 = model.objects.create()
    getattr(table_row_2, f"field_{link_field_1.id}").add(customers_row_2.id)
    results = getattr(table_row_2, f"field_{link_field_1.id}").all()
    assert len(results) == 1
    assert getattr(results[0], f"field_{customers_primary_field.id}") == "Jane"

    # Going to change only the name of the field. This should not result in any errors
    # of schema changes.
    link_field_1 = field_handler.update_field(
        user, link_field_1, name="Customer Renamed"
    )

    with pytest.raises(LinkRowTableNotInSameDatabase):
        field_handler.update_field(user, link_field_1, link_row_table=unrelated_table_1)

    model = table.get_model()
    assert model.objects.all().count() == 2

    # Change the table, this should destroy all relations.
    old_link_field_1_relation_id = link_field_1.link_row_relation_id
    link_field_1 = field_handler.update_field(
        user, link_field_1, link_row_table=cars_table
    )

    model = table.get_model()
    table_rows = model.objects.all()
    table_row = table_rows[0]
    table_row_2 = table_rows[1]

    assert link_field_1.link_row_table.id == cars_table.id
    assert link_field_1.link_row_relation_id == old_link_field_1_relation_id
    assert getattr(table_row, f"field_{link_field_1.id}").all().count() == 0
    assert getattr(table_row, f"field_{link_field_2.id}").all().count() == 2
    assert getattr(table_row_2, f"field_{link_field_1.id}").all().count() == 0
    assert getattr(table_row_2, f"field_{link_field_2.id}").all().count() == 0

    link_field_2 = field_handler.update_field(user, link_field_2, new_type_name="text")
    assert isinstance(link_field_2, TextField)

    model = table.get_model()
    table_row = model.objects.all().first()

    assert getattr(table_row, f"field_{link_field_2.id}") is None
    assert LinkRowField.objects.all().count() == 2

    setattr(table_row, f"field_{link_field_2.id}", "Text value")
    table_row.save()
    assert getattr(table_row, f"field_{link_field_2.id}") == "Text value"

    # Delete the existing field. Alter that the related field should be trashed.
    field_handler.delete_field(user, link_field_1)

    # Change a the text field back into a link row field.
    link_field_2 = field_handler.update_field(
        user,
        link_field_2,
        new_type_name="link_row",
        link_row_table=customers_table,
    )

    assert link_field_2.link_row_related_field.name == "Example"
    assert (
        link_field_2.through_table_name
        == link_field_2.link_row_related_field.through_table_name
    )
    assert link_field_2.through_table_name in connection.introspection.table_names()
    assert LinkRowField.objects.all().count() == 2

    model = table.get_model()
    table_row = model.objects.all().first()

    getattr(table_row, f"field_{link_field_2.id}").add(
        customers_row_1.id, customers_row_2.id
    )
    results = getattr(table_row, f"field_{link_field_2.id}").all()
    assert len(results) == 2
    assert getattr(results[0], f"field_{customers_primary_field.id}") == "John"
    assert getattr(results[1], f"field_{customers_primary_field.id}") == "Jane"


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_link_row_field_type_with_text_values(data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)

    field_handler = FieldHandler()
    row_handler = RowHandler()

    fake = Faker()
    Faker.seed(4324)
    cache = {}

    data = []
    row_values = {}

    for field_type in [
        f
        for f in field_type_registry.get_all()
        if f.can_get_unique_values and not f.read_only
    ]:
        field_type_name = field_type.type
        field_name = f"Field {field_type_name}"
        field_table = data_fixture.create_database_table(
            name=f"Link table {field_type_name}", database=database
        )
        # Create a primary field and some example data for the events table.
        primary_field = field_handler.create_field(
            user=user,
            table=field_table,
            type_name=field_type.type,
            name=field_name,
            primary=True,
        )
        if field_type.can_have_select_options:
            for order in range(10):
                data_fixture.create_select_option(
                    None, field=primary_field, order=order, value=f"Option {order}"
                )

        value1 = field_type.random_value(primary_field, fake, cache)
        value2 = field_type.random_value(primary_field, fake, cache)

        # To be sure we have different values
        while value1 == value2:
            value2 = field_type.random_value(primary_field, fake, cache)

        row_1 = row_handler.create_row(
            user=user,
            table=field_table,
            values={primary_field.db_column: value1},
        )
        row_2 = row_handler.create_row(
            user=user,
            table=field_table,
            values={primary_field.db_column: value2},
        )

        link_field = field_handler.create_field(
            user=user,
            table=table,
            type_name="link_row",
            name=f"Link field {field_type_name}",
            link_row_table=field_table,
        )

        field_object = {
            "field": primary_field,
            "type": field_type,
            "name": field_name,
        }

        text_value = field_type.get_export_value(
            getattr(row_2, primary_field.db_column), field_object
        )

        data.append((link_field, row_1, row_2, field_type_name))
        row_values[link_field.db_column] = [
            row_1.id,
            str(text_value),
        ]

    # If we mix ids and text values, we should still get the right result
    row = row_handler.create_row(user=user, table=table, values=row_values)

    for link_field, row_1, row_2, field_type_name in data:
        assert list(
            getattr(row, link_field.db_column).all().values_list("id", flat=True)
        ) == [
            row_1.id,
            row_2.id,
        ], f"Failed to import a {field_type_name} link"


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_link_row_field_type_rows(data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    example_table = data_fixture.create_database_table(
        name="Example", database=database
    )
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )
    data_fixture.create_text_field(name="Name", table=customers_table, primary=True)
    users_table = data_fixture.create_database_table(name="Users", database=database)

    field_handler = FieldHandler()
    row_handler = RowHandler()

    link_row_field = field_handler.create_field(
        user=user,
        table=example_table,
        name="Link Row",
        type_name="link_row",
        link_row_table=customers_table,
    )

    customers_row_1 = row_handler.create_row(user=user, table=customers_table)
    customers_row_2 = row_handler.create_row(user=user, table=customers_table)
    customers_row_3 = row_handler.create_row(user=user, table=customers_table)

    row = row_handler.create_row(
        user=user,
        table=example_table,
        values={
            f"field_{link_row_field.id}": [customers_row_1.id, customers_row_2.id],
        },
    )
    row_2 = row_handler.create_row(
        user=user,
        table=example_table,
        values={
            f"field_{link_row_field.id}": [customers_row_1.id],
        },
    )

    example_table.name = "Example2"
    example_table.save()

    customers_table.name = "Customers2"
    customers_table.save()

    row_1_all = getattr(row, f"field_{link_row_field.id}").all()
    row_2_all = getattr(row_2, f"field_{link_row_field.id}").all()
    row_1_ids = [i.id for i in row_1_all]
    row_2_ids = [i.id for i in row_2_all]

    assert row_1_all.count() == 2
    assert row_2_all.count() == 1
    assert customers_row_1.id in row_1_ids
    assert customers_row_2.id in row_1_ids
    assert customers_row_1.id in row_2_ids

    row = row_handler.update_row_by_id(
        user=user,
        table=example_table,
        row_id=row.id,
        values={f"field_{link_row_field.id}": [customers_row_3.id]},
    )
    row_2 = row_handler.update_row_by_id(
        user=user,
        table=example_table,
        row_id=row_2.id,
        values={f"field_{link_row_field.id}": [customers_row_2.id, customers_row_1.id]},
    )

    row_1_all = getattr(row, f"field_{link_row_field.id}").all()
    row_2_all = getattr(row_2, f"field_{link_row_field.id}").all()
    row_1_ids = [i.id for i in row_1_all]
    row_2_ids = [i.id for i in row_2_all]

    assert row_1_all.count() == 1
    assert row_2_all.count() == 2
    assert customers_row_3.id in row_1_ids
    assert customers_row_1.id in row_2_ids
    assert customers_row_2.id in row_2_ids

    # Check if the relations are there via the customers table.
    customers_table.refresh_from_db()
    customers_model = customers_table.get_model()
    related_field = link_row_field.link_row_related_field
    customer_rows = customers_model.objects.all()

    assert customer_rows.count() == 3
    row_1, row_2, row_3 = customer_rows

    customers_row_1 = row_1
    customers_row_2 = row_2
    customers_row_3 = row_3

    customer_row_1_all = getattr(customers_row_1, f"field_{related_field.id}").all()
    customer_row_2_all = getattr(customers_row_2, f"field_{related_field.id}").all()
    customer_row_3_all = getattr(customers_row_3, f"field_{related_field.id}").all()

    assert customer_row_1_all.count() == 1
    assert customer_row_2_all.count() == 1
    assert customer_row_3_all.count() == 1

    customers_row_1_ids = [i.id for i in customer_row_1_all]
    customers_row_2_ids = [i.id for i in customer_row_2_all]
    customers_row_3_ids = [i.id for i in customer_row_3_all]

    assert row_2.id in customers_row_1_ids
    assert row_2.id in customers_row_2_ids
    assert row.id in customers_row_3_ids

    # When changing the link row table table all the existing relations should be
    # deleted.
    link_row_field = field_handler.update_field(
        user=user,
        field=link_row_field,
        type_name="link_row",
        link_row_table=users_table,
    )

    example_table.refresh_from_db()
    model = example_table.get_model()
    rows = model.objects.all()
    row = rows[0]
    row_2 = rows[1]

    assert getattr(row, f"field_{link_row_field.id}").all().count() == 0
    assert getattr(row_2, f"field_{link_row_field.id}").all().count() == 0

    # Just check if the field can be deleted.
    field_handler.delete_field(user=user, field=link_row_field)
    # We expect only the primary field to be left.
    objects_all = Field.objects.all()
    assert objects_all.count() == 1


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_link_row_enhance_queryset(data_fixture, django_assert_num_queries):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    example_table = data_fixture.create_database_table(
        name="Example", database=database
    )
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )

    field_handler = FieldHandler()
    row_handler = RowHandler()

    link_row_field = field_handler.create_field(
        user=user,
        table=example_table,
        name="Link Row",
        type_name="link_row",
        link_row_table=customers_table,
    )

    customers_row_1 = row_handler.create_row(user=user, table=customers_table)
    customers_row_2 = row_handler.create_row(user=user, table=customers_table)
    customers_row_3 = row_handler.create_row(user=user, table=customers_table)

    row_handler.create_row(
        user=user,
        table=example_table,
        values={
            f"field_{link_row_field.id}": [customers_row_1.id, customers_row_2.id],
        },
    )
    row_handler.create_row(
        user=user,
        table=example_table,
        values={
            f"field_{link_row_field.id}": [customers_row_1.id],
        },
    )
    row_handler.create_row(
        user=user,
        table=example_table,
        values={
            f"field_{link_row_field.id}": [customers_row_3.id],
        },
    )

    model = example_table.get_model()
    rows = list(model.objects.all().enhance_by_fields())

    with django_assert_num_queries(0):
        for row in rows:
            list(getattr(row, f"field_{link_row_field.id}").all())


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_link_row_field_type_api_views(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1"
    )
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    unrelated_database = data_fixture.create_database_application(
        user=user, name="Unrelated"
    )
    table = data_fixture.create_database_table(name="Example", database=database)
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )
    cars_table = data_fixture.create_database_table(name="Cars", database=database)
    unrelated_table_1 = data_fixture.create_database_table(
        name="Unrelated", database=unrelated_database
    )
    unrelated_table_2 = data_fixture.create_database_table(name="Unrelated 2")

    # Try to make a relation with a table from another database
    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table.id}),
        {"name": "Link", "type": "link_row", "link_row_table_id": unrelated_table_1.id},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_LINK_ROW_TABLE_NOT_IN_SAME_DATABASE"
    assert LinkRowField.objects.all().count() == 0

    # Try to make a relation with a table that we don't have access to.
    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table.id}),
        {"name": "Link", "type": "link_row", "link_row_table_id": unrelated_table_2.id},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_USER_NOT_IN_GROUP"
    assert LinkRowField.objects.all().count() == 0

    # Try to make a relation without providing the table
    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table.id}),
        {"name": "Link", "type": "link_row"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_LINK_ROW_TABLE_NOT_PROVIDED"
    assert LinkRowField.objects.all().count() == 0

    # Create new link row field type using the deprecated `link_row_table` parameter.
    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table.id}),
        {
            "name": "Link 1",
            "type": "link_row",
            "link_row_table": customers_table.id,
            # The `link_row_related_field` is a read_only field so we deliberately set
            # an unknown id to see if it is ignored.
            "link_row_related_field": 999999,
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK, response_json
    assert response_json["name"] == "Link 1"
    assert response_json["type"] == "link_row"
    assert response_json["link_row_table_id"] == customers_table.id
    assert LinkRowField.objects.all().count() == 2
    field_id = response_json["id"]

    field = LinkRowField.objects.all().order_by("id").first()
    related_field = LinkRowField.objects.all().order_by("id").last()

    assert response_json["link_row_related_field_id"] == related_field.id
    assert response_json["link_row_related_field_id"] != 999999

    # Check if the correct fields are correctly linked.
    assert field.table.id == table.id
    assert field.link_row_table.id == customers_table.id
    assert related_field.table.id == customers_table.id
    assert related_field.link_row_table.id == table.id
    assert field.link_row_relation_id == related_field.link_row_relation_id

    # Just fetching the field and check if is has the correct values.
    response = api_client.get(
        reverse("api:database:fields:item", kwargs={"field_id": field_id}),
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == "Link 1"
    assert response_json["type"] == "link_row"
    assert response_json["link_row_table_id"] == customers_table.id
    assert response_json["link_row_related_field_id"] == related_field.id

    # Just fetching the related field and check if is has the correct values.
    response = api_client.get(
        reverse("api:database:fields:item", kwargs={"field_id": related_field.id}),
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == "Example"
    assert response_json["link_row_table_id"] == table.id
    assert response_json["link_row_related_field_id"] == field.id

    # Only updating the name of the field without changing anything else
    response = api_client.patch(
        reverse("api:database:fields:item", kwargs={"field_id": field_id}),
        {"name": "Link new name"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == "Link new name"
    assert response_json["type"] == "link_row"
    assert response_json["link_row_table_id"] == customers_table.id
    assert response_json["link_row_related_field_id"] == related_field.id

    # Only try to update the link_row_related_field, but this is a read only field so
    # nothing should happen.
    response = api_client.patch(
        reverse("api:database:fields:item", kwargs={"field_id": field_id}),
        {"link_row_related_field_id": 9999},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == "Link new name"
    assert response_json["type"] == "link_row"
    assert response_json["link_row_table_id"] == customers_table.id
    assert response_json["link_row_related_field_id"] == related_field.id

    response = api_client.patch(
        reverse("api:database:fields:item", kwargs={"field_id": field_id}),
        {"link_row_table_id": cars_table.id},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == "Link new name"
    assert response_json["type"] == "link_row"
    assert response_json["link_row_table_id"] == cars_table.id
    assert response_json["link_row_related_field_id"] == related_field.id

    field.refresh_from_db()
    related_field.refresh_from_db()

    # Check if the correct fields are still linked.
    assert field.table.id == table.id
    assert field.link_row_table.id == cars_table.id
    assert related_field.table.id == cars_table.id
    assert related_field.link_row_table.id == table.id

    url = reverse("api:database:fields:item", kwargs={"field_id": field_id})
    response = api_client.delete(url, HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_200_OK
    assert LinkRowField.objects.all().count() == 0


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_link_row_field_type_api_row_views(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    example_table = data_fixture.create_database_table(
        name="Example", database=database
    )
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )
    grid = data_fixture.create_grid_view(table=example_table)

    data_fixture.create_text_field(name="Name", table=example_table, primary=True)
    customers_primary = data_fixture.create_text_field(
        name="Customer name", table=customers_table, primary=True
    )

    field_handler = FieldHandler()
    row_handler = RowHandler()

    link_row_field = field_handler.create_field(
        user=user,
        table=example_table,
        name="Link Row",
        type_name="link_row",
        link_row_table=customers_table,
    )

    customers_row_1 = row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary.id}": "John Doe"},
    )
    customers_row_2 = row_handler.create_row(
        user=user,
        table=customers_table,
        values={f"field_{customers_primary.id}": "Jane Doe"},
    )
    customers_row_3 = row_handler.create_row(user=user, table=customers_table)

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": example_table.id}),
        {
            f"field_{link_row_field.id}": "Random",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert (
        response_json["detail"][f"field_{link_row_field.id}"][0]["code"] == "not_a_list"
    )

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": example_table.id}),
        {
            f"field_{link_row_field.id}": [{}],
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert (
        response_json["detail"][f"field_{link_row_field.id}"]["0"][0]["code"]
        == "invalid"
    )

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": example_table.id}),
        {
            f"field_{link_row_field.id}": [customers_row_1.id, customers_row_2.id, 999],
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    row_id = response_json["id"]
    assert response.status_code == HTTP_200_OK
    assert len(response_json[f"field_{link_row_field.id}"]) == 2
    assert response_json[f"field_{link_row_field.id}"][0]["id"] == customers_row_1.id
    assert response_json[f"field_{link_row_field.id}"][0]["value"] == "John Doe"
    assert response_json[f"field_{link_row_field.id}"][1]["id"] == customers_row_2.id
    assert response_json[f"field_{link_row_field.id}"][1]["value"] == "Jane Doe"

    model = example_table.get_model()
    assert model.objects.all().count() == 1

    url = reverse(
        "api:database:rows:item",
        kwargs={"table_id": example_table.id, "row_id": row_id},
    )
    response = api_client.patch(
        url,
        {
            f"field_{link_row_field.id}": [],
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json[f"field_{link_row_field.id}"]) == 0

    url = reverse(
        "api:database:rows:item",
        kwargs={"table_id": example_table.id, "row_id": row_id},
    )
    response = api_client.patch(
        url,
        {
            f"field_{link_row_field.id}": [customers_row_2.id, customers_row_3.id],
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json[f"field_{link_row_field.id}"]) == 2
    assert response_json[f"field_{link_row_field.id}"][0]["id"] == customers_row_2.id
    assert response_json[f"field_{link_row_field.id}"][0]["value"] == "Jane Doe"
    assert response_json[f"field_{link_row_field.id}"][1]["id"] == customers_row_3.id
    assert not response_json[f"field_{link_row_field.id}"][1]["value"]

    url = reverse("api:database:views:grid:list", kwargs={"view_id": grid.id})
    response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["count"] == 1
    assert response_json["results"][0]["id"] == row_id
    assert len(response_json["results"][0][f"field_{link_row_field.id}"]) == 2

    url = reverse(
        "api:database:rows:item",
        kwargs={"table_id": example_table.id, "row_id": row_id},
    )
    response = api_client.delete(url, HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_204_NO_CONTENT
    assert model.objects.all().count() == 0

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": example_table.id}),
        {},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json[f"field_{link_row_field.id}"]) == 0


@pytest.mark.django_db(transaction=True)
@pytest.mark.field_link_row
def test_import_export_link_row_field(data_fixture):
    user = data_fixture.create_user()
    imported_workspace = data_fixture.create_workspace(user=user)
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    customers_table = data_fixture.create_database_table(
        name="Customers", database=database
    )
    field_handler = FieldHandler()
    core_handler = CoreHandler()
    link_row_field = field_handler.create_field(
        user=user,
        table=table,
        name="Link Row",
        type_name="link_row",
        link_row_table=customers_table,
    )

    row_handler = RowHandler()
    c_row = row_handler.create_row(user=user, table=customers_table, values={})
    c_row_2 = row_handler.create_row(user=user, table=customers_table, values={})
    row = row_handler.create_row(
        user=user,
        table=table,
        values={f"field_{link_row_field.id}": [c_row.id, c_row_2.id]},
    )

    config = ImportExportConfig(include_permission_data=False)

    exported_applications = core_handler.export_workspace_applications(
        database.workspace, BytesIO(), config
    )
    imported_applications, id_mapping = core_handler.import_applications_to_workspace(
        imported_workspace, exported_applications, BytesIO(), config, None
    )
    imported_database = imported_applications[0]
    imported_tables = imported_database.table_set.all()
    imported_table = imported_tables[0]
    imported_customers_table = imported_tables[1]
    imported_link_row_field = imported_table.field_set.all().first().specific
    imported_link_row_relation_field = (
        imported_customers_table.field_set.all().first().specific
    )

    assert imported_table.id != table.id
    assert imported_table.name == table.name
    assert imported_customers_table.id != customers_table.id
    assert imported_customers_table.name == customers_table.name
    assert imported_link_row_field.id != link_row_field.id
    assert imported_link_row_field.name == link_row_field.name
    assert imported_link_row_field.link_row_table_id == imported_customers_table.id
    assert imported_link_row_relation_field.link_row_table_id == imported_table.id
    assert imported_link_row_field.link_row_relation_id == (
        imported_link_row_relation_field.link_row_relation_id
    )

    imported_c_row = row_handler.get_row(
        user=user, table=imported_customers_table, row_id=c_row.id
    )
    imported_c_row_2 = row_handler.get_row(
        user=user, table=imported_customers_table, row_id=c_row_2.id
    )
    imported_row = row_handler.get_row(user=user, table=imported_table, row_id=row.id)

    assert imported_row.id == row.id
    assert imported_c_row.id == c_row.id
    assert imported_c_row_2.id == c_row_2.id
    assert [
        r.id for r in getattr(imported_row, f"field_{imported_link_row_field.id}").all()
    ] == [imported_c_row.id, imported_c_row_2.id]


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_creating_a_linked_row_pointing_at_trashed_row_works_but_does_not_display(
    data_fixture, api_client
):
    user, token = data_fixture.create_user_and_token()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table_with_trashed_row = data_fixture.create_database_table(
        name="Customers", database=database
    )
    table_linking_to_trashed_row = data_fixture.create_database_table(
        name="Cars", database=database
    )

    field_handler = FieldHandler()
    row_handler = RowHandler()

    # Create a primary field and some example data for the customers table.
    customers_primary_field = field_handler.create_field(
        user=user,
        table=table_with_trashed_row,
        type_name="text",
        name="Name",
        primary=True,
    )
    trashed_row = row_handler.create_row(
        user=user,
        table=table_with_trashed_row,
        values={f"field_{customers_primary_field.id}": "John"},
    )

    link_field_1 = field_handler.create_field(
        user=user,
        table=table_linking_to_trashed_row,
        type_name="link_row",
        name="customer",
        link_row_table=table_with_trashed_row,
    )
    # Create a primary field and some example data for the cars table.
    field_handler.create_field(
        user=user,
        table=table_linking_to_trashed_row,
        type_name="text",
        name="Name",
        primary=True,
    )
    TrashHandler.trash(
        user,
        database.workspace,
        database,
        trashed_row,
    )

    response = api_client.post(
        reverse(
            "api:database:rows:list",
            kwargs={"table_id": table_linking_to_trashed_row.id},
        ),
        {
            f"field_{link_field_1.id}": [trashed_row.id],
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK

    # Even though the call succeeded, the linked row is not returned
    assert response_json[f"field_{link_field_1.id}"] == []

    row_id = response_json["id"]

    url = reverse(
        "api:database:rows:item",
        kwargs={"table_id": table_linking_to_trashed_row.id, "row_id": row_id},
    )
    response = api_client.get(url, HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_200_OK
    # Other endpoints also don't return this connection made whilst trashed
    assert response.json()[f"field_{link_field_1.id}"] == []

    TrashHandler.restore_item(
        user,
        "row",
        row_id,
        parent_trash_item_id=table_with_trashed_row.id,
    )

    url = reverse(
        "api:database:rows:item",
        kwargs={"table_id": table_linking_to_trashed_row.id, "row_id": row_id},
    )
    response = api_client.get(url, HTTP_AUTHORIZATION=f"JWT {token}")
    assert response.status_code == HTTP_200_OK
    # Now that the row was un-trashed, it appears.
    linked_field_values = response.json()[f"field_{link_field_1.id}"]
    assert len(linked_field_values) == 1
    assert linked_field_values[0]["id"] == trashed_row.id


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_change_type_to_link_row_field_when_field_with_same_related_name_already_exists(
    data_fixture,
):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user, name="Table")
    other_table = data_fixture.create_database_table(
        database=table.database, user=user, name="OtherTable"
    )
    field = data_fixture.create_text_field(table=table, order=1, name="Text")

    handler = FieldHandler()
    existing_link_row = handler.create_field(
        user, other_table, "link_row", link_row_table=table, name="Table"
    )

    model = table.get_model()
    model.objects.create(**{f"field_{field.id}": "9223372036854775807"})
    model.objects.create(**{f"field_{field.id}": "100"})

    # Change the field type to a link_row and test if names are changed correctly.
    new_link_row_field = handler.update_field(
        user=user,
        field=field,
        new_type_name="link_row",
        link_row_table=other_table,
    )

    existing_link_row.refresh_from_db()

    assert new_link_row_field.name == "Text"
    assert new_link_row_field.link_row_related_field.name == "Table - Text"
    assert existing_link_row.name == "Table"
    assert existing_link_row.link_row_related_field.name == "OtherTable"


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_change_link_row_related_table_when_field_with_related_name_exists(
    data_fixture,
):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user, name="Table")
    first_related_table = data_fixture.create_database_table(
        database=table.database, user=user, name="FirstRelatedTable"
    )
    second_related_table = data_fixture.create_database_table(
        database=table.database, user=user, name="SecondRelatedTable"
    )
    # Make a field in the second table whose name will clash with the link row
    # related field that will be created automatically from the first table.
    data_fixture.create_text_field(table=second_related_table, order=1, name="Table")

    handler = FieldHandler()
    link_row = handler.create_field(
        user, table, "link_row", link_row_table=first_related_table, name="Link"
    )

    # Change the link row table and test if the field name change.
    handler.update_field(
        user=user,
        field=link_row,
        new_type_name="link_row",
        link_row_table=second_related_table,
    )

    link_row.refresh_from_db()

    names = list(
        Field.objects.filter(table=second_related_table).values_list("name", flat=True)
    )
    assert names == ["Table", "Table - Link"]
    assert LinkRowField.objects.count() == 2


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_link_row_field_can_link_same_table(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user, name="Table")
    field_handler = FieldHandler()
    field = data_fixture.create_text_field(
        table=table, order=1, primary=True, name="Name"
    )
    link_row = field_handler.create_field(
        user, table, "link_row", link_row_table=table, name="Link"
    )
    link_row.refresh_from_db()
    assert link_row.link_row_related_field is None
    field_names = Field.objects.filter(table=table).values_list("name", flat=True)
    assert list(field_names) == ["Name", "Link"]

    row_handler = RowHandler()
    row_1 = row_handler.create_row(
        user=user,
        table=table,
        values={
            f"field_{field.id}": "Tesla",
        },
    )
    row_2 = row_handler.create_row(
        user=user,
        table=table,
        values={
            f"field_{field.id}": "Amazon",
            f"field_{link_row.id}": [row_1.id],
        },
    )

    assert getattr(row_2, f"field_{link_row.id}").count() == 1
    assert getattr(row_2, f"field_{link_row.id}").all()[0].id == row_1.id

    url = reverse(
        "api:database:rows:item",
        kwargs={"table_id": table.id, "row_id": row_1.id},
    )
    response = api_client.patch(
        url,
        {f"field_{link_row.id}": [row_1.id, row_2.id]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json[f"field_{link_row.id}"] == [
        {"id": row_1.id, "value": "Tesla"},
        {"id": row_2.id, "value": "Amazon"},
    ]

    # can be trashed and restored
    field_handler.delete_field(user, link_row)
    assert link_row.trashed is True

    TrashHandler().restore_item(user, "field", link_row.id)
    link_row.refresh_from_db()
    assert link_row.trashed is False


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_link_row_field_can_link_same_table_and_another_table(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table_a = data_fixture.create_database_table(user=user)
    table_b = data_fixture.create_database_table(user=user, database=table_a.database)
    grid = data_fixture.create_grid_view(user, table=table_a)

    table_a_primary = data_fixture.create_text_field(
        user, table=table_a, primary=True, name="table a pk"
    )
    table_b_primary = data_fixture.create_text_field(
        user, table=table_b, primary=True, name="table a pk"
    )

    field_handler = FieldHandler()
    table_a_self_link = field_handler.create_field(
        user, table_a, "link_row", link_row_table=table_a, name="A->A"
    )
    link_field = field_handler.create_field(
        user, table_b, "link_row", link_row_table=table_a, name="B->A"
    )

    row_handler = RowHandler()
    table_a_row_1 = row_handler.create_row(
        user=user,
        table=table_a,
        values={
            f"field_{table_a_primary.id}": "Tesla",
        },
    )
    table_a_row_2 = row_handler.create_row(
        user=user,
        table=table_a,
        values={
            f"field_{table_a_primary.id}": "Amazon",
            f"field_{table_a_self_link.id}": [table_a_row_1.id],
        },
    )

    table_b_row_1 = row_handler.create_row(
        user=user,
        table=table_b,
        values={
            f"field_{table_b_primary.id}": "Amazon",
            f"field_{link_field.id}": [table_a_row_1.id],
        },
    )

    url = reverse("api:database:views:grid:list", kwargs={"view_id": grid.id})
    response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
    response_json = response.json()
    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_link_row_can_change_link_from_same_table_to_another_table_and_back(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    table_a = data_fixture.create_database_table(user=user)
    table_b = data_fixture.create_database_table(user=user, database=table_a.database)
    table_a_primary = data_fixture.create_text_field(
        user, table=table_a, primary=True, name="table a pk"
    )
    table_b_primary = data_fixture.create_text_field(
        user, table=table_b, primary=True, name="table b pk"
    )
    grid_a = data_fixture.create_grid_view(user, table=table_a)
    grid_b = data_fixture.create_grid_view(user, table=table_b)

    field_handler = FieldHandler()
    table_a_link = field_handler.create_field(
        user, table_a, "link_row", link_row_table=table_a, name="A->A"
    )
    row_handler = RowHandler()
    table_a_row_1 = row_handler.create_row(
        user=user,
        table=table_a,
        values={
            f"field_{table_a_primary.id}": "Tesla",
        },
    )
    table_a_row_2 = row_handler.create_row(
        user=user,
        table=table_a,
        values={
            f"field_{table_a_primary.id}": "Amazon",
            f"field_{table_a_link.id}": [table_a_row_1.id],
        },
    )

    table_b_row_1 = row_handler.create_row(
        user=user,
        table=table_b,
        values={
            f"field_{table_b_primary.id}": "Jeff",
        },
    )

    table_a_link = field_handler.update_field(
        user,
        table_a_link,
        link_row_table=table_b,
        name="A->B",
        has_related_field=True,
    )

    # both grid views must be accessible
    url = reverse("api:database:views:grid:list", kwargs={"view_id": grid_a.id})
    response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
    response_json = response.json()
    assert response.status_code == HTTP_200_OK

    url = reverse("api:database:views:grid:list", kwargs={"view_id": grid_b.id})
    response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
    response_json = response.json()
    assert response.status_code == HTTP_200_OK

    names = list(Field.objects.filter(table=table_b).values_list("name", flat=True))
    assert len(names) == 2
    names = list(Field.objects.filter(table=table_a).values_list("name", flat=True))
    assert names == ["table a pk", "A->B"]

    # back to the original

    table_a_link = field_handler.update_field(
        user, table_a_link, link_row_table=table_a, name="A->A again"
    )

    # both grid views must be accessible
    url = reverse("api:database:views:grid:list", kwargs={"view_id": grid_a.id})
    response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
    assert response.status_code == HTTP_200_OK

    url = reverse("api:database:views:grid:list", kwargs={"view_id": grid_b.id})
    response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
    assert response.status_code == HTTP_200_OK

    names = list(Field.objects.filter(table=table_b).values_list("name", flat=True))
    assert names == ["table b pk"]
    names = list(Field.objects.filter(table=table_a).values_list("name", flat=True))
    assert names == ["table a pk", "A->A again"]


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_lookup_field_cannot_self_reference_itself_via_same_table_link_row(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user, name="Table")
    field_handler = FieldHandler()
    field = data_fixture.create_text_field(
        table=table, order=1, primary=True, name="Name"
    )
    link_row = field_handler.create_field(
        user, table, "link_row", link_row_table=table, name="Link"
    )
    lookup = field_handler.create_field(
        user,
        table,
        "lookup",
        through_field_id=link_row.id,
        target_field_id=field.id,
        name="Lookup",
    )

    link_row.refresh_from_db()
    assert link_row.link_row_related_field is None
    field_names = Field.objects.filter(table=table).values_list("name", flat=True)
    assert list(field_names) == ["Name", "Link", "Lookup"]

    with pytest.raises(SelfReferenceFieldDependencyError):
        field_handler.update_field(
            user,
            lookup,
            name="Lookup self",
            through_field_id=link_row.id,
            target_field_id=lookup.id,
        )


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_no_pending_operations_after_creating_self_linking_model(data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    field_handler = FieldHandler()
    field_handler.create_field(
        user=user,
        table=table,
        type_name="link_row",
        name="Test",
        link_row_table=table,
    )
    table.get_model()
    # Make sure that there are no pending operations in the app registry. Because a
    # Django ManyToManyField registers pending operations every time a table model is
    # generated, which can causes a memory leak if they are not triggered.
    assert len(apps._pending_operations) == 0


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_self_referencing_link_row_raise_if_link_row_table_has_related_field_is_set(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    table_a = data_fixture.create_database_table(user=user)
    table_b = data_fixture.create_database_table(user=user, database=table_a.database)

    field_handler = FieldHandler()

    # cannot create a self referencing field if link_row_table_has_related_field is True
    with pytest.raises(SelfReferencingLinkRowCannotHaveRelatedField):
        field_handler.create_field(
            user,
            table_a,
            "link_row",
            link_row_table=table_a,
            has_related_field=True,
            name="A->A",
        )

    # cannot update a self referencing field if link_row_table_has_related_field is True
    link_a_to_b = field_handler.create_field(
        user,
        table_a,
        "link_row",
        link_row_table=table_b,
        name="A->B with related",
    )

    with pytest.raises(SelfReferencingLinkRowCannotHaveRelatedField):
        field_handler.update_field(
            user,
            link_a_to_b,
            link_row_table=table_a,
            has_related_field=True,
            name="A->A",
        )

    # same results if the requests are made via the API
    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table_a.id}),
        {
            "name": "Link",
            "type": "link_row",
            "link_row_table": table_a.id,
            "has_related_field": True,
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert (
        response_json["error"]
        == "ERROR_SELF_REFERENCING_LINK_ROW_CANNOT_HAVE_RELATED_FIELD"
    )
    assert (
        response_json["detail"]
        == "A self referencing link row field cannot have a related field."
    )

    response = api_client.patch(
        reverse("api:database:fields:item", kwargs={"field_id": link_a_to_b.id}),
        {"link_row_table": table_a.id, "has_related_field": True},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert (
        response_json["error"]
        == "ERROR_SELF_REFERENCING_LINK_ROW_CANNOT_HAVE_RELATED_FIELD"
    )
    assert (
        response_json["detail"]
        == "A self referencing link row field cannot have a related field."
    )


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_updating_link_rows_always_ends_up_with_the_correct_number_of_related_fields(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    table_a = data_fixture.create_database_table(user=user)
    table_b = data_fixture.create_database_table(user=user, database=table_a.database)
    table_c = data_fixture.create_database_table(user=user, database=table_a.database)
    table_a_primary = data_fixture.create_text_field(
        user, table=table_a, primary=True, name="table a pk"
    )
    table_b_primary = data_fixture.create_text_field(
        user, table=table_b, primary=True, name="table b pk"
    )
    grid_a = data_fixture.create_grid_view(user, table=table_a)
    grid_b = data_fixture.create_grid_view(user, table=table_b)

    options = [
        {
            "name": "text",
            "type": "text",
        },
        {
            "name": "self link_row",
            "type": "link_row",
            "link_row_table": table_a.id,
        },
        {
            "name": "link_row to b with related",
            "type": "link_row",
            "link_row_table": table_b.id,
            "has_related_field": True,
        },
        {
            "name": "link_row to b without related",
            "type": "link_row",
            "link_row_table": table_b.id,
            "has_related_field": False,
        },
    ]

    for from_field in options:
        for to_field in options:
            if from_field is to_field:
                continue

            response = api_client.post(
                reverse("api:database:fields:list", kwargs={"table_id": table_a.id}),
                from_field,
                format="json",
                HTTP_AUTHORIZATION=f"JWT {token}",
            )

            response_json = response.json()
            assert response.status_code == HTTP_200_OK
            assert Field.objects.filter(table=table_a).count() == 2
            linkrow_field_id = response_json["id"]

            response = api_client.patch(
                reverse(
                    "api:database:fields:item", kwargs={"field_id": linkrow_field_id}
                ),
                to_field,
                format="json",
                HTTP_AUTHORIZATION=f"JWT {token}",
            )

            expected_count_in_b = 2 if to_field.get("has_related_field", False) else 1
            response_json = response.json()
            assert response.status_code == HTTP_200_OK
            assert Field.objects.filter(table=table_b).count() == expected_count_in_b
            linkrow_field_id = response_json["id"]

            # both grid views must be accessible
            url = reverse("api:database:views:grid:list", kwargs={"view_id": grid_a.id})
            response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
            assert response.status_code == HTTP_200_OK

            url = reverse("api:database:views:grid:list", kwargs={"view_id": grid_b.id})
            response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
            assert response.status_code == HTTP_200_OK

            response = api_client.delete(
                reverse(
                    "api:database:fields:item", kwargs={"field_id": linkrow_field_id}
                ),
                format="json",
                HTTP_AUTHORIZATION=f"JWT {token}",
            )
            assert response.status_code == HTTP_200_OK
            assert Field.objects.filter(table=table_b).count() == 1


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_deleting_table_delete_fields_referencing_it_even_if_with_there_is_no_related_field(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    table_a = data_fixture.create_database_table(user=user)
    table_b = data_fixture.create_database_table(user=user, database=table_a.database)
    # cannot update a self referencing field if link_row_table_has_related_field is True
    link_a_to_b = FieldHandler().create_field(
        user,
        table_a,
        "link_row",
        name="A->B",
        link_row_table=table_b,
        has_related_field=False,
    )

    assert link_a_to_b.link_row_related_field is None

    # deleting table_b should delete the field
    TableHandler().delete_table(user, table_b)

    link_a_to_b.refresh_from_db()
    assert link_a_to_b.trashed is True

    TrashHandler.restore_item(user, "table", table_b.id, parent_trash_item_id=None)

    link_a_to_b.refresh_from_db()
    assert link_a_to_b.trashed is False


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_deleting_only_one_side_of_a_link_row_field_update_deleted_side_dependencies(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    table_a = data_fixture.create_database_table(user=user)
    table_b = data_fixture.create_database_table(user=user, database=table_a.database)

    field_handler = FieldHandler()

    field = data_fixture.create_text_field(
        table=table_b, order=1, primary=True, name="Name"
    )

    link_a_and_b = field_handler.create_field(
        user,
        table_a,
        "link_row",
        name="A<->B",
        link_row_table=table_b,
        has_related_field=True,
    )

    lookup = field_handler.create_field(
        user,
        table_a,
        "lookup",
        through_field_id=link_a_and_b.id,
        target_field_id=field.id,
        name="Lookup",
    )

    # deletes only one side of the link row field and check
    # that the lookup breaks

    field_handler.update_field(
        user,
        link_a_and_b.link_row_related_field,
        name="B->A",
        has_related_field=False,
    )

    lookup.refresh_from_db()
    assert lookup.formula_type == "invalid"
    # ensure no entry in the trash is created for the update
    assert TrashEntry.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.field_link_row
def test_two_linked_tables_both_publically_shared_can_have_related_linked_field_removed(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    table_a = data_fixture.create_database_table(user=user)
    table_b = data_fixture.create_database_table(user=user, database=table_a.database)
    public_grid_view_a = data_fixture.create_grid_view(
        user,
        table=table_a,
        public=True,
    )
    public_grid_view_b = data_fixture.create_grid_view(
        user,
        table=table_b,
        public=True,
    )

    field_handler = FieldHandler()

    field = data_fixture.create_text_field(
        table=table_b, order=1, primary=True, name="Name"
    )

    link_a_and_b = field_handler.create_field(
        user,
        table_a,
        "link_row",
        name="A<->B",
        link_row_table=table_b,
        has_related_field=True,
    )

    field_handler.update_field(
        user,
        link_a_and_b,
        has_related_field=False,
    )


@pytest.mark.django_db
@pytest.mark.field_link_row
@pytest.mark.row_history
def test_link_row_serialize_metadata_for_row_history(
    data_fixture, django_assert_num_queries
):
    workspace = data_fixture.create_workspace()
    database = data_fixture.create_database_application(workspace=workspace)
    user = data_fixture.create_user(workspace=workspace)
    table = data_fixture.create_database_table(user=user, database=database)
    table2 = data_fixture.create_database_table(user=user, database=table.database)
    field = FieldHandler().create_field(
        user,
        table,
        "link_row",
        name="linkrowfield",
        link_row_table=table2,
    )
    table2_model = table2.get_model()
    table2_row1 = table2_model.objects.create()
    table2_row2 = table2_model.objects.create()
    table2_row3 = table2_model.objects.create()
    model = table.get_model()
    row_handler = RowHandler()
    original_row = row_handler.create_row(
        user=user,
        table=table,
        model=model,
        values={
            f"field_{field.id}": [table2_row1.id, table2_row2.id],
        },
    )
    original_row = model.objects.all().enhance_by_fields().get(id=original_row.id)

    with django_assert_num_queries(0):
        metadata = LinkRowFieldType().serialize_metadata_for_row_history(
            field, original_row, None
        )

    getattr(original_row, f"field_{field.id}").set(
        [table2_row1.id, table2_row2.id, table2_row3.id], clear=True
    )
    updated_row = model.objects.all().enhance_by_fields().get(id=original_row.id)

    with django_assert_num_queries(0):
        metadata = LinkRowFieldType().serialize_metadata_for_row_history(
            field, updated_row, metadata
        )

        assert metadata == {
            "id": AnyInt(),
            "linked_rows": {
                table2_row1.id: {"value": f"unnamed row {table2_row1.id}"},
                table2_row2.id: {"value": f"unnamed row {table2_row2.id}"},
                table2_row3.id: {"value": f"unnamed row {table2_row3.id}"},
            },
            "type": "link_row",
        }

    # empty values
    original_row = row_handler.create_row(
        user=user,
        table=table,
        model=model,
        values={f"field_{field.id}": []},
    )
    original_row = model.objects.all().enhance_by_fields().get(id=original_row.id)

    with django_assert_num_queries(0):
        assert LinkRowFieldType().serialize_metadata_for_row_history(
            field, original_row, None
        ) == {
            "id": AnyInt(),
            "linked_rows": {},
            "type": "link_row",
        }


@pytest.mark.django_db
@pytest.mark.field_link_row
@pytest.mark.row_history
def test_link_row_are_row_values_equal(data_fixture, django_assert_num_queries):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    table2 = data_fixture.create_database_table(user=user, database=table.database)
    field = FieldHandler().create_field(
        user,
        table,
        "link_row",
        name="linkrowfield",
        link_row_table=table2,
    )
    table2_model = table2.get_model()
    table2_row1 = table2_model.objects.create()
    table2_row2 = table2_model.objects.create()

    with django_assert_num_queries(0):
        assert (
            LinkRowFieldType().are_row_values_equal([table2_row1.id], [table2_row1.id])
            is True
        )

        assert (
            LinkRowFieldType().are_row_values_equal(
                [table2_row1.id, table2_row2.id], [table2_row2.id, table2_row1.id]
            )
            is True
        )

        assert LinkRowFieldType().are_row_values_equal([], []) is True

        assert LinkRowFieldType().are_row_values_equal([], [table2_row1.id]) is False

        assert (
            LinkRowFieldType().are_row_values_equal([table2_row1.id], [table2_row2.id])
            is False
        )
