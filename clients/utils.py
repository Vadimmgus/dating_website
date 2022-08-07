from django.conf import settings
from django.db.models import Q
from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from django.test import override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from clients.models import User, UserLike

from django.utils.timezone import now as tz_now

from .tasks import send_new_email


def generate_uniq_code():
    return str(tz_now().timestamp()).replace('.', '')


class MultiSerializerViewSet(ModelViewSet):
    filtersets = {
        'default': None,
    }
    serializers = {
        'default': Serializer,
    }

    @property
    def filterset_class(self):
        return self.filtersets.get(self.action) or self.filtersets.get('default')

    @property
    def serializer_class(self):
        return self.serializers.get(self.action) or self.serializers.get('default', Serializer)

    def get_response(self, data=None):
        return Response(data)

    def get_valid_data(self, many=False):
        serializer = self.get_serializer(data=self.request.data, many=many)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


@override_settings(SQL_DEBUG=False)
class TestCaseBase(APITestCase):
    """
    Базовый (без авторизации)
    """
    CONTENT_TYPE_JSON = 'application/json'

    def check_status(self, response, status):
        self.assertEqual(response.status_code, status, response.data)

    def generate_uniq_code(self):
        return generate_uniq_code()


class WithLoginTestCase(TestCaseBase):
    """
    С авторизацией
    """
    @classmethod
    def setUpClass(cls):
        user, is_create = User.objects.get_or_create(username='admin')
        if is_create:
            user.set_password('admin')
            user.save()
        cls.user = user
        cls.token, _ = Token.objects.get_or_create(user=user)
        super().setUpClass()

    def setUp(self) -> None:
        self.auth_user(self.user)
        super().setUp()

    def auth_user(self, user):
        """
        Авторизация
        """
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')


class SearchFilterSet(FilterSet):
    search_fields = ()
    search_method = 'icontains'
    q = CharFilter(method='filter_search', help_text='Поиск')

    def filter_search(self, queryset, name, value):
        if value:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__{self.search_method}': value})
            queryset = queryset.filter(q_objects)
        return queryset.distinct()


def set_like(liked_user_id, current_user):
    # найдем/установим лайк
    users_like = UserLike.objects.filter(user_id=liked_user_id, users_likes_id=current_user.id).first()
    if not users_like:
        UserLike.objects.create(user_id=liked_user_id, users_likes_id=current_user.id)

    # найдем ответный лайк
    reciprocal_like = UserLike.objects.filter(user_id=current_user.id, users_likes_id=liked_user_id).first()
    if reciprocal_like:
        user = User.objects.filter(pk=liked_user_id).values('email', 'first_name', 'last_name')[:1][0]
        if settings.EMAIL_HOST:
            send_new_email.delay(user['email'], 'Сайт знакомств',
                            f'Вы понравились {current_user.first_name}! Почта участника: {current_user.email}')
            send_new_email.delay(current_user.email, 'Сайт знакомств',
                            f'Вы понравились {user["first_name"]}! Почта участника: {user["email"]}')
        return user["email"]
    return True


class SearchFilterSet(FilterSet):
    search_fields = ()
    search_method = 'icontains'
    q = CharFilter(method='filter_search', help_text='Поиск')

    def filter_search(self, queryset, name, value):
        if value:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__{self.search_method}': value})
            queryset = queryset.filter(q_objects)
        return queryset.distinct()
