from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from teamflow.models import Team, TeamMember
from webcore.models import TimestampedModel

# Create your models here.
JOB_STATUS = (('Todo', 'Todo'),
            ('Doing', 'Doing'),
            ('Done', 'Done'),)

PROJECT_TYPES = (
    ('standard', 'Standard Project'),
    ('roadmap', 'Feature Roadmap'),
)

class JobModel(TimestampedModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=160)
    status = models.CharField(max_length=5, choices=JOB_STATUS)

    class Meta:
        abstract = True


class Project(JobModel):
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='projects', null=True)
    is_public = models.BooleanField(default=False, help_text="If checked, this project will be visible to all users")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subprojects')
    assigned_users = models.ManyToManyField(User, related_name='assigned_projects', blank=True)
    assigned_teams = models.ManyToManyField(Team, related_name='assigned_projects', blank=True)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='standard')
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_all_subprojects(self):
        """Recursively get all subprojects"""
        subprojects = list(self.subprojects.all())
        for subproject in self.subprojects.all():
            subprojects.extend(subproject.get_all_subprojects())
        return subprojects
    
    def get_completion_percentage(self):
        """Calculate the completion percentage based on completed tasks"""
        tasks = self.tasks.all()
        if not tasks:
            return 0
        
        completed = tasks.filter(status='Done').count()
        return int((completed / tasks.count()) * 100)
    
    def get_ordered_tasks(self):
        """Get all tasks ordered by their position"""
        return self.tasks.all().order_by('order', 'created_at')
    
    def is_overdue(self):
        """Check if the project is overdue"""
        if self.due_date and timezone.now().date() > self.due_date:
            return True
        return False


class Task(JobModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    team_member = models.ManyToManyField(TeamMember, related_name='assigned_tasks', blank=True)
    assigned_users = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    assigned_teams = models.ManyToManyField(Team, related_name='assigned_tasks', blank=True)
    is_milestone = models.BooleanField(default=False, help_text="Designate this task as a milestone in the project timeline")
    order = models.PositiveIntegerField(default=0, help_text="Position in the project timeline")
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.name} - {self.project.name}"
    
    def is_overdue(self):
        """Check if the task is overdue"""
        if self.due_date and timezone.now().date() > self.due_date:
            return True
        return False


class SubTask(JobModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    team_member = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_subtasks')
    assigned_users = models.ManyToManyField(User, related_name='assigned_subtasks', blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Position in the task")
    due_date = models.DateField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.name} - {self.task.name}"
    
    def is_overdue(self):
        """Check if the subtask is overdue"""
        if self.due_date and timezone.now().date() > self.due_date:
            return True
        return False
