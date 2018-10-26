from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from auctionApp.auctions_browse import BrowseAuctions
from auctionApp.models import Auction
from auctionApp.views import referer, admin_mail, get_user_name


class BidAuction(View):
    def get(self, request, number):
        return redirect('/auction/' + str(number))

    def post(self, request, number):
        error_message = None
        info_message = None
        if 'currency' in request.session:
            currency = request.session['currency']
        else:
            currency = 'EUR'

        if request.POST['action'] == "Place bid":
            if request.user.is_authenticated:
                auction = (Auction.objects.select_for_update().get(id=number))
                question = 'Do you want to bid ' + str(request.POST['new_bid']) + ' ' + currency + ' on this auction?'
                request.session['description'] = auction.description
                return render(request, 'confirm_bid.html', {'auction': auction,
                                                            'bid': float(request.POST['new_bid']),
                                                            'question': question})
            else:
                return referer(request)

        if request.POST['action'] == 'confirm':
            with transaction.atomic():
                auction = (Auction.objects.select_for_update().get(id=number))
                if auction.description == request.session['description']:
                    old_winner = auction.current_winner_id
                    new_winner = request.user.username
                    if old_winner is not None:
                        old_winner_email = User.objects.get(id=auction.current_winner_id).email
                    else:
                        old_winner_email = None
                    seller_email = auction.seller_email
                    new_bid = float(request.POST['bid'])

                    tf = '%Y%m%d%H%M%S'
                    current_time = datetime.now().strftime(tf)
                    closing_time = auction.time_closing.strftime(tf)

                    if new_bid > auction.current_price and current_time <= closing_time:
                        auction.current_price = new_bid
                        auction.current_winner_id = request.user.id
                        auction.current_winner_name = request.user.username
                        auction.bid_set.create(user_id=request.user.id, name=request.user.username, email=request.user.email, price=new_bid)
                        diff = int(closing_time) - int(current_time)
                        seconds = round((diff / 100 * 60) + (diff % 60), 0)
                        print(seconds)
                        if seconds < timedelta(minutes=5).seconds:
                            auction.time_closing = datetime.now() + timedelta(minutes=5)
                        auction.save()
                        info_message = 'Your bid has been registered'
                        success = True
                    else:
                        success = False
                        if new_bid <= auction.current_price:
                            error_message = 'Bid could not be registered: an older bid is higher.'
                        if current_time > closing_time:
                            error_message = 'Bid could not be registered: auction deadline has passed.'
                else:
                    success = False
                    error_message = 'Bid was not registered: Auction description has been changed. Please see new description before bidding again.'

            if success:
                if old_winner_email != None:
                    to_old_winner = 'Your winning bid in the auction "' + str(auction.title) + '" posted by ' + str(auction.seller_name) + ' has been outbidded.\n The new highest bid is ' + \
                                    str(auction.current_price) + ' made by ' + str(auction.current_winner_name) + '.\n\nYou can place a new bid by logging in to the page at ' + \
                                    str(request.META['HTTP_REFERER'])

                    to_seller = 'A new bid has been registered in your auction "' + str(auction.title) + '". The new highest bid is ' + str(auction.current_price) + ' and was made by the user ' \
                                + str(new_winner) + '.\n\nYou can view your auction at the adress ' + str(request.META['HTTP_REFERER'])

                    send_mail('Your bid has been beaten',
                              to_old_winner,
                              admin_mail,
                              [old_winner_email],
                              fail_silently=False)

                    send_mail('A new bid has been registered',
                              to_seller,
                              admin_mail,
                              [seller_email],
                              fail_silently=False)
            return BrowseAuctions.fetch_auction(request, number, info_message=info_message, error_message=error_message)
        else:
            return referer(request)

