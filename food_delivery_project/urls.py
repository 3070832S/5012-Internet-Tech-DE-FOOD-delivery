"""
URL configuration for food_delivery_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 临时测试页面
    path('test/', TemplateView.as_view(template_name='test.html'), name='test'),
    
    # User authentication (from PPT Page 8)
    # path('accounts/', include('accounts.urls')),
    
    # Shopping cart (from PPT Page 8)
    # path('carts/', include('carts.urls')),
    
    # Restaurants and menu (from PPT Page 8)
    # path('restaurants/', include('restaurants.urls')),
    
    # Orders management (from PPT Page 8)
    # path('orders/', include('orders.urls')),
    
    # ❗ 需要组员确认：merchants/ 这个URL前缀对不对？（商家端）
    # path('merchants/', include('merchants.urls')),
    
    # ❗ 需要组员确认：reviews/ 这个URL前缀对不对？（评价收藏）
    # path('reviews/', include('reviews.urls')),
]