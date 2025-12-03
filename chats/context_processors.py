from chats.models import Chat
import logging

logger = logging.getLogger(__name__)


def unread_messages(request):
    """Context processor для непрочитанных сообщений в чатах"""

    user_unread_count = 0
    admin_unread_count = 0

    if request.user.is_authenticated:
        if request.user.is_staff:
            admin_chats = Chat.objects.filter(is_active=True)
            admin_unread_count = sum(chat.admin_unread_count for chat in admin_chats)
            logger.debug(
                f"Admin {request.user.username} has {admin_unread_count} unread messages"
            )
        else:
            user_chats = Chat.objects.filter(user=request.user, is_active=True)
            user_unread_count = sum(chat.user_unread_count for chat in user_chats)
            logger.debug(
                f"User {request.user.username} has {user_unread_count} unread messages"
            )

    return {
        "user_unread_count": user_unread_count,
        "admin_unread_count": admin_unread_count,
    }
