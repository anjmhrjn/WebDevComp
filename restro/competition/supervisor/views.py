from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from customer.models import Order, Menu, OrderCount
from main.models import Reservations
import datetime


# Create your views here.
def orders(request):
    context = {
        "myOrders": sortOrders([o for o in Order.objects.all()]),
        "title": "Orders",
    }
    return render(request, 'supervisor/orders.html', context)


def sortOrders(data):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(data) - 1):
            if data[i].order_number.order_number < data[i+1].order_number.order_number:
                data[i], data[i+1] = data[i+1], data[i]
                swapped = True
    return data


def changeStatus(request):
    order_id = request.GET.get("order_id")
    order_status = request.GET.get("status")
    Order.objects.filter(id=order_id).update(order_status=order_status)
    messages.success(request, f'Status changed to {order_status}')
    return redirect('suv-orders')


def order_by(request):
    context = {
        "title": "Orders",
    }
    status = request.POST.get('status')
    if status == "Delivered":
        context["myOrders"] = Order.objects.filter(order_status='Delivered')

    elif status == "Cancelled":
        context["myOrders"] = Order.objects.filter(order_status="Cancelled")

    elif status == "In Process":
        context["myOrders"] = Order.objects.filter(order_status="In Process")

    elif status == "Processed":
        context["myOrders"] = Order.objects.filter(order_status="Processed")

    else:
        context["myOrders"] = None

    return render(request, 'supervisor/orders.html', context)


def search(items, search_data):
    menu = {}
    for item in items:
        if search_data.upper() in item.upper():
            menu[item] = items[item]
    return menu


def sold_items(request):
    menu = {}
    for data in Menu.objects.all():
        menu[data.item_name] = {"name": data.item_name, "stock": data.stock}
        if menu[data.item_name]["stock"] <= 0:
            menu[data.item_name]["status"] = "Sold Out"
        else:
            menu[data.item_name]["status"] = "Available"
    current_date = datetime.datetime.now().date()

    week_before = current_date - datetime.timedelta(days=7)

    filtered_orders = Order.objects.filter(date_ordered__gte=week_before).filter(date_ordered__lte=current_date)
    for kwarg in filtered_orders:
        check = menu[kwarg.item.item_name].get("quantity")
        if check:
            menu[kwarg.item.item_name]["quantity"] += kwarg.quantity
        else:
            menu[kwarg.item.item_name]["quantity"] = kwarg.quantity

    search_data = request.GET.get("item_name")
    if search_data:
        menu = search(menu, search_data)

    context = {
        "orders": menu,
        "title": "Items Sold",
        "start_date": week_before,
        "end_date": current_date,
    }

    return render(request, 'supervisor/items_sold.html', context)


def searchBill(request):
    context = {
        "date_today": datetime.datetime.now().strftime("%Y-%m-%d"),
        "title": "Sales",
    }

    table_name = request.GET.get('table_value')
    date = request.GET.get('date')
    filtered_orders = []
    order_filter = [o.order_number for o in Order.objects.filter(user__username=table_name)]

    for orders_placed in order_filter:
        if orders_placed.date_ordered.date().strftime("%Y-%m-%d") == date:
            filtered_orders.append(orders_placed)
    if len(filtered_orders) > 0:
        sets_of_orders = set(filtered_orders)
        final_orders = {}
        for data in sets_of_orders:
            final_orders[data] = [{o: {"price": o.item.price, "total": o.quantity*o.item.price}} for o in Order.objects.filter(order_number=data)]

        context["orders"] = final_orders

    return render(request, 'supervisor/search_bill.html', context)


def searchReservation(record, search_data):
    result = []
    for item in record:
        if item.first_name.upper() == search_data.upper():
            result.append(item)
    return result


def showReservations(request):
    date_now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

    reservations = [r for r in Reservations.objects.filter(registration_date__gte=datetime.datetime.now())]

    fname = request.GET.get("fname")
    if fname is not None:
        search_date = request.GET.get("date")
        date_time = search_date.replace("T", " ")
        search_date = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        filtered_reservations = Reservations.objects.filter(registration_date__gte=search_date.date())
        reservations = searchReservation(filtered_reservations, fname)

    context = {
        "title": "Reservations",
        "date": date_now,
        "reservations": reservations
    }

    return render(request, "supervisor/reservations.html", context)


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('login')
