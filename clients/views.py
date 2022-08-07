from rest_framework import status
from rest_framework.response import Response

from clients.filters import UserFilter
from clients.models import User
from clients.serializers import UserDetailSerializer, UserListSerializer
from clients.utils import MultiSerializerViewSet, set_like


class UserViewSet(MultiSerializerViewSet):
    queryset = User.objects.all()
    filtersets = {
        'list': UserFilter,
    }
    serializers = {
        'list': UserListSerializer,
        'create': UserDetailSerializer,
    }

    def create(self, request, *args, **kwargs):
        """
        Создание клиента
        """
        return super().create(request, *args, **kwargs)


class UserMatchViewSet(MultiSerializerViewSet):
    queryset = User.objects.all()
    serializers = {
        'like': UserDetailSerializer,
    }

    def like(self, request, *args, **kwargs):
        """
        Поставить лайк
        """
        email = set_like(liked_user_id=kwargs['pk'], current_user=request.user)
        return Response(dict(email=email), status=status.HTTP_201_CREATED)