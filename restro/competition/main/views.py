from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.

# this view is for home page
def home(request):
    return render(request=request, template_name='main/home.html', context={'title': 'Home'})


# this view is for about page
def about(request):
    return render(request, 'main/about.html')


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




