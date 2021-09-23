from django.conf import settings

REMOTE_ADDR_ATTR = getattr(settings, "REQUEST_POSITION_REMOTE_ADDR_ATTR", "REMOTE_ADDR")

DEFAULT_IP = getattr(settings, "REQUEST_POSITION_DEFAULT_IP", "127.0.0.1")
DEFAULT_POSITION = getattr(settings, "REQUEST_POSITION_DEFAULT_POSITION", None)
DEFAULT_COUNTRY_CODE = getattr(settings, "REQUEST_POSITION_DEFAULT_COUNTRY_CODE", None)

POSITION_COOKIE_NAME = getattr(
    settings, "REQUEST_POSITION_COOKIE_NAME", "_request_position"
)
GEO_HEADER = getattr(settings, "REQUEST_POSITION_GEO_HEADER", "HTTP_GEOLOCATION")

OVERRIDE_LATITUDE_PARAM = getattr(
    settings, "REQUEST_POSITION_OVERRIDE_LATITUDE_PARAM", "lat"
)
OVERRIDE_LONGITUDE_PARAM = getattr(
    settings, "REQUEST_POSITION_OVERRIDE_LONGITUDE_PARAM", "lon"
)
OVERRIDE_COUNTRY_CODE_PARAM = getattr(
    settings, "REQUEST_POSITION_OVERRIDE_COUNTRY_CODE_PARAM", "cc"
)

# If this is True, the request.position attribute will be a Point geometry, and if it's False, it'll be
# a tuple (latitude, longitude).
USE_GIS_POINT = getattr(settings, "REQUEST_POSITION_USE_GIS_POINT", False)
