"""Accounts app URL config (user auth M1)."""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('addresses/', views.address_list, name='address_list'),
    path('addresses/add/', views.address_add, name='address_add'),
    path('addresses/<int:pk>/edit/', views.address_edit, name='address_edit'),
    path('addresses/<int:pk>/delete/', views.address_delete, name='address_delete'),
    path('addresses/<int:pk>/set-default/', views.address_set_default, name='address_set_default'),
]
