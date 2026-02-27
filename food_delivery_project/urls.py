"""
URL configuration for food_delivery_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Test pages
    path('test/', TemplateView.as_view(template_name='test.html'), name='test'),
    
    # Auth pages (temporary direct routes, will be replaced by app routes later)
    path('accounts/login/', TemplateView.as_view(template_name='accounts/login.html'), name='login'),
    
    # Restaurant pages
    path('restaurants/list/', TemplateView.as_view(template_name='restaurants/list.html'), name='restaurant_list'),
    
    # Cart pages
    path('cart/', TemplateView.as_view(template_name='carts/cart.html'), name='cart'),
    
    # Order pages
    path('orders/checkout/', TemplateView.as_view(template_name='orders/checkout.html'), name='checkout'),
    path('orders/status/', TemplateView.as_view(template_name='orders/status.html'), name='order_status'),
    path('orders/history/', TemplateView.as_view(template_name='orders/history.html'), name='order_history'),
    path('orders/detail/', TemplateView.as_view(template_name='orders/detail.html'), name='order_detail'),
    
    # Merchant pages
    path('merchants/dashboard/', TemplateView.as_view(template_name='merchants/dashboard.html'), name='merchant_dashboard'),
    
    # Review pages
    path('reviews/list/', TemplateView.as_view(template_name='reviews/list.html'), name='review_list'),
    path('reviews/favorites/', TemplateView.as_view(template_name='reviews/favorites.html'), name='favorites'),
    
    # Future app routes (commented until backend is ready)
    # User authentication (from PPT Page 8)
    # path('accounts/', include('accounts.urls')),
    
    # Shopping cart (from PPT Page 8)
    # path('carts/', include('carts.urls')),
    
    # Restaurants and menu (from PPT Page 8)
    # path('restaurants/', include('restaurants.urls')),
    
    # Orders management (from PPT Page 8)
    # path('orders/', include('orders.urls')),
    
    # Merchant app routes (commented until backend is ready)
    # path('merchants/', include('merchants.urls')),
    
    # Review app routes (commented until backend is ready)
    # path('reviews/', include('reviews.urls')),
]
