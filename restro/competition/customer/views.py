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
            my_orders[name[0]] = {"quantity": check_item['quantity'] + quantity, "price": price[0], "update": True,
                                  "stock": False, "updated_quantity": quantity}
        else:
            my_orders[name[0]] = {"quantity": quantity, "price": price[0], "stock": False}

    else:
        my_orders = {name[0]: {"quantity": quantity, "price": price[0], "stock": False}}

    request.session['my_orders'] = my_orders
    messages.success(request, 'Item successfully added!')


def createFlag(request):
    my_orders = request.session.get("my_orders")
    orders_placed = Order.objects.filter(order_number__order_number=request.session.get("order_number"))

    for item in orders_placed:
        for data in my_orders:
            if str(item.item) == data:
                my_orders[str(item.item)]["flag"] = 1


def saveOrderCount(request):
    """Saving an order number with other default values"""
    order_count = OrderCount.objects.filter(order_number=request.session.get("order_number"))
    if order_count:
        pass
    else:
        order_num = OrderCount(order_number=request.session.get("order_number"))
        order_num.save()


def createOrdersList(request):
    orders = [o for o in Order.objects.filter(order_number__order_number=request.session.get("order_number"))]

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


def updateMenuStock(request):
    my_orders = request.session.get("my_orders")
    for key in my_orders:
        update_flag = my_orders[key].get("stock")
        updated_value = my_orders[key].get("updated_quantity")
        if not update_flag:
            present_stock = Menu.objects.get(item_name=key)
            if updated_value:
                updated_stock = present_stock.stock - my_orders[key]["updated_quantity"]
            else:
                updated_stock = present_stock.stock-my_orders[key]["quantity"]
            Menu.objects.filter(item_name=key).update(stock=updated_stock)
            my_orders[key]["stock"] = True
    request.session["my_orders"] = my_orders


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


def remove(request):
    item_name = request.GET.get("item_name")
    my_orders = request.session.get("my_orders")
    for key, value in request.session.get("my_orders").items():
        if item_name == key:
            to_update = my_orders[key].get("update")
            if to_update:
                my_orders[key]["quantity"] = my_orders[key]["quantity"] - my_orders[key]["updated_quantity"]
                del my_orders[key]["update"]
                del my_orders[key]["updated_quantity"]
            else:
                del my_orders[key]
            break
    request.session["my_orders"] = my_orders
    messages.warning(request, 'Item removed!')

    return redirect('cust-orders')


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


# this view is for my orders page
def myOrders(request):
    my_orders = request.session.get('my_orders')
    if request.method == "POST":
        if my_orders:

            user_id = request.session.get('_auth_user_id')
            username = User.objects.get(id=user_id)

            saveOrderCount(request)
            createFlag(request)
            order_num = OrderCount.objects.get(order_number=request.session.get("order_number"))

            for order, order_values in my_orders.items():

                flag = order_values.get("flag")
                update = order_values.get("update")
                item_name = Menu.objects.get(item_name=order)

                if update:
                    uq = [
                        uq.updated_quantity for uq in Order.objects.filter(item__item_name=order
                                                                           ).filter(
                            order_number__order_number=request.session.get("order_number")
                        )
                    ]
                    if uq[0] is None:
                        uq[0] = str(order_values["updated_quantity"])
                    else:
                        uq[0] += "+" + str(order_values["updated_quantity"])
                    Order.objects.filter(item__item_name=order,
                                         ).filter(order_number__order_number=request.session.get("order_number")
                                                  ).update(quantity=order_values["quantity"],
                                                           updated_quantity=uq[0])
                    if my_orders[order].get("saved"):
                        pass
                    else:
                        my_orders[order]["saved"] = True
                if flag == 1:
                    if my_orders[order].get("saved"):
                        pass
                    else:
                        my_orders[order]["saved"] = True
                else:

                    order_obj = Order(item=item_name,
                                      user=username,
                                      quantity=order_values["quantity"],
                                      order_number=order_num)
                    order_obj.save()

                    if my_orders[order].get("saved"):
                        pass
                    else:
                        my_orders[order]["saved"] = True

            updateOrderCount(request)
            updateMenuStock(request)
            request.session["my_orders"] = my_orders
            messages.success(request, 'Yay! Order confirmed!')

    if my_orders:
        context = {
            "title": "My Orders",
            "my_orders": [my_orders]
        }
    else:
        context = {"title": "My Orders"}
    return render(request, 'customer/myOrders.html', context)


# this view is for bill page
def bill(request):
    if request.method == "POST":

        Order.objects.filter(
                            order_number__order_number=request.session.get("order_number")
                            ).update(
                                    order_status="processed"
                                    )
        if request.session.get("order_number"):
            del request.session["order_number"]
        if request.session.get("my_orders"):
            del request.session["my_orders"]

    orders_list = createOrdersList(request)

    order_count = OrderCount.objects.filter(order_number=request.session.get("order_number"))

    if order_count:
        context = {"title": "Your bill",
                   "orders": orders_list,
                   "VAT": order_count[0].VAT,
                   "SC": order_count[0].SC,
                   "Amt": order_count[0].amt_to_pay}
    else:
        context = {"title": "Your bill",
                   "VAT": 0,
                   "SC": 0,
                   "Amt": 0}

    return render(request, 'customer/bill.html', context)


# this view is for logout page
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('login')

