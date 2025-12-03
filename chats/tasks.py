"""
Задачи для отложенной отправки уведомлений о непрочитанных сообщениях
"""

import logging
from threading import Timer
from django.contrib.auth import get_user_model
from notifications.email_sender import (
    send_user_message_notification,
    send_admin_message_notification,
)
from pallete_shop import settings

User = get_user_model()
logger = logging.getLogger(__name__)


def send_unread_message_notification_to_user(message_id):
    """
    Отправить уведомление пользователю о непрочитанном сообщении.
    Вызывается через 5 минут после создания сообщения.
    """
    from .models import Message

    try:
        message = Message.objects.select_related(
            "chat", "chat__user", "chat__guest_user"
        ).get(id=message_id)

        if message.is_read:
            logger.info(
                f"Сообщение {message_id} уже прочитано, уведомление не отправляется"
            )
            return

        if not message.is_admin:
            logger.warning(
                f"Попытка отправить уведомление пользователю о сообщении {message_id}, которое не от админа"
            )
            return

        chat = message.chat

        if chat.user and chat.user.email:
            logger.info(
                f"Отправка отложенного уведомления пользователю {chat.user.email}, чат #{chat.id}"
            )
            send_user_message_notification(
                settings.EMAIL_HOST_USER,
                chat.user.email,
                str(chat.id),
                "Донн Поддонн",
                message.text,
            )
        elif chat.guest_user and chat.guest_user.email:
            logger.info(
                f"Отправка отложенного уведомления гостю {chat.guest_user.email}, чат #{chat.id}"
            )
            send_user_message_notification(
                settings.EMAIL_HOST_USER,
                chat.guest_user.email,
                str(chat.id),
                "Поддержка Донн Поддонн",
                message.text,
            )
        else:
            logger.info(
                f"У пользователя чата {chat.id} нет email, уведомление не отправлено"
            )

    except Exception as e:
        logger.error(
            f"Ошибка при отправке отложенного уведомления для сообщения {message_id}: {e}"
        )


def send_unread_message_notification_to_admins(message_id):
    """
    Отправить уведомление администраторам о непрочитанном сообщении.
    Вызывается через 5 минут после создания сообщения.
    """
    from .models import Message

    try:
        message = Message.objects.select_related(
            "chat", "chat__user", "chat__guest_user"
        ).get(id=message_id)

        if message.is_read:
            logger.info(
                f"Сообщение {message_id} уже прочитано, уведомление администраторам не отправляется"
            )
            return

        if message.is_admin:
            logger.warning(
                f"Попытка отправить уведомление админам о сообщении {message_id}, которое от админа"
            )
            return

        chat = message.chat

        admin_emails = list(
            User.objects.filter(is_staff=True, email__isnull=False)
            .exclude(email="")
            .values_list("email", flat=True)
        )

        if not admin_emails:
            logger.info(
                f"Нет администраторов с email для отправки уведомления, чат {chat.id}"
            )
            return

        if chat.user:
            sender_name = chat.user.get_full_name() or chat.user.username
            sender_email = chat.user.email or "не указан"
            sender_phone = getattr(chat.user, "phone", "не указан")
        else:
            sender_name = chat.guest_user.name
            sender_email = chat.guest_user.email or "не указан"
            sender_phone = chat.guest_user.phone

        logger.info(
            f"Отправка отложенного уведомления администраторам {admin_emails}, чат #{chat.id}"
        )
        send_admin_message_notification(
            settings.EMAIL_HOST_USER,
            admin_emails,
            str(chat.id),
            sender_name,
            sender_email,
            sender_phone,
            message.text,
        )

    except Exception as e:
        logger.error(
            f"Ошибка при отправке отложенного уведомления администраторам для сообщения {message_id}: {e}"
        )


def schedule_notification(message_id, is_for_user=True, delay_seconds=300):
    """
    Запланировать отправку уведомления через указанное время (по умолчанию 5 минут = 300 секунд)

    Args:
        message_id: ID сообщения
        is_for_user: True - уведомление для пользователя, False - для админов
        delay_seconds: задержка в секундах (по умолчанию 300 = 5 минут)
    """
    if is_for_user:
        timer = Timer(
            delay_seconds, send_unread_message_notification_to_user, args=[message_id]
        )
    else:
        timer = Timer(
            delay_seconds, send_unread_message_notification_to_admins, args=[message_id]
        )

    timer.daemon = True
    timer.start()

    logger.info(
        f"Запланировано уведомление для сообщения {message_id} через {delay_seconds} секунд"
    )
