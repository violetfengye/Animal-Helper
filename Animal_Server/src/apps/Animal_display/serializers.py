from rest_framework import serializers
from .models import animal_information

class AnimalInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = animal_information
        fields = "__all__"  # 或者指定需要返回的字段，如 ['animal_id', 'name', 'status']

    # 额外的验证规则：
    animal_id = serializers.CharField(required=True, max_length=30)  # 必填
    name = serializers.CharField(required=True, max_length=20)  # 必填
    img = serializers.ImageField(required=False)  # 允许上传图片文件
    # latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)  # 必填
    # longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)  # 必填
    # power = serializers.BooleanField(required=True)  # 必填
    school = serializers.CharField(required=False, allow_blank=True, max_length=20)  # 可选，允许为空