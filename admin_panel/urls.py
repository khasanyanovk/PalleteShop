from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # Продукты
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_add, name="product_add"),
    path("products/<uuid:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<uuid:pk>/delete/", views.product_delete, name="product_delete"),
    # Пользователи
    path("users/", views.user_list, name="user_list"),
    path("users/<uuid:pk>/edit/", views.user_edit, name="user_edit"),
    path(
        "users/<uuid:pk>/toggle-active/",
        views.user_toggle_active,
        name="user_toggle_active",
    ),
    # Настройки сайта
    path("settings/", views.site_settings, name="site_settings"),
]
