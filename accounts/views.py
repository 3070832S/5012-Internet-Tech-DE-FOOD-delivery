"""
User registration, login, logout, profile and address management.
Profile and addresses require login.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST
from django.urls import reverse_lazy

from .models import UserProfile, UserAddress
from .forms import UserRegistrationForm, UserLoginForm, ProfileEditForm, AddressForm

User = get_user_model()


def register(request):
    """User registration: email/username, password stored hashed."""
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


class UserLoginView(LoginView):
    """Login; session handled by Django; merge anonymous cart after login."""
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('accounts:profile')

    def form_valid(self, form):
        from carts.utils import merge_cart_after_login
        response = super().form_valid(form)
        merge_cart_after_login(self.request)
        return response


@require_http_methods(['GET', 'POST'])
@login_required(login_url='/accounts/login/')
def profile(request):
    """View profile; POST to edit (nickname, phone, avatar)."""
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ProfileEditForm(instance=profile_obj)
    return render(request, 'accounts/profile.html', {
        'profile': profile_obj,
        'form': form,
    })


@login_required(login_url='/accounts/login/')
def address_list(request):
    """Address list: view, add, edit, delete, set default."""
    addresses = request.user.addresses.all()
    form = AddressForm()
    return render(request, 'accounts/addresses.html', {
        'addresses': addresses,
        'form': form,
    })


@require_http_methods(['GET', 'POST'])
@login_required(login_url='/accounts/login/')
def address_add(request):
    """Add delivery address."""
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = request.user
            addr.save()
            messages.success(request, 'Address added.')
            return redirect('accounts:address_list')
        else:
            messages.error(request, 'Please correct the errors in the form.')
            return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Add address'})
    form = AddressForm()
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Add address'})


@require_http_methods(['GET', 'POST'])
@login_required(login_url='/accounts/login/')
def address_edit(request, pk):
    """Edit address."""
    addr = get_object_or_404(UserAddress, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=addr)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated.')
            return redirect('accounts:address_list')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = AddressForm(instance=addr)
    return render(request, 'accounts/address_form.html', {'form': form, 'address': addr, 'title': 'Edit address'})


@require_POST
@login_required(login_url='/accounts/login/')
def address_delete(request, pk):
    """Delete address."""
    addr = get_object_or_404(UserAddress, pk=pk, user=request.user)
    addr.delete()
    messages.success(request, 'Address deleted.')
    return redirect('accounts:address_list')


@require_POST
@login_required(login_url='/accounts/login/')
def address_set_default(request, pk):
    """Set default address."""
    addr = get_object_or_404(UserAddress, pk=pk, user=request.user)
    UserAddress.objects.filter(user=request.user).update(is_default=False)
    addr.is_default = True
    addr.save()
    messages.success(request, 'Set as default address.')
    return redirect('accounts:address_list')
