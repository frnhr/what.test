from typing import ClassVar

from django.contrib import admin

from backend.apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display: ClassVar = ["email"]
    search_fields: ClassVar = ["email"]
