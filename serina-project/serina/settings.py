import os

from django.contrib.messages import constants as messages


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Project main

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-parties apps
    'crispy_forms',
    'django_extensions',
    'graphene_django',
    'import_export',
    'paypal.standard.ipn',

    # Project apps
    'api',
    'management',
    'rating',
    'registration',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'serina.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'serina.serina.context_processors.get_contact_mails',
            ],
        },
    },
]

WSGI_APPLICATION = 'serina.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', "django.db.backends.sqlite3"),
        'NAME': os.environ.get('DATABASE_NAME', os.path.join(BASE_DIR, "db.sqlite3")),
        'USER': os.environ.get('DATABASE_USER', "user"),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', "password"),
        'HOST': os.environ.get('DATABASE_HOST', "localhost"),
        'PORT': os.environ.get('DATABASE_PORT', "5432"),
    }
}


# Graphene

GRAPHENE = {
    'SCHEMA': 'api.schema.schema'
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


# URLs

LOGIN_URL = '/registration/login/'

LOGIN_REDIRECT_URL = '/'


# Internationalization

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
    ('nl', 'Dutch'),
]


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Paginators

PAGINATION = {
    "listview": 10,
}


# Paypal settings

PAYPAL_RECEIVER_EMAIL = os.environ.get('PAYPAL_RECEIVER_EMAIL')

PAYPAL_TEST = True


# SMTP configuration

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# Messages

MESSAGE_TAGS = {messages.ERROR: 'danger'}


# App settings

COURSE_MINIMUM_REGISTRATION_DAYS = 7
SUCCESS_SCORE_THRESHOLD = 50


# Billing data

BILLING = {
    "name": "SERINA-Project 2020 Fictional Inc.",
    "vat": "1234567890",
}

# Mails

CONTACT_MAILS = {
    "administrator": "administrators@serina-project.bryanmramsamy.com",
    "management": "management@serina-project.bryanmramsamy.com",
    "support": "support@serina-project.bryanmramsamy.com",
}
