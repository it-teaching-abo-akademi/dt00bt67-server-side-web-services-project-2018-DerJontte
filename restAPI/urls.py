from django.urls import path, include
from restAPI import views

urlpatterns = [
    path('auctions/', views.auction_list),
    path('auctions/<int:number>', views.auction_detail),
    path('auctions/search=<slug:query>', views.auction_search),
]
