import json

import pytest
from model_bakery import baker
from shop.models import ProductCategory
from hamcrest import *


@pytest.mark.django_db
class TestCatalogs:
    """
        Тесты на API по работе с каталогами товаров
    """
    endpoint = '/products/catalogs/'

    def test_no_catalog(self, client):
        """
            Получение списка каталогов. В БД нет ни одного каталога.
        """
        response = client.get(self.endpoint)
        assert_that(response.status_code, equal_to(200), "Incorrect status code")

        catalog_list = json.loads(response.content).get('results')
        assert_that(len(catalog_list), equal_to(0), "Incorrect catalog count")

    def test_one_catalog(self, client):
        """
            Получение списка каталогов. В БД только один каталог.
        """
        catalog = baker.make(ProductCategory)
        response = client.get(self.endpoint)

        expected_fields = {
            'name': catalog.name,
           # 'description': catalog.description,  ???
            'image': catalog.image
        }

        assert_that(response.status_code, equal_to(200), "Incorrect status code")
        catalog_list = json.loads(response.content).get('results')
        assert_that(len(catalog_list), equal_to(1), "Incorrect catalogs count")

        result_catalog = catalog_list[0]
        assert_that(result_catalog, has_entries(expected_fields))

    @pytest.mark.parametrize("limit, created_catalogs_count, visible_catalogs_count",
                             [(10, 10, 10),
                              (5, 10, 5),
                              (10, 5, 5)])
    def test_more_catalogs(self, client, limit, created_catalogs_count, visible_catalogs_count):
        """
            Получение списка каталогов по лимиту. В БД больше/меньше каталогов, чем указанный лимит.
        """
        baker.make(ProductCategory, _quantity=created_catalogs_count)
        response = client.get(f"{self.endpoint}?limit={limit}")
        assert_that(response.status_code, equal_to(200), "Incorrect status code")

        catalog_list = json.loads(response.content).get('results')
        assert_that(len(catalog_list), equal_to(visible_catalogs_count), "Incorrect catalogs count")

    def test_get_catalog(self, client):
        """
            Получение каталога по id.
        """
        catalog = baker.make(ProductCategory)
        response = client.get(f"{self.endpoint}{catalog.id}/")

        expected_fields = {
            'name': catalog.name,
            'image': catalog.image
        }

        assert_that(response.status_code, equal_to(200), "Incorrect status code")
        result_catalog = json.loads(response.content)
        assert_that(result_catalog, has_entries(expected_fields))

    def test_get_catalog_incorrect_id(self, client):
        """
            Получение каталога по id. Каталог с таким id отсутствует в БД
        """
        baker.make(ProductCategory)
        response = client.get(f"{self.endpoint}999/")
        assert_that(response.status_code, equal_to(404), "Incorrect status code")

        result_catalog = json.loads(response.content)
        assert_that(result_catalog, has_entry("detail", "Страница не найдена."))

