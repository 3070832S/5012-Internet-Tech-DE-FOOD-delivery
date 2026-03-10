"""Orders app URL config (orders M4, M5)."""
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('place/', views.place_order, name='place_order'),
    path('history/', views.order_list, name='history'),
    path('<int:pk>/', views.order_detail, name='detail'),
    path('<int:pk>/cancel/', views.cancel_order, name='cancel'),
]
