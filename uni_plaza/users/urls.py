from django.urls import path
from users.views import ActivateUser
from rest_framework import routers


app_name = 'users'

# router = routers.DefaultRouter()
# router.register(r'activate/<uid>/<token>', ActivateUser)

urlpatterns = [
    path('activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),
]