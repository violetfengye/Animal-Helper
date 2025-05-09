import warnings
import pandas as pd
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from src.utils.mapping_table import UPLOAD_STUDENT_MAPPING_TABLE
from src.utils.mapping_table import translate_fields
from .models import Common_user, Admin
from .serializers import Common_userSerializer, AdminSerializer, Common_userRegistrationSerializer, \
    AdminRegistrationSerializer
from src.middleware.authentication import CustomRefreshToken
from src.utils.response_utils import ResponseCode, api_response


# 忽略openpyxl的警告
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


class Common_userLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """post 普通用户登录接口
        Args:
            request (Object): 请求参数
        """
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = Common_user.objects.get(username=username)
        except Exception:
            return api_response(ResponseCode.BAD_REQUEST, '登录失败！用户不存在！')
        if user.is_deleted is True:
            return api_response(ResponseCode.BAD_REQUEST, '登录失败！用户不存在！')
        if user.is_active is False:
            return api_response(ResponseCode.BAD_REQUEST, '登录失败！用户没有激活！')
        if user.password == password:
            refresh = CustomRefreshToken.for_user(user)
            data = {
                'userId': user.id,
                'name': user.name,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return api_response(ResponseCode.SUCCESS, '登录成功', data)
        else:
            return api_response(ResponseCode.UNAUTHORIZED, '登录失败！用户名或密码错误！')

class Common_userRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """post 普通用户注册接口
        Args:
            request (Object): 请求参数
        """
        # 读取上传的普通用户信息
        common_user_info = Common_userRegistrationSerializer(data=request.data)
        if common_user_info.is_valid():
            # 保存普通用户信息
            common_user_info.save()
            # 返回成功响应
            return api_response(ResponseCode.SUCCESS, '注册成功')
        else:
            # 返回错误响应
            return api_response(ResponseCode.BAD_REQUEST, '注册失败！请检查输入信息！', common_user_info.errors)

class AdminLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """post 管理员登录接口
        Args:
            request (Object): 请求参数
        """
        username = request.data.get('username')
        password = request.data.get('password')
        # 标志是否为管理员登录
        is_SuperAdmin = request.data.get('isSuperAdmin',False)

        try:
            user = Admin.objects.get(username=username)
        except Admin.DoesNotExist:
            return api_response(ResponseCode.BAD_REQUEST, '登录失败！账号不存在！')

        if user.is_deleted is True:
            return api_response(ResponseCode.BAD_REQUEST, '登录失败！账号不存在！')

        if user.password == password:
            if is_SuperAdmin and user.role != 'super_admin':
                return api_response(ResponseCode.UNAUTHORIZED, '登录失败！非超级管理员账号！')

            refresh = CustomRefreshToken.for_user(user)
            data = {
                'userId': user.id,
                'name': user.name,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return api_response(ResponseCode.SUCCESS, '登录成功', data)
        else:
            return api_response(ResponseCode.UNAUTHORIZED, '登录失败！用户名或密码错误！')

class AdminRegistrationView(APIView):

    permission_classes = [AllowAny]
    def post(self, request):
        """post 管理员注册接口
        Args:
            request (Object): 请求参数
        """
        # 读取上传的管理员信息
        admin_info = AdminRegistrationSerializer(data=request.data)

        if admin_info.is_valid():
            # 保存管理员信息
            admin_info.save()
            # 返回成功响应
            return api_response(ResponseCode.SUCCESS, '注册成功')
        else:
            # 返回错误响应
            return api_response(ResponseCode.BAD_REQUEST, '注册失败！请检查输入信息！', admin_info.errors)



class BaseUserView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]
    # 需要在子类中设置具体的序列化器
    model_serializer = None 
    # 需要在子类中设置具体的Model
    model = None

    def post(self, request):
        """post 创建用户信息接口
        Args:
            request (Object): 请求参数
        """
        # 使用请求数据创建实例
        serializer = self.model_serializer(data=request.data)
        # 检查数据是否根据序列化器的规则有效
        if serializer.is_valid():
            # 保存验证过的数据以创建新的实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 201 Created 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '数据冲突或缺失！创建失败！请重新填写！', serializer.errors)

    def put(self, request, **kwargs):
        """put 编辑用户信息接口
        Args:
            request (Object): 请求参数
        """
        # 获取要编辑的用户实例
        try:
            user_instance = self.model.objects.get(id=kwargs['id'])
            request.data['password'] = user_instance.password
            # 删除不需要的参数
            del request.data['updated_at'], request.data['created_at'], request.data['id']
        except self.model.DoesNotExist:
            # 用户不存在，返回错误响应和 HTTP 404 Not Found 状态
            return api_response(ResponseCode.NOT_FOUND, '编辑失败!用户不存在，无法进行修改！')
        # 使用请求数据和用户实例创建实例，传入实例表示执行更新操作
        serializer = self.model_serializer(user_instance, data=request.data)
        # 检查数据是否根据序列化器的规则有效
        if serializer.is_valid():
            # 保存验证过的数据以更新现有的 User 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 200 OK 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '编辑成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '编辑失败! 存在校验失败的字段！', serializer.error_messages)

    def delete(self, _, **kwargs):
        """delete 删除用户信息接口
        Args:
            request (Object): 请求参数
        """
        try:
            # 获取要删除的用户实例
            user_instance = self.model.objects.get(id=kwargs['id'])
        except self.model.DoesNotExist:
            # 用户不存在，返回错误响应和 HTTP 404 Not Found 状态
            return api_response(ResponseCode.NOT_FOUND, '用户不存在，无法删除！')
        # 在这里添加逻辑删除的代码，例如将用户状态标记为已删除
        user_instance.is_deleted = True
        user_instance.save()
        # 返回成功响应和 HTTP 200 OK 状态
        return api_response(ResponseCode.SUCCESS, '删除成功')

    def get(self, request, **kwargs):
        """get 查询用户信息（列表 & 详情）
        Args:
            request (Object): 请求参数
        """
        if kwargs.items().__len__() != 0:
            try:
                # 获取指定用户实例
                user_instance = self.model.objects.get(id=kwargs['user_id'])
            except self.model.DoesNotExist:
                # 用户不存在，返回错误响应和 HTTP 404 Not Found 状态
                return api_response(ResponseCode.NOT_FOUND, '用户不存在！')
            # 序列化用户详情数据
            serializer = self.model_serializer(user_instance)
            # 返回序列化后的用户详情数据
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '查询用户详情成功', data.data)
        else:
            # 定义查询参数和它们对应的模型字段
            query_params_mapping = {
                'username': 'username',
                'name': 'name__icontains',  # 模糊搜索
                'common_user_id': 'common_user_id__icontains',  # 模糊搜索
                'admin_id': 'admin_id__icontains',  # 模糊搜索
                'gender': 'gender',
                'is_deleted': 'is_deleted',
                'is_active': 'is_active'
                # 添加其他查询参数和字段的映射
            }
            # 构建查询条件的字典
            filters = {}
            for param, field in query_params_mapping.items():
                value = request.query_params.get(param, None)
                if value is not None and value != '':
                    if field == 'is_active' or field == 'is_deleted':
                        filters[field] = True if value.lower() == 'true' else False
                    else:
                        filters[field] = value
            # 执行查询
            queryset = self.model.objects.filter(**filters).order_by('-created_at')
            # 实例化分页器并配置参数
            paginator = PageNumberPagination()
            paginator.page_size = int(request.query_params.get('pageSize', 50))
            paginator.page_query_param = 'currentPage'
            # 进行分页处理
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            # 序列化用户数据
            serializer = self.model_serializer(paginated_queryset, many=True)
            resp = { 'total': len(queryset), 'data': serializer.data }
            return api_response(ResponseCode.SUCCESS, '查询成功', resp)


class Common_userUserView(BaseUserView):
    model_serializer = Common_userSerializer
    model = Common_user
    

class AdminUserView(BaseUserView):
    model_serializer = AdminSerializer
    model = Admin


class Common_userBatchActivationView(APIView):
    """Common_userBatchActivation
        普通用户批量激活
    """
    # JWT校验
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ids = request.data['ids']
        # 兜底处理
        if len(ids) == 0:
            return api_response(ResponseCode.SUCCESS, '无用户！无需激活！')
        try:
            common_users = Common_user.objects.filter(id__in=ids)
        except Exception:
            return api_response(ResponseCode.BAD_REQUEST, '批量激活失败！有用户不存在，请重新操作！')
        # 更新是否激活字段
        common_users.update(is_active=True)
        return api_response(ResponseCode.SUCCESS, '批量激活成功')
        

class ChangePasswordBaseView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]
    # 需要在子类中设置具体的序列化器
    model_serializer = None 
    # 需要在子类中设置具体的Model
    model = None
    def put(self, request, **kwargs):
        """put 修改用户密码接口
        Args:
            request (Object): 请求参数
        """
        try:
            # 获取指定用户实例
            user = self.model.objects.get(id=kwargs['user_id'])
        except self.model.DoesNotExist:
            # 用户不存在，返回错误响应和 HTTP 404 Not Found 状态
            return api_response(ResponseCode.NOT_FOUND, '用户不存在！')
        # 序列化用户详情数据
        if user.password != request.data['old_password']:
            # 原密码错误
            return api_response(ResponseCode.BAD_REQUEST, '原密码错误！请重试！')
        else:
            user.password = request.data['new_password']
            user.save()
        return api_response(ResponseCode.SUCCESS, '修改密码成功')


class Common_userChangePasswordView(ChangePasswordBaseView):
    model_serializer = Common_userSerializer
    model = Common_user


class AdminChangePasswordView(ChangePasswordBaseView):
    model_serializer = AdminSerializer
    model = Admin


class UploadFileForCommon_userView(APIView):
    
    def __analysis_data(self, data):
        """__analysis_data 导入数据解析
        Returns:
            tuple: success_list: list, fail_list: list
        """
        success_list, fail_list = [], []
        for item in data:
            required_keys = ['common_user_id', 'name', 'gender', 'is_active']
            # 使用any()函数，如果任何一个键的值为None或'<NA>'，普通用户数据就放入失败组
            if any(item.get(key) is None for key in required_keys):
                fail_list.append(item)
            else:
                # 进行数据处理后，将数据放到成功组
                common_user_instance = Common_user()
                common_user_instance.common_user_id = item['common_user_id']
                common_user_instance.name = item['name']
                common_user_instance.username = item['username'] if item['username'] is not None else item['common_user_id']
                common_user_instance.password = item['password'] if item['password'] is not None else '123456'
                common_user_instance.gender = 'male' if item['gender'] == '男' else 'female'
                common_user_instance.is_active = True if item['is_active'] == '是' else False
                common_user_instance.phone = item['phone'] if item['phone'] is not None else ''
                common_user_instance.email = item['email'] if item['email'] is not None else ''
                success_list.append(common_user_instance)
        return success_list, fail_list
                

    def post(self, request):
        if 'Common_userTemplateFile' in request.FILES:
            excel_file = request.FILES['Common_userTemplateFile']
            try:
                # 导入并清洗数据
                df = pd.read_excel(excel_file)
                df = df.replace(np.NAN, None, regex=True)
                # df['学号'] = df['学号'].astype('Int32')
                # 数据转换，为每个字典添加一个 'row_number' 键
                list_of_dicts = []
                for index, row in df.iterrows():
                    row_dict = row.to_dict()
                    row_dict['row_number'] = index
                    list_of_dicts.append(row_dict)
                translated_data = [translate_fields(record, UPLOAD_STUDENT_MAPPING_TABLE) for record in list_of_dicts]
                # 数据解析处理
                success, fail = self.__analysis_data(translated_data)
                if success:
                    Common_user.objects.bulk_create(success)
                    if fail:
                        return api_response(ResponseCode.SUCCESS, 'Excel文件解析成功！部分新增成功！', { 'fail_list': fail })
                    else:
                        return api_response(ResponseCode.SUCCESS, 'Excel文件解析成功！全部新增成功！', { 'fail_list': fail })
                else:
                    return api_response(ResponseCode.BAD_REQUEST, 'Excel文件解析成功！全部新增失败！', { 'fail_list': fail })
            except Exception as e:
                return api_response(ResponseCode.INTERNAL_SERVER_ERROR, '解析失败！存在错误信息！请检查单元格类型和必填信息！')
        else:
            return api_response(ResponseCode.INTERNAL_SERVER_ERROR, '文件上传失败！')


if __name__ == '__main__':
    pass
