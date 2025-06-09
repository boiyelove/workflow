from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from webcore.models import TimestampedModel
import uuid

# Create your models here.

class Team(TimestampedModel):
    name = models.CharField(max_length=60)
    url = models.SlugField(max_length=60, unique=True)
    description = models.TextField(null=True, blank=True)
    teamAuthor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_teams')
    
    def __str__(self):
        return self.name
    
    def is_author(self, user):
        return self.teamAuthor == user
    
    def is_teammanager(self, user):
        return TeamMember.objects.filter(team=self, user=user, is_manager=True).exists()

class TeamMember(TimestampedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    handle = models.CharField(max_length=50, blank=True)
    is_manager = models.BooleanField(default=False)
    designation = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = ('team', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.team.name}"

class TeamInvite(TimestampedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    email = models.EmailField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    accepted = models.BooleanField(default=False)
    token = models.CharField(max_length=100, default='default-token')
    
    def __str__(self):
        return f"Invite to {self.team.name} for {self.email}"
    
    def is_pending(self):
        return not self.accepted
    
    def save(self, *args, **kwargs):
        if not self.token or self.token == 'default-token':
            self.token = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    def send_invite_email(self):
        message = render_to_string("teamflow/email/team_invite.txt", {
            "team": self.team,
            "sender": self.sender,
            "token": self.token,
            "site_name": settings.SITE_NAME,
            "site_url": settings.SITE_URL,
        })
        subject = f"Invitation to join {self.team.name} on {settings.SITE_NAME}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])
