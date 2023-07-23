import pytest


@pytest.fixture
def user(django_user_model):
    django_user_model.objects.create(email="someone", password="something")
