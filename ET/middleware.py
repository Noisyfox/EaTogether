from django.utils.deprecation import MiddlewareMixin


class UserAccountScopeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass
