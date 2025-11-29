from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.db.models import Sum, F
from core.models import Product
from chats.models import Chat
from .models import BasketItem
import json
from urllib.parse import quote


@login_required
def basket_view(request):
    """Отображение корзины"""
    basket_items = BasketItem.objects.filter(user=request.user).select_related(
        "product"
    )

    total = sum(item.get_total_price() for item in basket_items)

    basket_data = {
        str(item.product.id): {"item_id": str(item.id), "quantity": item.quantity}
        for item in basket_items
    }

    context = {
        "basket_items": basket_items,
        "total": total,
        "basket_data": basket_data,
    }
    return render(request, "basket/basket.html", context)


@login_required
@require_POST
def add_to_basket(request, product_id):
    """Добавление товара в корзину (AJAX)"""
    product = get_object_or_404(Product, id=product_id)

    if not product.in_stock or product.quantity <= 0:
        return JsonResponse({"success": False, "error": "Товар недоступен"}, status=400)

    basket_item, created = BasketItem.objects.get_or_create(
        user=request.user, product=product, defaults={"quantity": 1}
    )

    if not created:
        if basket_item.quantity + 1 > product.quantity:
            return JsonResponse(
                {
                    "success": False,
                    "error": f"Максимальное доступное количество: {product.quantity}",
                },
                status=400,
            )
        basket_item.quantity += 1
        basket_item.save()

    basket_count = (
        BasketItem.objects.filter(user=request.user).aggregate(total=Sum("quantity"))[
            "total"
        ]
        or 0
    )

    return JsonResponse(
        {
            "success": True,
            "item_id": str(basket_item.id),
            "quantity": basket_item.quantity,
            "basket_count": basket_count,
        }
    )


@login_required
@require_POST
def update_basket_item(request, item_id):
    """Обновление количества товара в корзине (AJAX)"""
    basket_item = get_object_or_404(BasketItem, id=item_id, user=request.user)

    try:
        data = json.loads(request.body)
        new_quantity = int(data.get("quantity", 1))

        if new_quantity < 1:
            return JsonResponse(
                {"success": False, "error": "Количество должно быть больше 0"},
                status=400,
            )

        if new_quantity > basket_item.product.quantity:
            return JsonResponse(
                {
                    "success": False,
                    "error": f"Максимальное доступное количество: {basket_item.product.quantity}",
                },
                status=400,
            )

        basket_item.quantity = new_quantity
        basket_item.save()

        basket_count = (
            BasketItem.objects.filter(user=request.user).aggregate(
                total=Sum("quantity")
            )["total"]
            or 0
        )

        basket_items = BasketItem.objects.filter(user=request.user)
        total = sum(item.get_total_price() for item in basket_items)

        return JsonResponse(
            {
                "success": True,
                "quantity": basket_item.quantity,
                "item_total": float(basket_item.get_total_price()),
                "basket_count": basket_count,
                "basket_total": float(total),
            }
        )
    except (ValueError, json.JSONDecodeError):
        return JsonResponse(
            {"success": False, "error": "Некорректные данные"}, status=400
        )


@login_required
@require_POST
def remove_from_basket(request, item_id):
    """Удаление товара из корзины (AJAX)"""
    basket_item = get_object_or_404(BasketItem, id=item_id, user=request.user)
    basket_item.delete()

    basket_count = (
        BasketItem.objects.filter(user=request.user).aggregate(total=Sum("quantity"))[
            "total"
        ]
        or 0
    )

    basket_items = BasketItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in basket_items)

    return JsonResponse(
        {
            "success": True,
            "basket_count": basket_count,
            "basket_total": float(total),
        }
    )


@login_required
def basket_count(request):
    """Получение количества товаров в корзине (AJAX)"""
    count = (
        BasketItem.objects.filter(user=request.user).aggregate(total=Sum("quantity"))[
            "total"
        ]
        or 0
    )

    return JsonResponse({"count": count})


@login_required
def checkout(request):
    """Оформление заказа - переход в чат с предзаполненным сообщением"""
    basket_items = BasketItem.objects.filter(user=request.user).select_related(
        "product"
    )

    if not basket_items.exists():
        return redirect("basket:view")

    message_parts = ["Добрый день, интересует покупка данных товаров:"]
    total = 0

    for item in basket_items:
        item_total = item.get_total_price()
        total += item_total
        message_parts.append(
            f"• {item.product.name} - {item.quantity} шт. × {item.product.price} ₽ = {item_total} ₽"
        )

    message_parts.append(f"\nИтого: {total} ₽")
    message_text = "\n".join(message_parts)

    chat, created = Chat.objects.get_or_create(user=request.user)

    basket_items.delete()

    encoded_message = quote(message_text)

    return redirect(f"/chats/{chat.id}/?message={encoded_message}")
