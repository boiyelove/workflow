from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from projectflow.models import Project
from teamflow.models import Team
from workspace.models import Workspace
from support.models import Ticket

class LinkTestCase(TestCase):
    """Test case to verify all links are working properly"""
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create a test project
        self.project = Project.objects.create(
            name='Test Project',
            slug='test-project',
            description='Test project description',
            status='Todo',
            is_public=True
        )
        
        # Create a test team
        self.team = Team.objects.create(
            name='Test Team',
            url='test-team',
            description='Test team description'
        )
        
        # Create a test workspace
        self.workspace = Workspace.objects.create(
            name='Test Workspace',
            description='Test workspace description'
        )
        
        # Create a test ticket
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test ticket description',
            created_by=self.user,
            status='Open',
            priority='Medium'
        )
        
        # Create a client
        self.client = Client()
        
        # Login the user
        self.client.login(username='testuser', password='testpassword')
    
    def test_home_page(self):
        """Test the home page"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_project_links(self):
        """Test project-related links"""
        # Project list
        response = self.client.get(reverse('projectflow:project-list'))
        self.assertEqual(response.status_code, 200)
        
        # Project detail
        response = self.client.get(reverse('projectflow:project-detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        
        # Project create
        response = self.client.get(reverse('projectflow:project-create'))
        self.assertEqual(response.status_code, 200)
        
        # Project timeline
        response = self.client.get(reverse('projectflow:project-timeline', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        
        # Task list
        response = self.client.get(reverse('projectflow:task-list'))
        self.assertEqual(response.status_code, 200)
        
        # Roadmap list
        response = self.client.get(reverse('projectflow:roadmap-list'))
        self.assertEqual(response.status_code, 200)
    
    def test_team_links(self):
        """Test team-related links"""
        # Team list
        response = self.client.get(reverse('teamflow:team-list'))
        self.assertEqual(response.status_code, 200)
        
        # Team detail
        response = self.client.get(reverse('teamflow:team-detail', kwargs={'url': self.team.url}))
        self.assertEqual(response.status_code, 200)
        
        # Team create
        response = self.client.get(reverse('teamflow:team-create'))
        self.assertEqual(response.status_code, 200)
    
    def test_workspace_links(self):
        """Test workspace-related links"""
        # Workspace list
        response = self.client.get(reverse('workspace:list'))
        self.assertEqual(response.status_code, 200)
        
        # Workspace detail
        response = self.client.get(reverse('workspace:detail', kwargs={'workspace_id': self.workspace.id}))
        self.assertEqual(response.status_code, 200)
        
        # Workspace create
        response = self.client.get(reverse('workspace:create'))
        self.assertEqual(response.status_code, 200)
    
    def test_support_links(self):
        """Test support-related links"""
        # Ticket list
        response = self.client.get(reverse('support:ticket_list'))
        self.assertEqual(response.status_code, 200)
        
        # Ticket detail
        response = self.client.get(reverse('support:ticket_detail', kwargs={'ticket_id': self.ticket.id}))
        self.assertEqual(response.status_code, 200)
        
        # Ticket create
        response = self.client.get(reverse('support:ticket_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_account_links(self):
        """Test account-related links"""
        # Login page
        self.client.logout()
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        
        # Password reset
        response = self.client.get(reverse('accounts:password_reset'))
        self.assertEqual(response.status_code, 200)
        
        # Signup page
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        
        # Invite code page
        response = self.client.get(reverse('accounts:invite_code'))
        self.assertEqual(response.status_code, 200)
