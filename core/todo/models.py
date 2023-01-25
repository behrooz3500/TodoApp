from django.db import models
from accounts.models import Profile


class Todo(models.Model):
    """Todo model"""

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
