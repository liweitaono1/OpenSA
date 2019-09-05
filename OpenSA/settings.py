"""
Django settings for OpenSA project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
from django.urls import reverse_lazy
import os
import pymysql
import configparser

pymysql.install_as_MySQLdb()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pcg4e2l#g8g)=0g$3%1co#+8+)va_og&#=ndzv@0o1pp9ma1h5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_celery_results',
    'django_celery_beat',
    'bootstrap3',
    'users',
    'asset',
    'audit',
    'jobs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'opensa.api.RequestMiddleware',
]

ROOT_URLCONF = 'OpenSA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'opensa.api.custom_project',
            ],
        },
    },
]

WSGI_APPLICATION = 'OpenSA.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'config.conf'))
DB_HOST = config.get('db', 'host')
DB_PORT = config.getint('db', 'port')
DB_USER = config.get('db', 'user')
DB_PASSWORD = config.get('db', 'password')
DB_DATABASE = config.get('db', 'database')
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_DATABASE,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'CONN_MAX_AGE': 60,
    }
}
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGIN_URL = reverse_lazy('users:login')
# 用户认证模块
AUTH_USER_MODEL = 'users.UserProfile'
TOKEN_TIMEOUT = 120
ugettext = lambda s: s
LANGUAGE_CODE = 'zh-Hans'
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True
LANGUAGES = (
    ('en', ugettext('Simple Chinese')),
    ('zh-hans', ugettext('English')),

)
TIME_ZONE = 'Asia/Shanghai'
DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    ),
}

SESSION_COOKIE_AGE = 60 * 60
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 3,
    'MARGIN_PAGES_DISPLAYED': 2,
    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

DISPLAY_PER_PAGE = 15

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'config.conf'))
redis_ip = config.get('redis', 'redis_ip')
redis_port = config.getint('redis', 'redis_port')
redis_pwd = config.get('redis', 'redis_pwd')
redis_db = config.get('redis', 'redis_db')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}".format(redis_ip, redis_port),
        "OPTIONS": {
            'DB': '{}'.format(redis_db),
            'PASSWORD': '{}'.format(redis_pwd),
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        }
    }
}

# celery
CELERY_ACCEPT_CONTENT = ['application/json']
# 将返回结果取到数据中
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BROKER_URL = 'redis://:{}@{}:{}/{}'.format(redis_pwd, redis_ip, redis_port, redis_db)
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERYD_CONCURRENCY = 1
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_MAX_TASKS_PER_CHILD = 1
CELERYD_FORCE_EXECV = True
CELERY_IGNORE_RESULT = True
CELERY_CREATE_MISSING_QUEUES = True
CELERY_DISABLE_RATE_LIMITS = True
CELERYD_TASK_SOFT_TIME_LIMIT = 1200
CELERY_TASK_RESULT_EXPIRES = 1200
CELERY_IMPORTS = ('opensa.celery')

# 文件或者配置目录
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'main': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s [%(module)s %(levelname)s] %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'msg': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main'
        },
        'error': {
            'encoding': 'utf8',
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 100,  # 文件大小
            'backupCount': 7,  # 备份份数
            'formatter': 'main',  # 使用哪种formatters日志格式
            'filename': '{}/error.log'.format(LOG_DIR),  # 日志输出文件
        },
        'default': {
            'encoding': 'utf8',
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 100,  # 文件大小
            'backupCount': 7,  # 备份份数
            'formatter': 'main',  # 使用哪种formatters日志格式
            'filename': '{}/all.log'.format(LOG_DIR),  # 日志输出文件
        },
    },
    'loggers': {
        'django':
            {
                'handlers': ['null'],
                'propagate': False,
                'level': 'INFO',
            },
        'django.request': {
            'handlers': ['console', 'default'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'default'],
            'level': 'INFO',
            'propagate': False,
        },
        'Opensa.log': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True
        },
        'celery.core.log': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True
        },

    }
}
