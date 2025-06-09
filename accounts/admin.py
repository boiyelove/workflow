from django.contrib import admin
from .models import UserProfile, InviteCode

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'phone')
    search_fields = ('user__username', 'user__email', 'position')

@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'is_used', 'created_by', 'created_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('email', 'code', 'created_by__username')
