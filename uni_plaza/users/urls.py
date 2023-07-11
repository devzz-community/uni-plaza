from django.urls import path, include
from users.views import ActivateUser

app_name = 'users'

urlpatterns = [
    path('activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),
]