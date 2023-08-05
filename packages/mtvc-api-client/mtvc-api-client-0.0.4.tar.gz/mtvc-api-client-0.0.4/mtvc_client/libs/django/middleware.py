import base64

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings

from mtvc_client.client import APIClientException


class APIClientExceptionMiddleware(object):
    """
    A middleware class that adds additional context information when
    APIClientExceptions are raised by the application
    """

    def process_exception(self, request, exception):
        if isinstance(exception, APIClientException):
            return render(
                request, 'smart/500.html', {
                    'error_code': exception.error_code,
                    'error_message': exception.error_message,
                }, context_instance=RequestContext(request), status=500)

        return None


class BasicAuthMiddleware(object):
    """
    Use this Middleware to password-protect a portal using HTTP Basic
    Authentication with creds stored in a settings file.

    This is useful for eg. locking down a QA site pre-launch.

    Requires BASIC_AUTH_CREDS in Django settings which should be a
    dict with passwords keyed by username.
    """

    def get_rfa_response(self):
        response = HttpResponse(
            '<html><title>Authentication required</title><body>'
            '<h1>Authentication Required</h1></body></html>', status=401)
        response['WWW-Authenticate'] = 'Basic realm="Restricted"'
        return response

    def process_request(self, request):
        # fail if we don't have proper BA headers
        try:
            auth_type, data = request.META['HTTP_AUTHORIZATION'].split()
        except KeyError:
            return self.get_rfa_response()

        # this is basic auth only
        if auth_type.lower() != 'basic':
            return self.get_rfa_response()

        # decode the BA data
        try:
            username, password = base64.b64decode(data).decode('utf-8').split(
                ':', 1)
        except (TypeError, ValueError):
            return self.get_rfa_response()

        if not hasattr(settings, 'BASIC_AUTH_CREDS') or \
                username not in settings.BASIC_AUTH_CREDS or \
                settings.BASIC_AUTH_CREDS[username] != password:
            return self.get_rfa_response()

        return None
