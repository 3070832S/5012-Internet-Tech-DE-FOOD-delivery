"""Cart: view, add, update quantity, remove, clear."""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib import messages
from restaurants.models import Dish
from .models import CartItem
from .utils import get_or_create_cart


@require_GET
def cart_detail(request):
    """Cart page: items, subtotal, delivery fee, total."""
    cart = get_or_create_cart(request)
    from decimal import Decimal
    items = list(cart.items.select_related('dish', 'dish__restaurant').all())
    subtotal = cart.subtotal
    delivery_fee = items[0].dish.restaurant.delivery_fee if items else Decimal('0')
    total = subtotal + delivery_fee
    return render(request, 'carts/cart.html', {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total': total,
    })


@require_POST
def add_to_cart(request, dish_id):
    """Add dish to cart (quantity via POST, default 1)."""
    dish = get_object_or_404(Dish, pk=dish_id, is_available=True)
    quantity = max(1, int(request.POST.get('quantity', 1)))
    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        dish=dish,
        defaults={'quantity': quantity, 'unit_price': dish.price}
    )
    if not created:
        item.quantity += quantity
        item.save()
    messages.success(request, f'Added {dish.name} x{quantity}')
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or '/restaurants/'
    return redirect(next_url)


@require_POST
def update_quantity(request, item_id):
    """Update cart item quantity."""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', item.quantity))
    if quantity < 1:
        item.delete()
        messages.success(request, 'Removed from cart')
    else:
        item.quantity = quantity
        item.save()
        messages.success(request, 'Quantity updated')
    return redirect('carts:cart')


@require_POST
def remove_item(request, item_id):
    """Remove one item from cart."""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    messages.success(request, 'Removed')
    return redirect('carts:cart')


@require_POST
def clear_cart(request):
    """Clear cart."""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared')
    return redirect('carts:cart')
