from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate
from django.contrib import messages
from .models import Menu, Order, User, OrderCount
from django.utils import timezone


def generateOrderNo():
    orders = OrderCount.objects.all()

    order_number = {0}
    for item in orders:
        order_number.add(item.order_number)

    return max(order_number)+1


def addToList(request):
    item = request.POST.get('item')
    quantity = int(request.POST.get('quantity'))
    name = [o.item_name for o in Menu.objects.filter(id=int(item))]
    price = [o.price for o in Menu.objects.filter(id=int(item))]

    my_orders = request.session.get('my_orders')

    order_number = request.session.get('order_number')
    if order_number:
        pass
    else:
        order_number = generateOrderNo()
    request.session["order_number"] = order_number
    if my_orders:
        check_item = my_orders.get(name[0])
        if check_item:
            my_orders[name[0]] = [{"quantity": check_item[0]['quantity'] + quantity, "price": price[0], "update": True}]
        else:
            my_orders[name[0]] = [{"quantity": quantity, "price": price[0]}]

    else:
        my_orders = {name[0]: [{"quantity": quantity, "price": price[0]}]}

    request.session['my_orders'] = my_orders


def createFlag(request):
    my_orders = request.session.get("my_orders")
    order_number = request.session.get('order_number')

    orders_placed = Order.objects.filter(order_number=order_number)
    for item in orders_placed:
        print(item.item)
        for data in my_orders:
            if str(item.item) == data:
                my_orders[str(item.item)][0]["flag"] = 1


# this view is for menu page
def food(request):
    context = {
        "title": "Menu-Food",
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
    if request.method == 'POST':
        addToList(request)
        return redirect('cust-food')
    else:
        # this is for get request

        return render(request, 'customer/menu_page.html', context)


def drink(request):
    if request.method == 'POST':
        addToList(request)
        return redirect('cust-drink')
    else:
        # this is for get request
        context = {
            "title": "Menu-Drink",
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
        addToList(request)
        return redirect('cust-dessert')
    else:
        context = {
            "title": "Menu-Dessert",
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


def saveOrderCount(request):
    """Saving an order number with other default values"""
    order_count = OrderCount.objects.filter(order_number=request.session.get("order_number"))
    if order_count:
        pass
    else:
        order_num = OrderCount(order_number=request.session.get("order_number"))
        order_num.save()


# this view is for my orders page
def myOrders(request):
    createFlag(request)
    my_orders = request.session.get('my_orders')
    if request.method == "POST":
        user_id = request.session.get('_auth_user_id')
        username = User.objects.get(id=user_id)

        saveOrderCount(request)
        order_num = OrderCount.objects.get(order_number=request.session.get("order_number"))

        for order in my_orders:
            flag = my_orders[order][0].get("flag")
            update = my_orders[order][0].get("update")

            item_name = Menu.objects.get(item_name=order)
            if update:
                menu_id = Menu.objects.filter(item_name=order)[0].id
                Order.objects.filter(item=menu_id
                                     ).filter(order_number=request.session.get("order_number")
                                              ).update(quantity=my_orders[order][0]["quantity"])
            if flag == 1:
                pass
            else:
                print(Menu.objects.filter(item_name=order)[0].item_name)
                order_obj = Order(item=item_name,
                                  user=username,
                                  quantity=my_orders[order][0]["quantity"],
                                  order_number=order_num)
                order_obj.save()
        updateOrderCount(request)
    if my_orders:
        context = {
            "title": "My Orders",
            "my_orders": [my_orders]
        }
    else:
        context = {"title": "My Orders"}
    return render(request, 'customer/myOrders.html', context)


def createOrdersList(request):
    orders = [o for o in Order.objects.filter(order_number=request.session.get("order_number"))]

    orders_details = {}
    for arg in orders:
        orders_details[arg.id] = {'id': arg.id, 'item': arg.item.item_name, 'quantity': arg.quantity,
                                  'price': arg.item.price, 'status': arg.order_status, 'username': arg.user.username,
                                  'total': arg.quantity * arg.item.price}

    orders_list = []
    for items in orders_details:
        if orders_details[items]['status'] == 'in process' or orders_details[items]['status'] == 'delivered':
            orders_list.append(orders_details[items])

    return orders_list


# this view is for bill page
def bill(request):
    orders_list = createOrdersList(request)
    order_count = OrderCount.objects.filter(order_number=request.session.get("order_number"))
    if order_count:
        context = {"title": "Your bill",
                   "orders": orders_list,
                   "VAT": order_count[0].VAT,
                   "SC": order_count[0].SC,
                   "Amt": order_count[0].amt_to_pay}
    else:
        context = {"title": "Your Bill",
                   "VAT": 0,
                   "SC": 0,
                   "Amt": 0}

    return render(request, 'customer/bill.html', context)


def updateOrderCount(request):
    orders_list = createOrdersList(request)

    # to calculate VAT, service charge and amount to pay
    count_orders = 0
    VAT = 0
    SC = 0
    total_amt = 0
    for data in orders_list:
        count_orders += 1
        VAT += round((0.13 * data["total"]), 2)
        SC += round(0.1 * data["total"], 2)
        total_amt += data["total"]
    amt_to_pay = total_amt + VAT + SC

    # to update OrderCount model
    OrderCount.objects.filter(order_number=request.session.get("order_number")).update(
        total=total_amt,
        VAT=VAT,
        SC=SC,
        amt_to_pay=amt_to_pay,
        date_ordered=timezone.now(),
        total_orders_placed=float(count_orders))


# this view is for logout page
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('login')

