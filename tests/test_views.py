from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import json

from projectflow.models import Project, Task, SubTask
from teamflow.models import Team, TeamMember
from workspace.models import Workspace, WorkspaceUser
from support.models import Ticket, TicketResponse

class ProjectViewTest(TestCase):
    """Test case for Project views"""
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create test team
        self.team = Team.objects.create(
            name='Test Team',
            url='test-team',
            description='Test team description'
        )
        
        # Add user to team
        self.team_member = TeamMember.objects.create(
            user=self.user,
            team=self.team,
            role='Admin'
        )
        
        # Create test projects
        self.project1 = Project.objects.create(
            name='Project 1',
            slug='project-1',
            description='Project 1 description',
            status='Todo',
            is_public=True,
            team=self.team
        )
        
        self.project2 = Project.objects.create(
            name='Project 2',
            slug='project-2',
            description='Project 2 description',
            status='Doing',
            is_public=False,
            team=self.team
        )
        
        # Create test tasks
        self.task1 = Task.objects.create(
            name='Task 1',
            description='Task 1 description',
            status='Todo',
            project=self.project1,
            order=1
        )
        
        self.task2 = Task.objects.create(
            name='Task 2',
            description='Task 2 description',
            status='Doing',
            project=self.project1,
            order=2
        )
        
        # Create test client
        self.client = Client()
        
        # Login the user
        self.client.login(username='testuser', password='testpassword')
    
    def test_project_list_view(self):
        """Test project list view"""
        response = self.client.get(reverse('projectflow:project-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/project_list_reimagined.html')
        self.assertContains(response, 'Project 1')
        self.assertContains(response, 'Project 2')
    
    def test_project_detail_view(self):
        """Test project detail view"""
        response = self.client.get(reverse('projectflow:project-detail', kwargs={'slug': self.project1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/project_detail.html')
        self.assertContains(response, 'Project 1')
        self.assertContains(response, 'Project 1 description')
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')
    
    def test_project_create_view(self):
        """Test project create view"""
        response = self.client.get(reverse('projectflow:project-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/project_form.html')
        
        # Test POST request
        project_data = {
            'name': 'New Project',
            'description': 'New project description',
            'status': 'Todo',
            'is_public': True,
            'team': self.team.id
        }
        response = self.client.post(reverse('projectflow:project-create'), project_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Check that the project was created
        self.assertTrue(Project.objects.filter(name='New Project').exists())
    
    def test_project_update_view(self):
        """Test project update view"""
        response = self.client.get(reverse('projectflow:project-update', kwargs={'slug': self.project1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/project_form.html')
        
        # Test POST request
        project_data = {
            'name': 'Updated Project',
            'description': 'Updated project description',
            'status': 'Doing',
            'is_public': True,
            'team': self.team.id
        }
        response = self.client.post(reverse('projectflow:project-update', kwargs={'slug': self.project1.slug}), project_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Check that the project was updated
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.name, 'Updated Project')
        self.assertEqual(self.project1.description, 'Updated project description')
        self.assertEqual(self.project1.status, 'Doing')
    
    def test_project_delete_view(self):
        """Test project delete view"""
        response = self.client.get(reverse('projectflow:project-delete', kwargs={'slug': self.project1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/project_confirm_delete.html')
        
        # Test POST request
        response = self.client.post(reverse('projectflow:project-delete', kwargs={'slug': self.project1.slug}))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        
        # Check that the project was deleted
        self.assertFalse(Project.objects.filter(slug='project-1').exists())
    
    def test_project_timeline_view(self):
        """Test project timeline view"""
        response = self.client.get(reverse('projectflow:project-timeline', kwargs={'slug': self.project1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/project_timeline.html')
        self.assertContains(response, 'Project 1')
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')
    
    def test_task_board_view(self):
        """Test task board view"""
        response = self.client.get(reverse('projectflow:project-task-board', kwargs={'slug': self.project1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/task_board.html')
        self.assertContains(response, 'Project 1')
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')
    
    def test_task_update_status_view(self):
        """Test task update status view"""
        # Test POST request
        response = self.client.post(
            reverse('projectflow:task-update-status', kwargs={'task_id': self.task1.id}),
            {'status': 'Done'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'  # Simulate AJAX request
        )
        self.assertEqual(response.status_code, 200)
        
        # Check that the task status was updated
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, 'Done')


class TeamViewTest(TestCase):
    """Test case for Team views"""
    
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpassword'
        )
        
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword'
        )
        
        # Create test team
        self.team = Team.objects.create(
            name='Test Team',
            url='test-team',
            description='Test team description'
        )
        
        # Add users to team
        self.team_member1 = TeamMember.objects.create(
            user=self.user1,
            team=self.team,
            role='Admin'
        )
        
        self.team_member2 = TeamMember.objects.create(
            user=self.user2,
            team=self.team,
            role='Member'
        )
        
        # Create test client
        self.client = Client()
        
        # Login the user
        self.client.login(username='testuser1', password='testpassword')
    
    def test_team_list_view(self):
        """Test team list view"""
        response = self.client.get(reverse('teamflow:team-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teamflow/team_list.html')
        self.assertContains(response, 'Test Team')
    
    def test_team_detail_view(self):
        """Test team detail view"""
        response = self.client.get(reverse('teamflow:team-detail', kwargs={'url': self.team.url}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teamflow/team_detail.html')
        self.assertContains(response, 'Test Team')
        self.assertContains(response, 'Test team description')
        self.assertContains(response, 'testuser1')
        self.assertContains(response, 'testuser2')
    
    def test_team_create_view(self):
        """Test team create view"""
        response = self.client.get(reverse('teamflow:team-create'))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        team_data = {
            'name': 'New Team',
            'url': 'new-team',
            'description': 'New team description'
        }
        response = self.client.post(reverse('teamflow:team-create'), team_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Check that the team was created
        self.assertTrue(Team.objects.filter(name='New Team').exists())
        
        # Check that the current user was added as an admin
        new_team = Team.objects.get(name='New Team')
        self.assertTrue(TeamMember.objects.filter(team=new_team, user=self.user1, role='Admin').exists())
    
    def test_team_update_view(self):
        """Test team update view"""
        response = self.client.get(reverse('teamflow:team-update', kwargs={'url': self.team.url}))
        self.assertEqual(response.status_code, 200)
        
        # Test POST request
        team_data = {
            'name': 'Updated Team',
            'url': 'updated-team',
            'description': 'Updated team description'
        }
        response = self.client.post(reverse('teamflow:team-update', kwargs={'url': self.team.url}), team_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Check that the team was updated
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, 'Updated Team')
        self.assertEqual(self.team.url, 'updated-team')
        self.assertEqual(self.team.description, 'Updated team description')


class WorkspaceViewTest(TestCase):
    """Test case for Workspace views"""
    
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpassword'
        )
        
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword'
        )
        
        # Create test workspace
        self.workspace = Workspace.objects.create(
            name='Test Workspace',
            description='Test workspace description'
        )
        
        # Add users to workspace
        self.workspace_user1 = WorkspaceUser.objects.create(
            user=self.user1,
            workspace=self.workspace,
            role='Admin'
        )
        
        self.workspace_user2 = WorkspaceUser.objects.create(
            user=self.user2,
            workspace=self.workspace,
            role='Member'
        )
        
        # Create test client
        self.client = Client()
        
        # Login the user
        self.client.login(username='testuser1', password='testpassword')
    
    def test_workspace_list_view(self):
        """Test workspace list view"""
        response = self.client.get(reverse('workspace:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workspace/workspace_list_reimagined.html')
        self.assertContains(response, 'Test Workspace')
    
    def test_workspace_detail_view(self):
        """Test workspace detail view"""
        response = self.client.get(reverse('workspace:detail', kwargs={'workspace_id': self.workspace.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workspace/workspace_detail.html')
        self.assertContains(response, 'Test Workspace')
        self.assertContains(response, 'Test workspace description')


class SupportViewTest(TestCase):
    """Test case for Support views"""
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create test ticket
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test ticket description',
            created_by=self.user,
            status='Open',
            priority='Medium'
        )
        
        # Create test response
        self.response = TicketResponse.objects.create(
            ticket=self.ticket,
            user=self.user,
            message='This is a response to the ticket'
        )
        
        # Create test client
        self.client = Client()
        
        # Login the user
        self.client.login(username='testuser', password='testpassword')
    
    def test_ticket_list_view(self):
        """Test ticket list view"""
        response = self.client.get(reverse('support:ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'support/ticket_list.html')
        self.assertContains(response, 'Test Ticket')
    
    def test_ticket_detail_view(self):
        """Test ticket detail view"""
        response = self.client.get(reverse('support:ticket_detail', kwargs={'ticket_id': self.ticket.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'support/ticket_detail.html')
        self.assertContains(response, 'Test Ticket')
        self.assertContains(response, 'Test ticket description')
        self.assertContains(response, 'This is a response to the ticket')
    
    def test_ticket_create_view(self):
        """Test ticket create view"""
        response = self.client.get(reverse('support:ticket_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'support/ticket_form.html')
        
        # Test POST request
        ticket_data = {
            'title': 'New Ticket',
            'description': 'New ticket description',
            'priority': 'High'
        }
        response = self.client.post(reverse('support:ticket_create'), ticket_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Check that the ticket was created
        self.assertTrue(Ticket.objects.filter(title='New Ticket').exists())
        
        # Check that the current user is set as the creator
        new_ticket = Ticket.objects.get(title='New Ticket')
        self.assertEqual(new_ticket.created_by, self.user)
    
    def test_ticket_response_create(self):
        """Test ticket response creation"""
        # Test POST request
        response_data = {
            'message': 'This is a new response'
        }
        response = self.client.post(
            reverse('support:ticket_detail', kwargs={'ticket_id': self.ticket.id}),
            response_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Check that the response was created
        self.assertTrue(TicketResponse.objects.filter(message='This is a new response').exists())
        
        # Check that the response is associated with the ticket
        new_response = TicketResponse.objects.get(message='This is a new response')
        self.assertEqual(new_response.ticket, self.ticket)
        self.assertEqual(new_response.user, self.user)
