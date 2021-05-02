"""
Django settings for todos_app project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path
import requests

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k3!$qbj2*m2j0u*pvzizd(k-qcg#ai*j1f8vnju3fa*#isd6^*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Add EC2 IP to ALLOWED_HOSTS
EC2_PRIVATE_IP = None
try:
    EC2_PRIVATE_IP = requests.get(
        'http://169.254.169.254/latest/meta-data/public-ipv4',
        timeout=0.01).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third-party libraries
    'rest_framework',
    'django_filters',
    # local apps
    'todos.apps.TodosConfig',
    'users.apps.UsersConfig',
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

ROOT_URLCONF = 'todos_app.urls'

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

WSGI_APPLICATION = 'todos_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME', 'todos-db'),
        'USER': os.environ.get('DATABASE_USER', 'root'),
        'PASSWORD': os.environ.get('DATABASE_PASS', 'password'),
        'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DATABASE_PORT', '3308'),
        'TEST': {
            'NAME': os.environ.get('TEST_DATABASE_NAME', 'test_todos'),
            'USER': os.environ.get('TEST_DATABASE_USER', None),
        },
        'OPTIONS': {},
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# users model for app authentication
AUTH_USER_MODEL = 'users.User'

# restframework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}


# djangorestframework-simplejwt
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=int(os.environ.get('ACCESS_TOKEN_LIFETIME','3600'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(seconds=int(os.environ.get('REFRESH_TOKEN_LIFETIME', '86400'))),
    'ROTATE_REFRESH_TOKENS': os.environ.get('ROTATE_REFRESH_TOKENS', True),
    'BLACKLIST_AFTER_ROTATION': os.environ.get('BLACKLIST_AFTER_ROTATION', True),
}

