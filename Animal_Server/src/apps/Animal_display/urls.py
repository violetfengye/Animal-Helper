from django.urls import path
from .views import (
    AnimalListCreateView,
    AnimalDetailView,
    AnimalUpdateView,
    AnimalDeleteView,
    AnimalStatusStatsView,
    AnimalImageUploadView,
    AnimalFilteredListView
)

urlpatterns = [
    path("animals/", AnimalListCreateView.as_view(), name="animal_list_create"),
    path("animals/<str:animal_id>/", AnimalDetailView.as_view(), name="animal_detail"),
    path("animals/update/<str:animal_id>/", AnimalUpdateView.as_view(), name="animal_update"),  # POST 更新
    path("animals/delete/<str:animal_id>/", AnimalDeleteView.as_view(), name="animal_delete"),  # POST 删除
    path("animals/stats/", AnimalStatusStatsView.as_view(), name="animal_status_stats"),
    path("animals/<str:animal_id>/upload/", AnimalImageUploadView.as_view(), name="animal_image_upload"),
    path("animals/filter/", AnimalFilteredListView.as_view(), name="animal_filtered_list"),
]
