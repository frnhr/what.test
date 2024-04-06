from django.contrib import admin
from django.db.models import Count

from prodselect.apps.selection.models import UserSelectionProxy, Selection


class SelectionInline(admin.TabularInline):
    model = Selection
    extra = 0
    fields = ["product"]
    autocomplete_fields = ["product"]


@admin.register(UserSelectionProxy)
class UserSelectionProxyAdmin(admin.ModelAdmin):
    list_display = ["email", "selection_count"]
    search_fields = ["email"]

    fields = ["email"]
    inlines = [SelectionInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(selection_count=Count("selections"))

    @admin.display(description="selections", ordering="selection_count")
    def selection_count(self, obj):
        return obj.selection_count
