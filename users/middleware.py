from django.shortcuts import redirect


class UserActiveRequiredOrRedirectMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_active \
                and request.path not in ['/accounts/activate/', '/accounts/logout/'] \
                and request.user.is_authenticated:
            return redirect('activate_profile')

        response = self.get_response(request)

        return response
