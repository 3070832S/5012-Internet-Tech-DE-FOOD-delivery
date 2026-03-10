"""Restaurants app URL config (restaurant and menu M2)."""
from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.restaurant_list, name='index'),
    path('list/', views.restaurant_list, name='restaurant_list'),
    path('<slug:slug>/', views.restaurant_menu, name='menu'),
]
