from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from projectflow.models import Project, Task, SubTask
from teamflow.models import Team, TeamMember
from workspace.models import Workspace, WorkspaceUser
from support.models import Ticket, TicketResponse

class ProjectModelBasicTest(TestCase):
    """Basic tests for Project model"""
    
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
            teamAuthor=self.user
        )
        
        self.project = Project.objects.create(
            name='Test Project',
            slug='test-project',
            description='Test project description',
            status='Todo',
            is_public=True,
            team=self.team
        )
    
    def test_project_creation(self):
        """Test project creation"""
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.slug, 'test-project')
        self.assertEqual(self.project.status, 'Todo')
        self.assertTrue(self.project.is_public)
        self.assertEqual(self.project.team, self.team)
    
    def test_project_str_method(self):
        """Test project string representation"""
        self.assertEqual(str(self.project), 'Test Project')


class TaskModelBasicTest(TestCase):
    """Basic tests for Task model"""
    
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
            teamAuthor=self.user
        )
        
        self.project = Project.objects.create(
            name='Test Project',
            slug='test-project',
            description='Test project description',
            status='Todo',
            is_public=True,
            team=self.team
        )
        
        self.task = Task.objects.create(
            name='Test Task',
            description='Test task description',
            status='Todo',
            project=self.project,
            order=1
        )
        
        # Assign user to task
        self.task.assigned_users.add(self.user)
    
    def test_task_creation(self):
        """Test task creation"""
        self.assertEqual(self.task.name, 'Test Task')
        self.assertEqual(self.task.status, 'Todo')
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.order, 1)
        self.assertIn(self.user, self.task.assigned_users.all())
    
    def test_task_str_method(self):
        """Test task string representation"""
        self.assertEqual(str(self.task), 'Test Task')


class TeamModelBasicTest(TestCase):
    """Basic tests for Team model"""
    
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
            teamAuthor=self.user
        )
    
    def test_team_creation(self):
        """Test team creation"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.url, 'test-team')
        self.assertEqual(self.team.description, 'Test team description')
        self.assertEqual(self.team.teamAuthor, self.user)
    
    def test_team_str_method(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class SupportModelBasicTest(TestCase):
    """Basic tests for Support models"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            is_staff=True
        )
        
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test ticket description',
            created_by=self.user,
            assigned_to=self.admin,
            status='Open',
            priority='Medium'
        )
        
        self.response = TicketResponse.objects.create(
            ticket=self.ticket,
            user=self.admin,
            message='This is a response to the ticket'
        )
    
    def test_ticket_creation(self):
        """Test ticket creation"""
        self.assertEqual(self.ticket.title, 'Test Ticket')
        self.assertEqual(self.ticket.description, 'Test ticket description')
        self.assertEqual(self.ticket.created_by, self.user)
        self.assertEqual(self.ticket.assigned_to, self.admin)
        self.assertEqual(self.ticket.status, 'Open')
        self.assertEqual(self.ticket.priority, 'Medium')
    
    def test_ticket_str_method(self):
        """Test ticket string representation"""
        self.assertEqual(str(self.ticket), 'Test Ticket - Open')
    
    def test_ticket_response_creation(self):
        """Test ticket response creation"""
        self.assertEqual(self.response.ticket, self.ticket)
        self.assertEqual(self.response.user, self.admin)
        self.assertEqual(self.response.message, 'This is a response to the ticket')
