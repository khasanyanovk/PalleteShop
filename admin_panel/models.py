from django.db import models


class SiteSettings(models.Model):
    """Настройки сайта (контактная информация)"""

    phone = models.CharField(
        max_length=20, verbose_name="Телефон", default="+7 (XXX) XXX-XX-XX"
    )
    email = models.EmailField(verbose_name="Email", default="info@palleteshop.ru")
    address = models.CharField(
        max_length=255, verbose_name="Адрес", default="Москва, ул. Примерная, 123"
    )
    address_link = models.URLField(
        verbose_name="Ссылка на карту",
        blank=True,
        null=True,
        help_text="Ссылка на Google Maps или Яндекс.Карты",
    )
    working_hours_weekdays = models.CharField(
        max_length=50,
        verbose_name="Режим работы (Пн-Пт)",
        default="9:00 - 18:00",
    )
    working_hours_saturday = models.CharField(
        max_length=50,
        verbose_name="Режим работы (Суббота)",
        default="10:00 - 16:00",
    )
    working_hours_sunday = models.CharField(
        max_length=50,
        verbose_name="Режим работы (Воскресенье)",
        default="Выходной",
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

    @classmethod
    def get_settings(cls):
        """Получить или создать единственный экземпляр настроек"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
