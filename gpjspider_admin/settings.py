# -*- coding: utf-8 -*-
"""
Django settings for gpjspider_admin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import sys
sys.path.append('/usr/lib/python2.7/dist-packages')
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5!_gm@a@ncrzg4mdrp22mhjc+jt99xh-6_p8e8a)8xz%63f26*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gpjspider',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gpjspider_admin.urls'

WSGI_APPLICATION = 'gpjspider_admin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    # 测试
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "pingjia",
        "USER": "pingjia",
        "PASSWORD": "De32wsxc",
        "HOST": "101.251.105.186",
        "PORT": "3306",
    },
    # 正式
    # "default": {
    #     "ENGINE": "django.db.backends.mysql",
    #     "NAME": "pingjia",
    #     "USER": "pingjia",
    #     "PASSWORD": "De32wsxc",
    #     "HOST": "192.168.206.212",
    #     "PORT": "3306",
    # },

    "certify": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "souche",
        "USER": "pingjia",
        "PASSWORD": "De32wsxc",
        "HOST": "192.168.206.212",
        "PORT": "3306",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
