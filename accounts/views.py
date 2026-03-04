"""
用户注册、登录、登出、个人资料与地址管理。
登录后才能访问个人中心与地址管理。
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST
from django.urls import reverse_lazy

from .models import UserProfile, UserAddress
from .forms import UserRegistrationForm, UserLoginForm, ProfileEditForm, AddressForm

User = get_user_model()


def register(request):
    """用户注册：邮箱/用户名，密码加密存储"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            messages.success(request, '注册成功，请登录。')
            return redirect('accounts:login')
        else:
            messages.error(request, '请修正表单中的错误。')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


class UserLoginView(LoginView):
    """登录：会话管理由 Django 处理；登录后合并匿名购物车"""
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
    """查看个人资料；POST 时编辑（昵称、手机、头像）"""
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, '资料已更新。')
            return redirect('accounts:profile')
        else:
            messages.error(request, '请修正表单中的错误。')
    else:
        form = ProfileEditForm(instance=profile_obj)
    return render(request, 'accounts/profile.html', {
        'profile': profile_obj,
        'form': form,
    })


@login_required(login_url='/accounts/login/')
def address_list(request):
    """地址列表：展示、添加、编辑、删除、设默认"""
    addresses = request.user.addresses.all()
    form = AddressForm()
    return render(request, 'accounts/addresses.html', {
        'addresses': addresses,
        'form': form,
    })


@require_http_methods(['GET', 'POST'])
@login_required(login_url='/accounts/login/')
def address_add(request):
    """添加收货地址"""
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = request.user
            addr.save()
            messages.success(request, '地址已添加。')
            return redirect('accounts:address_list')
        else:
            messages.error(request, '请修正表单中的错误。')
            return render(request, 'accounts/address_form.html', {'form': form, 'title': '添加地址'})
    form = AddressForm()
    return render(request, 'accounts/address_form.html', {'form': form, 'title': '添加地址'})


@require_http_methods(['GET', 'POST'])
@login_required(login_url='/accounts/login/')
def address_edit(request, pk):
    """编辑地址"""
    addr = get_object_or_404(UserAddress, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=addr)
        if form.is_valid():
            form.save()
            messages.success(request, '地址已更新。')
            return redirect('accounts:address_list')
        else:
            messages.error(request, '请修正表单中的错误。')
    else:
        form = AddressForm(instance=addr)
    return render(request, 'accounts/address_form.html', {'form': form, 'address': addr, 'title': '编辑地址'})


@require_POST
@login_required(login_url='/accounts/login/')
def address_delete(request, pk):
    """删除地址"""
    addr = get_object_or_404(UserAddress, pk=pk, user=request.user)
    addr.delete()
    messages.success(request, '地址已删除。')
    return redirect('accounts:address_list')


@require_POST
@login_required(login_url='/accounts/login/')
def address_set_default(request, pk):
    """设置默认地址"""
    addr = get_object_or_404(UserAddress, pk=pk, user=request.user)
    UserAddress.objects.filter(user=request.user).update(is_default=False)
    addr.is_default = True
    addr.save()
    messages.success(request, '已设为默认地址。')
    return redirect('accounts:address_list')
