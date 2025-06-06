# Samp/settings/dev.py

from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

STATICFILES_DIRS = [BASE_DIR / 'static']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
