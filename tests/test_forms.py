from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from projectflow.models import Project, Task
from projectflow.forms import ProjectForm, TaskForm, SubTaskForm
from teamflow.models import Team
from teamflow.forms import TeamForm, TeamMemberForm
from workspace.models import Workspace
from workspace.forms import WorkspaceForm
from support.forms import TicketForm, TicketResponseForm

class ProjectFormTest(TestCase):
    """Test case for Project forms"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.team = Team.objects.create(
            name='Test Team',
            url='test-team',
            description='Test team description',
            teamAuthor=self.user,
            teamAuthor=self.user
        )
        
        self.workspace = Workspace.objects.create(
            name='Test Workspace',
            description='Test workspace description'
        )
    
    def test_project_form_valid_data(self):
        """Test project form with valid data"""
        form_data = {
            'name': 'New Project',
            'description': 'New project description',
            'status': 'Todo',
            'is_public': True,
            'team': self.team.id,
            'workspace': self.workspace.id,
            'project_type': 'standard'
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_project_form_missing_name(self):
        """Test project form with missing name"""
        form_data = {
            'description': 'New project description',
            'status': 'Todo',
            'is_public': True
        }
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_project_form_with_due_date(self):
        """Test project form with due date"""
        tomorrow = timezone.now().date() + timedelta(days=1)
        form_data = {
            'name': 'New Project',
            'description': 'New project description',
            'status': 'Todo',
            'is_public': True,
            'due_date': tomorrow
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_project_form_with_past_due_date(self):
        """Test project form with past due date"""
        yesterday = timezone.now().date() - timedelta(days=1)
        form_data = {
            'name': 'New Project',
            'description': 'New project description',
            'status': 'Todo',
            'is_public': True,
            'due_date': yesterday
        }
        # Past due dates should still be valid for projects
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_project_form_roadmap_type(self):
        """Test project form with roadmap type"""
        form_data = {
            'name': 'Product Roadmap',
            'description': 'Product roadmap for 2025',
            'status': 'Todo',
            'is_public': True,
            'project_type': 'roadmap'
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())


class TaskFormTest(TestCase):
    """Test case for Task forms"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.project = Project.objects.create(
            name='Test Project',
            slug='test-project',
            description='Test project description',
            status='Todo',
            is_public=True
        )
        
        self.team = Team.objects.create(
            name='Test Team',
            url='test-team',
            description='Test team description',
            teamAuthor=self.user,
            teamAuthor=self.user
        )
    
    def test_task_form_valid_data(self):
        """Test task form with valid data"""
        form_data = {
            'name': 'New Task',
            'description': 'New task description',
            'status': 'Todo',
            'project': self.project.id,
            'is_milestone': False,
            'order': 1
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_task_form_missing_name(self):
        """Test task form with missing name"""
        form_data = {
            'description': 'New task description',
            'status': 'Todo',
            'project': self.project.id
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_task_form_missing_project(self):
        """Test task form with missing project"""
        form_data = {
            'name': 'New Task',
            'description': 'New task description',
            'status': 'Todo'
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('project', form.errors)
    
    def test_task_form_with_milestone(self):
        """Test task form with milestone"""
        form_data = {
            'name': 'Milestone Task',
            'description': 'Milestone task description',
            'status': 'Todo',
            'project': self.project.id,
            'is_milestone': True
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_task_form_with_due_date(self):
        """Test task form with due date"""
        tomorrow = timezone.now().date() + timedelta(days=1)
        form_data = {
            'name': 'New Task',
            'description': 'New task description',
            'status': 'Todo',
            'project': self.project.id,
            'due_date': tomorrow
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())


class TeamFormTest(TestCase):
    """Test case for Team forms"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_team_form_valid_data(self):
        """Test team form with valid data"""
        form_data = {
            'name': 'New Team',
            'url': 'new-team',
            'description': 'New team description'
        }
        form = TeamForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_team_form_missing_name(self):
        """Test team form with missing name"""
        form_data = {
            'url': 'new-team',
            'description': 'New team description'
        }
        form = TeamForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_team_form_duplicate_url(self):
        """Test team form with duplicate URL"""
        # Create a team first
        Team.objects.create(
            name='Existing Team',
            url='existing-team',
            description='Existing team description',
            teamAuthor=self.user
        )
        
        # Try to create another team with the same URL
        form_data = {
            'name': 'New Team',
            'url': 'existing-team',
            'description': 'New team description'
        }
        form = TeamForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('url', form.errors)


class WorkspaceFormTest(TestCase):
    """Test case for Workspace forms"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_workspace_form_valid_data(self):
        """Test workspace form with valid data"""
        form_data = {
            'name': 'New Workspace',
            'description': 'New workspace description'
        }
        form = WorkspaceForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_workspace_form_missing_name(self):
        """Test workspace form with missing name"""
        form_data = {
            'description': 'New workspace description'
        }
        form = WorkspaceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_workspace_form_duplicate_name(self):
        """Test workspace form with duplicate name"""
        # Create a workspace first
        Workspace.objects.create(
            name='Existing Workspace',
            description='Existing workspace description'
        )
        
        # Try to create another workspace with the same name
        form_data = {
            'name': 'Existing Workspace',
            'description': 'New workspace description'
        }
        form = WorkspaceForm(data=form_data)
        # Duplicate names should still be valid for workspaces
        self.assertTrue(form.is_valid())


class SupportFormTest(TestCase):
    """Test case for Support forms"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test ticket description',
            created_by=self.user,
            status='Open',
            priority='Medium'
        )
    
    def test_ticket_form_valid_data(self):
        """Test ticket form with valid data"""
        form_data = {
            'title': 'New Ticket',
            'description': 'New ticket description',
            'priority': 'High'
        }
        form = TicketForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_ticket_form_missing_title(self):
        """Test ticket form with missing title"""
        form_data = {
            'description': 'New ticket description',
            'priority': 'High'
        }
        form = TicketForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_ticket_form_missing_description(self):
        """Test ticket form with missing description"""
        form_data = {
            'title': 'New Ticket',
            'priority': 'High'
        }
        form = TicketForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
    
    def test_ticket_response_form_valid_data(self):
        """Test ticket response form with valid data"""
        form_data = {
            'message': 'This is a response to the ticket'
        }
        form = TicketResponseForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_ticket_response_form_missing_message(self):
        """Test ticket response form with missing message"""
        form_data = {}
        form = TicketResponseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
