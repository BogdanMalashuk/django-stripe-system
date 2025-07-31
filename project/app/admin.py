from django.contrib import admin
from .models import Item, Order, OrderItem, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency')
    search_fields = ('name',)
    list_filter = ('currency',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('item', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'is_paid', 'total_amount')
    list_filter = ('is_paid', 'created_at')
    inlines = [OrderItemInline]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')
