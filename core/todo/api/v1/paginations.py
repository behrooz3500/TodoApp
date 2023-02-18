# rest
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# internal
from todo.models import Todo


class TaskListPagination(PageNumberPagination):
    """Custom pagination class for listing all tasks"""

    page_size = 4

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "Total tasks": self.page.paginator.count,
                "Completed tasks": Todo.objects.filter(completed=True).count(),
                "results": data,
            }
        )
