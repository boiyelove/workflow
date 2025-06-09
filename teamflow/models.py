from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

class Team(models.Model):
    name = models.CharField(max_length=100)
    url = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    teamAuthor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(self.name)
        super().save(*args, **kwargs)

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_memberships')
    handle = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    is_manager = models.BooleanField(default=False)
    joined_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('team', 'user')
        
    def __str__(self):
        return f"{self.user.username} in {self.team.name}"
