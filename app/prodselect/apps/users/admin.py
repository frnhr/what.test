from typing import ClassVar

from django.contrib import admin

from prodselect.apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display: ClassVar = ["email"]
    search_fields: ClassVar = ["email"]
