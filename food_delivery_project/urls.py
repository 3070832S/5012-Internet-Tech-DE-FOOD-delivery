"""
URL configuration for food_delivery_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # 临时测试页面
    path('restaurants/test/', TemplateView.as_view(template_name='restaurants/test.html'), name='test'),
]