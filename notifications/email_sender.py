import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from admin_panel.models import SiteSettings

logger = logging.getLogger(__name__)


def get_site_context():
    """Получить общие данные для всех email-шаблонов"""
    settings = SiteSettings.get_settings()
    return {
        "contact_email": settings.email,
        "contact_phone": settings.phone,
        "contact_address": settings.address,
        "site_url": "http://localhost:8000",  # TODO: использовать реальный домен в продакшене
    }


def send_welcome_email(from_email, user_email, username):
    """Отправка приветственного письма новому пользователю"""
    if not user_email:
        return

    context = get_site_context()
    context["username"] = username

    subject = f"Добро пожаловать в Донн Поддонн, {username}!"
    text_content = render_to_string("emails/welcome.txt", context)
    html_content = render_to_string("emails/welcome.html", context)

    email = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=from_email, to=[user_email]
    )
    email.attach_alternative(html_content, "text/html")
    try:
        email.send(fail_silently=False)
        logger.info(f"Приветственное письмо отправлено: {user_email}")
    except Exception as e:
        logger.error(f"Ошибка отправки приветственного письма {user_email}: {e}")


def send_user_message_notification(
    from_email, to_email, chat_id, sender_name, message_preview
):
    """Отправка уведомления пользователю о новом сообщении от поддержки"""
    if not to_email:
        logger.warning("Попытка отправить уведомление пользователю без email")
        return

    context = get_site_context()
    context.update(
        {
            "sender_name": sender_name,
            "message_preview": message_preview[:200]
            + ("..." if len(message_preview) > 200 else ""),
        }
    )

    subject = f"Новое сообщение от {sender_name}"
    text_content = render_to_string("emails/new_message.txt", context)
    html_content = render_to_string("emails/new_message.html", context)

    email = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=from_email, to=[to_email]
    )
    email.attach_alternative(html_content, "text/html")
    try:
        email.send(fail_silently=False)
        logger.info(f"Уведомление пользователю отправлено: {to_email}, чат #{chat_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки уведомления пользователю {to_email}: {e}")
        logger.info(f"Письмо не отправлено, но работа продолжается")


def send_admin_message_notification(
    from_email,
    admin_emails,
    chat_id,
    sender_name,
    sender_email,
    sender_phone,
    message_preview,
):
    """Отправка уведомления администраторам о новом сообщении от клиента"""
    if not admin_emails:
        return

    context = get_site_context()
    context.update(
        {
            "sender_name": sender_name,
            "sender_email": sender_email,
            "sender_phone": sender_phone,
            "message_preview": message_preview[:200]
            + ("..." if len(message_preview) > 200 else ""),
        }
    )

    subject = f"⚠️ Новое обращение от {sender_name}"
    text_content = render_to_string("emails/admin_new_message.txt", context)
    html_content = render_to_string("emails/admin_new_message.html", context)

    email = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=from_email, to=admin_emails
    )
    email.attach_alternative(html_content, "text/html")
    try:
        email.send(fail_silently=False)
        logger.info(
            f"Уведомление администраторам отправлено: {admin_emails}, чат #{chat_id}"
        )
    except Exception as e:
        logger.error(f"Ошибка отправки уведомления администраторам {admin_emails}: {e}")
