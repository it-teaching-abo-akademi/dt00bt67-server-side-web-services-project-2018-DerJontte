from datetime import datetime
from django.shortcuts import render
from django.views import View
from auctionApp.currency import Currency
from auctionApp.models import Auction
from django import template


class BrowseAuctions(View):
    def get(self, request, **messages):
        if not 'currency' in request.session:
            request.session['currency'] = 'EUR'
        if not 'currencies' in request.session:
            request.session['currencies'] = Currency.code_list()
        auctions = Auction.objects.all().filter(active=True, banned=False).order_by('-time_closing')
        info_message = messages.get('info_message')
        error_message = messages.get('error_message')
        return render(request, 'browse.html', {'auctions': auctions,
                                               'info_message': info_message,
                                               'error_message': error_message, })

    def fetch_auction(request, number, **messages):
        auction = Auction.objects.get(id=number)
        session = request.session

        if 'currency' in session and session['currency'] != 'EUR':
            currency = session['currency']
            rate = Currency.get_rate(currency)
            starting_converted = auction.starting_price * rate
            current_converted = auction.current_price * rate
            starting_sum = "%.2f" % starting_converted
            starting_price = "%.2f EUR (%s %s)" % (auction.starting_price, starting_sum, currency)
            current_price = "%.2f EUR (%.2f %s)" % (auction.current_price, current_converted, currency)
        else:
            currency = 'EUR'
            starting_sum = None
            rate = 1
            starting_price = "%.2f EUR" % auction.starting_price
            current_price = "%.2f EUR" % auction.current_price

        ongoing = auction.time_closing.strftime('%Y%m%d%H%M%S') > datetime.now().strftime('%Y%m%d%H%M%S')
        print(ongoing)

        auction.time_posted = auction.time_posted.strftime('%H:%M %d/%m/%y')
        auction.time_closing = auction.time_closing.strftime('%H:%M %d/%m/%y')

        info_message = messages.get('info_message')
        error_message = messages.get('error_message')
        return render(request, 'view_auction_item.html', {'auction': auction,
                                                          'starting_sum': starting_sum,
                                                          'starting_price': starting_price,
                                                          'current_price': current_price,
                                                          'currency': currency,
                                                          'rate': rate,
                                                          'info_message': info_message,
                                                          'error_message': error_message,
                                                          'ongoing': ongoing})
