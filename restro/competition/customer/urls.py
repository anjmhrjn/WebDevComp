from django.urls import path
from . import views     # importing views of customer app


# defining paths for customer app
urlpatterns = [
    path('', views.food, name='cust-food'),
    path('drink/', views.drink, name='cust-drink'),
    path('dessert/', views.dessert, name='cust-dessert'),
    path('myOrders/', views.myOrders, name='cust-orders'),
    path('bill/', views.bill, name='cust-bill'),
    path('logout/', views.logout_request, name='logout'),
]
