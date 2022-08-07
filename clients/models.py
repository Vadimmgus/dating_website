from django.contrib.auth.models import AbstractUser
from django.db import models

from clients.choices import Gender


class User(AbstractUser):
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)

    email = models.EmailField('Почта', blank=True, null=True)
    gender = models.CharField('Пол', max_length=20, choices=Gender.CHOICES, default=Gender.MALE)

    avatar = models.ImageField(upload_to='images/users', verbose_name='Изображение', blank=True, null=True)

    latitude = models.FloatField('Широта', blank=True, null=True)
    longitude = models.FloatField('Долгота', blank=True, null=True)

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']


class UserLike(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='likes', on_delete=models.CASCADE)
    users_likes = models.ForeignKey(User, verbose_name='Лайк пользователя', related_name='users_likes', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Лайк пользователя'
        verbose_name_plural = 'Лайки пользователей'
