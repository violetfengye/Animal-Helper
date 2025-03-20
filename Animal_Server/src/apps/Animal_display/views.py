import os

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count, Q
from .models import animal_information
from .serializers import AnimalInformationSerializer
from src.utils.response_utils import ResponseCode, api_response

class AnimalListCreateView(APIView):
    """
    处理动物信息的获取和创建
    - GET: 获取所有动物信息
    - POST: 创建新的动物信息（包括图片上传）
    """
    # parser_classes = [MultiPartParser, FormParser]  # 允许上传文件

    def get(self, request):
        """获取所有动物信息"""
        animals = animal_information.objects.all()
        serializer = AnimalInformationSerializer(animals, many=True)
        return api_response(ResponseCode.SUCCESS, '获取成功', serializer.data)

    def post(self, request):
        """创建新的动物信息，包括图片上传"""
        animal_id = request.data.get('animal_id')

        if animal_information.objects.filter(animal_id=animal_id).exists():
            return api_response(ResponseCode.BAD_REQUEST, '创建失败！该 animal_id 已经存在！',
                                {'animal_id': ['此 animal_id 已存在']})

        serializer = AnimalInformationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return api_response(ResponseCode.CREATED, '创建成功', serializer.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败！请检查输入信息！', serializer.errors)

class AnimalDetailView(APIView):
    """
    查询单个动物信息
    """
    def get(self, request, animal_id):
        try:
            animal = animal_information.objects.get(animal_id=animal_id)
            serializer = AnimalInformationSerializer(animal)
            return api_response(ResponseCode.SUCCESS, "查询成功", serializer.data)
        except animal_information.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, "未找到该动物信息")

class AnimalUpdateView(APIView):
    """
    通过 POST 方式更新动物信息（模拟 PUT/PATCH）
    """
    def post(self, request, animal_id):
        try:
            animal = animal_information.objects.get(animal_id=animal_id)
            serializer = AnimalInformationSerializer(animal, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return api_response(ResponseCode.SUCCESS, "更新成功")
            else:
                return api_response(ResponseCode.BAD_REQUEST, "更新失败", serializer.errors)
        except animal_information.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, "该动物信息不存在")

class AnimalDeleteView(APIView):
    """
    通过 POST 方式删除动物信息（模拟 DELETE）
    """
    def post(self, request,animal_id):
        try:
            # 获取数据库记录
            animal = animal_information.objects.get(animal_id=animal_id)

            # 先保存图片路径
            image_path = animal.img.path if animal.img else None

            # 删除数据库中的记录
            animal.delete()

            # 删除对应的图片文件
            if image_path and os.path.exists(image_path):
                os.remove(image_path)  # 删除文件
                return api_response(ResponseCode.SUCCESS, "动物信息及图片删除成功")
            else:
                return api_response(ResponseCode.SUCCESS, "动物信息删除成功，但图片文件不存在")

        except animal_information.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, "该动物信息不存在")

class AnimalStatusStatsView(APIView):
    """
    统计不同状态的动物数量
    """
    def get(self, request):
        stats = animal_information.objects.values('status').annotate(count=Count('id'))
        return api_response(ResponseCode.SUCCESS, '统计成功', list(stats))

class AnimalImageUploadView(APIView):
    """
    上传动物图片
    """
    parser_classes = [MultiPartParser]

    def post(self, request, animal_id):
        try:
            animal = animal_information.objects.get(animal_id=animal_id)
            animal.img = request.FILES.get("img")
            animal.save()
            return api_response(ResponseCode.SUCCESS, "图片上传成功")
        except animal_information.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, "该动物信息不存在")


class AnimalFilteredListView(ListCreateAPIView):
    """
    过滤查询动物信息
    """
    serializer_class = AnimalInformationSerializer

    # 启用过滤、搜索和排序
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # 定义哪些字段可以被过滤
    filterset_fields = ['status', 'school']

    # 定义哪些字段可以被搜索
    search_fields = ['name', 'animal_id']

    # 定义哪些字段可以被排序
    ordering_fields = ['created_at', 'name']

    def get_queryset(self):
        # DRF 和 DjangoFilterBackend 自动处理过滤、搜索、排序等
        return animal_information.objects.all()