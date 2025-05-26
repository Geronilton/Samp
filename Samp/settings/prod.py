# Samp/settings/prod.py

from .base import *

# banco de dados produção
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['samp-ieum.onrender.com']

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = []


