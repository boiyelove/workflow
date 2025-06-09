from django.contrib import admin
from .models import Project, Board, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'author', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('team', 'author')

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'created_on')
    list_filter = ('project', 'created_on')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('project',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'board', 'project', 'assignee', 'creator', 'created_on')
    list_filter = ('status', 'board', 'project', 'created_on')
    search_fields = ('title', 'description')
    raw_id_fields = ('board', 'project', 'assignee', 'creator', 'parent_task')
