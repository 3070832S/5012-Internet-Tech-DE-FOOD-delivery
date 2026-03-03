"""
用户扩展资料与收货地址模型
密码由 Django 内置 User 模型加密存储，不在此定义。
"""
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """用户个人资料（昵称、手机、头像）"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    nickname = models.CharField('昵称', max_length=50, blank=True)
    phone = models.CharField('手机号', max_length=20, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/%Y/%m/', blank=True, null=True)

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname or self.user.username


class UserAddress(models.Model):
    """收货地址"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    recipient_name = models.CharField('收货人', max_length=50)
    phone = models.CharField('手机号', max_length=20)
    address_line = models.CharField('详细地址', max_length=200)
    city = models.CharField('城市', max_length=50, default='')
    postcode = models.CharField('邮编', max_length=20, blank=True)
    is_default = models.BooleanField('默认地址', default=False)

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name
        ordering = ['-is_default', 'id']

    def __str__(self):
        return f"{self.recipient_name} - {self.address_line}"

    def save(self, *args, **kwargs):
        if self.is_default:
            UserAddress.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
