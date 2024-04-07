# Generated by Django 5.0.4 on 2024-04-06 21:31

import uuid
from typing import ClassVar

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies: ClassVar = [
        ("users", "0001_initial"),
    ]

    operations: ClassVar = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254,
                unique=True,
                verbose_name="email address",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                default=uuid.uuid4,
                max_length=150,
                unique=True,
                verbose_name="username",
            ),
        ),
    ]
