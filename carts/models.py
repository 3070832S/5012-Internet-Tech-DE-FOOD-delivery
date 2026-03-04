"""购物车模型：支持登录用户持久化与匿名用户 session"""
from decimal import Decimal
from django.db import models
from django.conf import settings


class Cart(models.Model):
    """购物车：user 与 session_key 二选一"""
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
        verbose_name = '购物车'
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
    """购物车项：菜品、数量、加入时单价快照"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(
        'restaurants.Dish',
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField('数量', default=1)
    unit_price = models.DecimalField('单价', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = '购物车项'
        verbose_name_plural = verbose_name
        unique_together = [('cart', 'dish')]

    @property
    def line_total(self):
        return self.quantity * self.unit_price
