"""订单与订单项模型"""
from decimal import Decimal
from django.db import models
from django.conf import settings


class Order(models.Model):
    """订单"""
    STATUS_PENDING = 'pending'
    STATUS_PREPARING = 'preparing'
    STATUS_DELIVERING = 'delivering'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, '待处理'),
        (STATUS_PREPARING, '制作中'),
        (STATUS_DELIVERING, '配送中'),
        (STATUS_COMPLETED, '已完成'),
        (STATUS_CANCELLED, '已取消'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    order_no = models.CharField('订单号', max_length=32, unique=True, db_index=True)
    # 收货信息快照
    recipient_name = models.CharField('收货人', max_length=50)
    phone = models.CharField('手机号', max_length=20)
    address_line = models.CharField('详细地址', max_length=200)
    city = models.CharField('城市', max_length=50, default='')
    postcode = models.CharField('邮编', max_length=20, blank=True)

    status = models.CharField(
        '状态',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    note = models.TextField('订单备注', blank=True)

    subtotal = models.DecimalField('商品小计', max_digits=10, decimal_places=2, default=Decimal('0'))
    delivery_fee = models.DecimalField('配送费', max_digits=10, decimal_places=2, default=Decimal('0'))
    total = models.DecimalField('订单总价', max_digits=10, decimal_places=2, default=Decimal('0'))

    created_at = models.DateTimeField('下单时间', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_no} ({self.get_status_display()})"

    def can_cancel(self):
        return self.status == self.STATUS_PENDING


class OrderItem(models.Model):
    """订单项：菜品快照"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish_name = models.CharField('菜品名称', max_length=100)
    quantity = models.PositiveIntegerField('数量')
    unit_price = models.DecimalField('单价', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = verbose_name

    @property
    def line_total(self):
        return self.quantity * self.unit_price
