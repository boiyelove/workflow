from django.db import models
from django.utils.text import slugify
from django.conf import settings
from teamflow.models import Team, TeamMember
from accounts.models import TimestampedModel

# Create your models here.
JOB_STATUS = (('Todo', 'Todo'),
            ('Doing', 'Doing'),
            ('Done', 'Done'),)

class Project(TimestampedModel):
    name = models.CharField(max_length=100, default="New Project")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='projects', null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Board(TimestampedModel):
    name = models.CharField(max_length=100, default="Default Board")
    slug = models.SlugField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='boards')
    
    class Meta:
        unique_together = ('slug', 'project')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Task(TimestampedModel):
    title = models.CharField(max_length=200, default="New Task")
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=JOB_STATUS, default='Todo')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks', null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', null=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks', null=True)
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks')
    
    def __str__(self):
        return self.title
