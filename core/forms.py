from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации пользователя"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "style": "background: #1e1e22; border-color: #3a3a40; color: #e4e4e7; border-radius: 8px; padding: 12px;",
                "placeholder": "your@email.com",
            }
        ),
    )

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "background: #1e1e22; border-color: #3a3a40; color: #e4e4e7; border-radius: 8px; padding: 12px;",
                "placeholder": "Иван",
            }
        ),
    )

    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "background: #1e1e22; border-color: #3a3a40; color: #e4e4e7; border-radius: 8px; padding: 12px;",
                "placeholder": "Иванов",
            }
        ),
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "background: #1e1e22; border-color: #3a3a40; color: #e4e4e7; border-radius: 8px; padding: 12px;",
                "placeholder": "+7 (999) 123-45-67",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "background: #1e1e22; border-color: #3a3a40; color: #e4e4e7; border-radius: 8px; padding: 12px;",
                    "placeholder": "username",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация полей пароля
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "style": "background: #1e1e22; border-color: #3a3a40; color: #e4e4e7; border-radius: 8px; padding: 12px;",
                "placeholder": "••••••••",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "style": "background: #1e1e22; border-color: #3a3a40; color: #e4e4e7; border-radius: 8px; padding: 12px;",
                "placeholder": "••••••••",
            }
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
