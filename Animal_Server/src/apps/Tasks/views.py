from datetime import timedelta

from datetime import datetime

import django_filters
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import task_information as Task
from .serializers import TaskInformationSerializer
from src.utils.response_utils import ResponseCode, api_response
from ..UserManagement.models import Common_user, Admin
from django.db.models import Q


# 任务列表视图（GET: 获取任务列表，POST: 创建任务）
class TaskListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = TaskInformationSerializer

    def get(self, request, *args, **kwargs):
        """
        获取任务列表
        """
        tasks = self.get_queryset()
        serializer = self.get_serializer(tasks, many=True)
        return api_response(ResponseCode.SUCCESS, "获取任务列表成功", serializer.data)

    def post(self, request, *args, **kwargs):
        """
        创建新任务（仅管理员可用）
        """
        if request.user.role != "Admin":
            return api_response(ResponseCode.FORBIDDEN, "权限不足，仅管理员可以创建任务")

        administrator = Admin.objects.get(id=request.user.id)
        data = request.data.copy()
        data["task_publisher_id"] = administrator.admin_id
        request._full_data = data

        # 调用父类的post方法来创建任务
        response = super().post(request, *args, **kwargs)

        return api_response(ResponseCode.SUCCESS, "任务创建成功", response.data)


# 任务详情视图（GET: 获取任务详情，PATCH: 更新任务，DELETE: 删除任务）
class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskInformationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'task_id'

    def get(self, request, *args, **kwargs):
        """
        获取指定任务的详情
        """
        response = super().get(request, *args, **kwargs)
        return api_response(ResponseCode.SUCCESS, "获取成功", response.data)

    def patch(self, request, *args, **kwargs):
        """
        更新任务信息（仅管理员可用）
        """
        if request.user.role != "Admin":
            return api_response(ResponseCode.FORBIDDEN, "权限不足，仅管理员可以更新任务")

        response = super().patch(request, *args, **kwargs)
        return api_response(ResponseCode.SUCCESS, "任务更新成功", response.data)

    def delete(self, request, *args, **kwargs):
        """
        删除任务（仅管理员可用）
        """
        if request.user.role != "Admin":
            return api_response(ResponseCode.FORBIDDEN, "权限不足，仅管理员可以删除任务")

        super().delete(request, *args, **kwargs)
        return api_response(ResponseCode.SUCCESS, "任务删除成功")


# 用户接取任务视图
class TaskTakeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id, *args, **kwargs):
        """
        用户接取任务，更新任务状态为进行中，并将任务接取人设置为当前用户的ID
        """
        if request.user.role != "Common_user":
            return api_response(ResponseCode.FORBIDDEN, "权限不适，仅普通用户可以接取任务")

        try:
            task = Task.objects.get(task_id=task_id)
        except Task.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, "任务未找到")

        if task.status != "未被接取" or not task.is_published:
            return api_response(ResponseCode.BAD_REQUEST, "任务不可接取，当前状态不允许接取")

        try:
            user = Common_user.objects.get(id=request.user.id)
        except Common_user.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, "用户未找到")

        # 任务接取后更新
        task.status = "进行中"
        task.task_taker_id = user.common_user_id  # 设置任务接取人
        task.save()

        return api_response(ResponseCode.SUCCESS, "任务接取成功", TaskInformationSerializer(task).data)


# 用户完成任务视图
class TaskCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id, *args, **kwargs):
        """
        用户完成任务，更新任务状态为已完成，待确认
        """
        if request.user.role != "Common_user":
            return api_response(ResponseCode.FORBIDDEN, "权限不足，仅普通用户可以完成任务")

        try:
            task = Task.objects.get(task_id=task_id)
        except Task.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, "任务未找到")

        if task.status != "进行中" and task.status != "被驳回":
            return api_response(ResponseCode.BAD_REQUEST, "任务无法完成，当前状态不允许")

        task.status = "已完成，待确认"
        task.save()

        return api_response(ResponseCode.SUCCESS, "任务完成，等待管理员确认")

# 任务确认完成
class TaskToCompleteFinally(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id, *args, **kwargs):
        """
        # 任务确认完成
        """
        if request.user.role != "Admin":
            return api_response(ResponseCode.FORBIDDEN, "权限不足，仅管理员可以确认完成任务")

        try:
            task = Task.objects.get(task_id=task_id)
        except Task.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, "任务未找到")

        administer = Admin.objects.get(admin_id=task.task_publisher_id)
        if request.user.id!= administer.id:
            return api_response(ResponseCode.FORBIDDEN, "权限不足，只有任务发布者可以确认完成任务")

        user = Common_user.objects.get(common_user_id=task.task_taker_id)
        user.points += task.points
        task.status = "确认完成"
        task.save()
        user.save()

        return api_response(ResponseCode.SUCCESS, "任务确认完成，积分已添加")

# 任务驳回
class TaskToBack(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, task_id, *args, **kwargs):
        """
        # 任务被驳回
        """
        if request.user.role != "Admin":
            return api_response(ResponseCode.FORBIDDEN, "权限不足，仅管理员可以确认完成任务")

        try:
            task = Task.objects.get(task_id=task_id)
        except Task.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, "任务未找到")

        now_admin = Admin.objects.get(id=request.user.id)
        administer = Admin.objects.get(admin_id=task.task_publisher_id)
        if now_admin != administer:
            return api_response(ResponseCode.FORBIDDEN, "权限不足，只有任务发布者可以确认完成任务")

        task.status = "被驳回"
        task.save()

        return api_response(ResponseCode.SUCCESS, "任务成功被驳回")

# 获取指定用户所有的任务
class UserTasksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id, *args, **kwargs):
        """
        获取指定用户的所有任务
        """
        user_id=Common_user.objects.get(id=user_id).common_user_id
        try:
            # 查找当前用户关联的所有任务
            tasks = Task.objects.filter(task_taker_id=user_id)

            # 如果用户没有任务
            if not tasks.exists():
                return api_response(ResponseCode.NOT_FOUND, "没有找到该用户的任务")

            # 序列化任务数据
            serialized_tasks = TaskInformationSerializer(tasks, many=True)

            # 返回任务数据
            return api_response(ResponseCode.SUCCESS, "任务列表获取成功", serialized_tasks.data)

        except Exception as e:
            return api_response(ResponseCode.INTERNAL_SERVER_ERROR, f"获取任务列表失败: {str(e)}")

# 管理员发布任务
class TaskPublishView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,task_id, *args, **kwargs):
        """
        发布任务，设置截止日期并进行校验
        """
        if request.user.role != "Admin":
            return api_response(ResponseCode.FORBIDDEN, "权限不足，仅管理员可以发布任务")

        try:
            task = Task.objects.get(task_id=task_id)
        except Task.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, "任务未找到")

        user = Admin.objects.get(id=request.user.id)
        # 校验管理员是否为自己创建任务
        task_publisher_id = task.task_publisher_id  # 获取任务发布者的 ID
        if task_publisher_id != user.admin_id:
            return api_response(ResponseCode.FORBIDDEN, "管理员不能发布其他管理员的任务")

        task = Task.objects.get(task_id=task_id)
        task.is_published = True
        task.status="未被接取"
        task.save()

        return api_response(ResponseCode.SUCCESS, "任务发布成功", TaskInformationSerializer(task).data)

class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ['title', 'status']

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskInformationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def list(self, request, *args, **kwargs):
        """
        重写 list 方法，用于返回任务列表
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_response(ResponseCode.SUCCESS, "任务列表获取成功", serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        重写 retrieve 方法，用于返回单个任务详情
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(ResponseCode.SUCCESS, "任务详情获取成功", serializer.data)

    def create(self, request, *args, **kwargs):
        """
        重写 create 方法，用于创建新任务
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return api_response(ResponseCode.CREATED, "任务创建成功", serializer.data)

    def update(self, request, *args, **kwargs):
        """
        重写 update 方法，用于更新任务信息
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # 如果使用了 prefetch_related，需要使预取缓存失效
            instance._prefetched_objects_cache = {}

        return api_response(ResponseCode.SUCCESS, "任务更新成功", serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        重写 destroy 方法，用于删除任务
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_response(ResponseCode.NO_CONTENT, "任务删除成功")

# def check_task_overdue():
#     """
#     定时任务检查任务是否逾期，若逾期更新任务状态
#     """
#     now = timezone.now()
#     overdue_tasks = Task.objects.filter(
#         Q(status="进行中") & Q(deadline__lt=now)  # 已开始且已过截止日期的任务
#     )
#
#     for task in overdue_tasks:
#         task.status = "已逾期"
#         task.save()
#
#         # 扣除积分，假设积分为任务积分的一半
#         user = Common_user.objects.get(common_user_id=task.task_taker_id)  # 获取任务接取者
#         if user:
#             user.points -= task.points // 2  # 扣除积分
#             user.save()
#
#     print(f"Checked overdue tasks: {overdue_tasks.count()}")




