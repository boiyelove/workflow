from django.contrib import admin
from .models import Workspace, WorkspaceUser

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('teams',)

@admin.register(WorkspaceUser)
class WorkspaceUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'workspace', 'role', 'joined_at')
    list_filter = ('role', 'workspace')
    search_fields = ('user__username', 'workspace__name')
