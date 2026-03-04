# Generated manually for restaurants app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True, verbose_name='简介')),
                ('image', models.ImageField(blank=True, null=True, upload_to='restaurants/%Y/%m/', verbose_name='封面图')),
                ('min_order', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='起送价')),
                ('delivery_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='配送费')),
                ('estimate_minutes_min', models.PositiveSmallIntegerField(default=20, verbose_name='预计送达(分钟)起')),
                ('estimate_minutes_max', models.PositiveSmallIntegerField(default=40, verbose_name='预计送达(分钟)止')),
                ('rating', models.DecimalField(decimal_places=1, default=4.5, max_digits=3, verbose_name='评分')),
                ('tags', models.CharField(blank=True, help_text='如: 汉堡, 快餐', max_length=200, verbose_name='标签')),
                ('is_active', models.BooleanField(default=True, verbose_name='营业中')),
            ],
            options={
                'verbose_name': '餐厅',
                'verbose_name_plural': '餐厅',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='描述')),
                ('image', models.ImageField(blank=True, null=True, upload_to='dishes/%Y/%m/', verbose_name='图片')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格')),
                ('is_available', models.BooleanField(default=True, verbose_name='可售')),
                ('sort_order', models.PositiveSmallIntegerField(default=0, verbose_name='排序')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='restaurants.restaurant')),
            ],
            options={
                'verbose_name': '菜品',
                'verbose_name_plural': '菜品',
                'ordering': ['sort_order', 'id'],
            },
        ),
    ]
