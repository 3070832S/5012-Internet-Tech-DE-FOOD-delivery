"""购物车获取与登录后合并"""
from .models import Cart, CartItem


def get_or_create_cart(request):
    """按当前用户或 session 获取/创建购物车"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(
            user=request.user,
            defaults={}
        )
        return cart
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(
        session_key=request.session.session_key,
        defaults={}
    )
    return cart


def merge_cart_after_login(request):
    """登录后将 session 购物车合并到用户购物车"""
    if not request.user.is_authenticated or not request.session.session_key:
        return
    session_cart = Cart.objects.filter(
        session_key=request.session.session_key
    ).first()
    if not session_cart or not session_cart.items.exists():
        return
    user_cart, _ = Cart.objects.get_or_create(
        user=request.user,
        defaults={}
    )
    for item in session_cart.items.select_related('dish').all():
        existing = user_cart.items.filter(dish=item.dish).first()
        if existing:
            existing.quantity += item.quantity
            existing.save()
        else:
            CartItem.objects.create(
                cart=user_cart,
                dish=item.dish,
                quantity=item.quantity,
                unit_price=item.unit_price
            )
    session_cart.items.all().delete()
    session_cart.delete()
