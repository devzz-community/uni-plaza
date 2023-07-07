from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Расширяем модель пользователя"""

    image = models.ImageField(upload_to='users_images', null=True, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']
