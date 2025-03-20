import uuid

from django.utils import timezone
from .models import Common_user,Admin
from rest_framework import serializers

# 用户基础序列化（抽象类）
class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        # 指定在序列化器中包含的字段
        fields = [
            'id', 'username', 'password', 'name', 'role', 'phone', 'gender',
            'email', 'is_active', 'created_at', 'updated_at', 'is_deleted','points'
        ]
        # 将 'password' 字段设置为只写，以在响应中隐藏它
        extra_kwargs = {
            'password': { 'write_only': True },
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }


# 普通用户序列化
class Common_userSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        model = Common_user
        fields = UserBaseSerializer.Meta.fields + ['common_user_id']

class Common_userRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Common_user
        fields = ['username', 'password', 'name', 'gender', 'email', 'phone','common_user_id']
        extra_kwargs = {
            'password': { 'write_only': True },
        }

    def create(self, validated_data):
        # 创建普通用户对象
        common_user = Common_user.objects.create(
            id=str(uuid.uuid4()),  # 生成随机的普通用户编号
            role="Common_user",  # 手动指定角色为普通用户
            is_active=True,
            created_at=timezone.now(),  # 手动设置创建时间
            updated_at=timezone.now(),  # 手动设置更新时间
            is_deleted=False,

            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data['name'],
            gender=validated_data['gender'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            common_user_id=validated_data['common_user_id'],
        )
        return common_user

# 管理员序列化
class AdminSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        model = Admin
        fields = UserBaseSerializer.Meta.fields + ['admin_id']

class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['username', 'password', 'name', 'gender', 'email', 'phone','admin_id']
        extra_kwargs = {
            'password': { 'write_only': True },
        }

    def create(self, validated_data):
        # 创建管理员对象
        admin = Admin.objects.create(
            id=str(uuid.uuid4()),  # 生成随机的管理员编号
            role="Admin",  # 手动指定角色为管理员
            is_active=True,
            created_at=timezone.now(),  # 手动设置创建时间
            updated_at=timezone.now(),  # 手动设置更新时间
            is_deleted=False,

            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data['name'],
            gender=validated_data['gender'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            admin_id=validated_data['admin_id'],
        )
        return admin

if __name__ == '__main__':
    pass
