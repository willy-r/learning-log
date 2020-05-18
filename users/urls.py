"""URL patterns for users app."""

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views


app_name = 'users'

urlpatterns = [
    # Ex: /users/login/
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html'),
         name='login'),

    # Ex: /users/logout/
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Ex: /users/password_change/
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='users/password_change.html',
             success_url=reverse_lazy('users:password_change_done')),
         name='password_change'),

    # Ex: /users/password_change_done/
    path('password_change_done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'),
         name='password_change_done'),

    # Ex: /users/register/
    path('register/', views.register, name='register'),
]
