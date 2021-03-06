"""
Django settings for lyte_test_task project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import datetime
import environ


# https://github.com/joke2k/django-environ
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, '+2ynzhx=#eq1cc0qx+jmv-2pv&q=09+uonlxq+p6ar_^d%c7(j'),
    JWT_SECRET_KEY=(str, '0wf98h5y46tnw34rtnac,b4'),
    APP_WSGI_APPLICATION=(str, 'app.wsgi:application'),
    ALLOWED_HOSTS=(list, ['*']),
    TIME_ZONE=(str, 'UTC'),
    CELERY_TASK_ALWAYS_EAGER=(bool, False),
    # https://github.com/joke2k/django-environ/issues/160
    EVENTBRITE_SEARCH_LATITUDE=(str, '53.9'),   # Minsk
    EVENTBRITE_SEARCH_LONGITUDE=(str, '27.56667'),
    EVENTBRITE_SEARCH_WITHIN=(str, '10km'),
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
JWT_SECRET_KEY = env('JWT_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',

    'events.apps.EventsConfig',
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

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = env('APP_WSGI_APPLICATION')


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': env.db()
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'events.permissions.IsAdminUserOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'events.renderers.PrettyJsonRenderer' if DEBUG else 'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_ALLOW_REFRESH': True,
    'JWT_SECRET_KEY': JWT_SECRET_KEY,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

SESSION_COOKIE_SECURE = False if DEBUG else True
CSRF_COOKIE_SECURE = True

CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_TASK_ALWAYS_EAGER = env('CELERY_TASK_ALWAYS_EAGER')
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = env('TIME_ZONE')

EVENBRITE_KEY = env('EVENBRITE_KEY')
EVENTBRITE_SECRET = env('EVENTBRITE_SECRET')
EVENTBRITE_OAUTH_TOKEN = env('EVENTBRITE_OAUTH_TOKEN')
EVENTBRITE_SEARCH_LATITUDE = float(env('EVENTBRITE_SEARCH_LATITUDE'))
EVENTBRITE_SEARCH_LONGITUDE = float(env('EVENTBRITE_SEARCH_LONGITUDE'))
EVENTBRITE_SEARCH_WITHIN = env('EVENTBRITE_SEARCH_WITHIN')


ELASTICSEARCH_URL = env('ELASTICSEARCH_URL')
