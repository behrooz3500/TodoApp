# rest
from django_filters import rest_framework as rest_filters

# internal
from todo.models import Todo


class TaskFilter(rest_filters.FilterSet):
    """Filtering tasks based on created dates."""

    initial_date = rest_filters.DateFilter(field_name="created_date", lookup_expr="gte")

    final_date = rest_filters.DateFilter(field_name="created_date", lookup_expr="lte")

    class Meta:
        model = Todo
        fields = ["category", "completed", "user"]
