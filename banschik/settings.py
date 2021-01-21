from pathlib import Path
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env_file = Path.joinpath(BASE_DIR, ".env")
# reading .env file
environ.Env.read_env(env_file.as_posix())

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = []
HOSTS_ENV = env.list('ALLOWED_HOSTS', default=[])
if HOSTS_ENV:
    ALLOWED_HOSTS.extend(HOSTS_ENV)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'solo',
    'manifest_loader',
    'django_email_verification',
    'adminsortable',
    'cabinet.apps.CabinetConfig',
    'cms.apps.CmsConfig',
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

ROOT_URLCONF = 'banschik.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'banschik.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Custom User Model
AUTH_USER_MODEL = 'cabinet.Account'

from email.utils import getaddresses

ADMINS = getaddresses([env('ADMINS')])
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'dist'
]

MANIFEST_LOADER = {
    'cache': False,
}


def verified_callback(user):
    user.is_active = True


EMAIL_VERIFIED_CALLBACK = verified_callback
EMAIL_FROM_ADDRESS = 'noreply@banschikmagazin.ru'
EMAIL_MAIL_SUBJECT = 'Потвердите свой адрес электроной почты.'
EMAIL_MAIL_HTML = 'cabinet/email/mail_body.html'
EMAIL_MAIL_PLAIN = 'cabinet/email/mail_body.txt'
EMAIL_TOKEN_LIFE = 60 * 60
EMAIL_PAGE_TEMPLATE = 'cabinet/email/confirm.html'
EMAIL_PAGE_DOMAIN = 'http://127.0.0.1:8000/'

# For Django Email Backend
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = env('EMAIL_PORT')
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = env('EMAIL_USE_TLS')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SOLO_CACHE = 'default'
SOLO_CACHE_TIMEOUT = 60 * 5  # 5 mins
SOLO_CACHE_PREFIX = 'solo'

MENU_CACHE_KEY = 'menus'
MENU_CACHE_TIMEOUT = 60 * 5
