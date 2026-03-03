"""reviews 应用 URL 配置（评价与收藏 S1, S2, C1）"""
from django.urls import path
from django.views.generic import TemplateView

app_name = 'reviews'

urlpatterns = [
    path('list/', TemplateView.as_view(template_name='reviews/list.html'), name='review_list'),
    path('favorites/', TemplateView.as_view(template_name='reviews/favorites.html'), name='favorites'),
]
