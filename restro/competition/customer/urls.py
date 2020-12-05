from django.urls import path
from . import views     # importing views of customer app


# defining paths for customer app
urlpatterns = [
    path('', views.menu, name='cust-menu'),
    path('myOrders/', views.myOrders, name='cust-orders'),
    path('bill/', views.bill, name='cust-bill'),
]