"""
URL configuration for food_delivery_project project.
后端路由按应用模块划分，详见 docs/ARCHITECTURE.md
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/restaurants/', permanent=False), name='home'),
    path('test/', TemplateView.as_view(template_name='test.html'), name='test'),
    # 各应用路由（Python/Django 后端架构）
    path('accounts/', include('accounts.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('cart/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    path('merchants/', include('merchants.urls')),
    path('reviews/', include('reviews.urls')),
]
