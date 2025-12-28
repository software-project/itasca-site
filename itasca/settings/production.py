from .base import *
import os
from pathlib import Path

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

SECRET_KEY = os.environ.get('SECRET_KEY')

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'itasca_db'),
        'USER': os.environ.get('DB_USER', 'itasca_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'db'),  # Default to 'db' for Docker
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# ManifestStaticFilesStorage is recommended in production
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

WAGTAILADMIN_BASE_URL = os.environ.get('WAGTAILADMIN_BASE_URL', 'https://itasca.pl')

try:
    from .local import *
except ImportError:
    pass