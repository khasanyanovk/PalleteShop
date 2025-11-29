from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum
from core.models import Product, ProductImage, User
from .models import SiteSettings
from .forms import ProductForm, ProductImageForm, UserForm, SiteSettingsForm


def staff_required(user):
    return user.is_staff


@login_required
@user_passes_test(staff_required)
def dashboard(request):
    """Главная страница админ-панели с статистикой"""
    context = {
        "total_products": Product.objects.count(),
        "in_stock_products": Product.objects.filter(in_stock=True).count(),
        "new_products": Product.objects.filter(condition="new").count(),
        "used_products": Product.objects.filter(condition="used").count(),
        "total_users": User.objects.count(),
        "active_users": User.objects.filter(is_active=True).count(),
        "recent_products": Product.objects.all().order_by("-id")[:5],
    }
    return render(request, "admin_panel/dashboard.html", context)


@login_required
@user_passes_test(staff_required)
def product_list(request):
    """Список всех продуктов"""
    products = Product.objects.all().prefetch_related("images")
    return render(request, "admin_panel/product_list.html", {"products": products})


@login_required
@user_passes_test(staff_required)
def product_add(request):
    """Добавление нового продукта"""
    if request.method == "POST":
        form = ProductForm(request.POST)
        images = request.FILES.getlist("images")

        if form.is_valid():
            product = form.save()

            for image in images:
                ProductImage.objects.create(product=product, image=image)

            messages.success(request, "Продукт успешно добавлен!")
            return redirect("admin_panel:product_list")
    else:
        form = ProductForm()

    return render(
        request, "admin_panel/product_form.html", {"form": form, "action": "Добавить"}
    )


@login_required
@user_passes_test(staff_required)
def product_edit(request, pk):
    """Редактирование продукта"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        images = request.FILES.getlist("images")

        if form.is_valid():
            form.save()

            # Добавляем новые изображения
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            messages.success(request, "Продукт успешно обновлен!")
            return redirect("admin_panel:product_list")
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "admin_panel/product_form.html",
        {"form": form, "product": product, "action": "Редактировать"},
    )


@login_required
@user_passes_test(staff_required)
def product_delete(request, pk):
    """Удаление продукта"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Продукт успешно удален!")
        return redirect("admin_panel:product_list")

    return render(
        request, "admin_panel/product_confirm_delete.html", {"product": product}
    )


@login_required
@user_passes_test(staff_required)
def user_list(request):
    """Список всех пользователей"""
    users = User.objects.all().order_by("-date_joined")
    return render(request, "admin_panel/user_list.html", {"users": users})


@login_required
@user_passes_test(staff_required)
def user_edit(request, pk):
    """Редактирование пользователя"""
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно обновлен!")
            return redirect("admin_panel:user_list")
    else:
        form = UserForm(instance=user)

    return render(request, "admin_panel/user_form.html", {"form": form, "user": user})


@login_required
@user_passes_test(staff_required)
def user_toggle_active(request, pk):
    """Блокировка/разблокировка пользователя"""
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()

    status = "активирован" if user.is_active else "заблокирован"
    messages.success(request, f"Пользователь {user.username} {status}!")
    return redirect("admin_panel:user_list")


@login_required
@user_passes_test(staff_required)
def user_delete(request, pk):
    """Удаление пользователя"""
    user = get_object_or_404(User, pk=pk)

    if user.is_superuser:
        messages.error(request, "Невозможно удалить суперадминистратора!")
        return redirect("admin_panel:user_list")

    if user == request.user:
        messages.error(request, "Вы не можете удалить свой собственный аккаунт!")
        return redirect("admin_panel:user_list")

    if request.method == "POST":
        username = user.username
        user.delete()
        messages.success(request, f"Пользователь {username} успешно удален!")
        return redirect("admin_panel:user_list")

    return render(request, "admin_panel/user_confirm_delete.html", {"user": user})


@login_required
@user_passes_test(staff_required)
def site_settings(request):
    """Настройки сайта (контактная информация)"""
    settings = SiteSettings.get_settings()

    if request.method == "POST":
        form = SiteSettingsForm(request.POST, instance=settings)

        if form.is_valid():
            form.save()
            messages.success(request, "Настройки сайта успешно обновлены!")
            return redirect("admin_panel:site_settings")
    else:
        form = SiteSettingsForm(instance=settings)

    return render(
        request, "admin_panel/site_settings.html", {"form": form, "settings": settings}
    )
