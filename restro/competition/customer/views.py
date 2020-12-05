from django.shortcuts import render


# Create your views here.

# this view is for menu page
def menu(request):
    return render(request, 'customer/menu.html')


# this view is for my orders page
def myOrders(request):
    return render(request, 'customer/myOrders.html')


# this view is for bill page
def bill(request):
    return render(request, 'customer/bill.html')