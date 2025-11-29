from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    # Публичные маршруты для пользователей
    path("start/", views.chat_start, name="chat_start"),
    path("<uuid:chat_id>/", views.chat_view, name="chat_view"),
    path("my/", views.user_chat_list, name="user_chat_list"),
    # AJAX/HTMX endpoints
    path(
        "<uuid:chat_id>/new-messages/", views.get_new_messages, name="get_new_messages"
    ),
]
