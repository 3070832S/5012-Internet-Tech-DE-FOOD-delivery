"""餐厅与菜品模型"""
from decimal import Decimal
from django.db import models


class Restaurant(models.Model):
    """餐厅"""
    name = models.CharField('名称', max_length=100)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    description = models.TextField('简介', blank=True)
    image = models.ImageField('封面图', upload_to='restaurants/%Y/%m/', blank=True, null=True)
    min_order = models.DecimalField('起送价', max_digits=10, decimal_places=2, default=Decimal('0'))
    delivery_fee = models.DecimalField('配送费', max_digits=10, decimal_places=2, default=Decimal('0'))
    estimate_minutes_min = models.PositiveSmallIntegerField('预计送达(分钟)起', default=20)
    estimate_minutes_max = models.PositiveSmallIntegerField('预计送达(分钟)止', default=40)
    rating = models.DecimalField('评分', max_digits=3, decimal_places=1, default=Decimal('4.5'))
    tags = models.CharField('标签', max_length=200, blank=True, help_text='如: 汉堡, 快餐')
    is_active = models.BooleanField('营业中', default=True)

    class Meta:
        verbose_name = '餐厅'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Dish(models.Model):
    """菜品"""
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='dishes'
    )
    name = models.CharField('名称', max_length=100)
    description = models.CharField('描述', max_length=200, blank=True)
    image = models.ImageField('图片', upload_to='dishes/%Y/%m/', blank=True, null=True)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    is_available = models.BooleanField('可售', default=True)
    sort_order = models.PositiveSmallIntegerField('排序', default=0)

    class Meta:
        verbose_name = '菜品'
        verbose_name_plural = verbose_name
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"
