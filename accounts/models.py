from django.db import models
from django.contrib.auth.models import User
from webcore.models import Program, TimestampedModel
import uuid

def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'

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
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    headshot = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)
    programs = models.ManyToManyField(Program, blank=True)
    invite_code = models.ForeignKey(InviteCode, on_delete=models.SET_NULL, null=True, blank=True)
    referral = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='parent', editable=False)
    
    def __str__(self):
        return self.user.username

class EmailVerification(TimestampedModel):
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    action = models.CharField(max_length=100, default='/', blank=True)
    actiontype = models.CharField(max_length=20, default='VERIFICATION', blank=True)
    slug = models.CharField(max_length=25, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.email} - {'Verified' if self.is_verified else 'Not Verified'}"
