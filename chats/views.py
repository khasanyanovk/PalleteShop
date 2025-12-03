from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import logging
from .models import Chat, Message, GuestUser
from .forms import GuestUserForm, MessageForm, ChatStartForm

logger = logging.getLogger(__name__)


def staff_required(user):
    return user.is_staff


def chat_start(request):
    """Начало чата - для авторизованных и гостей"""

    if request.user.is_authenticated:
        existing_chat = Chat.objects.filter(user=request.user, is_active=True).first()
        if existing_chat:
            return redirect("chats:chat_view", chat_id=existing_chat.id)

        if request.method == "POST":
            form = ChatStartForm(request.POST)
            if form.is_valid():
                chat = Chat.objects.create(user=request.user)

                message = Message.objects.create(
                    chat=chat, text=form.cleaned_data["message"], is_admin=False
                )
                chat.refresh_from_db()

                return redirect(f"/chats/{chat.id}/?just_created=1")
        else:
            form = ChatStartForm()

        return render(request, "chats/chat_start.html", {"form": form})

    else:

        if request.method == "POST":
            guest_form = GuestUserForm(request.POST)
            chat_form = ChatStartForm(request.POST)

            if guest_form.is_valid() and chat_form.is_valid():
                try:
                    if not request.session.session_key:
                        request.session.create()

                    guest_user = GuestUser.objects.filter(
                        session_key=request.session.session_key
                    ).first()

                    if guest_user:
                        guest_user.name = guest_form.cleaned_data["name"]
                        guest_user.email = guest_form.cleaned_data.get("email")
                        guest_user.phone = guest_form.cleaned_data["phone"]
                        guest_user.save()
                    else:
                        guest_user = guest_form.save(commit=False)
                        guest_user.session_key = request.session.session_key
                        guest_user.save()

                    existing_chat = Chat.objects.filter(
                        guest_user=guest_user, is_active=True
                    ).first()

                    if existing_chat:
                        Message.objects.create(
                            chat=existing_chat,
                            text=chat_form.cleaned_data["message"],
                            is_admin=False,
                        )
                        return redirect(f"/chats/{existing_chat.id}/")

                    chat = Chat.objects.create(guest_user=guest_user)
                    Message.objects.create(
                        chat=chat,
                        text=chat_form.cleaned_data["message"],
                        is_admin=False,
                    )

                    request.session["guest_chat_id"] = str(chat.id)

                    return redirect(f"/chats/{chat.id}/?just_created=1")

                except Exception as e:
                    logger.error(f"Error creating guest chat: {e}", exc_info=True)
                    messages.error(
                        request,
                        "Произошла ошибка при создании чата. Попробуйте еще раз.",
                    )

        else:
            guest_form = GuestUserForm()
            chat_form = ChatStartForm()

        return render(
            request,
            "chats/chat_start_guest.html",
            {"guest_form": guest_form, "chat_form": chat_form},
        )


def chat_view(request, chat_id):
    """Просмотр чата"""

    chat = get_object_or_404(Chat, id=chat_id)

    has_access = False
    if request.user.is_authenticated:
        if chat.user == request.user or request.user.is_staff:
            has_access = True
    else:
        guest_chat_id = request.session.get("guest_chat_id")
        if guest_chat_id and str(chat.id) == guest_chat_id:
            has_access = True

    if not has_access:
        return redirect("core:index")

    if request.method == "GET" and not request.GET.get("just_created"):
        if request.user.is_staff:
            chat.mark_user_messages_as_read()
        else:
            chat.mark_admin_messages_as_read()

        chat.refresh_from_db()
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.is_admin = (
                request.user.is_staff if request.user.is_authenticated else False
            )
            message.save()

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "success": True,
                        "message_id": str(message.id),
                        "text": message.text,
                        "created_at": message.created_at.isoformat(),
                    }
                )

            if request.headers.get("HX-Request"):
                return render(
                    request,
                    "chats/partials/message.html",
                    {"message": message, "is_own": True},
                )

            return redirect("chats:chat_view", chat_id=chat.id)
    else:
        form = MessageForm()

    messages_list = Message.objects.filter(chat=chat).order_by("created_at")

    context = {
        "chat": chat,
        "messages": messages_list,
        "form": form,
        "is_admin": request.user.is_staff if request.user.is_authenticated else False,
    }

    return render(request, "chats/chat.html", context)


@login_required
def user_chat_list(request):
    """Список чатов пользователя"""

    chats = Chat.objects.filter(user=request.user, is_active=True).order_by(
        "-updated_at"
    )

    return render(request, "chats/chat_list.html", {"chats": chats})


@login_required
@user_passes_test(staff_required)
def admin_chat_list(request):
    """Список всех чатов для админа"""

    chats = (
        Chat.objects.filter(is_active=True)
        .select_related("user", "guest_user")
        .order_by("-updated_at")
    )

    total_unread = sum(chat.admin_unread_count for chat in chats)

    context = {"chats": chats, "total_unread": total_unread}

    return render(request, "admin_panel/chats/chat_list.html", context)


@login_required
@user_passes_test(staff_required)
def admin_chat_view(request, chat_id):
    """Просмотр и ответ в чате для админа"""

    chat = get_object_or_404(Chat, id=chat_id)

    if request.method == "GET":
        chat.mark_user_messages_as_read()

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.is_admin = True
            message.save()

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "success": True,
                        "message_id": str(message.id),
                        "text": message.text,
                        "created_at": message.created_at.isoformat(),
                    }
                )

            if request.headers.get("HX-Request"):
                return render(
                    request,
                    "chats/partials/message.html",
                    {"message": message, "is_own": True},
                )

            return redirect("admin_panel:admin_chat_view", chat_id=chat.id)
    else:
        form = MessageForm()

    messages_list = Message.objects.filter(chat=chat).order_by("created_at")

    context = {"chat": chat, "messages": messages_list, "form": form, "is_admin": True}

    return render(request, "admin_panel/chats/chat_view.html", context)


@login_required
@user_passes_test(staff_required)
def admin_chat_delete(request, chat_id):
    """Удаление чата админом"""

    chat = get_object_or_404(Chat, id=chat_id)

    if request.method == "POST":
        chat.delete()
        return redirect("admin_panel:admin_chat_list")

    return render(request, "admin_panel/chats/chat_confirm_delete.html", {"chat": chat})


def get_new_messages(request, chat_id):
    """Получить новые сообщения для polling"""

    chat = get_object_or_404(Chat, id=chat_id)
    last_message_id = request.GET.get("last_id")

    if last_message_id:
        try:
            last_message = Message.objects.get(id=last_message_id)
            new_messages = Message.objects.filter(
                chat=chat, created_at__gt=last_message.created_at
            ).order_by("created_at")
        except Message.DoesNotExist:
            new_messages = Message.objects.none()
    else:
        new_messages = Message.objects.none()

    is_admin = request.user.is_staff if request.user.is_authenticated else False

    return render(
        request,
        "chats/partials/new_messages.html",
        {"messages": new_messages, "is_admin": is_admin},
    )
