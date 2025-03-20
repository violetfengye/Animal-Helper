from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks_filter', TaskViewSet)
urlpatterns = [
    # 获取任务列表和创建任务（仅管理员）
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    # 获取、更新、删除任务的视图（任务详情）
    path('tasks/<str:task_id>/', views.TaskDetailView.as_view(), name='task-detail'),
    # 用户接取任务
    path('tasks/<str:task_id>/take/', views.TaskTakeView.as_view(), name='task-take'),
    # 用户完成任务
    path('tasks/<str:task_id>/complete/', views.TaskCompleteView.as_view(), name='task-complete'),
    # 管理员确认任务完成
    path('tasks/<str:task_id>/confirm-complete/', views.TaskToCompleteFinally.as_view(), name='task-confirm-complete'),
    # 管理员驳回任务
    path('tasks/<str:task_id>/reject/', views.TaskToBack.as_view(), name='task-reject'),
    # 获取指定用户所有任务
    path('user/<str:user_id>/tasks/', views.UserTasksView.as_view(), name='user-tasks'),
    # 管理员发布任务
    path('tasks/publish/<str:task_id>/', views.TaskPublishView.as_view(), name='task-publish'),
    path('', include(router.urls)),
]
