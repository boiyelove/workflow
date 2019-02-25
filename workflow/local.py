import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = []

DEFAULT_FROM_EMAIL = 'example@we.com'
SERVER_EMAIL = 'we@them.com'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


redis_host = os.environ.get('REDIS_HOST', 'localhost')

# Channel layer definitions
# http://channels.readthedocs.org/en/latest/deploying.html#setting-up-a-channel-backend

CHANNEL_LAYERS = {
    'default': {
    'BACKEND': 'asgi_redis.RedisChannelLayer',
    'CONFIG': {
    'hosts': [("localhost", 6379)],
    },
    'ROUTING': 'workflow.routing.channel_routing',
    },
} 


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "pstatic"),
]

SITE_URL = 'http://localhost:8000'
SITE_NAME = 'Testie Site'