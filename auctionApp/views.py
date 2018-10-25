import re

import pytz
import datetime
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect, render

from auctionApp.auctions_browse import BrowseAuctions
from auctionApp.currency import *
from auctionApp.models import *

admin_mail = 'broker@awesomeauctions.com'


def referer(request):
    return redirect(request.META['HTTP_REFERER'])


def home(request):
    return render(request, "home.html", None)


class Search(View):
    global results
    results = 'No search sting entered'

    def get(self, request):
        return render(request, 'search_results.html', {'results': results})

    def post(self, request):
        query = str(request.POST['search']).lower()
        results = {}
        try:
            for auction in Auction.objects.all():
                if query in auction.title.lower() and auction.active is True:
                    results[auction.id] = auction.title
        except:
            pass
        return render(request, 'search_results.html', {'results': results})


class ListBanned(View):
    def get(self, request):
        auctions = Auction.objects.all().filter(banned=True)
        return render(request, 'browse.html', {'auctions': auctions,
                                               'error_message': 'This is a list of banned auctions.'})


class BanAuction(View):
    def get(self, request):
        return redirect('home')

    def post(self, request, number):
        if request.POST['action'] == 'Ban':
            auction = Auction.objects.get(id=number)
            auction.banned = True
            auction.active = False
            auction.save()

            subject = 'Auction has been banned'
            message = 'The auction ' + str(auction.id) + ': ' + str(
                auction.title) + ' has been banned because it violates the YAAS TOS. No further bidding on the item will be possible and ' \
                                 'the auction will not be resolved.'
            recipients = []
            recipients.append(auction.seller_email)
            for bidder in auction.bidders_set.all():
                if bidder.email not in recipients:
                    recipients.append(bidder.email)
            send_mail(subject, message, admin_mail, recipients, fail_silently=False)
            return BrowseAuctions.fetch_auction(request, number, error_message='Auction banned.')

        if request.POST['action'] == 'Unban':
            auction = Auction.objects.get(id=number)
            auction.banned = False
            auction.active = True
            auction.save()

            subject = 'Auction unbanned'
            message = 'Your auction "' + str(auction.id) + ': ' + str(
                auction.title) + '" has been unbanned and can be bidded on again.'
            recipient = auction.seller_email
            send_mail(subject, message, admin_mail, [recipient], fail_silently=False)
            return BrowseAuctions.fetch_auction(request, number, info_message='Auction unbanned.')


def handler404(request, *args, **argv):
    return redirect('/home/')


def get_user_name(id):
    try:
        return User.objects.get(id=id)
    except:
        return 'User account has been disabled or deleted'


def make_slug_hash(input):
    input = make_password(input)
    output = re.sub('(\W)|(pbkdf2_sha256)', '', input);
    return output
