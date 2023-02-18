# dj
from django.urls import reverse

# rest
from rest_framework.test import APIClient
from rest_framework import status

# internal
from .BaseTest import BaseTest
from ..models import Todo


class BaseModelAPI(BaseTest):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.url = reverse(self.URL)
        self.task = Todo.objects.create(
            user=self.profile_object,
            title="test-task",
            category=self.category_object,
            completed=False,
        )
        self.put_url = reverse(self.PUT_URL, kwargs={"pk": self.task.pk})


class BaseModelAPITest:
    def test_get_model_response_200_authorized_user(self):
        self.client.force_login(self.user_object)
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_get_model_response_401_unauthorized_user(self):
        response = self.client.get(self.url)
        assert response.status_code == 401

    def test_create_task_with_valid_data_authorized_user(self):
        self.client.force_login(self.user_object)
        data = self.get_valid_data()
        response = self.client.post(self.url, data)
        assert response.status_code == 201

    def test_create_task_with_valid_data_unauthorized_user(self):
        data = self.get_valid_data()
        response = self.client.post(self.url, data)
        assert response.status_code == 401

    def test_create_task_with_invalid_data_authorized_user(self):
        self.client.force_login(self.user_object)
        data = self.get_invalid_data()
        response = self.client.post(self.url, data)
        assert response.status_code == 400

    def test_remove_object(self):
        self.client.force_login(self.user_object)
        task_pk = Todo.objects.get(pk=self.task.pk).pk
        response = self.client.delete(self.put_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_object_with_valid_data(self):
        self.client.force_login(self.user_object)
        data = self.get_valid_data()
        response = self.client.put(self.put_url, data)
        assert response.status_code == 200


class TestTaskAPI(BaseModelAPITest, BaseModelAPI):
    URL = "todo:api-v1:list-create-tasks"
    PUT_URL = "todo:api-v1:single-task-detail"

    def get_valid_data(self):
        return {
            "title": "test-title",
            "category": self.category_object.pk,
            "completed": False,
        }

    def get_invalid_data(self):
        return {"category": self.category_object.pk, "completed": False}


class TestCategoryAPI(BaseModelAPITest, BaseModelAPI):
    URL = "todo:api-v1:list-create-category"
    PUT_URL = "todo:api-v1:single-category-detail"

    def get_valid_data(self):
        return {
            "name": "test-title",
        }

    def get_invalid_data(self):
        return {
            "name": "",
        }
