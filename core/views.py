from threading import Thread
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from notifications.email_sender import send_welcome_email
from pallete_shop import settings
from .models import Product
from .forms import UserRegistrationForm, UserProfileForm


def index(request):
    filter_type = request.GET.get("filter", "all")

    products = Product.objects.filter(in_stock=True).prefetch_related("images")

    if filter_type == "new":
        products = products.filter(condition="new")
    elif filter_type == "used":
        products = products.filter(condition="used")

    basket_data = {}
    if request.user.is_authenticated:
        from basket.models import BasketItem

        basket_items = BasketItem.objects.filter(user=request.user).select_related(
            "product"
        )
        basket_data = {
            str(item.product.id): {"item_id": str(item.id), "quantity": item.quantity}
            for item in basket_items
        }

    if request.headers.get("HX-Request"):
        return render(
            request,
            "core/partials/product_list.html",
            {"products": products, "basket_data": basket_data},
        )

    context = {
        "products": products,
        "basket_data": basket_data,
    }
    return render(request, "core/index.html", context)


def product_detail(request, product_id):
    """Детальная страница товара с большими фото и информацией"""
    product = get_object_or_404(Product, id=product_id)
    images = product.images.all()

    basket_item = None
    if request.user.is_authenticated:
        from basket.models import BasketItem

        basket_item = BasketItem.objects.filter(
            user=request.user, product=product
        ).first()

    context = {
        "product": product,
        "images": images,
        "basket_item": basket_item,
    }
    return render(request, "core/product_detail.html", context)


def about(request):
    """Страница О нас"""
    return render(request, "core/about.html")


def contacts(request):
    """Страница Контакты"""
    return render(request, "core/contacts.html")


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
            login(request, user)
            Thread(
                target=send_welcome_email,
                args=(settings.EMAIL_HOST_USER, user.email, username),
            ).start()
            return redirect("core:index")
    else:
        form = UserRegistrationForm()

    return render(request, "core/register.html", {"form": form})


def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, "Вы вышли из системы.")
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
