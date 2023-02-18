from django.urls import path, include
from todo.views import (
    TodoMainView,
    # CreateTask,
    # DeleteTask,
    # UpdateTask,
    TodoMainView,
    TaskCreateView,
    TaskDeletionView,
    TaskUpdateView,
    TaskStatusToggle,
)

app_name = 'todo'
urlpatterns = [
    # path('', TodoMainView.as_view(), name='main_todo'),
    # path('create/', CreateTask.as_view(), name='create_task'),
    # path('delete/<int:pk>/', DeleteTask.as_view(), name='delete_task'),
    # path('update/<int:pk>/', UpdateTask.as_view(), name='update_task'),
    path('', TodoMainView.as_view(), name='main_todo'),
    path('create/', TaskCreateView.as_view(), name='create_task'),
    path('delete/<int:pk>/', TaskDeletionView.as_view(), name='delete_task'),
    path('update/<int:pk>', TaskUpdateView.as_view(), name='update_task'),
    path('change/<int:pk>', TaskStatusToggle.as_view(), name='toggle'),
    path('api/v1/', include('todo.api.v1.urls')),
]

