"""
Django settings for workflow project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'workflowmail'
EMAIL_HOST_PASSWORD = 'Cl@z1k@lCl@z1k@lm3Gr3@tn3ss!@$#@tn3ss!@$#'
DEFAULT_FROM_EMAIL = 'workflow-notifications@iboiye.com'
SERVER_EMAIL = 'workflow-@iboiye.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'workflow',
        'USER':'workkflowwadmin',
        'PASSWORD': 'R3v3nuPp@dm1N@ndw0RFlo!',
        'HOST': '',
        'PORT': '',
    }
}


ADMINS = [('Daahrmmie Boiyelove', 'daahrmmieboiye@gmail.com'), ('Boiyelove TestDev', 'boiyelovetestdevelopment@gmail.com')]

ALLOWED_HOSTS = ['.iboiye.com']



SITE_URL = 'http://workflow.iboiye.com'
SITE_NAME = 'Workflow'
VERIFY_EMAILS = False
USERNAMESNOTALLOWED = ['boiyelove', 'admin', 'support', 'hello', 'help', 'info']


STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'pstatic'),)
STATIC_ROOT = '/home/boiyelove/webapps/staticfiles/workflow/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/boiyelove/webapps/mediafiles/workflow/'