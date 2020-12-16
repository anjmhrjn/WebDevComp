from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from .models import Menu, Order, User


# Create your views here.
# this view is for menu page
def food(request):
    if request.method == 'POST':
        # form = AuthenticationForm(request, data=int(request.POST))
        # print(form)
        return render(request, 'customer/drink.html')
    else:
        # this is for get request
        context = {
            "food": [
                {
                    'name': 'Breakfast',
                    'item': Menu.objects.filter(item_type__item_type='Breakfast'),
                    "heading_id": "headingOne",
                    "collapse_id": "collapseOne"
                },
                {
                    'name': 'Lunch',
                    'item': Menu.objects.filter(item_type__item_type='Lunch'),
                    "heading_id": "headingTwo",
                    "collapse_id": "collapseTwo"
                },
                {
                    'name': 'Dinner',
                    'item': Menu.objects.filter(item_type__item_type='Dinner'),
                    "heading_id": "headingThree",
                    "collapse_id": "collapseThree"
                }
            ]
        }
        return render(request, 'customer/menu_page.html', context)


def drink(request):
    if request.method == 'POST':
        # form = AuthenticationForm(request, data=int(request.POST))
        # print(form)
        return render(request, 'customer/drink.html')
    else:
        # this is for get request
        context = {
            "drink": [
                {
                    'name': 'Soft Drink',
                    'item': Menu.objects.filter(item_type__item_type='Soft Drink'),
                    "heading_id": "headingOne",
                    "collapse_id": "collapseOne"
                },
                {
                    'name': 'Cold Drink',
                    'item': Menu.objects.filter(item_type__item_type='Cold Drink'),
                    "heading_id": "headingTwo",
                    "collapse_id": "collapseTwo"
                },
                {
                    'name': 'Hard Drink',
                    'item': Menu.objects.filter(item_type__item_type='Hard Drink'),
                    "heading_id": "headingThree",
                    "collapse_id": "collapseThree"
                },
                {
                    'name': 'Wine',
                    'item': Menu.objects.filter(item_type__item_type='Wine'),
                    "heading_id": "headingFour",
                    "collapse_id": "collapseFour"
                }
            ]

        }
        return render(request, 'customer/drink.html', context)


def dessert(request):
    if request.method == "POST":
        return render(request, 'customer/dessert.html')
    else:
        context = {
            "dessert": [
                {
                    'name': 'Dessert',
                    'item': Menu.objects.filter(item_type__item_type='Dessert Type'),
                    "heading_id": "headingOne",
                    "collapse_id": "collapseOne"
                }
                ]
        }
        return render(request, 'customer/dessert.html', context)


# this view is for my orders page
def myOrders(request):
    context = {
        "myOrders": Order.objects.all(),
    }
    return render(request, 'customer/myOrders.html', context)


# this view is for bill page
def bill(request):
    users = [o.user for o in Order.objects.filter(order_status='in process')]
    orders = [o for o in Order.objects.all()]
    print(orders)

    orders_details = {}
    for arg in orders:
        orders_details[arg.id] = {'item': arg.item.item_name, 'quantity': arg.quantity, 'price': arg.item.price,
                         'status': arg.order_status, 'user': arg.user.username, 'total': (arg.quantity)*(arg.item.price)}

    context = {}
    for key, value in orders_details.items():
        if orders_details[key] == value:
            if orders_details[key]['user'] == 'Table2' and (orders_details[key]['status'] == 'delivered' or orders_details[key]['status'] == 'in process'):
                context[key] = orders_details[key]
    print(context)
    # userid = [u.id for u in users]
    # username = {}
    # for id in userid:
    #     username[id] = User.objects.filter(id=id)
    # print(username)
    #
    # context = {}
    # for user in userid:
    #     context[user] = Order.objects.filter(user=user)
    # print(context)

    menu = Menu.objects.all()
    orders = Order.objects.all()

    # context = {'id': orders.id, 'item': orders.item, 'qty': }

    return render(request, 'customer/bill.html')


# this view is fro logout page
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('login')


def test(request):
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
    return render(request, 'customer/myOrders.html', context)
