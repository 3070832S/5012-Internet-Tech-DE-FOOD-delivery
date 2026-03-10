"""Cart model: persistence for logged-in users, session for anonymous."""
from decimal import Decimal
from django.db import models
from django.conf import settings


class Cart(models.Model):
    """Cart: either user or session_key."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts',
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"Cart {self.pk} ({self.user or self.session_key})"

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(
            item.quantity * item.unit_price
            for item in self.items.select_related('dish').all()
        )


class CartItem(models.Model):
    """Cart item: dish, quantity, unit price at add time."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(
        'restaurants.Dish',
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField('Quantity', default=1)
    unit_price = models.DecimalField('Unit price', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Cart item'
        verbose_name_plural = verbose_name
        unique_together = [('cart', 'dish')]

    @property
    def line_total(self):
        return self.quantity * self.unit_price
