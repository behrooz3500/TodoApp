# rest
from rest_framework.routers import DefaultRouter

# internal
from todo.api.v1 import views

app_name = 'api-v1'

urlpatterns = [
]

router = DefaultRouter()
router.register('tasks', views.TaskViewSet, basename='task')
router.register('categories', views.CategoryViewSet, basename='category')
urlpatterns += router.urls
