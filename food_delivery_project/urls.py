"""
URL configuration for food_delivery_project project.
后端路由按应用模块划分，详见 docs/ARCHITECTURE.md
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/restaurants/', permanent=False), name='home'),
    path('test/', TemplateView.as_view(template_name='test.html'), name='test'),
    path('accounts/', include('accounts.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('cart/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    path('merchants/', include('merchants.urls')),
    path('reviews/', include('reviews.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
