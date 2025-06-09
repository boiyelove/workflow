from django.contrib import admin
from .models import Team, TeamMember, TeamInvite

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created_on')
    search_fields = ('name', 'description')
    raw_id_fields = ('author',)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'is_manager', 'created_on')
    list_filter = ('is_manager', 'team')
    search_fields = ('user__username', 'team__name')
    raw_id_fields = ('user', 'team')

@admin.register(TeamInvite)
class TeamInviteAdmin(admin.ModelAdmin):
    list_display = ('email', 'team', 'sender', 'accepted', 'created_on')
    list_filter = ('accepted', 'team')
    search_fields = ('email', 'team__name', 'sender__username')
    raw_id_fields = ('team', 'sender')
