from django.contrib import admin
from .models import Team, TeamMember

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'teamAuthor', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'url': ('name',)}

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'handle', 'is_manager', 'joined_at')
    list_filter = ('is_manager', 'team')
    search_fields = ('user__username', 'handle', 'team__name')
