"""
Django settings for shop project.
"""

from os import getenv
from pathlib import Path
import logging.config

from dotenv import load_dotenv


env_file = Path(__file__).parent.parent.parent.parent / ".env"
load_dotenv(env_file)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('DJANGO_SECRET_KEY', 'django-insecure-%vcbd1!81dbl&*16lv-#!0ot_pzpv3%zwzu#n!$z)shbgq-)bk')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "0.0.0.0",
    "localhost",
] + getenv("DJANGO_ALLOWED_HOSTS", "").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'frontend',

    'storages',
    'rest_framework',
    'django_filters',
    'drf_spectacular',

    'order.apps.OrderConfig',
    'user_profile.apps.UserProfileConfig',
    'authentication.apps.AuthenticationConfig',
    'catalog.apps.CatalogConfig',
    'basket.apps.BasketConfig',
    'tags.apps.TagsConfig',
    'product.apps.ProductConfig',
    'payment.apps.PaymentConfig',
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

ROOT_URLCONF = 'shop.urls'

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

WSGI_APPLICATION = 'shop.wsgi.application'


# Database
if DEBUG:
    print('--- Database is SqLite ---')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    print('--- Database is PostgreSQL ---')

    POSTGRES_USER = getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
    POSTGRES_NAME = getenv("POSTGRES_NAME")
    POSTGRES_PORT = getenv("POSTGRES_PORT", "5432")

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': POSTGRES_NAME,
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': "postgres",
            'PORT': POSTGRES_PORT,
        }
    }


# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ============== S3 ДЛЯ МЕДИА (картинки) ==============
AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = getenv('AWS_STORAGE_BUCKET_NAME')

AWS_S3_ENDPOINT_URL = 'https://s3.twcstorage.ru'
AWS_S3_REGION_NAME = 'ru-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False

# --- Настройки хранилищ ---
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "endpoint_url": AWS_S3_ENDPOINT_URL,
            "location": "media",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# ============== СТАТИКА (локально) ==============
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ============== МЕДИА (S3) ==============
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/media/'

# ============== REDIS ==============
if not DEBUG:
    REDIS_URL = getenv('REDIS_URL')
    REDIS_PORT = getenv('REDIS_PORT', 6379)
    REDIS_CACHE_NUMBER_DATABASE = getenv('REDIS_CACHE_NUMBER_DATABASE', 1)
    REDIS_HOST = getenv("REDIS_HOST")

    REDIS_CACHE_URL = f'{REDIS_URL}{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_NUMBER_DATABASE}'

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_CACHE_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'SOCKET_CONNECT_TIMEOUT': 5,
                'SOCKET_TIMEOUT': 5,
                'RETRY_ON_TIMEOUT': True,
                'MAX_CONNECTIONS': 100,
                'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
                'CONNECTION_POOL_CLASS_KWARGS': {
                    'max_connections': 50,
                    'timeout': 20,
                },
            },
            'KEY_PREFIX': 'django_cache',
            'TIMEOUT': 120,
        }
    }

    REST_FRAMEWORK_CACHE = {
        'DEFAULT_CACHE_RESPONSE_TIMEOUT': 120,
    }


# ============== DRF ==============
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Mysite",
    "DESCRIPTION": "Mysite shop",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# ============== LOGGING ==============
LOGLEVEL = getenv("DJANGO_LOGLEVEL", "INFO")

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": LOGLEVEL,
        },
    },
})
