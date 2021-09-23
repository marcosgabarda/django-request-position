from threading import local
from typing import TYPE_CHECKING

from request_position.settings import DEFAULT_COUNTRY_CODE, DEFAULT_POSITION

if TYPE_CHECKING:
    from django.contrib.gis.geos import Point

_active = local()


def save_position(position: "Point") -> None:
    """Saves given position in the current thread.
    :param position:
    :return:
    """
    _active.position = position


def get_position() -> "Point":
    """Gets current position, saved in current thread.
    :return: tuple
    """
    position = getattr(_active, "position", DEFAULT_POSITION)
    return position


def save_country_code(country_code: str) -> None:
    """Saves given country_code in the current thread.
    :param country_code:
    :return:
    """
    _active.country_code = country_code


def get_country_code() -> str:
    """Gets current country_code, saved in current thread.
    :return: tuple
    """
    country_code = getattr(_active, "country_code", DEFAULT_COUNTRY_CODE)
    return country_code
