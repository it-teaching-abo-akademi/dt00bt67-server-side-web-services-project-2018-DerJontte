import re
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views import View

from auctionApp.auctions_browse import BrowseAuctions
from auctionApp.models import *

admin_mail = 'broker@awesomeauctions.com'


def referer(request):
    if 'override' in request.session:
        go_to = request.session['override']
        del request.session['override']
        return redirect(go_to)
    return redirect(request.META['HTTP_REFERER'])


def home(request):
    return render(request, "home.html", None)


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
            message = 'The auction %d: "%s" has been banned because it violates the YAAS TOS. No further bidding on the item is possible and ' \
                      'the auction will not be resolved.' % (auction.id, auction.title)
            recipients = []
            recipients.append(auction.seller_email)
            for bidder in auction.bid_set.all():
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
            message = 'Your auction %d: "%s" has been unbanned and can be bid on again.' % (auction.id, auction.title)
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


