from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RequestPositionConfig(AppConfig):

    name: str = "request_position"
    verbose_name: str = _("Request position")
