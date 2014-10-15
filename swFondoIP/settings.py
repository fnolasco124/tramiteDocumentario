"""
Django settings for swFondoIP project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.core.urlresolvers import reverse_lazy

#LOGIN_URL = reverse_lazy('Login_View')
#LOGIN_REDIRECT_URL = reverse_lazy('Login_View')
#LOGOUT_URL = reverse_lazy('Logout_View')


BASE_DIR = os.path.dirname(__file__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gx2(@1n*gqn3xgl_+38)d4418c8!&zifz7^*mj6h!&v&k0=49r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ADMINS = (
    ('Francisco Nolasco Bonilla','fnolasco@fondoitaloperuano.org'),
    )   

MANAGER = ADMINS

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'swFondoIP.apps.tramiteDoc',
    #'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'swFondoIP.urls'

WSGI_APPLICATION = 'swFondoIP.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'APPWEBFIP',
        'USER': 'root',
        'PASSWORD':'fip4210909', # modificar siempre para sincronizar con maquina virtual
        'HOST':'',
        'PORT':'',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-PE'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
#MEDIA_ROOT = '/home/francisco/PROYECTO/swFondoIP/swFondoIP/media'
STATIC_URL = '/static/'
STATIC_ROOT = ''

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
    )

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,'template')
    )


URL_LOGIN = '/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

EMAIL_HOST = "192.168.1.3"
EMAIL_PORT = "25"
EMAIL_HOST_USER = "wffip@fondoitaloperuano.org"
EMAIL_HOST_PASSWORD = "F1p205052"
EMAIL_USE_TLS = True
ACOUNT_EMAIL_VERIFICATION = 'none'
