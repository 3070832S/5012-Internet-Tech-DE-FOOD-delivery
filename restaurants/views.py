"""Restaurant list and menu."""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST
from .models import Restaurant, Dish


@require_GET
def restaurant_list(request):
    """Restaurant list."""
    restaurants = Restaurant.objects.filter(is_active=True)
    return render(request, 'restaurants/list.html', {'restaurants': restaurants})


@require_GET
def restaurant_menu(request, slug):
    """Restaurant detail and menu with add to cart."""
    restaurant = get_object_or_404(Restaurant, slug=slug, is_active=True)
    dishes = restaurant.dishes.filter(is_available=True)
    return render(request, 'restaurants/menu.html', {
        'restaurant': restaurant,
        'dishes': dishes,
    })
