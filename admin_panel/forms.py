from django import forms
from core.models import Product, ProductImage, User
from .models import SiteSettings


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "condition",
            "price",
            "length",
            "width",
            "wood_type",
            "load_capacity",
            "quantity",
            "in_stock",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "condition": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "length": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "width": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "wood_type": forms.TextInput(attrs={"class": "form-control"}),
            "load_capacity": forms.NumberInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "in_stock": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "is_active",
            "is_staff",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            "phone",
            "email",
            "address",
            "address_link",
            "working_hours_weekdays",
            "working_hours_saturday",
            "working_hours_sunday",
        ]
        widgets = {
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "address_link": forms.URLInput(attrs={"class": "form-control"}),
            "working_hours_weekdays": forms.TextInput(attrs={"class": "form-control"}),
            "working_hours_saturday": forms.TextInput(attrs={"class": "form-control"}),
            "working_hours_sunday": forms.TextInput(attrs={"class": "form-control"}),
        }
