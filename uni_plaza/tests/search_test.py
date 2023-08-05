import json

import pytest
from model_bakery import baker
from shop.models import Product, ProductCategory
from hamcrest import *


@pytest.mark.django_db
class TestSearchProduct:
    """
        Тесты на API по работе с поиском товаров по названию
    """
    endpoint = '/products/search/'

    @pytest.fixture
    def products_list(self):
        baker.make(Product, _quantity=100)

    def test_no_product_for_search(self, client):
        """
            Поиск товаров по названию. В БД нет ни одного товара.
        """
        response = client.get(f"{self.endpoint}?name=test")
        assert_that(response.status_code, equal_to(200), "Incorrect status code")

        product_list = json.loads(response.content).get('results')
        assert_that(len(product_list), equal_to(0), "Incorrect product count")

    def test_empty_search(self, client, products_list):
        """
            Поиск товаров по названию. Задана пустая строка поиска.
        """
        response = client.get(f"{self.endpoint}?name=''")
        assert_that(response.status_code, equal_to(200), "Incorrect status code")

        product_list = json.loads(response.content).get('results')
        assert_that(len(product_list), equal_to(0), "Incorrect product count")

    def test_limit_search(self, client, products_list):
        """
            Поиск товаров по названию. Задан limit на возврат кол-ва товаров.
        """
        response = client.get(f"{self.endpoint}?limit=78")
        assert_that(response.status_code, equal_to(200), "Incorrect status code")

        product_list = json.loads(response.content).get('results')
        assert_that(len(product_list), equal_to(78), "Incorrect product count")

    def test_offset_search(self, client, products_list):
        """
            Поиск товаров по названию. Offset сдвинут на 6ой элемент.
        """
        response = client.get(f"{self.endpoint}?limit=15&offset=5")
        assert_that(response.status_code, equal_to(200), "Incorrect status code")

        product_list = json.loads(response.content).get('results')
        assert_that(len(product_list), equal_to(15), "Incorrect product count")
        assert_that(product_list[0].get("id"), equal_to(6), "Incorrect first offset found")

    @pytest.mark.parametrize("search_string, product_name",
                             [("TestProd", "TestProduct232434"),
                              ("4564745754", "tst4564745754456product"),
                              ("Тестовый продукт", "Тестовый продукт 123"),
                              ("BOSCH", "Тестовый bosch продукт"),
                              ("bosch", "Тестовый BOSCH! продукт"),
                              ("Тестовый продукт", "Тестовый продукт")])
    def test_find_one_product(self, client, products_list, search_string, product_name):
        """
            Поиск товаров по названию. В БД только один товар, подходящий под запрос.
        """
        baker.make(Product, name=product_name)
        response = client.get(f"{self.endpoint}?name={search_string}")
        assert_that(response.status_code, equal_to(200), "Incorrect status code")

        product_list = json.loads(response.content).get('results')
        assert_that(len(product_list), equal_to(1), "Incorrect product count")
        assert_that(product_list[0].get("name"), equal_to(product_name), "Incorrect product found")

    def test_find_product_from_catalog(self, client, products_list):
        """
            Поиск товаров из определенного каталога. Товар с искомым назанием есть в нескольких каталогах
        """
        product_name = "Тестовый продукт"
        catalog_name = "Тестовый каталог"
        catalog = baker.make(ProductCategory, name=catalog_name)
        baker.make(Product, name=product_name, category=catalog)
        baker.make(Product, name=product_name)
        response = client.get(f"{self.endpoint}?name={product_name}&category={catalog_name}")
        assert_that(response.status_code, equal_to(200), "Incorrect status code")

        product_list = json.loads(response.content).get('results')
        assert_that(len(product_list), equal_to(1), "Incorrect product count")
        assert_that(product_list[0].get("name"), equal_to(product_name), "Incorrect product found")
        assert_that(product_list[0].get("category"), equal_to(catalog_name), "Incorrect product catalog found")

    def test_find_more_product(self, client, products_list):
        """
            Поиск товаров по названию. В БД несколько товаров, подходящий под запрос.
        """
        product_name = "test product"
        baker.make(Product, name=f"{product_name}123")   # <-- found
        baker.make(Product, name=f"123{product_name}")   # <-- found
        baker.make(Product, name=product_name)           # <-- found
        baker.make(Product, name="test' prod ")          # <-- NOT found
        baker.make(Product, name="testprod ")            # <-- NOT found

        response = client.get(f"{self.endpoint}?limit=10&name=test p")
        assert_that(response.status_code, equal_to(200), "Incorrect status code")

        product_list = json.loads(response.content).get('results')
        assert_that(len(product_list), equal_to(3), "Incorrect product count")
