from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Experience, Table, Reservations
from customer.models import Menu
import datetime


# Create your views here.

# this view is for home page
def home(request):
    return render(request=request, template_name='main/home_page.html', context={'title': 'Home'})


def eat_food(request):
    context = {
        'title': 'Home-Food',
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
    return render(request=request, template_name='main/eat_food_page.html', context=context)


def eat_dessert(request):
    context = {
        "title": "Home-Dessert",
        "dessert": [
                {
                    'name': 'Dessert',
                    'item': Menu.objects.filter(item_type__item_type='Dessert Type'),
                    "heading_id": "headingOne",
                    "collapse_id": "collapseOne"
                }
                ]
    }
    return render(request=request, template_name='main/eat_dessert_page.html', context=context)


def drink(request):
    context = {
        "title": "Home-Drink",
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
    return render(request=request, template_name='main/drink_page.html', context=context)


# this view is for about page
def about(request):
    context = {
        "photo": [data for data in Experience.objects.all()],
        "title": 'About Us',
    }
    return render(request, 'main/about.html', context)


def reservation(request):
    if request.method == 'POST':
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        phone = request.POST.get("phone")
        seats = request.POST.get("seats")
        date = request.POST.get("date")
        my_reservation = {"fname": fname, "lname": lname, "phone": phone, "seats": seats, "date": date}
        request.session["reservation"] = my_reservation
        return redirect("book")

    data = request.session.get("reservation")
    if data is not None:
        date = data.get("date")
    else:
        data = {}
        date = ""
    if date == "":
        data["date"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

    context = {
        "title": 'Reservation',
        "data": data,
    }
    return render(request, 'main/reservation.html', context)


def bookTable(request):
    data = request.session.get("reservation")
    date_time = data["date"].replace("T", " ")
    data["date"] = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M")

    if request.method == "POST":
        name = request.POST.get("table_name")
        table_name = Table.objects.get(table_name=name)
        reserve_obj = Reservations(table_name=table_name,
                                   first_name=data["fname"],
                                   last_name=data["lname"],
                                   user_contact=data["phone"],
                                   registration_date=data["date"],
                                   no_of_seats=data["seats"])
        reserve_obj.save()
        messages.success(request, "Yay! Table has been booked")

        return redirect("reserv")

    one_hour_before = data["date"] - datetime.timedelta(minutes=60)
    one_hour_after = data["date"] + datetime.timedelta(minutes=60)

    tables = [table for table in Table.objects.filter(capacity__gte=data["seats"])]
    reserved_tables = Reservations.objects.filter(
        registration_date__gte=one_hour_before).filter(
        registration_date__lte=one_hour_after)
    for item in reserved_tables:
        tables.remove(item.table_name)

    context = {
        "title": 'Reservation-Book Table',
        "tables": tables,
        "data": data
    }
    return render(request, 'main/book_table.html', context)


# this view is for login page
def signIn(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                check_staff = User.objects.filter(is_staff=0)
                if user in check_staff:
                    messages.success(request, f'Logged in as {username}!')
                    return redirect('cust-food')
                else:
                    messages.success(request, f'Logged in as {username}!')
                    return redirect('suv-orders')
        else:
            messages.warning(request, "Invalid username or password")
            return redirect('/login')
    context = {"title": 'Sign In'}

    return render(request, 'main/sign_up.html', context)




