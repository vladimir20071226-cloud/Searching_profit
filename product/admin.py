from django.contrib import admin
from .models import Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=("name", "buy_price", "url", "source_buy", "source_sell", "buy_price", "sell_price", "created_at", "status",)
    search_fields=("status", "created_at", "name",)