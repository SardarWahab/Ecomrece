from django.contrib import admin
from .models import Store, Product, Cart, CartItem, Order, OrderItem, Payment

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'owner', 'created_at')
    prepopulated_fields = {'slug': ('store_name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'price', 'stock', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('store',)
    search_fields = ('name', 'store__store_name')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('customer',)}

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'status')
    list_filter = ('status',)
