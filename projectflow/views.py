from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Project

@login_required
def project_list(request):
    """View for listing projects"""
    projects = Project.objects.filter(
        Q(is_public=True) | 
        Q(team__members__user=request.user) |
        Q(assigned_users=request.user) |
        Q(assigned_teams__members__user=request.user)
    ).distinct()
    
    return render(request, 'projectflow/project_list.html', {'projects': projects})

@login_required
def project_detail(request, slug):
    """View for project details"""
    project = get_object_or_404(Project, slug=slug)
    
    # Check if user has access to this project
    if not (project.is_public or 
            project.team.members.filter(user=request.user).exists() or
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
