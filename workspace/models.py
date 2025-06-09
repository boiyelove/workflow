from django.db import models
from django.contrib.auth.models import User

class Workspace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, through='WorkspaceUser', related_name='workspaces')
    teams = models.ManyToManyField('teamflow.Team', related_name='workspaces')
    
    def __str__(self):
        return self.name

class WorkspaceUser(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role_choices = [
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('guest', 'Guest'),
    ]
    role = models.CharField(max_length=20, choices=role_choices, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('workspace', 'user')
        
    def __str__(self):
        return f"{self.user.username} in {self.workspace.name}"
