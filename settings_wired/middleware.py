"""Plain middleware + in-file helper — mirrors pitchaware.route.RouteMiddleware."""


def _matched_route(request) -> str | None:
    path = getattr(request, "path_info", None) or getattr(request, "path", "")
    if not path:
        return None
    return path.rstrip("/") or "/"


class RouteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if route := _matched_route(request):
            request.META = getattr(request, "META", {})
            request.META["app.route"] = route
        return response
