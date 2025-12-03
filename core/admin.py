from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Product, ProductImage


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "phone", "is_staff")
    fieldsets = list(BaseUserAdmin.fieldsets) + [
        ("Дополнительная информация", {"fields": ("phone",)}),
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "is_primary")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "condition",
        "price",
        "wood_type",
        "load_capacity",
        "in_stock",
        "quantity",
        "created_at",
    )
    list_filter = ("condition", "in_stock", "wood_type", "created_at")
    search_fields = ("name", "wood_type", "id")
    list_editable = ("price", "in_stock", "quantity")
    inlines = [ProductImageInline]
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Основная информация",
            {"fields": ("name", "condition", "price", "wood_type")},
        ),
        ("Размеры и характеристики", {"fields": ("length", "width", "load_capacity")}),
        ("Наличие", {"fields": ("in_stock", "quantity")}),
        (
            "Системная информация",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "is_primary", "created_at")
    list_filter = ("is_primary", "created_at")
    search_fields = ("product__wood_type",)
