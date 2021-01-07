from django.urls import path
from . import views     # importing views of main app
from django.contrib.auth import views as auth_views


# defining paths for main app
urlpatterns = [
    path('', views.home, name='restro-home'),
    path('about/', views.about, name='restro-about'),
    path('eat/', views.eat_food, name='food'),
    path('dessert/', views.eat_dessert, name='food'),
    path('drink/', views.drink, name='food'),
    path('reservation/', views.reservation, name='reserv'),
    path('book/', views.bookTable, name='book'),
    path('login/', views.signIn, name='login'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="main/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="main/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="main/password_reset_change.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="main/password_reset_done.html"),
         name="password_reset_complete"),
]