from django.shortcuts import render
from django.generic.views import DetailView, ListView
from .models import Project, Task
# Create your views here.

class ProjectDetail(DetailView):
	model = Project
	template_name = 'project_admin.html'

class ProjectList(ListView):
	model = Project
	template_name = 'projects.html'

class TaskDetail(DetailView):
	model = Task
	template = 'task.html'

class TaskList(ListView):
	model = Task
	template_name = "task.html"