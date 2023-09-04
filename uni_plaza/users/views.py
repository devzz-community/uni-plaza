from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from users.models import User
from users.serializers import UserSerializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        # Строка отличается от базовой реализации
        kwargs['data'] = {'uid': self.kwargs['uid'], 'token': self.kwargs['token']}

        return serializer_class(*args, **kwargs)

    # def activation(self, request, uid, token, *args, **kwargs):
    #     super().activation(request, *args, **kwargs)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def activation(self, request, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(ModelViewSet):
    """ Работа с пользователем """
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super(UserViewSet, self).get_permissions()


def get_tokens_for_user(user):
    """ Функция получения токена """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    """
    Получение данных пользователя и отправка cookie
    """

    def post(self, request, format=None):
        data = request.data
        response = Response()
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                # data = get_tokens_for_user(user)
                tokens = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    # value=data["access"],
                    value=tokens['refresh'],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = {"Success": "Login successfully", "access": tokens['access']}
                return response
            else:
                # return Response({"No active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
                return Response({"errors": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"errors": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)


# class UserVerify(APIView):
#     """ Проверка пользователя """
#     queryset = User.objects.all()
#
#     def get(self, request):
#         request.user.
#         # if request.user.is_authenticated:
#         #     return Response({'True'}, status=status.HTTP_200_OK)
#         # else:
#         #     return Response({'False'}, status=status.HTTP_204_NO_CONTENT)
#
#         # if user is not None:
#
#         # if self.action in ('create', 'update', 'destroy'):
#         #     self.permission_classes = (IsAdminUser,)
#         # return super(UserViewSet, self).get_permissions()
