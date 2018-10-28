from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import View

from auctionApp.currency import Currency
from auctionApp.views import referer, UserSettings


class Login(View):
    def get(self, request):
        return redirect('home')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                settings = UserSettings.objects.get(id=request.user.id)
                request.session['currency'] = settings.currency
                request.session['currencies'] = Currency.code_list()
        except:
            pass
        return referer(request)

    def request_login(request, username, password):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                return True
            return False
        except:
            return False


class Logout(View):
    def get(self, request):
        return referer(request)

    def post(self, request):
        override = request.session['override'] if 'override' in request.session else None
        logout(request)
        if override is not None:
            request.session['override'] = override
        return referer(request)

