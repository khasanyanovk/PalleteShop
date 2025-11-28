from django.shortcuts import render
from .models import Product


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
