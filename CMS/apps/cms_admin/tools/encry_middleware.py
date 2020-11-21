from django.utils.deprecation import MiddlewareMixin


class EncryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass
        # print(request)

    def process_response(self, request, response):
        # print("Md1返回")
        return response

