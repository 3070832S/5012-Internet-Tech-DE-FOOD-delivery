"""carts 应用 URL 配置（购物车 M3）"""
from django.urls import path
from django.views.generic import TemplateView

app_name = 'carts'

urlpatterns = [
    path('', TemplateView.as_view(template_name='carts/cart.html'), name='cart'),
]
