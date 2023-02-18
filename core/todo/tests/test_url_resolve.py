# dj
from django.test import TestCase
from django.urls import reverse, resolve

# internal
from todo.views import (
    TodoMainView,
    TaskCreateView,
    TaskDeletionView,
    TaskUpdateView,
    TaskStatusToggle,
)


# Create your tests here.
class BaseUrlTest(TestCase):
    pk = 1

    def check_url_resolve_without_pk(self, url, class_name):
        self.url = reverse(url)
        self.assertEqual(resolve(self.url).func.view_class, class_name)

    def check_url_resolve_with_pk(self, url, class_name):
        self.url = reverse(url, kwargs={"pk": self.pk})
        self.assertEqual(resolve(self.url).func.view_class, class_name)


class TestUrl(BaseUrlTest):
    def test_todo_index_url_resolve(self):
        """Check whether todo:index resolves to TodoMainView class"""
        self.check_url_resolve_without_pk("todo:main_todo", TodoMainView)

    def test_task_create_url_resolve(self):
        """Check whether todo:create resolves to TaskCreateView class"""
        self.check_url_resolve_without_pk("todo:create_task", TaskCreateView)

    def test_task_delete_url_resolve(self):
        """Check whether todo:delete resolves to TaskDeletionView class"""
        self.check_url_resolve_with_pk("todo:delete_task", TaskDeletionView)

    def test_task_update_url_resolve(self):
        """Check whether todo:update_task resolves to TaskUpdateView class"""
        self.check_url_resolve_with_pk("todo:update_task", TaskUpdateView)

    def test_task_status_toggle_url_resolve(self):
        """Check whether todo:toggle resolves to TaskStatusToggle class"""
        self.check_url_resolve_with_pk("todo:toggle", TaskStatusToggle)
