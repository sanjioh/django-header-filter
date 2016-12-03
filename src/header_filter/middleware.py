from .compat import MiddlewareMixin


class HeaderFilterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass
