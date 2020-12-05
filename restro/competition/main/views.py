from django.shortcuts import render


# Create your views here.

# this view is for home page
def home(request):
    return render(request=request, template_name='main/home.html', context=None)


# this view is for about page
def about(request):
    return render(request, 'main/about.html')


# # this view is for login page
def signIn(request):
    return render(request, 'main/log.html')
