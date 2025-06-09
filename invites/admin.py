from django.contrib import admin
from .models import Invite

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('email', 'target_type', 'role', 'invited_by', 'created_at', 'accepted')
    list_filter = ('accepted', 'role', 'content_type')
    search_fields = ('email', 'invited_by__username', 'token')
    date_hierarchy = 'created_at'
    readonly_fields = ('token', 'created_at', 'accepted_at')
    
    def target_type(self, obj):
        return obj.target_type
