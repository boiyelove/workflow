from django.contrib import admin
from .models import Project, Task, SubTask

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'status', 'created_at')
    list_filter = ('status', 'project', 'created_at')
    search_fields = ('name', 'description')

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'task', 'status', 'team_member', 'created_at')
    list_filter = ('status', 'task', 'created_at')
    search_fields = ('name', 'description')
