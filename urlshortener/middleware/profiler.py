from django.http.request import HttpRequest
import cProfile


class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):

        profile = cProfile.Profile()
        profile.enable()
        response = self.get_response(request)
        profile.disable()
        profile.dump_stats('test.pstat')
        return response
