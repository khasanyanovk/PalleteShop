from django.urls import path
from . import views

app_name = "basket"

urlpatterns = [
    path("", views.basket_view, name="view"),
    path("add/<uuid:product_id>/", views.add_to_basket, name="add"),
    path("update/<uuid:item_id>/", views.update_basket_item, name="update"),
    path("remove/<uuid:item_id>/", views.remove_from_basket, name="remove"),
    path("count/", views.basket_count, name="count"),
    path("checkout/", views.checkout, name="checkout"),
]
