from rest_framework import serializers
from .models import task_information

class TaskInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = task_information
        fields = "__all__"  # 或者指定需要返回的字段，如 ['animal_id', 'name', 'status']

    # 额外的验证规则：
    task_id = serializers.CharField(required=True, max_length=20)  # 必填
    title = serializers.CharField(required=True, max_length=20)  # 必填
    task_publisher_id =serializers.CharField(required=True, max_length=20)
    description = serializers.CharField(required=True)  # 必填
    school = serializers.CharField(required=True, max_length=20)  # 必填