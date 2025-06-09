from django import forms
from django.contrib.auth.models import User
from .models import Project, Task, SubTask
from teamflow.models import Team

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'team', 'is_public', 'parent', 
                  'assigned_users', 'assigned_teams', 'project_type', 'due_date', 'due_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'team': forms.Select(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'project_type': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
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
        fields = ['name', 'description', 'status', 'project', 'team_member', 
                  'assigned_users', 'assigned_teams', 'is_milestone', 'order', 'due_date', 'due_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'is_milestone': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
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
        fields = ['name', 'description', 'status', 'task', 'team_member', 
                  'assigned_users', 'order', 'due_date', 'due_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'task': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'team_member': forms.Select(attrs={
                'class': 'form-control select2-team-member',
                'data-placeholder': 'Select team member...'
            }),
            'assigned_users': forms.SelectMultiple(attrs={
                'class': 'form-control select2-users',
                'data-placeholder': 'Select users...'
            }),
        }
