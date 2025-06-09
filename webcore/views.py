from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projectflow.models import Project, Task
from teamflow.models import Team

@login_required
def home(request):
    user = request.user
    teams = Team.objects.filter(teammember__user=user)
    projects = Project.objects.filter(team__in=teams)[:5]
    tasks = Task.objects.filter(team_member__user=user)[:5]
    
    context = {
        'title': 'Dashboard',
        'projects': projects,
        'tasks': tasks,
        'teams': teams,
    }
    
    return render(request, 'index.html', context)
