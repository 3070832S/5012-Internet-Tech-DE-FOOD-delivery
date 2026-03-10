"""Order and order item models."""
from decimal import Decimal
from django.db import models
from django.conf import settings


class Order(models.Model):
    """Order."""
    STATUS_PENDING = 'pending'
    STATUS_PREPARING = 'preparing'
    STATUS_DELIVERING = 'delivering'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PREPARING, 'Preparing'),
        (STATUS_DELIVERING, 'Delivering'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    order_no = models.CharField('Order no.', max_length=32, unique=True, db_index=True)
    recipient_name = models.CharField('Recipient', max_length=50)
    phone = models.CharField('Phone', max_length=20)
    address_line = models.CharField('Address', max_length=200)
    city = models.CharField('City', max_length=50, default='')
    postcode = models.CharField('Postcode', max_length=20, blank=True)

    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    note = models.TextField('Order note', blank=True)

    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=Decimal('0'))
    delivery_fee = models.DecimalField('Delivery fee', max_digits=10, decimal_places=2, default=Decimal('0'))
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=Decimal('0'))

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_no} ({self.get_status_display()})"

    def can_cancel(self):
        return self.status == self.STATUS_PENDING


class OrderItem(models.Model):
    """Order item: dish snapshot."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish_name = models.CharField('Dish name', max_length=100)
    quantity = models.PositiveIntegerField('Quantity')
    unit_price = models.DecimalField('Unit price', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Order item'
        verbose_name_plural = verbose_name

    @property
    def line_total(self):
        return self.quantity * self.unit_price
