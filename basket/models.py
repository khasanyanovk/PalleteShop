import uuid
from django.db import models
from django.conf import settings
from core.models import Product


class BasketItem(models.Model):
    """Модель для хранения товаров в корзине"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="basket_items",
        verbose_name="Пользователь",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="basket_items",
        verbose_name="Товар",
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        ordering = ["-created_at"]
        unique_together = ["user", "product"]

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x{self.quantity}"

    def get_total_price(self):
        """Возвращает общую стоимость товара"""
        return self.product.price * self.quantity
