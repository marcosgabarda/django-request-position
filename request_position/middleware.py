import re
from typing import TYPE_CHECKING, Callable, Optional, Tuple, Union

from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from geoip2.errors import AddressNotFoundError

from request_position.helpers import save_country_code, save_position
from request_position.settings import (
    DEFAULT_COUNTRY_CODE,
    DEFAULT_IP,
    DEFAULT_POSITION,
    GEO_HEADER,
    OVERRIDE_COUNTRY_CODE_PARAM,
    OVERRIDE_LATITUDE_PARAM,
    OVERRIDE_LONGITUDE_PARAM,
    POSITION_COOKIE_NAME,
    REMOTE_ADDR_ATTR,
    USE_GIS_POINT,
)

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class RequestPositionMiddleware:
    """Obtains the position associated to the request, and saves it in the
    request and in the current thread.
    """

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    @staticmethod
    def _parse_position(position: Optional[Tuple]) -> Union["Point", Tuple]:
        if position is not None and USE_GIS_POINT:
            return Point(float(position[1]), float(position[0]))
        return position

    @staticmethod
    def _params_position(request: "HttpRequest"):
        return (
            (
                request.GET.get(OVERRIDE_LATITUDE_PARAM),
                request.GET.get(OVERRIDE_LONGITUDE_PARAM),
            )
            if OVERRIDE_LATITUDE_PARAM in request.GET
            and OVERRIDE_LONGITUDE_PARAM in request.GET
            else None
        )

    @staticmethod
    def _cookie_position(request: "HttpRequest") -> Tuple[float, float]:
        raw_cookie_position = request.COOKIES.get(POSITION_COOKIE_NAME)
        lat, lon = map(lambda x: float(x), raw_cookie_position.split("|"))
        return lat, lon

    @staticmethod
    def _header_position(request: "HttpRequest") -> Optional[Tuple[float, ...]]:
        header_position = None
        raw_header_position = request.META.get(GEO_HEADER, "")
        match = re.match("<geo:([-+]?\d+\.\d+);([-+]?\d+\.\d+)>", raw_header_position)
        if match:
            position = match.groups()
            position = tuple(map(float, position))
            if position != (0.0, 0.0):
                header_position = position
        return header_position

    def process_request(self, request: "HttpRequest") -> None:
        """Obtain the position from several places, to attach it to the
        request. The preference is:

        - Request params (exact)
        - Header (exact)
        - Cookie (exact)
        - IP (approximate)
        """
        params_position = self._params_position(request)
        cookie_position = self._params_position(request)
        header_position = self._header_position(request)

        request_position = None
        positions = [params_position, cookie_position, header_position]
        for position in positions:
            if position is not None:
                request_position = self._parse_position(position)
        is_approximate_location = request_position is None
        if is_approximate_location:
            try:
                ip = request.META.get(REMOTE_ADDR_ATTR, DEFAULT_IP).split(",")[0]
                geo_ip = GeoIP2()
                request_position = self._parse_position(geo_ip.lat_lon(ip))
            except (ValidationError, AddressNotFoundError):
                request_position = self._parse_position(DEFAULT_POSITION)

        save_position(request_position)
        request.position = request_position
        request.override_position = positions[0] is not None
        request.is_approximate_location = is_approximate_location
        return None

    def process_response(self, request, response):
        """Process the response to override the cookie in case this is necessary."""
        if hasattr(request, "override_position") and request.override_position:
            response.set_cookie(
                key=POSITION_COOKIE_NAME,
                value="%s|%s" % (request.position[0], request.position[1]),
            )
        return response

    def __call__(self, request: "HttpRequest") -> "HttpResponse":
        self.process_request(request=request)
        response = self.get_response(request)
        response = self.process_response(request=request, response=response)
        return response


class RequestCountryMiddleware:
    """Middleware to select the country of the request."""

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def process_request(self, request: "HttpRequest") -> None:
        """Use the IP to obtain the country of the request. It can be override using
        a parameter in the request.
        """
        ip = request.META.get(REMOTE_ADDR_ATTR, DEFAULT_IP).split(",")[0]
        geo_ip = GeoIP2()
        if request.GET.get(OVERRIDE_COUNTRY_CODE_PARAM):
            country_code = request.GET.get(OVERRIDE_COUNTRY_CODE_PARAM).lower()
        else:
            try:
                country_code = geo_ip.country_code(ip)
            except (ValidationError, AddressNotFoundError):
                country_code = DEFAULT_COUNTRY_CODE
        request.country = country_code
        if request.country:
            save_country_code(request.country.lower())
        else:
            save_country_code(request.country)

    def __call__(self, request: "HttpRequest") -> "HttpResponse":
        self.process_request(request=request)
        response = self.get_response(request)
        return response
