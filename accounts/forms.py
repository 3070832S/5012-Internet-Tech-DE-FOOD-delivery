"""
User registration, login, profile and address forms with validation and error messages.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, UserAddress


class UserRegistrationForm(UserCreationForm):
    """Email/username registration; password is hashed by parent class."""
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'})
    )
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        help_text='At least 8 characters, not entirely numeric'
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
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
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username


class UserLoginForm(AuthenticationForm):
    """Login form."""
    username = forms.CharField(
        label='Username or email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class ProfileEditForm(forms.ModelForm):
    """Edit profile: nickname, phone, avatar (optional)."""
    class Meta:
        model = UserProfile
        fields = ('nickname', 'phone', 'avatar')
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
           
        }
        labels = {'nickname': 'Nickname', 'phone': 'Phone', 'avatar': 'Avatar (optional)'}


class AddressForm(forms.ModelForm):
    """Add/edit delivery address."""
    class Meta:
        model = UserAddress
        fields = ('recipient_name', 'phone', 'address_line', 'city', 'postcode', 'is_default')
        widgets = {
            'recipient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipient name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'address_line': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street, building, etc.'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postcode (optional)'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'recipient_name': 'Recipient',
            'phone': 'Phone',
            'address_line': 'Address',
            'city': 'City',
            'postcode': 'Postcode',
            'is_default': 'Set as default address',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise forms.ValidationError('Please enter a phone number.')
        return phone

    def clean_address_line(self):
        value = self.cleaned_data.get('address_line', '').strip()
        if not value:
            raise forms.ValidationError('Please enter the address.')
        return value
