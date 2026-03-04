"""餐厅列表与菜单展示"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST
from .models import Restaurant, Dish


@require_GET
def restaurant_list(request):
    """餐厅列表"""
    restaurants = Restaurant.objects.filter(is_active=True)
    return render(request, 'restaurants/list.html', {'restaurants': restaurants})


@require_GET
def restaurant_menu(request, slug):
    """餐厅详情与菜单，支持加购"""
    restaurant = get_object_or_404(Restaurant, slug=slug, is_active=True)
    dishes = restaurant.dishes.filter(is_available=True)
    return render(request, 'restaurants/menu.html', {
        'restaurant': restaurant,
        'dishes': dishes,
    })
