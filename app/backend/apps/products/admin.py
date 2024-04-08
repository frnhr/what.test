from typing import ClassVar

from django.contrib import admin

from backend.apps.products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display: ClassVar = ["name", "price", "stock", "description_preview"]
    search_fields: ClassVar = ["name", "description"]

    def description_preview(self, obj: Product) -> str:
        cutoff = 100
        maybe_ellipsis = "..." if len(obj.description) > cutoff else ""
        return obj.description[:cutoff] + maybe_ellipsis
