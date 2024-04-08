from __future__ import annotations

import uuid
from typing import ClassVar

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as AuthUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from shared.typing.required import required


class UserManager(AuthUserManager):
    """Custom user manager that doesn't require a username field."""

    def _create_user(self, email: str, password: str, **extra_fields) -> User:
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str | None = None,
        password: str | None = None,
        **extra_fields,
    ) -> User:
        email = required(email)
        password = required(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self,
        email: str | None = None,
        password: str | None = None,
        **extra_fields,
    ) -> User:
        email = required(email)
        password = required(password)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        blank=False,
        null=False,
        unique=True,
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        default=uuid.uuid4,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    objects = UserManager()
