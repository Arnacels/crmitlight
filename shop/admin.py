from django.contrib import admin
from .models import Product, Discount, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price_buy', 'price_sell', 'amount', 'unit')


@admin.register(Discount)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    pass
