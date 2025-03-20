import uuid
from django.db import models
from django.utils import timezone

def animal_image_upload_path(instance, filename):
    """指定上传路径，防止用户提供的路径影响存储"""
    return f'Animal_images/{instance.animal_id}_{filename}'

class animal_information(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=255)
    animal_id = models.CharField(max_length=30, unique=True, help_text='动物编号')
    img = models.ImageField(upload_to=animal_image_upload_path, help_text='动物图片')
    name = models.CharField(max_length=20, help_text='动物名')
    status = models.CharField(max_length=24,default="active", help_text='动物状态')
    # latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text='纬度')
    # longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text='经度')
    # power = models.BooleanField('当前设备电量')
    school = models.CharField(max_length=20, help_text='动物所属学校')
    created_at = models.DateTimeField(default=timezone.now, help_text='创建时间')
    updated_at = models.DateTimeField(auto_now=True, help_text='更新时间')

    def __str__(self):
        return f"Animal: {self.name}"

if __name__ == '__main__':
    pass