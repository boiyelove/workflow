from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Project, Task, SubTask
from .forms import ProjectForm, TaskForm, SubTaskForm
from teamflow.models import Team, TeamMember

class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projectflow/project_detail.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all()
        return context

class ProjectList(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projectflow/project_list.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        user = self.request.user
        teams = Team.objects.filter(teammember__user=user)
        return Project.objects.filter(team__in=teams)

class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projectflow/project_form.html'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['team'].queryset = Team.objects.filter(teammember__user=user, teammember__is_manager=True)
        return form
    
    def get_success_url(self):
        return reverse('projectflow:project-detail', kwargs={'slug': self.object.slug})

class ProjectUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projectflow/project_form.html'
    
    def test_func(self):
        project = self.get_object()
        return TeamMember.objects.filter(
            user=self.request.user,
            team=project.team,
            is_manager=True
        ).exists()
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['team'].queryset = Team.objects.filter(teammember__user=user, teammember__is_manager=True)
        return form
    
    def get_success_url(self):
        return reverse('projectflow:project-detail', kwargs={'slug': self.object.slug})

class ProjectDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'projectflow/project_confirm_delete.html'
    success_url = reverse_lazy('projectflow:project-list')
    
    def test_func(self):
        project = self.get_object()
        return TeamMember.objects.filter(
            user=self.request.user,
            team=project.team,
            is_manager=True
        ).exists()

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'projectflow/task_detail.html'
    context_object_name = 'task'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtasks'] = self.object.subtasks.all()
        return context

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "projectflow/task_list.html"
    context_object_name = 'tasks'
    
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(team_member__user=user)

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'projectflow/task_form.html'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        teams = Team.objects.filter(teammember__user=user)
        form.fields['project'].queryset = Project.objects.filter(team__in=teams)
        form.fields['team_member'].queryset = TeamMember.objects.filter(team__in=teams)
        
        # Pre-select project if provided in URL
        project_id = self.kwargs.get('project_id')
        if project_id:
            form.initial['project'] = project_id
        
        return form
    
    def get_success_url(self):
        return reverse('projectflow:task-detail', kwargs={'pk': self.object.pk})

class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'projectflow/task_form.html'
    
    def test_func(self):
        task = self.get_object()
        return TeamMember.objects.filter(
            user=self.request.user,
            team=task.project.team,
        ).exists()
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        teams = Team.objects.filter(teammember__user=user)
        form.fields['project'].queryset = Project.objects.filter(team__in=teams)
        form.fields['team_member'].queryset = TeamMember.objects.filter(team__in=teams)
        return form
    
    def get_success_url(self):
        return reverse('projectflow:task-detail', kwargs={'pk': self.object.pk})

class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'projectflow/task_confirm_delete.html'
    
    def test_func(self):
        task = self.get_object()
        return TeamMember.objects.filter(
            user=self.request.user,
            team=task.project.team,
            is_manager=True
        ).exists()
    
    def get_success_url(self):
        return reverse('projectflow:project-detail', kwargs={'slug': self.object.project.slug})

class SubTaskCreate(LoginRequiredMixin, CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'projectflow/subtask_form.html'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        teams = Team.objects.filter(teammember__user=user)
        
        # Pre-select task if provided in URL
        task_id = self.kwargs.get('task_id')
        if task_id:
            task = get_object_or_404(Task, id=task_id)
            form.initial['task'] = task
            form.fields['task'].queryset = Task.objects.filter(project__team__in=teams)
            form.fields['team_member'].queryset = TeamMember.objects.filter(team=task.project.team)
        else:
            form.fields['task'].queryset = Task.objects.filter(project__team__in=teams)
            form.fields['team_member'].queryset = TeamMember.objects.filter(team__in=teams)
        
        return form
    
    def get_success_url(self):
        return reverse('projectflow:task-detail', kwargs={'pk': self.object.task.pk})

class SubTaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'projectflow/subtask_form.html'
    
    def test_func(self):
        subtask = self.get_object()
        return TeamMember.objects.filter(
            user=self.request.user,
            team=subtask.task.project.team
        ).exists()
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        teams = Team.objects.filter(teammember__user=user)
        form.fields['task'].queryset = Task.objects.filter(project__team__in=teams)
        form.fields['team_member'].queryset = TeamMember.objects.filter(team__in=teams)
        return form
    
    def get_success_url(self):
        return reverse('projectflow:task-detail', kwargs={'pk': self.object.task.pk})

class SubTaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SubTask
    template_name = 'projectflow/subtask_confirm_delete.html'
    
    def test_func(self):
        subtask = self.get_object()
        return TeamMember.objects.filter(
            user=self.request.user,
            team=subtask.task.project.team,
            is_manager=True
        ).exists()
    
    def get_success_url(self):
        return reverse('projectflow:task-detail', kwargs={'pk': self.object.task.pk})

@login_required
def update_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(task.JOB_STATUS).keys():
            task.status = new_status
            task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('projectflow:task-detail', kwargs={'pk': pk})))

@login_required
def update_subtask_status(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(subtask.JOB_STATUS).keys():
            subtask.status = new_status
            subtask.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('projectflow:task-detail', kwargs={'pk': subtask.task.pk})))
