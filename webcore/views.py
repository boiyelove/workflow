from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from projectflow.models import Project, Task
from teamflow.models import Team

@login_required
def dashboard(request):
    """View for the dashboard"""
    # Get counts for dashboard stats
    projects_count = Project.objects.filter(
        Q(is_public=True) | 
        Q(team__members__user=request.user) |
        Q(assigned_users=request.user) |
        Q(assigned_teams__members__user=request.user)
    ).distinct().count()
    
    active_projects_count = Project.objects.filter(
        Q(is_public=True) | 
        Q(team__members__user=request.user) |
        Q(assigned_users=request.user) |
        Q(assigned_teams__members__user=request.user),
        status='Doing'
    ).distinct().count()
    
    tasks_count = Task.objects.filter(
        Q(project__is_public=True) | 
        Q(project__team__members__user=request.user) |
        Q(assigned_users=request.user) |
        Q(assigned_teams__members__user=request.user) |
        Q(project__assigned_users=request.user) |
        Q(project__assigned_teams__members__user=request.user)
    ).distinct().count()
    
    completed_tasks_count = Task.objects.filter(
        Q(project__is_public=True) | 
        Q(project__team__members__user=request.user) |
        Q(assigned_users=request.user) |
        Q(assigned_teams__members__user=request.user) |
        Q(project__assigned_users=request.user) |
        Q(project__assigned_teams__members__user=request.user),
        status='Done'
    ).distinct().count()
    
    teams_count = Team.objects.filter(
        members__user=request.user
    ).distinct().count()
    
    team_members_count = Team.objects.filter(
        members__user=request.user
    ).aggregate(total_members=Count('members'))['total_members']
    
    # Get recent projects
    recent_projects = Project.objects.filter(
        Q(is_public=True) | 
        Q(team__members__user=request.user) |
        Q(assigned_users=request.user) |
        Q(assigned_teams__members__user=request.user)
    ).distinct().order_by('-updated_at')[:5]
    
    # Get user's tasks
    user_tasks = Task.objects.filter(
        Q(assigned_users=request.user) |
        Q(assigned_teams__members__user=request.user)
    ).exclude(status='Done').order_by('due_date', 'created_at')[:10]
    
    # Get upcoming milestones
    upcoming_milestones = Task.objects.filter(
        Q(project__is_public=True) | 
        Q(project__team__members__user=request.user) |
        Q(assigned_users=request.user) |
        Q(assigned_teams__members__user=request.user) |
        Q(project__assigned_users=request.user) |
        Q(project__assigned_teams__members__user=request.user),
        is_milestone=True
    ).exclude(status='Done').order_by('due_date')[:5]
    
    # Get user's teams
    user_teams = Team.objects.filter(
        members__user=request.user
    ).distinct()
    
    context = {
        'projects_count': projects_count,
        'active_projects_count': active_projects_count,
        'tasks_count': tasks_count,
        'completed_tasks_count': completed_tasks_count,
        'teams_count': teams_count,
        'team_members_count': team_members_count,
        'recent_projects': recent_projects,
        'user_tasks': user_tasks,
        'upcoming_milestones': upcoming_milestones,
        'user_teams': user_teams,
    }
    
    return render(request, 'dashboard.html', context)
