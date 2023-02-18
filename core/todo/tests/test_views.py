# dj
from django.urls import reverse

# internal
from .BaseTest import BaseTest

# rest
from rest_framework import status


class TestViewBase:

    def test_url_authorized_user_valid_data_successful_response(self):
        authorized_client = self.client
        authorized_client.force_login(self.user_object)
        # authorized_client.login(username="test@test.com", password="testpasswordA@1")
        # self.client.force_login(self.user_object)

        self.assertEqual(
            authorized_client.get(self.URL).status_code, status.HTTP_200_OK)

    def test_url_authorized_user_invalid_data_successful_response(self):
        pass

    def test_url_unauthorized_user_valid_data_response(self):
        pass

    def test_url_unauthorized_user_invalid_data_response(self):
        pass


class TestTodoMainView(TestViewBase, BaseTest):
    URL = reverse("todo:main_todo")
