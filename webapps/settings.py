"""
Django settings for webapps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os

import dj_database_url
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

SECRET_KEY = os.getenv("SECRET_KEY")

LOCAL = os.getenv("RUNNING_LOCAL")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'everest'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'webapps.urls'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'

WSGI_APPLICATION = 'webapps.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Parse database configuration from $DATABASE_URL
DATABASES = {'default': dj_database_url.config()}

# Enable Connection Pooling (if desired)
DATABASES['default']['ENGINE'] = 'django_postgrespool'

# if we did not find a database engine, use sqlite
# this allows us to use sqlite locally, but postgres on heroku
if 'NAME' not in DATABASES['default']:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['localhost', 'everest-english.herokuapp.com']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# aws config
AWS_STORAGE_BUCKET_NAME = 'everestesl'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# set up the media url
S3_URL = 'http://s3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = '/media/'
MEDIA_URL = S3_URL + '/'
# settings for ffmpeg
FFMPEG_INSTALL = os.getenv('FFMPEG_INSTALL') or ''
# settings for email
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
# django secret key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
# search engine pls pls pls
from urlparse import urlparse

if LOCAL != 'running_local':
    es = urlparse(os.environ.get('SEARCHBOX_URL') or 'http://127.0.0.1:9200/')

    port = es.port or 80

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': es.scheme + '://' + es.hostname + ':' + str(port),
            'INDEX_NAME': 'documents',
        },
    }

    if es.username:
        HAYSTACK_CONNECTIONS['default']['KWARGS'] = {"http_auth": es.username + ':' + es.password}

    HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
else:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        },
    }

