from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from teamflow.models import Team, TeamMember
from webcore.models import TimestampedModel

# Create your models here.
JOB_STATUS = (('Todo', 'Todo'),
            ('Doing', 'Doing'),
            ('Done', 'Done'),)

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


class Task(JobModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    team_member = models.ManyToManyField(TeamMember, related_name='assigned_tasks', blank=True)
    assigned_users = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    assigned_teams = models.ManyToManyField(Team, related_name='assigned_tasks', blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.project.name}"


class SubTask(JobModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    team_member = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_subtasks')
    assigned_users = models.ManyToManyField(User, related_name='assigned_subtasks', blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.task.name}"
