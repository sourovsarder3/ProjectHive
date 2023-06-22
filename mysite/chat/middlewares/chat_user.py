from django.shortcuts import redirect


class UserAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.session.get('user_id'):
            return redirect('login')

        response = self.get_response(request)
        return response


class LoginMiddlware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.session.get('user_id'):
            return redirect('chat_page')

        response = self.get_response(request)
        return response
