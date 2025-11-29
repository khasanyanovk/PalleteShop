import uuid
from django.db import models
from django.utils import timezone
from core.models import User


class GuestUser(models.Model):
    """Модель для гостевых пользователей (неавторизованных)"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    session_key = models.CharField(
        max_length=40, unique=True, verbose_name="Ключ сессии"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Гостевой пользователь"
        verbose_name_plural = "Гостевые пользователи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Chat(models.Model):
    """Модель чата - поддерживает как авторизованных, так и гостевых пользователей"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chats",
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    guest_user = models.ForeignKey(
        GuestUser,
        on_delete=models.CASCADE,
        related_name="chats",
        verbose_name="Гостевой пользователь",
        null=True,
        blank=True,
    )

    subject = models.CharField(max_length=200, verbose_name="Тема чата", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активен")
    admin_unread_count = models.PositiveIntegerField(
        default=0, verbose_name="Непрочитанных у админа"
    )
    user_unread_count = models.PositiveIntegerField(
        default=0, verbose_name="Непрочитанных у пользователя"
    )

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"
        ordering = ["-updated_at"]

    def __str__(self):
        if self.user:
            return f"Чат с {self.user.username}"
        return f"Чат с {self.guest_user.name}"

    def get_participant_name(self):
        """Получить имя участника чата"""
        if self.user:
            return self.user.get_full_name() or self.user.username
        return self.guest_user.name

    def get_participant_contact(self):
        """Получить контакт участника чата"""
        if self.user:
            return self.user.email or self.user.phone
        return self.guest_user.phone

    def mark_admin_messages_as_read(self):
        """Пометить все сообщения админа как прочитанные пользователем"""
        self.messages.filter(is_admin=True, is_read=False).update(is_read=True)
        self.user_unread_count = 0
        self.save(update_fields=["user_unread_count"])

    def mark_user_messages_as_read(self):
        """Пометить все сообщения пользователя как прочитанные админом"""
        self.messages.filter(is_admin=False, is_read=False).update(is_read=True)
        self.admin_unread_count = 0
        self.save(update_fields=["admin_unread_count"])
        self.admin_unread_count = 0
        self.save(update_fields=["admin_unread_count"])


class Message(models.Model):
    """Модель сообщения в чате"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="messages", verbose_name="Чат"
    )

    text = models.TextField(verbose_name="Текст сообщения")

    is_admin = models.BooleanField(default=False, verbose_name="От администратора")
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["created_at"]

    def __str__(self):
        sender = "Админ" if self.is_admin else "Пользователь"
        return f"{sender}: {self.text[:50]}"

    def get_formatted_text(self):
        """Возвращает текст с правильными переносами строк для HTML"""
        import html

        safe_text = html.escape(self.text)
        return safe_text.replace("\n", "<br>")

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        super().save(*args, **kwargs)
        if is_new:
            if self.is_admin:
                self.chat.user_unread_count += 1
            else:
                self.chat.admin_unread_count += 1

            self.chat.save(
                update_fields=["user_unread_count", "admin_unread_count", "updated_at"]
            )
