from django.test import TestCase, Client, TransactionTestCase

# internal
from ..models import TaskCategory
from accounts.models import User, Profile


class BaseTest(TestCase):
    URL = ""
    FORM = None
    MODEL = None
    METHOD = []

    def setUp(self):
        self.title = "test_title"
        self.user_object = User.objects.create_user(
            email="test@test.com", password="testpasswordA@1", is_verified=True
        )

        self.profile_object = Profile.objects.create(
            user=self.user_object,
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
        )

        self.category_object = TaskCategory.objects.create(
            name="test_category2",
        )
        self.client = Client()

    def get_url_response_status_code(self):
        return self.client.get(self.URL).status_code

    def get_valid_data(self):
        return dict()

    def get_invalid_data(self):
        return dict()
