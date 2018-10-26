"""AnotherAuctionSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from auctionApp.account_management import EditUser, AddUser, ChangeCurrency
from auctionApp.auction_add import AddAuction
from auctionApp.auction_bid import BidAuction
from auctionApp.auction_edit import EditAuction
from auctionApp.auctions_browse import BrowseAuctions
from auctionApp.login import Login, Logout
from auctionApp.views import home, Search, BanAuction, ListBanned

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', home,),
    path('home/', home, name = 'home'),
    path('auctions/', BrowseAuctions.as_view(), name='auctions'),
    path('auctions/<int:number>', BrowseAuctions.fetch_auction, name='auctionFetch'),
    path('auctions/add/', AddAuction.as_view(), name='auctionAdd'),
    path('auctions/edit/', BrowseAuctions.as_view(), name='auctionEdit'),
    path('auctions/edit/<slug:query>', EditAuction.as_view(), name='auctionEdit'),
    path('auctions/bid/', BidAuction.as_view(), name='auctionBid'),
    path('auctions/bid/<int:number>', BidAuction.as_view(), name='auctionBid'),
    path('search/', Search.as_view(), name='search'),
    path('search/<slug:query>', Search.as_view, name='search'),
    path('signup/', AddUser.as_view(), name='signup'),
    path('edit_account/', EditUser.as_view(), name='edit_account'),
    path('change_currency/', ChangeCurrency.as_view(), name='change_currency'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('admin_task/', BanAuction.as_view(), name='ban_auction'),
    path('admin_task/ban/<int:number>', BanAuction.as_view(), name='auctionBan'),
    path('admin_task/list_banned/', ListBanned.as_view(), name='auctionListBanned'),
]
