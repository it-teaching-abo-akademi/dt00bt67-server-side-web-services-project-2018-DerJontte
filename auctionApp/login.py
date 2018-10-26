from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views import View

from auctionApp.currency import Currency
from auctionApp.models import UserSettings
from auctionApp.views import referer


class Login(View):
    def get(self, request):
        return redirect('home')

    def post(self, request):
        request.session['currencies'] = Currency.code_list()
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                settings = UserSettings.objects.get(id=request.user.id)
                request.session['currency'] = settings.currency
        except:
            pass
        return referer(request)


class Logout(View):
    def get(self, request):
        return referer(request)

    def post(self, request):
        logout(request)
        return referer(request)

