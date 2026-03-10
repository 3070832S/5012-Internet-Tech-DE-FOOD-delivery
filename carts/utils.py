"""Cart get/create and merge after login."""
from .models import Cart, CartItem


def get_or_create_cart(request):
    """Get or create cart for current user or session."""
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
    """Merge session cart into user cart after login."""
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
