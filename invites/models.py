from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import uuid

class Invite(models.Model):
    # Basic invite information
    email = models.EmailField()
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invites_sent')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    token = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)
    
    # Generic relationship to the target entity
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    
    # Role information
    ROLE_CHOICES = [
        # Platform roles
        ('platform_admin', 'Platform Administrator'),
        ('platform_user', 'Platform User'),
        
        # Workspace roles
        ('workspace_admin', 'Workspace Administrator'),
        ('workspace_member', 'Workspace Member'),
        ('workspace_guest', 'Workspace Guest'),
        
        # Team roles
        ('team_manager', 'Team Manager'),
        ('team_member', 'Team Member'),
        
        # Project roles
        ('project_manager', 'Project Manager'),
        ('project_member', 'Project Member'),
        ('project_viewer', 'Project Viewer'),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    
    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['token']),
            models.Index(fields=['email', 'accepted']),
        ]
    
    def __str__(self):
        return f"Invite for {self.email} to {self.target}"
    
    def save(self, *args, **kwargs):
        # Set default expiration (30 days from creation)
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=30)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at
    
    @property
    def target_type(self):
        """Returns the type of entity this invite is for (e.g., 'workspace', 'team')"""
        return self.content_type.model
    
    def accept(self, user):
        """Accept the invitation and add the user to the target entity"""
        if self.accepted or self.is_expired:
            return False
        
        # Mark as accepted
        self.accepted = True
        self.accepted_at = timezone.now()
        self.save()
        
        # Add user to the target entity based on type
        target_type = self.target_type
        
        if target_type == 'workspace':
            from workspace.models import WorkspaceUser
            WorkspaceUser.objects.create(
                workspace=self.target,
                user=user,
                role=self.role.replace('workspace_', '')
            )
        
        elif target_type == 'team':
            from teamflow.models import TeamMember
            is_manager = 'manager' in self.role
            TeamMember.objects.create(
                team=self.target,
                user=user,
                is_manager=is_manager
            )
        
        elif target_type == 'project':
            # For projects, we might just add them to assigned_users
            self.target.assigned_users.add(user)
        
        elif target_type == 'platform':
            # For platform invites, we might just activate the user account
            user.is_active = True
            user.save()
        
        return True
