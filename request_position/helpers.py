# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division, absolute_import

from threading import local

from request_position.settings import DEFAULT_POSITION, DEFAULT_COUNTRY_CODE

_active = local()


def save_position(position):
    """Saves given position in the current thread.
    :param position:
    :return:
    """
    _active.position = position


def get_position():
    """Gets current position, saved in current thread.
    :return: tuple
    """
    position = getattr(_active, "position", DEFAULT_POSITION)
    return position


def save_country_code(country_code):
    """Saves given country_code in the current thread.
    :param country_code:
    :return:
    """
    _active.country_code = country_code


def get_country_code():
    """Gets current country_code, saved in current thread.
    :return: tuple
    """
    country_code = getattr(_active, "country_code", DEFAULT_COUNTRY_CODE)
    return country_code

