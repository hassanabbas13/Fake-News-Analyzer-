"""
Django settings for fake_news_project.

This file contains all the configuration for the Django project.
For a student project, the key settings are:
- INSTALLED_APPS: lists all apps (including our 'analyzer' app)
- DATABASES: we use SQLite (a simple file-based database)
- TEMPLATES: tells Django where to find HTML templates
- STATIC: tells Django where to find CSS/JS files
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR points to the root folder of the project (where manage.py is)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# For a student project, this is fine as-is
SECRET_KEY = 'django-insecure-fake-news-analyzer-student-project-key-2024'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG=True shows detailed error pages — useful during development
DEBUG = True

# Hosts that are allowed to access this app
ALLOWED_HOSTS = ['*']

# ---------------------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',        # Built-in admin panel
    'django.contrib.auth',         # User authentication system
    'django.contrib.contenttypes', # Content type framework
    'django.contrib.sessions',     # Session management
    'django.contrib.messages',     # Flash messages
    'django.contrib.staticfiles',  # Static file handling (CSS, JS, images)
    'analyzer',                    # Our custom app for fake news analysis
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fake_news_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # We use app-level templates (inside analyzer/templates/)
        'APP_DIRS': True,  # Django looks for templates inside each app's templates/ folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fake_news_project.wsgi.application'

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
# SQLite is a file-based database — no separate server needed
# The database file (db.sqlite3) is created automatically in BASE_DIR
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# ---------------------------------------------------------------------------
# URL prefix for static files
STATIC_URL = '/static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
