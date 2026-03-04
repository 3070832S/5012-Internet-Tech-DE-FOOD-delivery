from django.contrib import admin
from .models import Restaurant, Dish


class DishInline(admin.TabularInline):
    model = Dish
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'min_order', 'delivery_fee', 'rating', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [DishInline]


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'is_available')
    list_filter = ('restaurant', 'is_available')
