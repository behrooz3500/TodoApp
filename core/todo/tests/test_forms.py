# internal
from ..forms import CreateTaskForm, UpdateTaskForm
from .BaseTest import BaseTest


class BaseFormTest:
    def test_create_task_form_with_valid_data(self):
        form = self.FORM(data={"title": self.title, "category": self.category_object})
        self.assertTrue(form.is_valid())

    def test_create_task_form_with_no_data(self):
        form = self.FORM(data={})
        self.assertFalse(form.is_valid())

    def test_create_task_form_with_empty_title(self):
        form = self.FORM(data={"title": "", "category": self.category_object})
        self.assertFalse(form.is_valid())

    def test_create_task_form_with_no_category(self):
        form1 = self.FORM(data={"title": "", "category": ""})
        form2 = self.FORM(
            data={
                "title": "",
            }
        )
        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())


class TestTodoCreateForms(BaseFormTest, BaseTest):
    FORM = CreateTaskForm


class TestTodoUpdateForms(BaseFormTest, BaseTest):
    FORM = UpdateTaskForm
