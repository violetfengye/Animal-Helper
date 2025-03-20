import uuid
from django.db import models
from django.utils import timezone

class task_information(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=255)
    task_id = models.CharField(max_length=20, unique=True, help_text='任务编号')
    title = models.CharField(max_length=20, help_text='任务标题')
    description = models.TextField(help_text='任务描述')
    STATUS_CHOICES = [
        ("未发布", "未发布"),
        ("未被接取", "未被接取"),
        ("未完成", "未完成"),
        ("进行中", "进行中"),
        ("确认完成", "确认完成"),
        ("已逾期", "已逾期"),
        ("已完成，待确认", "已完成，待确认"),
        ("被驳回", "被驳回"),
    ]
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="未被接取", help_text='任务状态')
    points = models.PositiveIntegerField(default=0, help_text='任务积分')
    school = models.CharField(max_length=20, help_text='任务所属学校')
    task_taker_id = models.CharField(max_length=20,default="None", help_text='任务接取人编号')
    task_publisher_id = models.CharField(max_length=20,help_text='任务发布管理员编号')
    is_published = models.BooleanField(default=False, help_text='任务是否已发布')
    publish_time = models.DateTimeField(null=True, blank=True, help_text='任务发布时间')
    deadline = models.DateTimeField(null=True, blank=True,help_text='任务截止时间')
    created_at = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    updated_at = models.DateTimeField(auto_now=True, help_text='更新时间')

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    def __str__(self):
        return f"Task: {self.title}"

if __name__ == '__main__':
    pass