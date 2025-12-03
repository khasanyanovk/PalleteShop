import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from unidecode import unidecode
import os
from datetime import datetime


def product_image_upload_to(instance, filename):
    """
    Генерирует безопасный путь для загрузки изображений продуктов.
    Преобразует кириллицу в латиницу для избежания проблем с URL.
    """
    ext = filename.split(".")[-1]
    name = ".".join(filename.split(".")[:-1])
    safe_name = slugify(unidecode(name))
    if not safe_name:
        safe_name = f"image_{int(datetime.now().timestamp() * 1000000)}"
    else:
        safe_name = f"{safe_name}_{int(datetime.now().timestamp() * 1000000)}"
    return os.path.join(
        "products", datetime.now().strftime("%Y/%m/%d"), f"{safe_name}.{ext}"
    )


class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Телефон"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Product(models.Model):

    class ConditionChoices(models.TextChoices):
        NEW = "new", "Новый"
        USED = "used", "Б/У"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=200, verbose_name="Название", help_text="Краткое название продукта"
    )
    condition = models.CharField(
        max_length=10, choices=ConditionChoices.choices, verbose_name="Состояние"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Стоимость"
    )
    length = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Длина (см)"
    )
    width = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Ширина (см)"
    )
    wood_type = models.CharField(max_length=100, verbose_name="Вид древесины")
    load_capacity = models.IntegerField(verbose_name="Грузоподъемность (кг)")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Поддон"
        verbose_name_plural = "Поддоны"
        ordering = ["-created_at"]

    def get_condition_display(self):
        return self.ConditionChoices(self.condition).label

    def get_primary_image(self):
        """Возвращает главное изображение или первое доступное"""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()

    def __str__(self):
        if self.name:
            return self.name
        return f"Поддон {self.length}x{self.width} - {self.get_condition_display()}"


class ProductImage(models.Model):
    """Модель для хранения фотографий продуктов"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="Продукт"
    )
    image = models.ImageField(
        upload_to=product_image_upload_to, verbose_name="Изображение"
    )
    is_primary = models.BooleanField(default=False, verbose_name="Главное изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"
        ordering = ["-is_primary", "created_at"]

    def __str__(self):
        return f"Фото для {self.product}"
