import json
from config.settings.base import *
# READ Secured environments
LOCAL_ENV_LOCATION = dirname(BASE_DIR)
ENV_FILE = join(LOCAL_ENV_LOCATION, 'django_email_hunter_local.env.json')
if not exists(ENV_FILE):
    raise ImproperlyConfigured("No local environment file was found in directory: {0}".format(LOCAL_ENV_LOCATION))
with open(ENV_FILE) as data_file:
    ENV_JSON = json.load(data_file)


if not ENV_JSON:
    raise ImproperlyConfigured("No environment variables were found")

SECRET_KEY = ENV_JSON.get('DJANGO_SECRET_KEY')


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


DEBUG = True
THUMBNAIL_DEBUG = DEBUG
TEMPLATES[0]['OPTIONS'].update({'debug': DEBUG})



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