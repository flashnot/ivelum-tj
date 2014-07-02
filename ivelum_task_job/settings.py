"""
Django settings for ivelum_task_job project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&xgm#5k^!ztu6gl$q-k4lbsf2wpq(72_0ptz6@k(_@sqjwt&b&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'task',
    'extauth',
    'corsheaders',
    'django_rq',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # If you want redirect (now we return access denied message) to login page unauthorized\
    # user from anywhere (except LOGIN_EXEMPT_URLS) then uncomment line below:
    #'ivelum_task_job.middleware.LoginRequiredMiddleware'
)


ROOT_URLCONF = 'ivelum_task_job.urls'

WSGI_APPLICATION = 'ivelum_task_job.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

AUTH_USER_MODEL = 'extauth.ExtendedUser'

LOGIN_URL = '/api-auth/login/'
LOGIN_REDIRECT_URL = '/api/v1/task/'
LOGIN_EXEMPT_URLS = (
    r'^$',
    r'^/$',
)

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
)

# where worker running parameters:
RQ_SHOW_ADMIN_LINK = True
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    'high': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    }
}

REST_FRAMEWORK = {
    # only json response:
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', ),
    # human-readable result presentation, json response possibility if add ?format=json to url:
    #'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', 'rest_framework.renderers.BrowsableAPIRenderer', ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),
    'PAGINATE_BY': 10
}
