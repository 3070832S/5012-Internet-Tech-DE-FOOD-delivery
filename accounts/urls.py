"""accounts 应用 URL 配置（用户认证 M1）"""
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', TemplateView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', TemplateView.as_view(template_name='accounts/index.html'), name='register'),
    path('profile/', TemplateView.as_view(template_name='accounts/index.html'), name='profile'),
]
