from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product
from .forms import UserRegistrationForm, UserProfileForm


def index(request):
    filter_type = request.GET.get("filter", "all")

    products = Product.objects.filter(in_stock=True).prefetch_related("images")

    if filter_type == "new":
        products = products.filter(condition="new")
    elif filter_type == "used":
        products = products.filter(condition="used")

    if request.headers.get("HX-Request"):
        return render(
            request, "core/partials/product_list.html", {"products": products}
        )

    context = {"products": products}
    return render(request, "core/index.html", context)


def login_view(request):
    """Страница входа с редиректом на админку для staff"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Добро пожаловать, {user.username}!")
                if user.is_staff or user.is_superuser:
                    return redirect("admin_panel:dashboard")
                return redirect("core:index")
    else:
        form = AuthenticationForm()

    return render(request, "core/login.html", {"form": form})


def register_view(request):
    """Регистрация нового пользователя"""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Аккаунт {username} успешно создан! Теперь вы можете войти."
            )
            login(request, user)  # Автоматический вход после регистрации
            return redirect("core:index")
    else:
        form = UserRegistrationForm()

    return render(request, "core/register.html", {"form": form})


def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect("core:index")


@login_required
def profile_view(request):
    """Профиль пользователя"""
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш профиль успешно обновлен!")
            return redirect("core:profile")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "core/profile.html", {"form": form})
