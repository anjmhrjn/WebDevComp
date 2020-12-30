from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from customer.models import Order, Menu


# Create your views here.
def orders(request):
    context = {
        "myOrders": Order.objects.all(),
    }
    return render(request, 'supervisor/orders.html', context)


def order_by(request):
    status = request.POST.get('status')
    if status == "Delivered":
        context = {
            "myOrders": Order.objects.filter(order_status='Delivered')
        }

    elif status == "Cancelled":
        context = {
            "myOrders": Order.objects.filter(order_status="Cancelled")
        }
    elif status == "In Process":
        context = {
            "myOrders": Order.objects.filter(order_status="In Process")
        }
    else:
        context = {}
    return render(request, 'supervisor/orders.html', context)


def sold_items(request):
    return render(request, 'supervisor/items_sold.html')


def profile(request):
    return render(request, 'supervisor/profile.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('login')
