import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Animal_Server.settings')
django.setup()

from src.apps.Animal_display.models import animal_information
from src.apps.Tasks.models import  task_information

# 清空动物信息表
animal_information.objects.all().delete()

# 清空任务信息表
task_information.objects.all().delete()

print("样例数据已清空！")