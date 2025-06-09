from django.contrib import admin
from .models import Project, Task, SubTask

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'team', 'workspace', 'project_type', 'created_at')
    list_filter = ('status', 'project_type', 'team', 'workspace')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('assigned_users', 'assigned_teams')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'status', 'is_milestone', 'due_date', 'created_at')
    list_filter = ('status', 'is_milestone', 'project')
    search_fields = ('name', 'description')
    filter_horizontal = ('assigned_users', 'assigned_teams', 'team_member')

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'task', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'task__project')
    search_fields = ('name', 'description')
    filter_horizontal = ('assigned_users', 'team_member')
