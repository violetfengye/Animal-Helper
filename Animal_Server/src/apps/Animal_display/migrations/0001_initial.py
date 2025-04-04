# Generated by Django 5.1.7 on 2025-03-18 17:25

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="animal_information",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=uuid.uuid4,
                        editable=False,
                        max_length=255,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "animal_id",
                    models.CharField(help_text="动物编号", max_length=30, unique=True),
                ),
                (
                    "img",
                    models.ImageField(
                        help_text="动物图片", upload_to="../../../Animal_images/"
                    ),
                ),
                ("name", models.CharField(help_text="动物名", max_length=20)),
                ("status", models.CharField(help_text="动物状态", max_length=24)),
                ("school", models.CharField(help_text="动物所属学校", max_length=20)),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, help_text="创建时间"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="更新时间"),
                ),
            ],
        ),
    ]
