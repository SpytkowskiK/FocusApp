from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q


class CustomLoginView(LoginView):
    template_name = 'focus_website/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterView(FormView):
    template_name = 'focus_website/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterView, self).get(*args, **kwargs)


class CustomLogoutView(LogoutView):
    next_page = 'login'


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            context = super().get_context_data(**kwargs)
            context['tasks'] = context['tasks']
            context['count'] = context['tasks']

            search_input = self.request.GET.get('search') or ''
            if search_input:
                context['tasks'] = context['tasks'].filter(
                    Q(title__icontains=search_input) |
                    Q(user__username__icontains = search_input)
                )
                context['search_input'] = search_input
        else:
            context = super().get_context_data(**kwargs)
            context['tasks'] = context['tasks'].filter(user=self.request.user)
            context['count'] = context['tasks'].filter(complete=False).count()

            search_input = self.request.GET.get('search') or ''
            if search_input:
                context['tasks'] = context['tasks'].filter(
                    Q(title__icontains=search_input) |
                    Q(user__username__icontains=search_input)
                )
                context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'focus_website/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')
    

class PersonalCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete', 'deadline']
    success_url = reverse_lazy('tasks')
    template_name = 'focus_website/personal_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PersonalCreate, self). form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class PersonalTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'deadline']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'focus_website/task_delete.html'
