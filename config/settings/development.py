# Development settings file
import json
import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from os.path import exists
from .base import *


"""
Configure environment and environment file location.
Note: The environment file (which contains secrets) should be stored outside of VCS.
"""

ON_HEROKU_SERVER = 'ON_HEROKU_SERVER'
ON_PRODUCTION = 'ON_PRODUCTION'
HEROKU_ENV_KEY = 'DEVELOPMENT_ENV'
LOCAL_ENV_LOCATION = ''

ON_HEROKU = False
if ON_HEROKU_SERVER in os.environ:
  ON_HEROKU = True

if ON_PRODUCTION in os.environ:
  raise ImproperlyConfigured("The development settings are trying to run on the production environment!")

if ON_HEROKU:
    ENV_JSON = json.loads(os.environ.get(HEROKU_ENV_KEY, None))
else:
    LOCAL_ENV_LOCATION = os.environ.get(LOCAL_ENV_LOCATION, dirname(dirname(dirname(dirname(__file__)))))
    ENV_FILE = join(LOCAL_ENV_LOCATION, 'django_email_hunter_local.env.json')
    if not exists(ENV_FILE):
        raise ImproperlyConfigured("No local environment file was found in directory: {0}".format(LOCAL_ENV_LOCATION))
    with open(ENV_FILE) as data_file:
        ENV_JSON = json.load(data_file)
if not ENV_JSON:
    raise ImproperlyConfigured("No environment variables were found")


"""
Django debug toolbar settings
"""

ENABLE_DEBUG_TOOLBAR = False
if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]


"""
Django SSL Development Server Configuration
Instead of using ngrok (which has request limits) we may use the SSLServer development server for https.
"""

if not ON_HEROKU:
    INSTALLED_APPS = ['sslserver'] + INSTALLED_APPS


"""
General Django Debug settings.
"""

DEBUG = True
TEMPLATES[0]['OPTIONS'].update({'debug': DEBUG})

if not ON_HEROKU:
    INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

SECRET_KEY = ENV_JSON.get('DJANGO_SECRET_KEY', None)


"""
Database configuration.
We need the multi-tenant backend for schema routing.
TODO: Resolve this issue: https://github.com/tomturner/django-tenants/issues/149
"""

if ON_HEROKU:
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config(conn_max_age=500, engine='django_tenants.postgresql_backend')
else:
     DATABASES = {
         'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': ENV_JSON.get('DATABASE_NAME'),
            'USER': ENV_JSON.get('DATABASE_USER'),
            'PASSWORD': ENV_JSON.get('DATABASE_PW'),
            'HOST': ENV_JSON.get('DATABASE_HOST'),
            'PORT': '5432',
         }
     }


"""
Django Storage AWS Configuration settings
"""

# AWS_ACCESS_KEY_ID = ENV_JSON.get('AWS_ACCESS_KEY_ID', None)
# AWS_SECRET_ACCESS_KEY = ENV_JSON.get('AWS_SECRET_ACCESS_KEY', None)
# AWS_STORAGE_BUCKET_NAME = "charity-returns-storage"
# AWS_DEFAULT_ACL = "private"
# AWS_S3_ENCRYPTION = True
# AWS_S3_FILE_OVERWRITE = True
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_LOCATION = ''
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


"""
Django Task Queue settings.
"""

if ON_HEROKU:
    CELERY_BROKER_URL = os.environ.get('REDIS_URL', None)
else:
    CELERY_BROKER_URL = ENV_JSON.get('REDIS_URL', None)



"""
Logging Configuration
"""

import logging.config
from django.utils.log import DEFAULT_LOGGING
LOGLEVEL = os.environ.get('LOGLEVEL', 'debug').upper()
LOGGING_CONFIG = None