from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from teamflow.models import Team, TeamMember

JOB_STATUS = (
    ('Todo', 'Todo'),
    ('Doing', 'Doing'),
    ('Done', 'Done'),
)

class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='Todo')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='projects', null=True)
    workspace = models.ForeignKey('workspace.Workspace', on_delete=models.CASCADE, related_name='projects', null=True)
    assigned_users = models.ManyToManyField(User, related_name='assigned_projects', blank=True)
    assigned_teams = models.ManyToManyField(Team, related_name='assigned_projects', blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    project_type = models.CharField(max_length=20, choices=[
        ('standard', 'Standard Project'),
        ('roadmap', 'Feature Roadmap'),
    ], default='standard')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subprojects')
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        if self.due_date:
            from django.utils import timezone
            return self.due_date < timezone.now().date()
        return False
    
    def get_completion_percentage(self):
        tasks = self.tasks.all()
        if not tasks:
            return 0
        completed = tasks.filter(status='Done').count()
        return int((completed / tasks.count()) * 100)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='Todo')
    assigned_users = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    assigned_teams = models.ManyToManyField(Team, related_name='assigned_tasks', blank=True)
    team_member = models.ManyToManyField(TeamMember, related_name='tasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    is_milestone = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_overdue(self):
        if self.due_date:
            from django.utils import timezone
            return self.due_date < timezone.now().date()
        return False

class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='Todo')
    assigned_users = models.ManyToManyField(User, related_name='assigned_subtasks', blank=True)
    team_member = models.ManyToManyField(TeamMember, related_name='subtasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_overdue(self):
        if self.due_date:
            from django.utils import timezone
            return self.due_date < timezone.now().date()
        return False
