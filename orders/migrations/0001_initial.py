# Generated manually for orders app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_no', models.CharField(db_index=True, max_length=32, unique=True, verbose_name='订单号')),
                ('recipient_name', models.CharField(max_length=50, verbose_name='收货人')),
                ('phone', models.CharField(max_length=20, verbose_name='手机号')),
                ('address_line', models.CharField(max_length=200, verbose_name='详细地址')),
                ('city', models.CharField(default='', max_length=50)),
                ('postcode', models.CharField(blank=True, max_length=20)),
                ('status', models.CharField(choices=[('pending', '待处理'), ('preparing', '制作中'), ('delivering', '配送中'), ('completed', '已完成'), ('cancelled', '已取消')], default='pending', max_length=20, verbose_name='状态')),
                ('note', models.TextField(blank=True, verbose_name='订单备注')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='商品小计')),
                ('delivery_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='配送费')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='订单总价')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='下单时间')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_name', models.CharField(max_length=100, verbose_name='菜品名称')),
                ('quantity', models.PositiveIntegerField(verbose_name='数量')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='单价')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
            ],
            options={
                'verbose_name': '订单项',
                'verbose_name_plural': '订单项',
            },
        ),
    ]
