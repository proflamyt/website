"""
Django settings for real project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True #  config('DEBUG', cast=bool)



ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
   
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'school.apps.SchoolConfig',
     'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
     'django.contrib.auth',
     'phonenumber_field',
     'sorl.thumbnail',
 'allauth',   # <--
 'allauth.account',   # <--
 'allauth.socialaccount',   # <--
 'allauth.socialaccount.providers.google',
 'allauth.socialaccount.providers.github',
# 'allauth.socialaccount.providers.HackerEarth',
 'django.contrib.sites', 
 'djangorave' , # <--,

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

ROOT_URLCONF = 'real.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.normpath(os.path.join(BASE_DIR,'public_html')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'real.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR +'/'+ 'db.sqlite3',
    }
}


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#       'default': {
#         'ENGINE':'django.db.backends.postgresql_psycopg2',
#         'NAME': 'olamide',
#         'USER': 'proflamyt',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '5432'
#     }
# }
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = 'seehowtv@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
EMAIL_HOST_USER = SERVER_EMAIL
EMAIL_PORT = 587
DEFAULT_AUTO_FIELD='django.db.models.AutoField'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMINS = [('cHowTV', 'seehowtv@gmail.com')]
AUTH_USER_MODEL = 'school.User'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


AUTHENTICATION_BACKENDS = (
 'django.contrib.auth.backends.ModelBackend',
 'allauth.account.auth_backends.AuthenticationBackend',
 )
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'


#STATICFILES_DIRS =[
 #   os.path.join(BASE_DIR, 'school/static'),
   
#]
STATIC_ROOT =  os.path.join(BASE_DIR, 'school/static')


MEDIA_ROOT = os.path.join(BASE_DIR, 'book')
MEDIA_URL = '/book/'

STAR_RATINGS_STAR_HEIGHT = 15
STAR_RATINGS_STAR_WIDTH =15

 
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
    'default':
    {
        'toolbar':'Custom',
        'height': 500,
       
        
        'toolbar_Custom': [
            ['Unlink', 'Link' , 'Image'],
            ['Styles', 'Format', 'Bold', 'Italic', 'SpellChecker', 'Undo', 'Redo'],
            ['Smiley', 'SpecialChar'],
            ['CodeSnippet', 'about']
        ],
        'extraPlugins':'codesnippet'
    },
    'novellas':{
        'toolbar':'Custom',
        'height': 500,
        'width': '105%',
        'display': 'inline-block',
        'placeholder': 'maximize to start writing',
        
        'toolbar_Custom': [
          
            ['Styles', 'Format', 'Bold', 'Italic', 'SpellChecker', 'Undo', 'Redo'],
            ['Smiley', 'SpecialChar'],
            ['Indent', 'Outdent','Maximize'],
            ['JustifyLeft', 'JustifyCenter','JustifyRight','JustifyBlock']
        ],
        
    }
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'


RAVE_SANDBOX = True
API_key = config('API_KEY')

import django_heroku
django_heroku.settings(locals())