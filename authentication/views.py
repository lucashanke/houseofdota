from django.contrib.auth.views import logout
from django.shortcuts import redirect

from django.views import View


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
