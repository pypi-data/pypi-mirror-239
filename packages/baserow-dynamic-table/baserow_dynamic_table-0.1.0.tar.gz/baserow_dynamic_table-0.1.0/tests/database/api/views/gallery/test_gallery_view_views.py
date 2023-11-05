import json

from django.shortcuts import reverse

import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from baserow_dynamic_table.api.constants import PUBLIC_PLACEHOLDER_ENTITY_ID
from baserow_dynamic_table.fields.handler import FieldHandler
from baserow_dynamic_table.rows.handler import RowHandler
from baserow_dynamic_table.search.handler import ALL_SEARCH_MODES, SearchHandler


@pytest.mark.django_db
def test_list_rows(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1"
    )
    table = data_fixture.create_database_table(user=user)
    text_field = data_fixture.create_text_field(
        table=table, order=0, name="Color", text_default="white"
    )
    gallery = data_fixture.create_gallery_view(table=table)
    gallery_2 = data_fixture.create_gallery_view()

    model = gallery.table.get_model()
    row_1 = model.objects.create(**{f"field_{text_field.id}": "Green"})
    row_2 = model.objects.create()
    row_3 = model.objects.create(**{f"field_{text_field.id}": "Orange"})
    row_4 = model.objects.create(**{f"field_{text_field.id}": "Purple"})

    url = reverse("api:database:views:gallery:list", kwargs={"view_id": 999})
    response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_GALLERY_DOES_NOT_EXIST"

    url = reverse("api:database:views:gallery:list", kwargs={"view_id": gallery_2.id})
    response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_USER_NOT_IN_GROUP"

    url = reverse("api:database:views:gallery:list", kwargs={"view_id": gallery.id})
    response = api_client.get(
        url, {"limit": 2}, **{"HTTP_AUTHORIZATION": f"JWT {token}"}
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["count"] == 4
    assert response_json["results"][0]["id"] == row_1.id
    assert response_json["results"][1]["id"] == row_2.id
    assert "field_options" not in response_json

    url = reverse("api:database:views:gallery:list", kwargs={"view_id": gallery.id})
    response = api_client.get(
        url, {"limit": 1, "offset": 2}, **{"HTTP_AUTHORIZATION": f"JWT {token}"}
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["count"] == 4
    assert response_json["results"][0]["id"] == row_3.id

    sort = data_fixture.create_view_sort(view=gallery, field=text_field, order="ASC")
    url = reverse("api:database:views:gallery:list", kwargs={"view_id": gallery.id})
    response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["count"] == 4
    assert response_json["results"][0]["id"] == row_1.id
    assert response_json["results"][1]["id"] == row_3.id
    assert response_json["results"][2]["id"] == row_4.id
    assert response_json["results"][3]["id"] == row_2.id
    sort.delete()

    view_filter = data_fixture.create_view_filter(
        view=gallery, field=text_field, value="Green"
    )
    url = reverse("api:database:views:gallery:list", kwargs={"view_id": gallery.id})
    response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["count"] == 1
    assert len(response_json["results"]) == 1
    assert response_json["results"][0]["id"] == row_1.id
    view_filter.delete()

    url = reverse("api:database:views:gallery:list", kwargs={"view_id": gallery.id})
    response = api_client.get(
        url, data={"count": ""}, **{"HTTP_AUTHORIZATION": f"JWT {token}"}
    )
    response_json = response.json()
    assert response_json["count"] == 4
    assert len(response_json.keys()) == 1

    row_1.delete()
    row_2.delete()
    row_3.delete()
    row_4.delete()

    url = reverse("api:database:views:gallery:list", kwargs={"view_id": gallery.id})
    response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["count"] == 0
    assert not response_json["previous"]
    assert not response_json["next"]
    assert len(response_json["results"]) == 0

    url = reverse("api:database:views:gallery:list", kwargs={"view_id": gallery.id})
    response = api_client.get(url)
    assert response.status_code == HTTP_401_UNAUTHORIZED

    data_fixture.create_template(workspace=gallery.table.database.workspace)
    url = reverse("api:database:views:gallery:list", kwargs={"view_id": gallery.id})
    response = api_client.get(url)
    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_list_rows_include_field_options(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1"
    )
    table = data_fixture.create_database_table(user=user)
    text_field = data_fixture.create_text_field(
        table=table, order=0, name="Color", text_default="white"
    )
    gallery = data_fixture.create_gallery_view(table=table)

    # The second field is deliberately created after the creation of the gallery field
    # so that the GalleryViewFieldOptions entry is not created. This should
    # automatically be created when the page is fetched.
    number_field = data_fixture.create_number_field(
        table=table, order=1, name="Horsepower"
    )

    url = reverse("api:database:views:gallery:list", kwargs={"view_id": gallery.id})
    response = api_client.get(url, **{"HTTP_AUTHORIZATION": f"JWT {token}"})
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert "field_options" not in response_json

    url = reverse("api:database:views:gallery:list", kwargs={"view_id": gallery.id})
    response = api_client.get(
        url, {"include": "field_options"}, **{"HTTP_AUTHORIZATION": f"JWT {token}"}
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json["field_options"]) == 2
    assert response_json["field_options"][str(text_field.id)]["hidden"] is True
    assert response_json["field_options"][str(text_field.id)]["order"] == 32767
    assert response_json["field_options"][str(number_field.id)]["hidden"] is True
    assert response_json["field_options"][str(number_field.id)]["order"] == 32767
    assert "filters_disabled" not in response_json


@pytest.mark.django_db
@pytest.mark.parametrize("search_mode", ALL_SEARCH_MODES)
def test_list_rows_search(api_client, data_fixture, search_mode):
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1"
    )
    table = data_fixture.create_database_table(user=user)
    text_field = data_fixture.create_text_field(
        table=table, order=0, name="Name", text_default=""
    )
    gallery = data_fixture.create_gallery_view(table=table)
    search_term = "Smith"
    model = gallery.table.get_model()
    not_matching_row1 = model.objects.create(
        **{f"field_{text_field.id}": "Mark Spencer"}
    )
    matching_row1 = model.objects.create(
        **{f"field_{text_field.id}": f"Elon {search_term}"}
    )
    matching_row2 = model.objects.create(
        **{f"field_{text_field.id}": f"James {search_term}"}
    )
    not_matching_row2 = model.objects.create(
        **{f"field_{text_field.id}": "Robin Backham"}
    )

    SearchHandler.update_tsvector_columns(
        table, update_tsvectors_for_changed_rows_only=False
    )

    url = reverse("api:database:views:gallery:list", kwargs={"view_id": gallery.id})
    response = api_client.get(
        url,
        {"search": search_term, "search_mode": search_mode},
        **{"HTTP_AUTHORIZATION": f"JWT {token}"},
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["count"] == 2
    assert response_json["results"][0]["id"] == matching_row1.id
    assert response_json["results"][1]["id"] == matching_row2.id


@pytest.mark.django_db
def test_patch_gallery_view_field_options(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl",
        password="password",
        first_name="Test1",
    )
    table = data_fixture.create_database_table(user=user)
    text_field = data_fixture.create_text_field(table=table)
    gallery = data_fixture.create_gallery_view(table=table)

    url = reverse("api:database:views:field_options", kwargs={"view_id": gallery.id})
    response = api_client.patch(
        url,
        {"field_options": {text_field.id: {"width": 300, "hidden": False}}},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json["field_options"]) == 1
    assert response_json["field_options"][str(text_field.id)]["hidden"] is False
    assert response_json["field_options"][str(text_field.id)]["order"] == 32767
    options = gallery.get_field_options()
    assert len(options) == 1
    assert options[0].field_id == text_field.id
    assert options[0].hidden is False
    assert options[0].order == 32767


@pytest.mark.django_db
def test_create_gallery_view(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)
    file_field = data_fixture.create_file_field(table=table)

    response = api_client.post(
        reverse("api:database:views:list", kwargs={"table_id": table.id}),
        {
            "name": "Test 2",
            "type": "gallery",
            "filter_type": "AND",
            "filters_disabled": False,
            "card_cover_image_field": file_field.id,
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == "Test 2"
    assert response_json["type"] == "gallery"
    assert response_json["filter_type"] == "AND"
    assert response_json["filters_disabled"] is False
    assert response_json["card_cover_image_field"] == file_field.id


@pytest.mark.django_db
def test_create_gallery_view_invalid_card_card_cover_image_field(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)
    text = data_fixture.create_text_field(table=table)
    file_field = data_fixture.create_file_field()

    response = api_client.post(
        reverse("api:database:views:list", kwargs={"table_id": table.id}),
        {"name": "Test 2", "type": "gallery", "card_cover_image_field": text.id},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert (
        response_json["detail"]["card_cover_image_field"][0]["code"] == "does_not_exist"
    )

    response = api_client.post(
        reverse("api:database:views:list", kwargs={"table_id": table.id}),
        {"name": "Test 2", "type": "gallery", "card_cover_image_field": file_field.id},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_FIELD_NOT_IN_TABLE"


@pytest.mark.django_db
def test_update_gallery_view(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)
    gallery_view = data_fixture.create_gallery_view(table=table)

    response = api_client.patch(
        reverse("api:database:views:item", kwargs={"view_id": gallery_view.id}),
        {
            "name": "Test 2",
            "type": "gallery",
            "filter_type": "AND",
            "filters_disabled": False,
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == "Test 2"
    assert response_json["type"] == "gallery"
    assert response_json["filter_type"] == "AND"
    assert response_json["filters_disabled"] is False


@pytest.mark.django_db
def test_get_public_gallery_view(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)

    # Only information related the public field should be returned
    public_field = data_fixture.create_text_field(table=table, name="public")
    hidden_field = data_fixture.create_text_field(table=table, name="hidden")

    gallery_view = data_fixture.create_gallery_view(
        table=table,
        user=user,
        public=True,
    )

    data_fixture.create_gallery_view_field_option(
        gallery_view, public_field, hidden=False
    )
    data_fixture.create_gallery_view_field_option(
        gallery_view, hidden_field, hidden=True
    )

    # This view sort shouldn't be exposed as it is for a hidden field
    data_fixture.create_view_sort(view=gallery_view, field=hidden_field, order="ASC")
    visible_sort = data_fixture.create_view_sort(
        view=gallery_view, field=public_field, order="DESC"
    )

    # View filters should not be returned at all for any and all fields regardless of
    # if they are hidden.
    data_fixture.create_view_filter(
        view=gallery_view, field=hidden_field, type="contains", value="hidden"
    )
    data_fixture.create_view_filter(
        view=gallery_view, field=public_field, type="contains", value="public"
    )

    # Can access as an anonymous user
    response = api_client.get(
        reverse("api:database:views:public_info", kwargs={"slug": gallery_view.slug})
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK, response_json
    assert response_json == {
        "fields": [
            {
                "id": public_field.id,
                "table_id": PUBLIC_PLACEHOLDER_ENTITY_ID,
                "name": "public",
                "order": 0,
                "primary": False,
                "text_default": "",
                "type": "text",
                "read_only": False,
            }
        ],
        "view": {
            "id": gallery_view.slug,
            "name": gallery_view.name,
            "order": 0,
            "public": True,
            "slug": gallery_view.slug,
            "sortings": [
                # Note the sorting for the hidden field is not returned
                {
                    "field": visible_sort.field.id,
                    "id": visible_sort.id,
                    "order": "DESC",
                    "view": gallery_view.slug,
                }
            ],
            "group_bys": [],
            "table": {
                "database_id": PUBLIC_PLACEHOLDER_ENTITY_ID,
                "id": PUBLIC_PLACEHOLDER_ENTITY_ID,
            },
            "type": "gallery",
            "card_cover_image_field": None,
            "show_logo": True,
        },
    }


@pytest.mark.django_db
def test_list_rows_public_doesnt_show_hidden_columns(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)

    # Only information related the public field should be returned
    public_field = data_fixture.create_text_field(table=table, name="public")
    hidden_field = data_fixture.create_text_field(table=table, name="hidden")

    gallery_view = data_fixture.create_gallery_view(table=table, user=user, public=True)

    public_field_option = data_fixture.create_gallery_view_field_option(
        gallery_view, public_field, hidden=False
    )
    data_fixture.create_gallery_view_field_option(
        gallery_view, hidden_field, hidden=True
    )

    RowHandler().create_row(user, table, values={})

    # Get access as an anonymous user
    response = api_client.get(
        reverse(
            "api:database:views:gallery:public_rows", kwargs={"slug": gallery_view.slug}
        )
        + "?include=field_options"
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json == {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                f"field_{public_field.id}": None,
                "id": 1,
                "order": "1.00000000000000000000",
            }
        ],
        "field_options": {
            f"{public_field.id}": {
                "hidden": False,
                "order": public_field_option.order,
            },
        },
    }


@pytest.mark.django_db
def test_list_rows_public_with_query_param_filter(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)
    public_field = data_fixture.create_text_field(table=table, name="public")
    hidden_field = data_fixture.create_text_field(table=table, name="hidden")
    gallery_view = data_fixture.create_gallery_view(table=table, user=user, public=True)
    data_fixture.create_gallery_view_field_option(
        gallery_view, public_field, hidden=False
    )
    data_fixture.create_gallery_view_field_option(
        gallery_view, hidden_field, hidden=True
    )

    first_row = RowHandler().create_row(
        user, table, values={"public": "a", "hidden": "y"}, user_field_names=True
    )
    RowHandler().create_row(
        user, table, values={"public": "b", "hidden": "z"}, user_field_names=True
    )

    url = reverse(
        "api:database:views:gallery:public_rows", kwargs={"slug": gallery_view.slug}
    )
    get_params = [f"filter__field_{public_field.id}__contains=a"]
    response = api_client.get(f'{url}?{"&".join(get_params)}')
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json["results"]) == 1
    assert response_json["results"][0]["id"] == first_row.id

    url = reverse(
        "api:database:views:gallery:public_rows", kwargs={"slug": gallery_view.slug}
    )
    get_params = [
        f"filter__field_{public_field.id}__contains=a",
        f"filter__field_{public_field.id}__contains=b",
        f"filter_type=OR",
    ]
    response = api_client.get(f'{url}?{"&".join(get_params)}')
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json["results"]) == 2

    url = reverse(
        "api:database:views:gallery:public_rows", kwargs={"slug": gallery_view.slug}
    )
    get_params = [f"filter__field_{hidden_field.id}__contains=y"]
    response = api_client.get(f'{url}?{"&".join(get_params)}')
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_FILTER_FIELD_NOT_FOUND"

    url = reverse(
        "api:database:views:gallery:public_rows", kwargs={"slug": gallery_view.slug}
    )
    get_params = [f"filter__field_{public_field.id}__random=y"]
    response = api_client.get(f'{url}?{"&".join(get_params)}')
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_VIEW_FILTER_TYPE_DOES_NOT_EXIST"

    url = reverse(
        "api:database:views:gallery:public_rows", kwargs={"slug": gallery_view.slug}
    )
    get_params = [f"filter__field_{public_field.id}__higher_than=1"]
    response = api_client.get(f'{url}?{"&".join(get_params)}')
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_VIEW_FILTER_TYPE_UNSUPPORTED_FIELD"


@pytest.mark.django_db
def test_list_rows_public_with_query_param_order(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)
    table_2 = data_fixture.create_database_table(database=table.database)
    public_field = data_fixture.create_text_field(table=table, name="public")
    hidden_field = data_fixture.create_text_field(table=table, name="hidden")
    link_row_field = FieldHandler().create_field(
        user=user,
        table=table,
        type_name="link_row",
        name="Link",
        link_row_table=table_2,
    )
    gallery_view = data_fixture.create_gallery_view(table=table, user=user, public=True)
    data_fixture.create_gallery_view_field_option(
        gallery_view, public_field, hidden=False
    )
    data_fixture.create_gallery_view_field_option(
        gallery_view, hidden_field, hidden=True
    )
    data_fixture.create_gallery_view_field_option(
        gallery_view, link_row_field, hidden=False
    )

    first_row = RowHandler().create_row(
        user, table, values={"public": "a", "hidden": "y"}, user_field_names=True
    )
    second_row = RowHandler().create_row(
        user, table, values={"public": "b", "hidden": "z"}, user_field_names=True
    )

    url = reverse(
        "api:database:views:gallery:public_rows", kwargs={"slug": gallery_view.slug}
    )
    response = api_client.get(
        f"{url}?order_by=-field_{public_field.id}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json["results"]) == 2
    assert response_json["results"][0]["id"] == second_row.id
    assert response_json["results"][1]["id"] == first_row.id

    url = reverse(
        "api:database:views:gallery:public_rows", kwargs={"slug": gallery_view.slug}
    )
    response = api_client.get(
        f"{url}?order_by=field_{hidden_field.id}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_ORDER_BY_FIELD_NOT_FOUND"

    url = reverse(
        "api:database:views:gallery:public_rows", kwargs={"slug": gallery_view.slug}
    )
    response = api_client.get(
        f"{url}?order_by=field_{link_row_field.id}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_ORDER_BY_FIELD_NOT_POSSIBLE"


@pytest.mark.django_db
def test_list_rows_public_filters_by_visible_and_hidden_columns(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)

    # Only information related the public field should be returned
    public_field = data_fixture.create_text_field(table=table, name="public")
    hidden_field = data_fixture.create_text_field(table=table, name="hidden")

    gallery_view = data_fixture.create_gallery_view(table=table, user=user, public=True)

    data_fixture.create_gallery_view_field_option(
        gallery_view, public_field, hidden=False
    )
    data_fixture.create_gallery_view_field_option(
        gallery_view, hidden_field, hidden=True
    )

    data_fixture.create_view_filter(
        view=gallery_view, field=hidden_field, type="equal", value="y"
    )
    data_fixture.create_view_filter(
        view=gallery_view, field=public_field, type="equal", value="a"
    )
    # A row whose hidden column doesn't match the first filter
    RowHandler().create_row(
        user, table, values={"public": "a", "hidden": "not y"}, user_field_names=True
    )
    # A row whose public column doesn't match the second filter
    RowHandler().create_row(
        user, table, values={"public": "not a", "hidden": "y"}, user_field_names=True
    )
    # A row which matches all filters
    visible_row = RowHandler().create_row(
        user, table, values={"public": "a", "hidden": "y"}, user_field_names=True
    )

    # Get access as an anonymous user
    response = api_client.get(
        reverse(
            "api:database:views:gallery:public_rows", kwargs={"slug": gallery_view.slug}
        )
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK, response_json
    assert len(response_json["results"]) == 1
    assert response_json["count"] == 1
    assert response_json["results"][0]["id"] == visible_row.id


@pytest.mark.django_db
def test_list_rows_public_with_query_param_advanced_filters(api_client, data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    public_field = data_fixture.create_text_field(table=table, name="public")
    hidden_field = data_fixture.create_text_field(table=table, name="hidden")
    gallery_view = data_fixture.create_gallery_view(
        table=table, user=user, public=True, create_options=False
    )
    data_fixture.create_gallery_view_field_option(
        gallery_view, public_field, hidden=False
    )
    data_fixture.create_gallery_view_field_option(
        gallery_view, hidden_field, hidden=True
    )

    first_row = RowHandler().create_row(
        user, table, values={"public": "a", "hidden": "y"}, user_field_names=True
    )
    RowHandler().create_row(
        user, table, values={"public": "b", "hidden": "z"}, user_field_names=True
    )

    url = reverse(
        "api:database:views:gallery:public_rows", kwargs={"slug": gallery_view.slug}
    )
    advanced_filters = {
        "filter_type": "AND",
        "filters": [
            {
                "field": public_field.id,
                "type": "contains",
                "value": "a",
            }
        ],
    }
    get_params = ["filters=" + json.dumps(advanced_filters)]
    response = api_client.get(f'{url}?{"&".join(get_params)}')
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json["results"]) == 1
    assert response_json["results"][0]["id"] == first_row.id

    advanced_filters = {
        "filter_type": "AND",
        "groups": [
            {
                "filter_type": "OR",
                "filters": [
                    {
                        "field": public_field.id,
                        "type": "contains",
                        "value": "a",
                    },
                    {
                        "field": public_field.id,
                        "type": "contains",
                        "value": "b",
                    },
                ],
            }
        ],
    }
    get_params = ["filters=" + json.dumps(advanced_filters)]
    response = api_client.get(f'{url}?{"&".join(get_params)}')
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json["results"]) == 2

    # groups can be arbitrarily nested
    advanced_filters = {
        "filter_type": "AND",
        "groups": [
            {
                "filter_type": "AND",
                "filters": [
                    {
                        "field": public_field.id,
                        "type": "contains",
                        "value": "",
                    },
                ],
                "groups": [
                    {
                        "filter_type": "OR",
                        "filters": [
                            {
                                "field": public_field.id,
                                "type": "contains",
                                "value": "a",
                            },
                            {
                                "field": public_field.id,
                                "type": "contains",
                                "value": "b",
                            },
                        ],
                    },
                ],
            },
        ],
    }
    get_params = ["filters=" + json.dumps(advanced_filters)]
    response = api_client.get(f'{url}?{"&".join(get_params)}')
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json["results"]) == 2

    advanced_filters = {
        "filter_type": "AND",
        "filters": [
            {
                "field": hidden_field.id,
                "type": "contains",
                "value": "y",
            }
        ],
    }
    get_params = ["filters=" + json.dumps(advanced_filters)]
    response = api_client.get(f'{url}?{"&".join(get_params)}')
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_FILTER_FIELD_NOT_FOUND"

    advanced_filters = {
        "filter_type": "AND",
        "filters": [
            {
                "field": public_field.id,
                "type": "random",
                "value": "y",
            }
        ],
    }
    get_params = ["filters=" + json.dumps(advanced_filters)]
    response = api_client.get(f'{url}?{"&".join(get_params)}')
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_VIEW_FILTER_TYPE_DOES_NOT_EXIST"

    advanced_filters = {
        "filter_type": "AND",
        "filters": [
            {
                "field": public_field.id,
                "type": "higher_than",
                "value": "y",
            }
        ],
    }
    get_params = ["filters=" + json.dumps(advanced_filters)]
    response = api_client.get(f'{url}?{"&".join(get_params)}')
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_VIEW_FILTER_TYPE_UNSUPPORTED_FIELD"

    for filters in [
        "invalid_json",
        json.dumps({"filter_type": "invalid"}),
        json.dumps({"filter_type": "OR", "filters": "invalid"}),
    ]:
        get_params = [f"filters={filters}"]
        response = api_client.get(f'{url}?{"&".join(get_params)}')
        response_json = response.json()
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response_json["error"] == "ERROR_FILTERS_PARAM_VALIDATION_ERROR"


@pytest.mark.django_db
@pytest.mark.parametrize("search_mode", ALL_SEARCH_MODES)
def test_list_rows_public_only_searches_by_visible_columns(
    api_client, data_fixture, search_mode
):
    user, token = data_fixture.create_user_and_token()
    table = data_fixture.create_database_table(user=user)

    # Only information related the public field should be returned
    public_field = data_fixture.create_text_field(table=table, name="public")
    hidden_field = data_fixture.create_text_field(table=table, name="hidden")

    gallery_view = data_fixture.create_gallery_view(table=table, user=user, public=True)

    data_fixture.create_gallery_view_field_option(
        gallery_view, public_field, hidden=False
    )
    data_fixture.create_gallery_view_field_option(
        gallery_view, hidden_field, hidden=True
    )

    search_term = "search_term"
    RowHandler().create_row(
        user,
        table,
        values={"public": "other", "hidden": search_term},
        user_field_names=True,
    )
    RowHandler().create_row(
        user,
        table,
        values={"public": "other", "hidden": "other"},
        user_field_names=True,
    )
    visible_row = RowHandler().create_row(
        user,
        table,
        values={"public": search_term, "hidden": "other"},
        user_field_names=True,
    )
    SearchHandler.update_tsvector_columns(
        table, update_tsvectors_for_changed_rows_only=False
    )

    # Get access as an anonymous user
    response = api_client.get(
        reverse(
            "api:database:views:gallery:public_rows", kwargs={"slug": gallery_view.slug}
        )
        + f"?search={search_term}&search_mode={search_mode}"
    )
    response_json = response.json()
    assert response.status_code == HTTP_200_OK, response_json
    assert len(response_json["results"]) == 1
    assert response_json["count"] == 1
    assert response_json["results"][0]["id"] == visible_row.id
