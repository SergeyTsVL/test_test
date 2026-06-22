from django.shortcuts import redirect
from django.urls import reverse


class DevPasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [reverse('ads:dev_password_page')]

        if request.path in exempt_urls:
            return self.get_response(request)

        if not request.session.get('dev_authenticated'):
            request.session['next_url'] = request.get_full_path()
            return redirect('ads:dev_password_page')

        return self.get_response(request)