import uuid
from typing import ClassVar

from django.contrib.auth import get_user_model
from django.db import models

user_model: type = get_user_model()


class UserSelectionProxy(user_model):
    class Meta:
        proxy = True
        verbose_name = "User"


class Selection(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        null=False,
    )
    user = models.ForeignKey(
        UserSelectionProxy,
        on_delete=models.CASCADE,
        related_name="selections",
        null=False,
        blank=False,
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="selections",
        null=False,
        blank=False,
    )

    class Meta:
        unique_together: ClassVar = ["user", "product"]

    def __str__(self) -> str:
        return f"{self.user} - {self.product}"
