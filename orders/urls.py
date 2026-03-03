"""orders 应用 URL 配置（订单 M4, M5）"""
from django.urls import path
from django.views.generic import TemplateView

app_name = 'orders'

urlpatterns = [
    path('', TemplateView.as_view(template_name='orders/history.html'), name='index'),
    path('checkout/', TemplateView.as_view(template_name='orders/checkout.html'), name='checkout'),
    path('status/', TemplateView.as_view(template_name='orders/status.html'), name='order_status'),
    path('history/', TemplateView.as_view(template_name='orders/history.html'), name='order_history'),
    path('detail/', TemplateView.as_view(template_name='orders/detail.html'), name='order_detail'),
]
