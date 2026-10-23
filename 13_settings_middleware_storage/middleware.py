"""Middleware class — referenced only via MIDDLEWARE dotted path."""


class RouteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
