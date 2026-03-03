# Generated manually for accounts app

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
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=50, verbose_name='昵称')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='手机号')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/%Y/%m/', verbose_name='头像')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户资料',
                'verbose_name_plural': '用户资料',
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient_name', models.CharField(max_length=50, verbose_name='收货人')),
                ('phone', models.CharField(max_length=20, verbose_name='手机号')),
                ('address_line', models.CharField(max_length=200, verbose_name='详细地址')),
                ('city', models.CharField(default='', max_length=50)),
                ('postcode', models.CharField(blank=True, max_length=20)),
                ('is_default', models.BooleanField(default=False, verbose_name='默认地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '收货地址',
                'verbose_name_plural': '收货地址',
                'ordering': ['-is_default', 'id'],
            },
        ),
    ]
