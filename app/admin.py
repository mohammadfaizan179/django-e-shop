from django.contrib import admin
from .models import Customer, Product, Cart, Order_Place
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discount_price', 'description', 'brand', 'category', 'product_image']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


@admin.register(Order_Place)
class Order_PlaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status']

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args = [obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)