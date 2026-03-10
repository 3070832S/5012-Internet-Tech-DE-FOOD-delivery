"""Carts app URL config (shopping cart M3)."""
from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart_detail, name='cart'),
    path('add/<int:dish_id>/', views.add_to_cart, name='add'),
    path('item/<int:item_id>/update/', views.update_quantity, name='update_quantity'),
    path('item/<int:item_id>/remove/', views.remove_item, name='remove_item'),
    path('clear/', views.clear_cart, name='clear'),
]
