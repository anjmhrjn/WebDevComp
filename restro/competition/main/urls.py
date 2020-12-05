from django.urls import path
from . import views     # importing views of main app


# defining paths for main app
urlpatterns = [
    path('', views.home, name='restro-home'),
    path('about/', views.about, name='restro-about'),
    path('login/', views.signIn, name='restro-login'),
]