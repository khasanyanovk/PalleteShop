from chats.models import Chat


def unread_messages(request):
    """Context processor для непрочитанных сообщений в чатах"""

    user_unread_count = 0
    admin_unread_count = 0

    if request.user.is_authenticated:
        if request.user.is_staff:
            admin_chats = Chat.objects.filter(is_active=True)
            admin_unread_count = sum(chat.admin_unread_count for chat in admin_chats)
        else:
            user_chats = Chat.objects.filter(user=request.user, is_active=True)
            user_unread_count = sum(chat.user_unread_count for chat in user_chats)

    return {
        "user_unread_count": user_unread_count,
        "admin_unread_count": admin_unread_count,
    }
