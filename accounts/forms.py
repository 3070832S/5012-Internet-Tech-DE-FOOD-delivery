"""
用户注册、登录、资料与地址表单，含基本验证与错误提示。
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, UserAddress


class UserRegistrationForm(UserCreationForm):
    """邮箱/用户名注册，密码由父类处理（加密存储）"""
    email = forms.EmailField(
        label='邮箱',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'})
    )
    username = forms.CharField(
        label='用户名',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'})
    )
    password1 = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}),
        help_text='至少 8 位，不能全为数字'
    )
    password2 = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '再次输入密码'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册。')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已被使用。')
        return username


class UserLoginForm(AuthenticationForm):
    """登录表单"""
    username = forms.CharField(
        label='用户名或邮箱',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名或邮箱'})
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'})
    )


class ProfileEditForm(forms.ModelForm):
    """编辑个人资料：昵称、手机、头像（可选）"""
    class Meta:
        model = UserProfile
        fields = ('nickname', 'phone', 'avatar')
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '昵称'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '手机号'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {'nickname': '昵称', 'phone': '手机号', 'avatar': '头像（可选）'}


class AddressForm(forms.ModelForm):
    """添加/编辑收货地址"""
    class Meta:
        model = UserAddress
        fields = ('recipient_name', 'phone', 'address_line', 'city', 'postcode', 'is_default')
        widgets = {
            'recipient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '收货人姓名'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '手机号'}),
            'address_line': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '街道、门牌号等'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '城市'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '邮编（可选）'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'recipient_name': '收货人',
            'phone': '手机号',
            'address_line': '详细地址',
            'city': '城市',
            'postcode': '邮编',
            'is_default': '设为默认地址',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise forms.ValidationError('请输入手机号。')
        return phone

    def clean_address_line(self):
        value = self.cleaned_data.get('address_line', '').strip()
        if not value:
            raise forms.ValidationError('请输入详细地址。')
        return value
