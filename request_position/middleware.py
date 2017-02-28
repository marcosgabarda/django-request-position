# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

import re

from django.conf import settings
from django.contrib.gis.geoip import GeoIP
from django.contrib.gis.geos import Point
from django.utils.deprecation import MiddlewareMixin

from request_position.helpers import save_position, save_country_code
from request_position.settings import DEFAULT_IP, POSITION_COOKIE_NAME, GEO_HEADER, DEFAULT_POSITION, USE_GIS_POINT, \
    OVERRIDE_LATITUDE_PARAM, OVERRIDE_LONGITUDE_PARAM, OVERRIDE_COUNTRY_CODE_PARAM, DEFAULT_COUNTRY_CODE


class RequestPositionMiddleware(MiddlewareMixin):
    """Obtains the position associated to the request, and saves it in the
    request and in the current thread.
    """

    @staticmethod
    def _parse_position(position):
        if position is not None and USE_GIS_POINT:
            return Point(float(position[1]), float(position[0]))
        return position

    @staticmethod
    def _params_position(request):
        return (request.GET.get(OVERRIDE_LATITUDE_PARAM), request.GET.get(OVERRIDE_LONGITUDE_PARAM)) \
            if OVERRIDE_LATITUDE_PARAM in request.GET and OVERRIDE_LONGITUDE_PARAM in request.GET else None

    @staticmethod
    def _cookie_position(request):
        raw_cookie_position = request.COOKIES.get(POSITION_COOKIE_NAME)
        lat, lon = map(lambda x: float(x), raw_cookie_position.split("|"))
        return lat, lon

    @staticmethod
    def _header_position(request):
        header_position = None
        raw_header_position = request.META.get(GEO_HEADER)
        match = re.match("<geo:([-+]?\d+\.\d+);([-+]?\d+\.\d+)>", raw_header_position)
        if match:
            position = match.groups()
            if tuple(map(lambda item: int(float(item)), position)) != (0, 0):
                header_position = position
        return header_position

    def process_request(self, request):
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
            ip = request.META.get(settings.REMOTE_ADDR_ATTR, DEFAULT_IP)
            g = GeoIP()
            request_position = self._parse_position(g.lat_lon(ip) or DEFAULT_POSITION)

        save_position(request_position)
        request.position = request_position
        request.override_position = positions[0] is not None
        request.is_approximate_location = is_approximate_location
        return None

    def process_response(self, request, response):
        """Process the response to override the cookie in case this is necessary."""
        if hasattr(request, 'override_position') and request.override_position:
            response.set_cookie(key=POSITION_COOKIE_NAME, value="%s|%s" % (request.position[0], request.position[1]))
        return response


class RequestCountryMiddleware(MiddlewareMixin):
    """Middleware to select the country of the request."""

    def process_request(self, request):
        """Use the IP to obtain the country of the request. It can be override using
        a parameter in the request.
        """
        ip = request.META.get(settings.REMOTE_ADDR_ATTR, DEFAULT_IP)
        g = GeoIP()
        if request.GET.get(OVERRIDE_COUNTRY_CODE_PARAM):
            country_code = request.GET.get(OVERRIDE_COUNTRY_CODE_PARAM).lower()
        else:
            country_code = g.country_code(ip)
        request.country = country_code or DEFAULT_COUNTRY_CODE
        save_country_code(request.country.lower())
        return None
