from django import forms
from .models import GuestUser, Message


class GuestUserForm(forms.ModelForm):
    """Форма для создания гостевого пользователя"""

    class Meta:
        model = GuestUser
        fields = ["name", "email", "phone"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ваше имя",
                    "style": "background: #1e1e22; border-color: #3a3a40; color: #e4e4e7; border-radius: 8px; padding: 12px;",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email (необязательно)",
                    "style": "background: #1e1e22; border-color: #3a3a40; color: #e4e4e7; border-radius: 8px; padding: 12px;",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+7 (XXX) XXX-XX-XX",
                    "style": "background: #1e1e22; border-color: #3a3a40; color: #e4e4e7; border-radius: 8px; padding: 12px;",
                }
            ),
        }
        labels = {"name": "Имя", "email": "Email", "phone": "Телефон"}


class MessageForm(forms.ModelForm):
    """Форма для отправки сообщения"""

    class Meta:
        model = Message
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control message-input",
                    "placeholder": "Введите сообщение...",
                    "rows": 1,
                    "style": "background: #1e1e22; border-color: #3a3a40; color: #e4e4e7; border-radius: 12px; padding: 12px; resize: none;",
                }
            ),
        }
        labels = {"text": ""}


class ChatStartForm(forms.Form):
    """Форма для начала чата с первым сообщением"""

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Опишите ваш вопрос или интерес к товару...",
                "rows": 4,
                "style": "background: #1e1e22; border-color: #3a3a40; color: #e4e4e7; border-radius: 12px; padding: 12px; resize: none;",
            }
        ),
        label="Сообщение",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["message"].widget.attrs["class"] += " chat-start-input"
