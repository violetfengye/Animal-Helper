# Generated by Django 5.1.7 on 2025-03-19 05:31

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="task_information",
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
                    "task_id",
                    models.CharField(help_text="任务编号", max_length=20, unique=True),
                ),
                ("title", models.CharField(help_text="任务标题", max_length=20)),
                ("description", models.TextField(help_text="任务描述")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("未完成", "未完成"),
                            ("进行中", "进行中"),
                            ("已完成", "已完成"),
                        ],
                        default="未完成",
                        help_text="任务状态",
                        max_length=20,
                    ),
                ),
                (
                    "points",
                    models.PositiveIntegerField(default=0, help_text="任务积分"),
                ),
                ("school", models.CharField(help_text="任务所属学校", max_length=20)),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="创建时间"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="更新时间"),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["status"], name="Tasks_task__status_3af955_idx"
                    ),
                    models.Index(
                        fields=["created_at"], name="Tasks_task__created_505094_idx"
                    ),
                ],
            },
        ),
    ]
