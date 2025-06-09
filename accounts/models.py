from django.db import models
from django.contrib.auth.models import User
from webcore.models import Program, TimestampedModel
import uuid

class InviteCode(TimestampedModel):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField()
    is_used = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_invites')
    
    def __str__(self):
        return f"Invite for {self.email} - {'Used' if self.is_used else 'Unused'}"

class UserProfile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)
    programs = models.ManyToManyField(Program, blank=True)
    invite_code = models.ForeignKey(InviteCode, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
