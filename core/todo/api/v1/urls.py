# dj
from django.urls import path

# rest
from rest_framework.routers import DefaultRouter

# internal
from todo.api.v1 import views

app_name = "api-v1"

urlpatterns = [
    path(
        "tasks/",
        views.ListAllTasksOrCreateNewTaskAPIView.as_view(),
        name="list-create-tasks",
    ),
    path(
        "tasks/<int:pk>",
        views.SingleTaskDetailAPIView.as_view(),
        name="single-task-detail",
    ),
    path(
        "category/",
        views.ListAllCategoriesOrCreateNew.as_view(),
        name="list-create-category",
    ),
    path(
        "category/<int:pk>",
        views.SingleCategoryDetailAPIView.as_view(),
        name="single-category-detail",
    ),
]

"""router = DefaultRouter()
router.register("tasks", views.TaskViewSet, basename="task")
router.register("categories", views.CategoryViewSet, basename="category")
urlpatterns += router.urls"""
