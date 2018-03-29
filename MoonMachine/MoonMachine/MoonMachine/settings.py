"""
Django settings for MoonMachine project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import posixpath
from MoonMachine.HiddenSettings import HiddenSettings
from MoonMachine.SelectionOptions.LabeledConstants import LOG_FILE

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = HiddenSettings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = HiddenSettings.DEBUG_MODE

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'app', #Enables locating the templates
    'MoonMachine',
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'MoonMachine.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [            
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'MoonMachine.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases



DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'Moon Machine database',
        'HOST': 'moonmachine-server.database.windows.net',
        'PORT': '1433',
        'USER': HiddenSettings.DB_USER,
        'PASSWORD': HiddenSettings.DB_PASS,
        'AUTOCOMMIT': True,
        'OPTIONS': {
            'driver': 'ODBC Driver 13 for SQL Server',
        },
    }
}

import socket
currentHostname = socket.gethostname()

if currentHostname == HiddenSettings.LOCAL_HOSTNAME:
    DATABASES['default'] = {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'MoonMachineTestDatabase',
        'HOST': HiddenSettings.LOCAL_SERVERNAME,
        'PORT': '',
        'AUTOCOMMIT': True,
        'OPTIONS': {
            'driver': 'ODBC Driver 13 for SQL Server',
        },
    }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))

STATICFILESS_DIRS = [
        os.path.join (BASE_DIR, "static"),
    ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + LOG_FILE,
            'formatter': 'dated'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'dated'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True
        },
    },
    'formatters': {
        'dated': {
            'format': "%(created)f; %(levelname)s; %(message)s"
        }
    }
}

STATICFILES_FINDERS = ( 'django.contrib.staticfiles.finders.FileSystemFinder', 
                       'django.contrib.staticfiles.finders.AppDirectoriesFinder'
                       ) 

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
CSRF_USE_SESSIONS = False #leave as false. if true, it sets the csrf token 

TEMPLATE_CONTEXT_PROCESSORS = [ # required in order to fetch the current user from an import, instead of a dependency injection
    'django.core.context_processors.request'    
] 