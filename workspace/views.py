from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Workspace, WorkspaceUser

@login_required
def workspace_list(request):
    """View for listing workspaces"""
    workspaces = Workspace.objects.filter(workspaceuser__user=request.user)
    return render(request, 'workspace/workspace_list_reimagined.html', {'workspaces': workspaces})

@login_required
def workspace_detail(request, workspace_id):
    """View for workspace details"""
    workspace = get_object_or_404(Workspace, id=workspace_id)
    
    # Check if user has access to this workspace
    if not workspace.workspaceuser_set.filter(user=request.user).exists():
        messages.error(request, "You don't have access to this workspace.")
        return redirect('workspace:list')
    
    return render(request, 'workspace/workspace_detail.html', {'workspace': workspace})

@login_required
def workspace_create(request):
    """View for creating a workspace"""
    # Placeholder for now
    return redirect('workspace:list')

@login_required
def workspace_update(request, workspace_id):
    """View for updating a workspace"""
    # Placeholder for now
    return redirect('workspace:detail', workspace_id=workspace_id)

@login_required
def workspace_delete(request, workspace_id):
    """View for deleting a workspace"""
    # Placeholder for now
    return redirect('workspace:list')
