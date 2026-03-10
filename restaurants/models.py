"""Restaurant and dish models."""
from decimal import Decimal
from django.db import models


class Restaurant(models.Model):
    """Restaurant."""
    name = models.CharField('Name', max_length=100)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    description = models.TextField('Description', blank=True)
    image = models.ImageField('Image', upload_to='restaurants/%Y/%m/', blank=True, null=True)
    min_order = models.DecimalField('Min order', max_digits=10, decimal_places=2, default=Decimal('0'))
    delivery_fee = models.DecimalField('Delivery fee', max_digits=10, decimal_places=2, default=Decimal('0'))
    estimate_minutes_min = models.PositiveSmallIntegerField('Est. delivery (min)', default=20)
    estimate_minutes_max = models.PositiveSmallIntegerField('Est. delivery (max)', default=40)
    rating = models.DecimalField('Rating', max_digits=3, decimal_places=1, default=Decimal('4.5'))
    tags = models.CharField('Tags', max_length=200, blank=True, help_text='e.g. Burgers, Fast food')
    is_active = models.BooleanField('Open', default=True)

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Dish(models.Model):
    """Dish."""
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='dishes'
    )
    name = models.CharField('Name', max_length=100)
    description = models.CharField('Description', max_length=200, blank=True)
    image = models.ImageField('Image', upload_to='dishes/%Y/%m/', blank=True, null=True)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    is_available = models.BooleanField('Available', default=True)
    sort_order = models.PositiveSmallIntegerField('Sort order', default=0)

    class Meta:
        verbose_name = 'Dish'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"
