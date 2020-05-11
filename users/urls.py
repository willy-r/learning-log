"""URL patterns for users app."""

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'users'

urlpatterns = [
    # ex: /users/login/
    path(
        'login/', 
        auth_views.LoginView.as_view(template_name='users/login.html'),
        name='login',
    ),

    # ex: /users/logout/
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # ex: /users/register/
    path('register/', views.register, name='register'),
]

