from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q, Max
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Project, Task, SubTask, JOB_STATUS
from .forms import ProjectForm, TaskForm, SubTaskForm
from teamflow.models import Team, TeamMember

# API views for Select2 autocomplete
@login_required
def user_search(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = 10
    
    users = User.objects.filter(
        Q(username__icontains=q) | 
        Q(first_name__icontains=q) | 
        Q(last_name__icontains=q) | 
        Q(email__icontains=q)
    ).distinct()
    
    # Pagination
    start = (page - 1) * page_size
    end = page * page_size
    total = users.count()
    
    results = []
    for user in users[start:end]:
        display_name = f"{user.get_full_name() or user.username}"
        results.append({
            'id': user.id,
            'text': display_name,
        })
    
    return JsonResponse({
        'results': results,
        'pagination': {
            'more': total > page * page_size
        }
    })

@login_required
def team_search(request):
    q = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    page_size = 10
    
    user = request.user
    teams = Team.objects.filter(
        Q(name__icontains=q) | 
        Q(description__icontains=q)
    ).filter(
        Q(teammember__user=user) | Q(is_public=True)
    ).distinct()
    
    # Pagination
    start = (page - 1) * page_size
    end = page * page_size
    total = teams.count()
    
    results = []
    for team in teams[start:end]:
        results.append({
            'id': team.id,
            'text': team.name,
        })
    
    return JsonResponse({
        'results': results,
        'pagination': {
            'more': total > page * page_size
        }
    })

@login_required
def team_member_search(request):
    q = request.GET.get('q', '')
    team_id = request.GET.get('team_id')
    page = int(request.GET.get('page', 1))
    page_size = 10
    
    query = Q(user__username__icontains=q) | Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q)
    
    if team_id:
        team_members = TeamMember.objects.filter(query, team_id=team_id)
    else:
        team_members = TeamMember.objects.filter(query)
    
    # Pagination
    start = (page - 1) * page_size
    end = page * page_size
    total = team_members.count()
    
    results = []
    for member in team_members[start:end]:
        display_name = f"{member.user.get_full_name() or member.user.username}"
        if member.handle:
            display_name = f"{display_name} ({member.handle})"
            
        results.append({
            'id': member.id,
            'text': display_name,
            'designation': member.designation,
        })
    
    return JsonResponse({
        'results': results,
        'pagination': {
            'more': total > page * page_size
        }
    })

class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projectflow/project_detail.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all().order_by('order', 'created_at')
        context['subprojects'] = self.object.subprojects.all()
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        # Show public projects or projects where user is a team member
        return queryset.filter(
            Q(is_public=True) | 
            Q(team__teammember__user=user) |
            Q(assigned_users=user) |
            Q(assigned_teams__teammember__user=user)
        ).distinct()

class ProjectList(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projectflow/project_list.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        user = self.request.user
        # Show public projects or projects where user is a team member
        return Project.objects.filter(
            Q(is_public=True) | 
            Q(team__teammember__user=user) |
            Q(assigned_users=user) |
            Q(assigned_teams__teammember__user=user)
        ).filter(
            parent__isnull=True  # Only show top-level projects
        ).distinct()

class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projectflow/project_form.html'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['team'].queryset = Team.objects.filter(teammember__user=user, teammember__is_manager=True)
        form.fields['parent'].queryset = Project.objects.filter(
            Q(is_public=True) | 
            Q(team__teammember__user=user, team__teammember__is_manager=True)
        ).distinct()
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
        
        # Exclude self and its subprojects from parent options to prevent circular references
        if self.object.pk:
            subproject_ids = [p.pk for p in self.object.get_all_subprojects()]
            subproject_ids.append(self.object.pk)
            form.fields['parent'].queryset = Project.objects.filter(
                Q(is_public=True) | 
                Q(team__teammember__user=user, team__teammember__is_manager=True)
            ).exclude(pk__in=subproject_ids).distinct()
        
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

@login_required
def project_timeline_view(request, slug):
    """View for displaying the project timeline"""
    project = get_object_or_404(Project, slug=slug)
    tasks = project.tasks.all().order_by('order', 'created_at')
    
    # Check if user has permission to view this project
    user = request.user
    if not (project.is_public or 
            TeamMember.objects.filter(user=user, team=project.team).exists() or
            user in project.assigned_users.all() or
            Team.objects.filter(teammember__user=user).filter(pk__in=project.assigned_teams.all()).exists()):
        return HttpResponseRedirect(reverse('projectflow:project-list'))
    
    return render(request, 'projectflow/project_timeline.html', {
        'project': project,
        'tasks': tasks,
    })

@login_required
def roadmap_list_view(request):
    """View for displaying all roadmaps"""
    user = request.user
    roadmaps = Project.objects.filter(
        project_type='roadmap'
    ).filter(
        Q(is_public=True) | 
        Q(team__teammember__user=user) |
        Q(assigned_users=user) |
        Q(assigned_teams__teammember__user=user)
    ).distinct()
    
    return render(request, 'projectflow/roadmap_list.html', {
        'roadmaps': roadmaps
    })

@login_required
def roadmap_detail_view(request, slug):
    """View for displaying a roadmap with its features (subprojects)"""
    roadmap = get_object_or_404(Project, slug=slug, project_type='roadmap')
    features = Project.objects.filter(parent=roadmap).order_by('due_date', 'name')
    
    # Check if user has permission to view this roadmap
    user = request.user
    if not (roadmap.is_public or 
            TeamMember.objects.filter(user=user, team=roadmap.team).exists() or
            user in roadmap.assigned_users.all() or
            Team.objects.filter(teammember__user=user).filter(pk__in=roadmap.assigned_teams.all()).exists()):
        return HttpResponseRedirect(reverse('projectflow:roadmap-list'))
    
    return render(request, 'projectflow/roadmap_detail.html', {
        'roadmap': roadmap,
        'features': features,
    })

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'projectflow/task_detail.html'
    context_object_name = 'task'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtasks'] = self.object.subtasks.all().order_by('order', 'created_at')
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        # Show tasks from public projects or projects where user is a team member
        return queryset.filter(
            Q(project__is_public=True) | 
            Q(project__team__teammember__user=user) |
            Q(assigned_users=user) |
            Q(assigned_teams__teammember__user=user) |
            Q(project__assigned_users=user) |
            Q(project__assigned_teams__teammember__user=user)
        ).distinct()

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "projectflow/task_list.html"
    context_object_name = 'tasks'
    
    def get_queryset(self):
        user = self.request.user
        # Show tasks from public projects or projects where user is a team member
        return Task.objects.filter(
            Q(project__is_public=True) | 
            Q(project__team__teammember__user=user) |
            Q(assigned_users=user) |
            Q(assigned_teams__teammember__user=user) |
            Q(project__assigned_users=user) |
            Q(project__assigned_teams__teammember__user=user)
        ).distinct().order_by('project', 'order', 'created_at')

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'projectflow/task_form.html'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        teams = Team.objects.filter(teammember__user=user)
        form.fields['project'].queryset = Project.objects.filter(
            Q(is_public=True) | 
            Q(team__in=teams) |
            Q(assigned_users=user) |
            Q(assigned_teams__in=teams)
        ).distinct()
        form.fields['team_member'].queryset = TeamMember.objects.filter(team__in=teams)
        
        # Pre-select project if provided in URL
        project_id = self.kwargs.get('project_id')
        if project_id:
            form.initial['project'] = project_id
            
            # Set the order to be the next available order
            project = Project.objects.get(pk=project_id)
            max_order = project.tasks.aggregate(Max('order'))['order__max'] or 0
            form.initial['order'] = max_order + 1
        
        return form
    
    def get_success_url(self):
        return reverse('projectflow:task-detail', kwargs={'pk': self.object.pk})

class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'projectflow/task_form.html'
    
    def test_func(self):
        task = self.get_object()
        user = self.request.user
        return (
            TeamMember.objects.filter(user=user, team=task.project.team).exists() or
            user in task.assigned_users.all() or
            user in task.project.assigned_users.all() or
            Team.objects.filter(teammember__user=user).filter(
                Q(pk__in=task.assigned_teams.all()) |
                Q(pk__in=task.project.assigned_teams.all())
            ).exists()
        )
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        teams = Team.objects.filter(teammember__user=user)
        form.fields['project'].queryset = Project.objects.filter(
            Q(is_public=True) | 
            Q(team__in=teams) |
            Q(assigned_users=user) |
            Q(assigned_teams__in=teams)
        ).distinct()
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
            form.fields['task'].queryset = Task.objects.filter(
                Q(project__is_public=True) | 
                Q(project__team__in=teams) |
                Q(assigned_users=user) |
                Q(assigned_teams__in=teams) |
                Q(project__assigned_users=user) |
                Q(project__assigned_teams__in=teams)
            ).distinct()
            form.fields['team_member'].queryset = TeamMember.objects.filter(team=task.project.team)
            
            # Set the order to be the next available order
            max_order = task.subtasks.aggregate(Max('order'))['order__max'] or 0
            form.initial['order'] = max_order + 1
        else:
            form.fields['task'].queryset = Task.objects.filter(
                Q(project__is_public=True) | 
                Q(project__team__in=teams) |
                Q(assigned_users=user) |
                Q(assigned_teams__in=teams) |
                Q(project__assigned_users=user) |
                Q(project__assigned_teams__in=teams)
            ).distinct()
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
        user = self.request.user
        return (
            TeamMember.objects.filter(user=user, team=subtask.task.project.team).exists() or
            user in subtask.assigned_users.all() or
            user in subtask.task.assigned_users.all() or
            user in subtask.task.project.assigned_users.all()
        )
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        teams = Team.objects.filter(teammember__user=user)
        form.fields['task'].queryset = Task.objects.filter(
            Q(project__is_public=True) | 
            Q(project__team__in=teams) |
            Q(assigned_users=user) |
            Q(assigned_teams__in=teams) |
            Q(project__assigned_users=user) |
            Q(project__assigned_teams__in=teams)
        ).distinct()
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
        if new_status in dict(JOB_STATUS).keys():
            task.status = new_status
            task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('projectflow:task-detail', kwargs={'pk': pk})))

@login_required
def update_subtask_status(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(JOB_STATUS).keys():
            subtask.status = new_status
            subtask.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('projectflow:task-detail', kwargs={'pk': subtask.task.pk})))

@login_required
@require_POST
@csrf_exempt
def reorder_tasks(request, project_slug):
    """API endpoint for reordering tasks via drag and drop"""
    try:
        project = get_object_or_404(Project, slug=project_slug)
        data = json.loads(request.body)
        task_order = data.get('taskOrder', [])
        
        # Check if user has permission to modify this project
        user = request.user
        if not (TeamMember.objects.filter(user=user, team=project.team).exists() or
                user in project.assigned_users.all()):
            return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
        
        # Update the order of each task
        for index, task_id in enumerate(task_order):
            Task.objects.filter(pk=task_id, project=project).update(order=index)
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@require_POST
@csrf_exempt
def reorder_subtasks(request, task_id):
    """API endpoint for reordering subtasks via drag and drop"""
    try:
        task = get_object_or_404(Task, pk=task_id)
        data = json.loads(request.body)
        subtask_order = data.get('subtaskOrder', [])
        
        # Check if user has permission to modify this task
        user = request.user
        if not (TeamMember.objects.filter(user=user, team=task.project.team).exists() or
                user in task.assigned_users.all() or
                user in task.project.assigned_users.all()):
            return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
        
        # Update the order of each subtask
        for index, subtask_id in enumerate(subtask_order):
            SubTask.objects.filter(pk=subtask_id, task=task).update(order=index)
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
