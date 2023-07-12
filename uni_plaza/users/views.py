from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework import status


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        # Строка отличается от базовой реализации
        kwargs['data'] = {'uid': self.kwargs['uid'], 'token': self.kwargs['token']}

        return serializer_class(*args, **kwargs)


    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
