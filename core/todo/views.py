# dj
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import (
    ListView,
    # CreateView,
    # UpdateView,
    # DeleteView,
)
# from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# internal
from todo.models import Todo, Profile, TaskCategory
from todo.forms import CreateTaskForm, UpdateTaskForm
from django.core.paginator import Paginator


# Create your views here.
class BaseView(LoginRequiredMixin, View):
    """Base class for altering tasks"""
    tasks = Todo.objects.all()
    categories = TaskCategory.objects.all()


class TodoMainView(BaseView):
    """Todo app main view"""
    PAGE_NUMBER = 8

    def get(self, request):
        paginator = Paginator(self.tasks.filter(user__user__email=self.request.user), self.PAGE_NUMBER)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        profile = Profile.objects.get(user=request.user)
        user = request.user
        context = {
            'tasks': self.tasks.filter(user__user__email=self.request.user),
            'page_obj': page_obj,
            'user': user,
            'profile': profile,
            'categories': self.categories
        }
        return render(request, template_name='index.html', context=context)


class TaskCreateView(BaseView):
    """View for creating new tasks"""

    def post(self, request):
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = Profile.objects.filter(user__email=self.request.user)[0]
            new_task.save()
        return redirect('/')


class TaskDeletionView(BaseView):
    """View for deleting a task"""

    def get(self, request, pk):
        Todo.objects.filter(id=pk).delete()
        return redirect('/')


class TaskUpdateView(BaseView):
    """View for updating a task"""

    def get(self, request, pk, **kwargs):
        task_title = {'title': self.tasks.get(pk=pk).title}
        update_form = UpdateTaskForm(initial=task_title)
        context = {'form': update_form}
        return render(request, template_name='update.html', context=context)

    def post(self, request, pk, **kwargs):
        old_task = Todo.objects.get(pk=pk)
        form = UpdateTaskForm(request.POST, instance=old_task)
        if form.is_valid():
            form.save()
        return redirect('/')


class TaskStatusToggle(BaseView):
    """View for toggling a task status between completed/pending"""

    def get(self, request, pk, **kwargs):
        if self.tasks.get(pk=pk).completed:
            self.tasks.filter(pk=pk).update(completed=False)
        else:
            self.tasks.filter(pk=pk).update(completed=True)
        return redirect('/')






'''
class TodoMainView(LoginRequiredMixin, ListView):
    """Main view for todo app"""
    
    model = Todo
    template_name = 'index.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.filter(user__user__email__exact=self.request.user)
class CreateTask(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title']
    success_url = reverse_lazy('todo:main_todo')

    def form_valid(self, form):
        # Todo foreign key is profile and profile's foreign key is user, so current
        # user can not be used to refer to an instance for creating a new todo task
        form.instance.user = Profile.objects.filter(user__email=self.request.user)[0]
        return super(CreateTask, self).form_valid(form)


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy('todo:main_todo')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user__user__email__exact=self.request.user)


class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title']
    success_url = reverse_lazy('todo:main_todo')
'''
