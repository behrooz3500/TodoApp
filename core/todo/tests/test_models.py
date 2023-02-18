# internal
from ..models import Todo
from ..models import TaskCategory
from .BaseTest import BaseTest


class TestModelBase:

    def test_create_task_with_valid_data(self):

        task_object = self.MODEL.objects.create(
            **self.get_valid_date()
        )
        self.assertTrue(self.MODEL.objects.filter(pk=task_object.pk).exists())


class TestTodoModel(TestModelBase, BaseTest):

    MODEL = Todo

    def get_valid_date(self):
        return {
                "user": self.profile_object,
                "title": "test_task",
                "category": self.category_object,
                "completed": False,
        }


class TestCategoryModel(TestModelBase, BaseTest):

    MODEL = TaskCategory

    def get_valid_date(self):
        return {'name': 'test-category'}
