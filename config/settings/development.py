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


DEBUG = ENV_JSON.get('DEBUG', True)
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
MYPRIVATEPROXY_ACCESS_KEY = ENV_JSON.get('MYPRIVATEPROXY_ACCESS_KEY', None)

# Email and phone number to be used as recovery email or phone for google accounts
DEFAULT_RECOVERY_EMAIL = ENV_JSON.get('DEFAULT_RECOVERY_EMAIL', None)
DEFAULT_RECOVERY_PHONE = ENV_JSON.get('DEFAULT_RECOVERY_PHONE', None)

if not DEFAULT_RECOVERY_EMAIL or not DEFAULT_RECOVERY_PHONE:
    raise ImportError('You should specify recovery email and phone.')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ALLOWED_HOSTS = ENV_JSON.get('ALLOWED_HOSTS', [])
DEBUG

"""
Django Task Queue settings.
"""

CELERY_BROKER_URL = ENV_JSON.get('REDIS_URL', None)
CELERY_RESULT_BACKEND = ENV_JSON.get('REDIS_URL', None)
# CELERY_TASK_ALWAYS_EAGER = True


# SMTP CONFIGURATION
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ENV_JSON.get('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = ENV_JSON.get('EMAIL_HOST_PASSWORD', None)
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = ENV_JSON.get('DEFAULT_FROM_EMAIL', None)

ADMINS = ENV_JSON.get('ADMINS', [])
EMAIL_SUBJECT_PREFIX = '[HUNTER ADMIN]'