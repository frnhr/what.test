from django.contrib import admin

from prodselect.apps.products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "stock", "description_preview"]
    search_fields = ["name", "description"]

    def description_preview(self, obj):
        cutoff = 100
        maybe_ellipsis = "..." if len(obj.description) > cutoff else ""
        return obj.description[:cutoff] + maybe_ellipsis
