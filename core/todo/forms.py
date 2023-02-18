from unicodedata import category

from django.forms import ModelForm
from todo.models import Todo


class CreateTaskForm(ModelForm):
    """Form for creating new tasks"""
    class Meta:
        model = Todo
        fields = ['title', 'category', ]


class UpdateTaskForm(ModelForm):
    """Form for updating Tasks"""
    class Meta:
        model = Todo
        fields = ['title', 'category', ]
