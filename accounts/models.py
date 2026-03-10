"""
User profile and delivery address models.
Password is stored hashed by Django's built-in User model.
"""
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """User profile (nickname, phone, avatar)."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    nickname = models.CharField('Nickname', max_length=50, blank=True)
    phone = models.CharField('Phone', max_length=20, blank=True)
    avatar = models.ImageField('Avatar', upload_to='avatars/%Y/%m/', blank=True, null=True)

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname or self.user.username


class UserAddress(models.Model):
    """Delivery address."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    recipient_name = models.CharField('Recipient', max_length=50)
    phone = models.CharField('Phone', max_length=20)
    address_line = models.CharField('Address', max_length=200)
    city = models.CharField('City', max_length=50, default='')
    postcode = models.CharField('Postcode', max_length=20, blank=True)
    is_default = models.BooleanField('Default address', default=False)

    class Meta:
        verbose_name = 'Delivery address'
        verbose_name_plural = verbose_name
        ordering = ['-is_default', 'id']

    def __str__(self):
        return f"{self.recipient_name} - {self.address_line}"

    def save(self, *args, **kwargs):
        if self.is_default:
            UserAddress.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
