import uuid
from django.db import models
from django.utils import timezone


# 用户模型（抽象模型）
class User(models.Model):
    class Meta:
        abstract = True
    
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=255)
    username = models.CharField(max_length=30, unique=True, help_text='用户名')
    password = models.CharField(max_length=30, help_text='用户密码')
    name = models.CharField(max_length=30, help_text='用户姓名')
    ROLE_CHOICES = [('common_user', 'Common_user'),('admin', 'Admin'),('super_admin', 'Super_admin'),]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='common_user', help_text='角色名')
    GENDER_CHOICES = [('male', 'Male'),('female', 'Female')]
    gender = models.CharField(max_length=10,  choices=GENDER_CHOICES, default='male', help_text='性别')
    is_active = models.BooleanField(default=True, help_text='是否激活')
    is_deleted = models.BooleanField(default=False, help_text='是否删除')
    phone = models.CharField(max_length=20, null=True, blank=True, help_text='电话号码')
    email = models.CharField(max_length=255, null=True, blank=True, help_text='邮箱账号')
    points = models.IntegerField(default=0, help_text='积分')
    created_at = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    updated_at = models.DateTimeField(auto_now=True, help_text='更新时间')


# 普通用户模型（实例模型）
class Common_user(User):
    class Meta:
        db_table = 'common_user'

    common_user_id = models.CharField(max_length=30, unique=True, help_text='用户编号')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'common_user_id', 'username', 'name', 'gender', 
        'role', 'is_active', 'is_deleted'
    ]

    def __str__(self):
        return 'Common_user: ' + self.username
    
    # 根据你的身份验证逻辑返回相应的布尔值
    @property
    def is_authenticated(self):
        return True


# 管理员用户模型（实例模型）
class Admin(User):
    class Meta:
        db_table = 'admin'

    admin_id = models.CharField(max_length=30, unique=True, help_text='管理员编号')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'admin_id', 'username', 'name', 'gender', 
        'role', 'is_active', 'is_deleted'
    ]
     
    def __str__(self):
        return 'Admin: ' + self.username
    
    # 根据你的身份验证逻辑返回相应的布尔值
    @property
    def is_authenticated(self):
        return True

if __name__ == '__main__':
    pass
