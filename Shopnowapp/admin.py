from django.contrib import admin

from .models import *
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'price', 'stock_quantity', 'is_active', 
        'image', 'created_at', 'updated_at'
    )

    list_filter = ('category', 'is_active')

    search_fiels = ('name', 'category__name')
    ordering = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'created_at', 'status',)
    search_fields = ['user']
    list_filter = ('status', 'created_at')

    readonly_fields = ('user','order_id', 'payment_id', 'amount', 'created_at', 'status')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'product', 'quantity')
    readonly_fields = ('user', 'order', 'product', 'quantity')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user','product', 'quantity', 'created_at')
    list_filter = ['created_at']
    readonly_fields = ('user', 'product', 'quantity', 'created_at')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'city', 'state', 'pin_code')
    search_fields = ('name', 'city')
    list_filter = ['state']

    readonly_fields = ('name', 'phone', 'address', 'city', 'state', 'pin_code')


# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):

#     list_display = ['user', 'amount','razorpay_order_id','razorpay_payment_status', 'razorpay_payment_id' , 'paid']
    
#     readonly_fields = ('user', 'amount','razorpay_order_id','razorpay_payment_status', 'razorpay_payment_id' , 'paid')
