"""Checkout flow and order management."""
import random
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from carts.utils import get_or_create_cart
from accounts.models import UserAddress
from .models import Order, OrderItem


@require_GET
@login_required(login_url='/accounts/login/')
def order_list(request):
    """Order list."""
    orders = request.user.orders.all()
    return render(request, 'orders/history.html', {'orders': orders})


@require_GET
@login_required(login_url='/accounts/login/')
def order_detail(request, pk):
    """Order detail."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})


def _generate_order_no():
    return f"FD-{timezone.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"


@require_GET
@login_required(login_url='/accounts/login/')
def checkout(request):
    """Checkout: confirm cart, select address, note, show total."""
    cart = get_or_create_cart(request)
    items = list(cart.items.select_related('dish', 'dish__restaurant').all())
    if not items:
        messages.warning(request, 'Your cart is empty. Add items first.')
        return redirect('carts:cart')
    addresses = request.user.addresses.all()
    subtotal = cart.subtotal
    delivery_fee = items[0].dish.restaurant.delivery_fee if items else Decimal('0')
    total = subtotal + delivery_fee
    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'items': items,
        'addresses': addresses,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total': total,
    })


@require_POST
@login_required(login_url='/accounts/login/')
def place_order(request):
    """Place order: address, note, compute total and create order."""
    cart = get_or_create_cart(request)
    items = list(cart.items.select_related('dish', 'dish__restaurant').all())
    if not items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('carts:cart')

    address_id = request.POST.get('address_id')
    if not address_id:
        messages.error(request, 'Please select a delivery address.')
        return redirect('orders:checkout')
    address = get_object_or_404(UserAddress, pk=address_id, user=request.user)

    note = (request.POST.get('note') or '').strip()
    subtotal = cart.subtotal
    delivery_fee = items[0].dish.restaurant.delivery_fee if items else Decimal('0')
    total = subtotal + delivery_fee

    order_no = _generate_order_no()
    order = Order.objects.create(
        user=request.user,
        order_no=order_no,
        recipient_name=address.recipient_name,
        phone=address.phone,
        address_line=address.address_line,
        city=address.city,
        postcode=address.postcode,
        status=Order.STATUS_PENDING,
        note=note,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        total=total,
    )
    for cart_item in items:
        OrderItem.objects.create(
            order=order,
            dish_name=cart_item.dish.name,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
        )
    cart.items.all().delete()
    messages.success(request, f'Order {order_no} placed.')
    return redirect('orders:detail', pk=order.pk)


@require_POST
@login_required(login_url='/accounts/login/')
def cancel_order(request, pk):
    """Cancel order (only when pending)."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if not order.can_cancel():
        messages.error(request, 'This order cannot be cancelled.')
        return redirect('orders:detail', pk=pk)
    order.status = Order.STATUS_CANCELLED
    order.save(update_fields=['status', 'updated_at'])
    messages.success(request, 'Order cancelled.')
    return redirect('orders:detail', pk=pk)
