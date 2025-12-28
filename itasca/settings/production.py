from .base import *
import os
from pathlib import Path

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Fix ALLOWED_HOSTS parsing - filter out empty strings
ALLOWED_HOSTS_STR = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR.split(',') if host.strip()]

# Ensure SECRET_KEY is set
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'itasca_db'),
        'USER': os.environ.get('DB_USER', 'itasca_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# ManifestStaticFilesStorage is recommended in production
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

WAGTAILADMIN_BASE_URL = os.environ.get('WAGTAILADMIN_BASE_URL', 'https://itasca.pl')

# Security Settings for HTTPS/SSL
# Only enable these if you're serving over HTTPS (which you are with Let's Encrypt)

# HTTP Strict Transport Security (HSTS)
# Tells browsers to only connect via HTTPS for the specified time period
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Redirect all HTTP connections to HTTPS
SECURE_SSL_REDIRECT = True

# Use secure cookies (only sent over HTTPS)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Additional security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Trust the X-Forwarded-Proto header from Nginx
# This is important when using a reverse proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

try:
    from .local import *
except ImportError:
    pass