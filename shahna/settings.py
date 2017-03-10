import os
from os.path import join

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = '&!4bopz)64nfp&u@5bp!+orox&qaaw!4^guim3!^!ejy&p7vg3'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'widget_tweaks',
    'account',
    'forum',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'utils.middleware.MultiLangMiddleware',
]

ROOT_URLCONF = 'shahna.urls'

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
                "django.core.context_processors.media",
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'account.context_processors.profile_completion_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'shahna.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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



TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATIC_ROOT = 'collected_static/'

MEDIA_ROOT = join(BASE_DIR, 'media/')

LANGUAGES = (
    ('fa', 'Persian'),
    ('en', 'English'),
)
LANGUAGE_CODE = 'fa-IR'
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MAX_UPLOAD_SIZE = 500 * 1024 # 500 KB

STAR_RULES = {
    'ASKING_QUESTION': 1,
    'STAR_QUESTION': 3,
    'ANSWERING': 1,
    'STAR_ANSWER': 3,
    'ACCEPTING_ANSWER': 5,
}

SITE_ID = 1

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'Shahnay <noreply@shahnay.ir>'
EMAIL_HOST = 'localhost'
EMAIL_USER = 'shahna'
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'me@gmail.com'
#EMAIL_HOST_PASSWORD = 'pass'
