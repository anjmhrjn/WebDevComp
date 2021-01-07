from django.urls import path
from customer.views import logout_request
from . import views     # importing views of customer app


# defining paths for customer app
urlpatterns = [
    path('', views.orders, name='suv-orders'),
    path('sold/', views.sold_items, name='suv-sold'),
    path('status', views.order_by, name='status'),
    path('change/', views.changeStatus, name='change'),
    path('sales/', views.searchBill, name='search_bill'),
    path('resrv/', views.showReservations, name='reservation'),
    path('logout/', logout_request, name='logout'),
]