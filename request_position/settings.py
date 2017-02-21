# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import
from django.conf import settings


DEFAULT_IP = getattr(settings, "REQUEST_LOCATION_DEFAULT_IP", "127.0.0.1")
DEFAULT_POSITION = getattr(settings, "REQUEST_DEFAULT_POSITION", None)
DEFAULT_COUNTRY_CODE = getattr(settings, "REQUEST_DEFAULT_COUNTRY_CODE", None)

POSITION_COOKIE_NAME = getattr(settings, "REQUEST_POSITION_COOKIE_NAME", "_request_position")
GEO_HEADER = getattr(settings, "REQUEST_POSITION_GEO_HEADER", "HTTP_GEOLOCATION")

OVERRIDE_LATITUDE_PARAM = getattr(settings, "REQUEST_LOCATION_OVERRIDE_LATITUDE_PARAM", "lat")
OVERRIDE_LONGITUDE_PARAM = getattr(settings, "REQUEST_LOCATION_OVERRIDE_LONGITUDE_PARAM", "lon")
OVERRIDE_COUNTRY_CODE_PARAM = getattr(settings, "REQUEST_LOCATION_OVERRIDE_COUNTRY_CODE_PARAM", "cc")

# If this is True, the request.position attribute will be a Point geometry, and if it's False, it'll be
# a tuple (latitude, longitude).
USE_GIS_POINT = getattr(settings, "REQUEST_POSITION_USE_GIS_POINT", False)
