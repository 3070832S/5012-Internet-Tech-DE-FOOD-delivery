"""下单流程与订单管理"""
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
    """订单列表"""
    orders = request.user.orders.all()
    return render(request, 'orders/history.html', {'orders': orders})


@require_GET
@login_required(login_url='/accounts/login/')
def order_detail(request, pk):
    """订单详情"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})


def _generate_order_no():
    return f"FD-{timezone.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"


@require_GET
@login_required(login_url='/accounts/login/')
def checkout(request):
    """结账页：确认购物车、选择地址、填写备注、显示总价"""
    cart = get_or_create_cart(request)
    items = list(cart.items.select_related('dish', 'dish__restaurant').all())
    if not items:
        messages.warning(request, '购物车为空，请先添加菜品。')
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
    """提交订单：地址、备注、计算总价并创建订单"""
    cart = get_or_create_cart(request)
    items = list(cart.items.select_related('dish', 'dish__restaurant').all())
    if not items:
        messages.warning(request, '购物车为空。')
        return redirect('carts:cart')

    address_id = request.POST.get('address_id')
    if not address_id:
        messages.error(request, '请选择收货地址。')
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
    messages.success(request, f'订单 {order_no} 已提交。')
    return redirect('orders:detail', pk=order.pk)


@require_POST
@login_required(login_url='/accounts/login/')
def cancel_order(request, pk):
    """取消订单（仅待处理时可取消）"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if not order.can_cancel():
        messages.error(request, '当前状态不可取消。')
        return redirect('orders:detail', pk=pk)
    order.status = Order.STATUS_CANCELLED
    order.save(update_fields=['status', 'updated_at'])
    messages.success(request, '订单已取消。')
    return redirect('orders:detail', pk=pk)
