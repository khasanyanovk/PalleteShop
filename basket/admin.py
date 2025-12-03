from django.contrib import admin
from .models import BasketItem


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity", "get_total_price", "created_at"]
    list_filter = ["created_at", "user"]
    search_fields = ["user__username", "product__name"]
    readonly_fields = ["created_at", "updated_at"]
