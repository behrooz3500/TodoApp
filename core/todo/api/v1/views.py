# rest
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# internal
from .serializers import TodoSerializer, CategorySerializer
from todo.models import Todo, TaskCategory
from .permissions import IsOwnerOrReadOnly
from .paginations import TaskListPagination
from .filters import TaskFilter


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    search_filter = filters.SearchFilter
    ordering_filter = filters.OrderingFilter
    filter_backends = [DjangoFilterBackend, search_filter, ordering_filter]
    filterset_class = TaskFilter
    filterset_fields = {
        'category': ["in", 'exact'],
        'completed': ['exact'],
        'user': ['exact']
    }
    search_fields = ['title']
    ordering_fields = ['created_date', 'updated_date']
    pagination_class = TaskListPagination

    @action(methods=['GET'], detail=False)
    def get_completed_tasks(self, request):
        queryset = self.queryset.filter(completed=True)
        serializer = TodoSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = TaskCategory.objects.all()
