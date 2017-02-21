# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django

DEBUG = True
USE_TZ = True

SECRET_KEY = "dummy"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "request_position",
    "tests.app",
]

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = (
        'request_position.middleware.RequestPositionMiddleware',
        'request_position.middleware.RequestCountryMiddleware',
    )
else:
    MIDDLEWARE_CLASSES = (
        'request_position.middleware.RequestPositionMiddleware',
        'request_position.middleware.RequestCountryMiddleware',
    )
