"""
Django settings for meeting_website project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = environ.Path(__file__) - 2

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',

    'drf_yasg',

    'clients',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meeting_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meeting_website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.str('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': env.str('SQL_DATABASE', os.path.join(BASE_DIR, "db.sqlite3")),
        'USER': env.str('SQL_USER', 'user'),
        'PASSWORD': env.str('SQL_PASSWORD', 'password'),
        'HOST': env.str('SQL_HOST', 'localhost'),
        'PORT': env.str('SQL_PORT', '5432'),
    }
}

# region REST
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.permissions.IsAdminUser',
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
}
# endregion

AUTH_USER_MODEL = 'clients.User'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# region tz

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# endregion

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'

MEDIA_ROOT = env.str('MEDIA_ROOT', default=str(ROOT_DIR('media')))
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# region SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = env.str('EMAIL_USE_TLS', False)
EMAIL_HOST = env.str('EMAIL_HOST', '')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = env.str('EMAIL_PORT', 0)
# endregion

# region Redis
REDIS_HOST = env.str('REDIS_HOST', 'redis')
REDIS_PORT = env.str('REDIS_PORT', '6379')
# endregion

# region Celery
CELERY_BROKER_URL = 'redis://redis:6381/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://redis:6381/0'
CELERY_ACCEPT_CONTENT = env.list('CELERY_ACCEPT_CONTENT')
CELERY_TASK_SERIALIZER = env.str('CELERY_TASK_SERIALIZER', '')
CELERY_RESULT_SERIALIZER = env.str('CELERY_RESULT_SERIALIZER', '')
CELERY_TIMEZONE = env.str('CELERY_TIMEZONE', '')
# endregion

GEOS_LIBRARY_PATH = env.bool('GEOS_LIBRARY_PATH', '')

if DEBUG:
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]