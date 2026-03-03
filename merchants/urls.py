"""merchants 应用 URL 配置（商家管理 C2）"""
from django.urls import path
from django.views.generic import TemplateView

app_name = 'merchants'

urlpatterns = [
    path('dashboard/', TemplateView.as_view(template_name='merchants/dashboard.html'), name='merchant_dashboard'),
]
