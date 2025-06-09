from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Max
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Project, Task, SubTask, JOB_STATUS

@login_required
def project_list(request):
    """View for listing projects"""
    projects = Project.objects.filter(
        Q(is_public=True) | 
        Q(team__members__user=request.user) |
        Q(assigned_users=request.user) |
        Q(assigned_teams__members__user=request.user)
    ).distinct()
    
    return render(request, 'projectflow/project_list_reimagined.html', {'projects': projects})

@login_required
def project_detail(request, slug):
    """View for project details"""
    project = get_object_or_404(Project, slug=slug)
    
    # Check if user has access to this project
    if not (project.is_public or 
            project.team and project.team.members.filter(user=request.user).exists() or
            project.assigned_users.filter(id=request.user.id).exists() or
            project.assigned_teams.filter(members__user=request.user).exists()):
        messages.error(request, "You don't have access to this project.")
        return redirect('projectflow:project-list')
    
    return render(request, 'projectflow/project_detail.html', {'project': project})

@login_required
def project_create(request):
    """View for creating a project"""
    # Placeholder for now
    return redirect('projectflow:project-list')

@login_required
def project_update(request, slug):
    """View for updating a project"""
    # Placeholder for now
    return redirect('projectflow:project-detail', slug=slug)

@login_required
def project_delete(request, slug):
    """View for deleting a project"""
    # Placeholder for now
    return redirect('projectflow:project-list')

@login_required
def project_timeline_view(request, slug):
    """View for displaying the project timeline"""
    project = get_object_or_404(Project, slug=slug)
    tasks = project.tasks.all().order_by('order', 'created_at')
    
    # Check if user has access to this project
    if not (project.is_public or 
            project.team and project.team.members.filter(user=request.user).exists() or
            project.assigned_users.filter(id=request.user.id).exists() or
            project.assigned_teams.filter(members__user=request.user).exists()):
        messages.error(request, "You don't have access to this project.")
        return redirect('projectflow:project-list')
    
    return render(request, 'projectflow/project_timeline.html', {
        'project': project,
        'tasks': tasks,
    })

@login_required
def project_task_board(request, slug):
    """View for project task board (Trello-like interface)"""
    project = get_object_or_404(Project, slug=slug)
    
    # Check if user has access to this project
    if not (project.is_public or 
            project.team and project.team.members.filter(user=request.user).exists() or
            project.assigned_users.filter(id=request.user.id).exists() or
            project.assigned_teams.filter(members__user=request.user).exists()):
        messages.error(request, "You don't have access to this project.")
        return redirect('projectflow:project-list')
    
    # Get tasks grouped by status
    todo_tasks = project.tasks.filter(status='Todo').order_by('order')
    doing_tasks = project.tasks.filter(status='Doing').order_by('order')
    done_tasks = project.tasks.filter(status='Done').order_by('order')
    
    return render(request, 'projectflow/task_board.html', {
        'project': project,
        'todo_tasks': todo_tasks,
        'doing_tasks': doing_tasks,
        'done_tasks': done_tasks,
    })

@login_required
def roadmap_list_view(request):
    """View for displaying all roadmaps"""
    roadmaps = Project.objects.filter(
        project_type='roadmap'
    ).filter(
        Q(is_public=True) | 
        Q(team__members__user=request.user) |
        Q(assigned_users=request.user) |
        Q(assigned_teams__members__user=request.user)
    ).distinct()
    
    return render(request, 'projectflow/roadmap_list.html', {
        'roadmaps': roadmaps
    })

@login_required
def roadmap_detail_view(request, slug):
    """View for displaying a roadmap with its features (subprojects)"""
    roadmap = get_object_or_404(Project, slug=slug, project_type='roadmap')
    features = Project.objects.filter(parent=roadmap).order_by('due_date', 'name')
    
    # Check if user has access to this roadmap
    if not (roadmap.is_public or 
            roadmap.team and roadmap.team.members.filter(user=request.user).exists() or
            roadmap.assigned_users.filter(id=request.user.id).exists() or
            roadmap.assigned_teams.filter(members__user=request.user).exists()):
        messages.error(request, "You don't have access to this roadmap.")
        return redirect('projectflow:roadmap-list')
    
    return render(request, 'projectflow/roadmap_detail.html', {
        'roadmap': roadmap,
        'features': features,
    })

@login_required
def task_list(request):
    """View for listing tasks"""
    tasks = Task.objects.filter(
        Q(project__is_public=True) | 
        Q(project__team__members__user=request.user) |
        Q(assigned_users=request.user) |
        Q(assigned_teams__members__user=request.user) |
        Q(project__assigned_users=request.user) |
        Q(project__assigned_teams__members__user=request.user)
    ).distinct().order_by('project', 'order', 'created_at')
    
    return render(request, 'projectflow/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    """View for task details"""
    task = get_object_or_404(Task, pk=pk)
    
    # Check if user has access to this task
    if not (task.project.is_public or 
            task.project.team and task.project.team.members.filter(user=request.user).exists() or
            task.assigned_users.filter(id=request.user.id).exists() or
            task.assigned_teams.filter(members__user=request.user).exists() or
            task.project.assigned_users.filter(id=request.user.id).exists() or
            task.project.assigned_teams.filter(members__user=request.user).exists()):
        messages.error(request, "You don't have access to this task.")
        return redirect('projectflow:task-list')
    
    return render(request, 'projectflow/task_detail.html', {'task': task})

@login_required
def task_create(request, project_id=None):
    """View for creating a task"""
    # Placeholder for now
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        return redirect('projectflow:project-detail', slug=project.slug)
    return redirect('projectflow:task-list')

@login_required
def task_update(request, pk):
    """View for updating a task"""
    task = get_object_or_404(Task, pk=pk)
    # Placeholder for now
    return redirect('projectflow:task-detail', pk=pk)

@login_required
def task_delete(request, pk):
    """View for deleting a task"""
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    # Placeholder for now
    return redirect('projectflow:project-detail', slug=project.slug)

@login_required
def subtask_create(request, task_id=None):
    """View for creating a subtask"""
    # Placeholder for now
    if task_id:
        task = get_object_or_404(Task, id=task_id)
        return redirect('projectflow:task-detail', pk=task.id)
    return redirect('projectflow:task-list')

@login_required
def subtask_update(request, pk):
    """View for updating a subtask"""
    subtask = get_object_or_404(SubTask, pk=pk)
    # Placeholder for now
    return redirect('projectflow:task-detail', pk=subtask.task.id)

@login_required
def subtask_delete(request, pk):
    """View for deleting a subtask"""
    subtask = get_object_or_404(SubTask, pk=pk)
    task = subtask.task
    # Placeholder for now
    return redirect('projectflow:task-detail', pk=task.id)

@login_required
def update_task_status(request, pk):
    """View for updating a task's status"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(JOB_STATUS).keys():
            task.status = new_status
            task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('projectflow:task-detail', kwargs={'pk': pk})))

@login_required
def update_subtask_status(request, pk):
    """View for updating a subtask's status"""
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
        if not (project.team and project.team.members.filter(user=request.user).exists() or
                project.assigned_users.filter(id=request.user.id).exists()):
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
        if not (task.project.team and task.project.team.members.filter(user=request.user).exists() or
                task.assigned_users.filter(id=request.user.id).exists() or
                task.project.assigned_users.filter(id=request.user.id).exists()):
            return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
        
        # Update the order of each subtask
        for index, subtask_id in enumerate(subtask_order):
            SubTask.objects.filter(pk=subtask_id, task=task).update(order=index)
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
