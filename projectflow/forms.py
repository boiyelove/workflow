from django import forms
from django.contrib.auth.models import User
from .models import Project, Task, SubTask
from teamflow.models import Team

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'team', 'is_public', 'parent', 'assigned_users', 'assigned_teams']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'team': forms.Select(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'assigned_users': forms.SelectMultiple(attrs={
                'class': 'form-control select2-users',
                'data-placeholder': 'Select users...'
            }),
            'assigned_teams': forms.SelectMultiple(attrs={
                'class': 'form-control select2-teams',
                'data-placeholder': 'Select teams...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude self from parent options to prevent circular references
        if self.instance.pk:
            self.fields['parent'].queryset = Project.objects.exclude(
                pk__in=[self.instance.pk] + [p.pk for p in self.instance.get_all_subprojects()]
            )

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'project', 'team_member', 'assigned_users', 'assigned_teams']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'team_member': forms.SelectMultiple(attrs={
                'class': 'form-control select2-team-members',
                'data-placeholder': 'Select team members...'
            }),
            'assigned_users': forms.SelectMultiple(attrs={
                'class': 'form-control select2-users',
                'data-placeholder': 'Select users...'
            }),
            'assigned_teams': forms.SelectMultiple(attrs={
                'class': 'form-control select2-teams',
                'data-placeholder': 'Select teams...'
            }),
        }

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['name', 'description', 'status', 'task', 'team_member', 'assigned_users']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'task': forms.Select(attrs={'class': 'form-control'}),
            'team_member': forms.Select(attrs={
                'class': 'form-control select2-team-member',
                'data-placeholder': 'Select team member...'
            }),
            'assigned_users': forms.SelectMultiple(attrs={
                'class': 'form-control select2-users',
                'data-placeholder': 'Select users...'
            }),
        }
