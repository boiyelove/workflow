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

class ProjectWorkflowTest(TestCase):
    """Test case for complete project workflow"""
    
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
        
        # Create test client
        self.client = Client()
        
        # Login the user
        self.client.login(username='testuser', password='testpassword')
    
    def test_complete_project_workflow(self):
        """Test complete project workflow from creation to completion"""
        # Step 1: Create a new project
        project_data = {
            'name': 'Integration Test Project',
            'description': 'Project for integration testing',
            'status': 'Todo',
            'is_public': True,
            'team': self.team.id
        }
        response = self.client.post(reverse('projectflow:project-create'), project_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        # Get the created project
        project = Project.objects.get(name='Integration Test Project')
        
        # Step 2: Create tasks for the project
        task1_data = {
            'name': 'Task 1',
            'description': 'First task description',
            'status': 'Todo',
            'project': project.id,
            'order': 1
        }
        response = self.client.post(reverse('projectflow:task-create'), task1_data)
        self.assertEqual(response.status_code, 302)
        
        task2_data = {
            'name': 'Task 2',
            'description': 'Second task description',
            'status': 'Todo',
            'project': project.id,
            'order': 2
        }
        response = self.client.post(reverse('projectflow:task-create'), task2_data)
        self.assertEqual(response.status_code, 302)
        
        # Get the created tasks
        task1 = Task.objects.get(name='Task 1')
        task2 = Task.objects.get(name='Task 2')
        
        # Step 3: Create subtasks for Task 1
        subtask1_data = {
            'name': 'Subtask 1',
            'description': 'First subtask description',
            'status': 'Todo',
            'task': task1.id,
            'order': 1
        }
        response = self.client.post(reverse('projectflow:subtask-create'), subtask1_data)
        self.assertEqual(response.status_code, 302)
        
        subtask2_data = {
            'name': 'Subtask 2',
            'description': 'Second subtask description',
            'status': 'Todo',
            'task': task1.id,
            'order': 2
        }
        response = self.client.post(reverse('projectflow:subtask-create'), subtask2_data)
        self.assertEqual(response.status_code, 302)
        
        # Get the created subtasks
        subtask1 = SubTask.objects.get(name='Subtask 1')
        subtask2 = SubTask.objects.get(name='Subtask 2')
        
        # Step 4: Update project status to Doing
        project_update_data = {
            'name': 'Integration Test Project',
            'description': 'Project for integration testing',
            'status': 'Doing',
            'is_public': True,
            'team': self.team.id
        }
        response = self.client.post(reverse('projectflow:project-update', kwargs={'slug': project.slug}), project_update_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify project status
        project.refresh_from_db()
        self.assertEqual(project.status, 'Doing')
        
        # Step 5: Update Task 1 status to Doing
        response = self.client.post(
            reverse('projectflow:task-update-status', kwargs={'task_id': task1.id}),
            {'status': 'Doing'}
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify task status
        task1.refresh_from_db()
        self.assertEqual(task1.status, 'Doing')
        
        # Step 6: Update Subtask 1 status to Done
        response = self.client.post(
            reverse('projectflow:subtask-update-status', kwargs={'subtask_id': subtask1.id}),
            {'status': 'Done'}
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify subtask status
        subtask1.refresh_from_db()
        self.assertEqual(subtask1.status, 'Done')
        
        # Step 7: Update Subtask 2 status to Done
        response = self.client.post(
            reverse('projectflow:subtask-update-status', kwargs={'subtask_id': subtask2.id}),
            {'status': 'Done'}
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify subtask status
        subtask2.refresh_from_db()
        self.assertEqual(subtask2.status, 'Done')
        
        # Step 8: Update Task 1 status to Done
        response = self.client.post(
            reverse('projectflow:task-update-status', kwargs={'task_id': task1.id}),
            {'status': 'Done'}
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify task status
        task1.refresh_from_db()
        self.assertEqual(task1.status, 'Done')
        
        # Step 9: Update Task 2 status to Done
        response = self.client.post(
            reverse('projectflow:task-update-status', kwargs={'task_id': task2.id}),
            {'status': 'Done'}
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify task status
        task2.refresh_from_db()
        self.assertEqual(task2.status, 'Done')
        
        # Step 10: Update project status to Done
        project_update_data = {
            'name': 'Integration Test Project',
            'description': 'Project for integration testing',
            'status': 'Done',
            'is_public': True,
            'team': self.team.id
        }
        response = self.client.post(reverse('projectflow:project-update', kwargs={'slug': project.slug}), project_update_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify project status
        project.refresh_from_db()
        self.assertEqual(project.status, 'Done')
        
        # Verify project completion percentage
        self.assertEqual(project.get_completion_percentage(), 100.0)


class TeamProjectIntegrationTest(TestCase):
    """Test case for team and project integration"""
    
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
        
        # Create test client
        self.client = Client()
        
        # Login the first user
        self.client.login(username='testuser1', password='testpassword')
    
    def test_team_project_integration(self):
        """Test integration between teams and projects"""
        # Step 1: Create a new team
        team_data = {
            'name': 'Integration Team',
            'url': 'integration-team',
            'description': 'Team for integration testing'
        }
        response = self.client.post(reverse('teamflow:team-create'), team_data)
        self.assertEqual(response.status_code, 302)
        
        # Get the created team
        team = Team.objects.get(name='Integration Team')
        
        # Verify that the current user is added as an admin
        self.assertTrue(TeamMember.objects.filter(team=team, user=self.user1, role='Admin').exists())
        
        # Step 2: Add another user to the team
        team_member_data = {
            'user': self.user2.id,
            'role': 'Member'
        }
        response = self.client.post(reverse('teamflow:team-add-member', kwargs={'url': team.url}), team_member_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify that the user was added to the team
        self.assertTrue(TeamMember.objects.filter(team=team, user=self.user2, role='Member').exists())
        
        # Step 3: Create a project for the team
        project_data = {
            'name': 'Team Project',
            'description': 'Project for team integration testing',
            'status': 'Todo',
            'is_public': True,
            'team': team.id
        }
        response = self.client.post(reverse('projectflow:project-create'), project_data)
        self.assertEqual(response.status_code, 302)
        
        # Get the created project
        project = Project.objects.get(name='Team Project')
        
        # Verify that the project is associated with the team
        self.assertEqual(project.team, team)
        
        # Step 4: Create a task and assign it to the second user
        task_data = {
            'name': 'Assigned Task',
            'description': 'Task assigned to the second user',
            'status': 'Todo',
            'project': project.id,
            'order': 1
        }
        response = self.client.post(reverse('projectflow:task-create'), task_data)
        self.assertEqual(response.status_code, 302)
        
        # Get the created task
        task = Task.objects.get(name='Assigned Task')
        
        # Assign the task to the second user
        task.assigned_users.add(self.user2)
        task.save()
        
        # Verify that the task is assigned to the second user
        self.assertIn(self.user2, task.assigned_users.all())
        
        # Step 5: Login as the second user
        self.client.logout()
        self.client.login(username='testuser2', password='testpassword')
        
        # Verify that the second user can access the project
        response = self.client.get(reverse('projectflow:project-detail', kwargs={'slug': project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Team Project')
        
        # Verify that the second user can access the task
        response = self.client.get(reverse('projectflow:task-detail', kwargs={'task_id': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Assigned Task')
        
        # Step 6: Update the task status as the second user
        response = self.client.post(
            reverse('projectflow:task-update-status', kwargs={'task_id': task.id}),
            {'status': 'Doing'}
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify task status
        task.refresh_from_db()
        self.assertEqual(task.status, 'Doing')


class WorkspaceProjectIntegrationTest(TestCase):
    """Test case for workspace and project integration"""
    
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
        
        # Create test client
        self.client = Client()
        
        # Login the first user
        self.client.login(username='testuser1', password='testpassword')
    
    def test_workspace_project_integration(self):
        """Test integration between workspaces and projects"""
        # Step 1: Add another user to the workspace
        workspace_user_data = {
            'user': self.user2.id,
            'role': 'Member'
        }
        response = self.client.post(reverse('workspace:add-user', kwargs={'workspace_id': self.workspace.id}), workspace_user_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify that the user was added to the workspace
        self.assertTrue(WorkspaceUser.objects.filter(workspace=self.workspace, user=self.user2, role='Member').exists())
        
        # Step 2: Create a project in the workspace
        project_data = {
            'name': 'Workspace Project',
            'description': 'Project for workspace integration testing',
            'status': 'Todo',
            'is_public': True,
            'workspace': self.workspace.id
        }
        response = self.client.post(reverse('projectflow:project-create'), project_data)
        self.assertEqual(response.status_code, 302)
        
        # Get the created project
        project = Project.objects.get(name='Workspace Project')
        
        # Verify that the project is associated with the workspace
        self.assertEqual(project.workspace, self.workspace)
        
        # Step 3: Login as the second user
        self.client.logout()
        self.client.login(username='testuser2', password='testpassword')
        
        # Verify that the second user can access the workspace
        response = self.client.get(reverse('workspace:detail', kwargs={'workspace_id': self.workspace.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Workspace')
        
        # Verify that the second user can access the project
        response = self.client.get(reverse('projectflow:project-detail', kwargs={'slug': project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Workspace Project')


class SupportTicketWorkflowTest(TestCase):
    """Test case for support ticket workflow"""
    
    def setUp(self):
        # Create test users
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
        
        # Create test client
        self.client = Client()
        
        # Login the user
        self.client.login(username='testuser', password='testpassword')
    
    def test_support_ticket_workflow(self):
        """Test complete support ticket workflow"""
        # Step 1: Create a new ticket
        ticket_data = {
            'title': 'Support Ticket',
            'description': 'This is a test support ticket',
            'priority': 'High'
        }
        response = self.client.post(reverse('support:ticket_create'), ticket_data)
        self.assertEqual(response.status_code, 302)
        
        # Get the created ticket
        ticket = Ticket.objects.get(title='Support Ticket')
        
        # Verify ticket details
        self.assertEqual(ticket.description, 'This is a test support ticket')
        self.assertEqual(ticket.priority, 'High')
        self.assertEqual(ticket.status, 'Open')
        self.assertEqual(ticket.created_by, self.user)
        
        # Step 2: Add a response to the ticket
        response_data = {
            'message': 'This is a response from the user'
        }
        response = self.client.post(reverse('support:ticket_detail', kwargs={'ticket_id': ticket.id}), response_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify that the response was added
        self.assertTrue(TicketResponse.objects.filter(ticket=ticket, user=self.user).exists())
        
        # Step 3: Login as admin
        self.client.logout()
        self.client.login(username='admin', password='adminpassword')
        
        # Verify that the admin can access the ticket
        response = self.client.get(reverse('support:ticket_detail', kwargs={'ticket_id': ticket.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Support Ticket')
        
        # Step 4: Admin assigns the ticket to themselves and changes status
        ticket.assigned_to = self.admin
        ticket.status = 'In Progress'
        ticket.save()
        
        # Step 5: Admin adds a response
        response_data = {
            'message': 'This is a response from the admin'
        }
        response = self.client.post(reverse('support:ticket_detail', kwargs={'ticket_id': ticket.id}), response_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify that the response was added
        self.assertTrue(TicketResponse.objects.filter(ticket=ticket, user=self.admin).exists())
        
        # Step 6: Admin resolves the ticket
        ticket.status = 'Resolved'
        ticket.save()
        
        # Verify ticket status
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, 'Resolved')
        
        # Step 7: Login as the user again
        self.client.logout()
        self.client.login(username='testuser', password='testpassword')
        
        # Verify that the user can see the resolved ticket
        response = self.client.get(reverse('support:ticket_detail', kwargs={'ticket_id': ticket.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Support Ticket')
        self.assertContains(response, 'Resolved')
        
        # Step 8: User adds a final response
        response_data = {
            'message': 'Thank you for resolving my ticket'
        }
        response = self.client.post(reverse('support:ticket_detail', kwargs={'ticket_id': ticket.id}), response_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify that the response was added
        self.assertTrue(TicketResponse.objects.filter(ticket=ticket, user=self.user, message='Thank you for resolving my ticket').exists())
