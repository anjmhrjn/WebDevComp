from django.urls import path
from customer.views import logout_request
from . import views     # importing views of customer app


# defining paths for customer app
urlpatterns = [
    path('', views.orders, name='suv-orders'),
    path('sold/', views.sold_items, name='suv-sold'),
    path('profile/', views.profile, name='suv-profile'),
    path('status', views.order_by, name='test'),
    path('logout/', logout_request, name='logout'),
]