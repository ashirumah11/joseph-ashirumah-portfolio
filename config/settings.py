"""
Django settings for Joseph Ashirumah - Full-Stack Software Engineer Portfolio.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present
load_dotenv(BASE_DIR / '.env')

# Security settings
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-portfolio-dev-secret-key-replace-in-production-198273645'
)

DEBUG = os.getenv('DEBUG', 'True').strip().lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost,0.0.0.0,testserver').split(',')
    if host.strip()
]

# CSRF Trusted Origins (useful for production deployment e.g. Render, Railway)
csrf_trusted = os.getenv('CSRF_TRUSTED_ORIGINS', '')
if csrf_trusted:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_trusted.split(',') if origin.strip()]
else:
    CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom Portfolio Apps
    'core.apps.CoreConfig',
    'projects.apps.ProjectsConfig',
    'contact.apps.ContactConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# Uses DATABASE_URL if provided (e.g. PostgreSQL), otherwise defaults to local SQLite
default_db_url = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
database_url = os.getenv('DATABASE_URL', default_db_url)

DATABASES = {
    'default': dj_database_url.config(
        default=database_url,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploads: profile photos, project screenshots, CV)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload security limits
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Production Static Storage via Whitenoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').strip().lower() in ('true', '1', 'yes')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@josephashirumah.dev')
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'joseph.ashirumah@example.com')

# If SMTP credentials are provided, switch automatically to SMTP backend
if EMAIL_HOST:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Security Headers & Cookie settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').strip().lower() == 'true'
    CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True').strip().lower() == 'true'
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').strip().lower() == 'true'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
