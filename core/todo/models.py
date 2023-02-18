from django.db import models
from django.urls import reverse
from accounts.models import Profile


class TaskCategory(models.Model):
    """ Task category model"""
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Todo(models.Model):
    """Todo model"""

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    category = models.ForeignKey(TaskCategory, null=True, blank=True, on_delete=models.SET_NULL)
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def has_been_updated(self):
        if str(self.created_date)[0:18] == str(self.updated_date)[0:18]:
            return False
        else:
            return True

    def get_relative_api_url(self):
        return reverse("todo:api-v1:task-detail", kwargs={"pk": self.pk})




