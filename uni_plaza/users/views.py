from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from shop.models import Basket
from common.views import TitleMixin

# """ Вход пользователя """
#
#
# class UserLoginView(TitleMixin, LoginView):
#     template_name = 'users/login.html'
#     form_class = UserLoginForm
#     title = 'Авторизация'
#
#
# """Регистрация пользователя"""
#
#
# class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
#     model = User
#     form_class = UserRegistrationForm
#     template_name = 'users/registration.html'
#     title = 'Регистрация'
#     success_url = reverse_lazy('users:login')
#     success_message = 'Вы успешно зарегистрированы!'
#
#
# """Личный кабинет пользователя"""
#
#
# class UserProfileView(TitleMixin, UpdateView):
#     model = User
#     form_class = UserProfileForm
#     template_name = 'users/profile.html'
#     title = 'Личный кабинет'
#
#     def get_success_url(self):
#         return reverse_lazy('users:profile', args=(self.object.id,))

    # def get_context_data(self, **kwargs):
    #     context = super(UserProfileView, self).get_context_data()
    #     context['baskets'] = Basket.objects.filter(user=self.object)
    #     return context
