"""Django root URLconf error handlers — looked up by name, not imported."""

from django.http import (
    HttpRequest,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
)


def _bad_request(request: HttpRequest, exception):
    return HttpResponseBadRequest("Bad request")


def _not_found(request: HttpRequest, exception):
    return HttpResponseNotFound("Not found")


def _forbidden(request: HttpRequest, exception):
    return HttpResponseForbidden("Forbidden")


def _server_error(request: HttpRequest, exception=None):
    return HttpResponseServerError("Server error")


# Django looks these up by name in the root URLconf for error dispatch.
handler400 = _bad_request
handler404 = _not_found
handler403 = _forbidden
handler500 = _server_error

urlpatterns = []
