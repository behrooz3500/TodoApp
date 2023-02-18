from django.contrib import admin
from todo.models import Todo, TaskCategory


# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    model = Todo
    list_display = (
        "user",
        "title",
        "completed",
        "created_date",
        "updated_date",
    )

    list_filter = (
        "user",
        "completed",
    )
    search_fields = (
        "user",
        "title",
    )
    ordering = ("created_date",)


@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    model = TaskCategory
    list_display = ("name",)
