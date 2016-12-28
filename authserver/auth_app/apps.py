from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext as _


class AuthAppConfig(AppConfig):
    name = 'auth_app'
    verbose_name = 'Auth App'
