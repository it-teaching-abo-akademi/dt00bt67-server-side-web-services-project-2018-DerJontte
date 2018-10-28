from django.shortcuts import render
from django.views import View

from auctionApp.auctions_browse import BrowseAuctions
from auctionApp.models import Auction


class Search(View):
    global results

    def get(self, request):
        if 'search_query' in request.session:
            return self.post(request, query=request.session['search_query'])
        return render(request, 'search_results.html', {'results': results})

    def post(self, request, **messages):
        info_message = ''
        error_message = ''
        if 'search' in request.POST:
            query = str(request.POST['search']).lower()
            request.session['search_query'] = query
        else:
            query = messages.get('query')

        if query != '':
            auctions = Auction.objects.all().filter(active=True, title__contains=query).order_by('time_closing')
            info_message = 'Auctions matching your search'
        else:
            auctions = ''
            error_message = 'No auctions matching query'

        return BrowseAuctions.get(None, request, info_message=info_message, error_message=error_message, auctions=auctions)
