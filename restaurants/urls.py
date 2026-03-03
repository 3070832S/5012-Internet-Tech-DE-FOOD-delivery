"""restaurants 应用 URL 配置（餐厅与菜单 M2）"""
from django.urls import path
from django.views.generic import TemplateView

app_name = 'restaurants'

urlpatterns = [
    path('', TemplateView.as_view(template_name='restaurants/list.html'), name='index'),
    path('list/', TemplateView.as_view(template_name='restaurants/list.html'), name='restaurant_list'),
]
