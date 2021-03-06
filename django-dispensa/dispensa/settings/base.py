import os
import dj_database_url

from getenv import env


# django-dispensa is the root folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(BASE_DIR, '..')

# security
SECRET_KEY = env('DJANGO_SECRET_KEY')

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

ALLOWED_HOSTS = [
    env('DJANGO_ALLOWED_HOSTS'),
]

DEBUG = env('DJANGO_DEBUG', False)

# apps and middleware
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_s3_storage',

    'wagtail.wagtailforms',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'wagtail.contrib.settings',
    'wagtail.contrib.wagtailsitemaps',

    'modelcluster',
    'taggit',

    'wheelie',
    'options',
    'home',
    'blog',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
]

ROOT_URLCONF = 'dispensa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'dispensa.wsgi.application'

# database configuration
DATABASES_DEFAULT = 'postgres://devel:123456@127.0.0.1:5432/dispensa'
DATABASES = {
    'default': dj_database_url.config(default=DATABASES_DEFAULT),
}

# Cache
CACHES_DEFAULT = 'redis://127.0.0.1:6379/1'
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('CACHE_URL', CACHES_DEFAULT),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 3600
    }
}

# internationalization
LANGUAGE_CODE = 'it'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# static files and media
ASSETS_ROOT = env('DJANGO_ASSETS_ROOT', BASE_DIR)
STATIC_ROOT = os.path.join(ASSETS_ROOT, 'static')
MEDIA_ROOT = os.path.join(ASSETS_ROOT, 'media')

# using a CDN if available
STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST', '')
MEDIA_HOST = os.environ.get('DJANGO_MEDIA_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'
MEDIA_URL = MEDIA_HOST + '/media/'

# emails
DEFAULT_FROM_EMAIL = env('DJANGO_FROM_EMAIL')

DEFAULT_EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', DEFAULT_EMAIL_BACKEND)

# logging
LOGSTASH_HOST = env('LOGSTASH_HOST', '127.0.0.1')
LOGSTASH_PORT = env('LOGSTASH_PORT', 5000)

# WagTail
WAGTAIL_SITE_NAME = 'Dispensa 63'
TAGGIT_CASE_INSENSITIVE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s [%(process)d] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
        'syslog': {
            'format': '%(levelname)s %(name)s [%(process)d] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'syslog': {
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'syslog',
        },
        'logstash': {
            'class': 'logstash.LogstashHandler',
            'host': LOGSTASH_HOST,
            'port': LOGSTASH_PORT,
            'version': 1,
            'message_type': 'dispensa',
        },
    },
}
