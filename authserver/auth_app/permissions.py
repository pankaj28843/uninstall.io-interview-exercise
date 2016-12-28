from __future__ import unicode_literals

from django.http import Http404

from rest_framework.compat import is_authenticated
from rest_framework_jwt.settings import api_settings


jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class JWTPermission(object):
    """
    A base class from which all permission classes should inherit.
    """

    def get_payload(self, request):
        return jwt_decode_handler(request.auth)

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if not (request.user and is_authenticated(request.user)):
            return False

        payload = self.get_payload(request)

        try:
            resource_name = view.resource_name
        except AttributeError:
            return False

        try:
            available_permissions = [x['name'] for x in payload['permissions']]
        except KeyError:
            return False

        required_permission = '%s-%s' % (resource_name, request.method)

        return required_permission in available_permissions

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return False
