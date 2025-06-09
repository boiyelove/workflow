from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, TeamMember

@login_required
def team_list(request):
    """View for listing teams"""
    teams = Team.objects.filter(members__user=request.user)
    return render(request, 'teamflow/team_list.html', {'teams': teams})

@login_required
def team_detail(request, url):
    """View for team details"""
    team = get_object_or_404(Team, url=url)
    
    # Check if user is a member of this team
    if not team.members.filter(user=request.user).exists():
        messages.error(request, "You don't have access to this team.")
        return redirect('teamflow:team-list')
    
    return render(request, 'teamflow/team_detail.html', {'team': team})

@login_required
def team_create(request):
    """View for creating a team"""
    # Placeholder for now
    return redirect('teamflow:team-list')

@login_required
def team_update(request, url):
    """View for updating a team"""
    # Placeholder for now
    return redirect('teamflow:team-detail', url=url)

@login_required
def team_delete(request, url):
    """View for deleting a team"""
    # Placeholder for now
    return redirect('teamflow:team-list')
