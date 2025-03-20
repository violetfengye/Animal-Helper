import os
import django
import uuid
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Animal_Server.settings')
django.setup()

from src.apps.Animal_display.models import animal_information
from src.apps.Tasks.models import  task_information

# 学校列表
schools = ["学校A", "学校B", "学校C", "学校D", "学校E"]

# 动物名称列表
animal_names = ["猫咪", "狗狗", "兔子", "仓鼠", "鹦鹉", "金鱼", "乌龟", "刺猬", "龙猫", "荷兰猪",
                "孔雀", "鸽子", "鸭子", "鹅", "猴子", "袋鼠", "熊猫", "考拉", "狐狸", "猫头鹰"]

# 任务标题列表
task_titles = ["动物健康检查", "动物喂食", "动物笼舍清洁", "动物疾病预防", "动物疫苗接种",
               "动物行为观察", "动物数据记录", "动物训练", "动物救援", "动物运输",
               "动物营养研究", "动物环境改善", "动物繁殖管理", "动物医疗护理", "动物美容",
               "动物社交活动组织", "动物安全检查", "动物设备维护", "动物档案整理", "动物展览布置"]

# 生成 20 个动物信息样例
for _ in range(20):
    animal = animal_information(
        animal_id=f"ANI-{_}",
        name=random.choice(animal_names),
        status=random.choice(["active", "inactive"]),
        school=random.choice(schools)
    )
    animal.save()

# 生成 20 个任务信息样例
for _ in range(20):
    task = task_information(
        task_id=f"TASK-{_}",
        title=random.choice(task_titles),
        description=f"这是一个关于{random.choice(animal_names)}的任务。",
        status="未被接取",
        points=random.randint(10, 100),
        school=random.choice(schools),
        task_taker_id="None",
        task_publisher_id="admin01",
        is_published=False,
        publish_time=None,
        deadline=None
    )
    task.save()

print("样例数据生成完成！")