import json

import pytest
from model_bakery import baker
from shop.models import Product
from hamcrest import *


@pytest.mark.django_db
class TestProduct:
    """
        Тесты на API по работе с товарами
    """
    endpoint = '/products/products/'

    def test_no_product(self, client):
        """
            Получение списка товаров. В БД нет ни одного товара.
        """
        response = client.get(self.endpoint)
        assert_that(response.status_code, equal_to(200), "Incorrect status code")

        product_list = json.loads(response.content).get('results')
        assert_that(len(product_list), equal_to(0), "Incorrect product count")

    @pytest.mark.parametrize("limit, created_products_count, visible_products_count",
                             [(10, 10, 10),
                              (5, 10, 5),
                              (10, 5, 5)])
    def test_more_products(self, client, limit, created_products_count, visible_products_count):
        """
            Получение списка товаров по лимиту. В БД больше/меньше товаров, чем указанный лимит.
        """
        baker.make(Product, _quantity=created_products_count)
        response = client.get(f"{self.endpoint}?limit={limit}")
        assert_that(response.status_code, equal_to(200), "Incorrect status code")

        product_list = json.loads(response.content).get('results')
        assert_that(len(product_list), equal_to(visible_products_count), "Incorrect product count")

    def test_one_product(self, client):
        """
            Получение списка товаров. В БД только один товар.
        """
        product = baker.make(Product)
        response = client.get(self.endpoint)

        expected_fields = {
            'name': product.name,
            'description': product.description,
            'category': str(product.category),
            'image': product.image,
            'price': str(product.price)
        }

        assert_that(response.status_code, equal_to(200), "Incorrect status code")
        product_list = json.loads(response.content).get('results')
        assert_that(len(product_list), equal_to(1), "Incorrect product count")

        result_product = product_list[0]
        assert_that(result_product, has_entries(expected_fields))

    def test_get_product(self, client):
        """
            Получение товара по id.
        """
        product = baker.make(Product)
        response = client.get(f"{self.endpoint}{product.id}/")

        expected_fields = {
            'name': product.name,
            'description': product.description,
            'category': str(product.category),
            'image': product.image,
            'price': str(product.price)
        }

        assert_that(response.status_code, equal_to(200), "Incorrect status code")
        result_product = json.loads(response.content)
        assert_that(result_product, has_entries(expected_fields))

    def test_get_product_incorrect_id(self, client):
        """
            Получение товара по id. Товар с таким id отсутствует в БД
        """
        baker.make(Product)
        response = client.get(f"{self.endpoint}999/")
        assert_that(response.status_code, equal_to(404), "Incorrect status code")

        result_product = json.loads(response.content)
        assert_that(result_product, has_entry("detail", "Страница не найдена."))

