from string import ascii_lowercase

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from clients.models import User


class UserFactory(DjangoModelFactory):
    """
    Фабрика Пользователя
    """
    class Meta:
        model = User

    username = FuzzyText(length=12, chars=ascii_lowercase)
    first_name = FuzzyText(length=12, chars=ascii_lowercase)
    last_name = FuzzyText(length=12, chars=ascii_lowercase)
    email = FuzzyText(length=12, suffix='_a@yandex.ru')
    gender = FuzzyText(length=12)
