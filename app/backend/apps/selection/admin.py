from typing import ClassVar

from django.contrib import admin
from django.db.models import Count, QuerySet
from django.http import HttpRequest

from backend.apps.selection.models import Selection, UserSelectionProxy


class SelectionInline(admin.TabularInline):
    model = Selection
    extra = 0
    fields: ClassVar = ["product"]
    autocomplete_fields: ClassVar = ["product"]


@admin.register(UserSelectionProxy)
class UserSelectionProxyAdmin(admin.ModelAdmin):
    list_display: ClassVar = ["email", "selection_count"]
    search_fields: ClassVar = ["email"]

    fields: ClassVar = ["email"]
    inlines: ClassVar = [SelectionInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.annotate(selection_count=Count("selections"))

    @admin.display(description="selections", ordering="selection_count")
    def selection_count(self, obj: Selection) -> int:
        return obj.selection_count
