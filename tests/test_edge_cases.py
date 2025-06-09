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

class PermissionEdgeCaseTest(TestCase):
    """Test case for permission edge cases"""
    
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
        
        # Create test team for user1
        self.team = Team.objects.create(
            name='Test Team',
            url='test-team',
            description='Test team description',
            teamAuthor=self.user1,
            teamAuthor=self.user1
        )
        
        # Add user1 to team
        self.team_member = TeamMember.objects.create(
            user=self.user1,
            team=self.team,
            role='Admin'
        )
        
        # Create test project for user1's team
        self.project = Project.objects.create(
            name='Private Project',
            slug='private-project',
            description='Private project description',
            status='Todo',
            is_public=False,  # Private project
            team=self.team
        )
        
        # Create test task in the project
        self.task = Task.objects.create(
            name='Private Task',
            description='Private task description',
            status='Todo',
            project=self.project,
            order=1
        )
        
        # Create test workspace for user1
        self.workspace = Workspace.objects.create(
            name='Private Workspace',
            description='Private workspace description'
        )
        
        # Add user1 to workspace
        self.workspace_user = WorkspaceUser.objects.create(
            user=self.user1,
            workspace=self.workspace,
            role='Admin'
        )
        
        # Create test ticket for user1
        self.ticket = Ticket.objects.create(
            title='Private Ticket',
            description='Private ticket description',
            created_by=self.user1,
            status='Open',
            priority='Medium'
        )
        
        # Create test clients
        self.client1 = Client()
        self.client2 = Client()
        
        # Login the users
        self.client1.login(username='testuser1', password='testpassword')
        self.client2.login(username='testuser2', password='testpassword')
    
    def test_private_project_access(self):
        """Test access to private project"""
        # User1 should be able to access their private project
        response = self.client1.get(reverse('projectflow:project-detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Private Project')
        
        # User2 should not be able to access user1's private project
        response = self.client2.get(reverse('projectflow:project-detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 302)  # Redirect to project list with error message
    
    def test_private_task_access(self):
        """Test access to private task"""
        # User1 should be able to access their private task
        response = self.client1.get(reverse('projectflow:task-detail', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Private Task')
        
        # User2 should not be able to access user1's private task
        response = self.client2.get(reverse('projectflow:task-detail', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 302)  # Redirect to task list with error message
    
    def test_private_workspace_access(self):
        """Test access to private workspace"""
        # User1 should be able to access their private workspace
        response = self.client1.get(reverse('workspace:detail', kwargs={'workspace_id': self.workspace.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Private Workspace')
        
        # User2 should not be able to access user1's private workspace
        response = self.client2.get(reverse('workspace:detail', kwargs={'workspace_id': self.workspace.id}))
        self.assertEqual(response.status_code, 302)  # Redirect to workspace list with error message
    
    def test_private_ticket_access(self):
        """Test access to private ticket"""
        # User1 should be able to access their private ticket
        response = self.client1.get(reverse('support:ticket_detail', kwargs={'ticket_id': self.ticket.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Private Ticket')
        
        # User2 should not be able to access user1's private ticket
        response = self.client2.get(reverse('support:ticket_detail', kwargs={'ticket_id': self.ticket.id}))
        self.assertEqual(response.status_code, 302)  # Redirect to ticket list with error message


class ValidationEdgeCaseTest(TestCase):
    """Test case for validation edge cases"""
    
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
            description='Test team description',
            teamAuthor=self.user1,
            teamAuthor=self.user1
        )
        
        # Add user to team
        self.team_member = TeamMember.objects.create(
            user=self.user,
            team=self.team,
            role='Admin'
        )
        
        # Create test project
        self.project = Project.objects.create(
            name='Test Project',
            slug='test-project',
            description='Test project description',
            status='Todo',
            is_public=True,
            team=self.team
        )
        
        # Create test client
        self.client = Client()
        
        # Login the user
        self.client.login(username='testuser', password='testpassword')
    
    def test_project_name_validation(self):
        """Test project name validation"""
        # Try to create a project with an empty name
        project_data = {
            'name': '',
            'description': 'Project with empty name',
            'status': 'Todo',
            'is_public': True,
            'team': self.team.id
        }
        response = self.client.post(reverse('projectflow:project-create'), project_data)
        self.assertEqual(response.status_code, 200)  # Form should be redisplayed with errors
        self.assertContains(response, 'This field is required')
        
        # Try to create a project with a very long name
        project_data = {
            'name': 'A' * 256,  # Assuming max length is 255
            'description': 'Project with very long name',
            'status': 'Todo',
            'is_public': True,
            'team': self.team.id
        }
        response = self.client.post(reverse('projectflow:project-create'), project_data)
        self.assertEqual(response.status_code, 200)  # Form should be redisplayed with errors
        self.assertContains(response, 'Ensure this value has at most')
    
    def test_task_order_validation(self):
        """Test task order validation"""
        # Create tasks with the same order
        task1_data = {
            'name': 'Task 1',
            'description': 'First task description',
            'status': 'Todo',
            'project': self.project.id,
            'order': 1
        }
        response = self.client.post(reverse('projectflow:task-create'), task1_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful creation
        
        task2_data = {
            'name': 'Task 2',
            'description': 'Second task description',
            'status': 'Todo',
            'project': self.project.id,
            'order': 1  # Same order as Task 1
        }
        response = self.client.post(reverse('projectflow:task-create'), task2_data)
        self.assertEqual(response.status_code, 302)  # Should still work, but order should be adjusted
        
        # Verify that the tasks have different orders
        task1 = Task.objects.get(name='Task 1')
        task2 = Task.objects.get(name='Task 2')
        self.assertNotEqual(task1.order, task2.order)
    
    def test_team_url_validation(self):
        """Test team URL validation"""
        # Try to create a team with an empty URL
        team_data = {
            'name': 'Empty URL Team',
            'url': '',
            'description': 'Team with empty URL'
        }
        response = self.client.post(reverse('teamflow:team-create'), team_data)
        self.assertEqual(response.status_code, 200)  # Form should be redisplayed with errors
        self.assertContains(response, 'This field is required')
        
        # Try to create a team with a duplicate URL
        team_data = {
            'name': 'Duplicate URL Team',
            'url': 'test-team',  # Same URL as existing team
            'description': 'Team with duplicate URL'
        }
        response = self.client.post(reverse('teamflow:team-create'), team_data)
        self.assertEqual(response.status_code, 200)  # Form should be redisplayed with errors
        self.assertContains(response, 'already exists')


class PerformanceEdgeCaseTest(TestCase):
    """Test case for performance edge cases"""
    
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
            description='Test team description',
            teamAuthor=self.user1,
            teamAuthor=self.user1
        )
        
        # Add user to team
        self.team_member = TeamMember.objects.create(
            user=self.user,
            team=self.team,
            role='Admin'
        )
        
        # Create test project
        self.project = Project.objects.create(
            name='Large Project',
            slug='large-project',
            description='Project with many tasks',
            status='Todo',
            is_public=True,
            team=self.team
        )
        
        # Create test client
        self.client = Client()
        
        # Login the user
        self.client.login(username='testuser', password='testpassword')
    
    def test_large_project_performance(self):
        """Test performance with a large number of tasks"""
        # Create 50 tasks for the project
        for i in range(1, 51):
            Task.objects.create(
                name=f'Task {i}',
                description=f'Description for Task {i}',
                status='Todo',
                project=self.project,
                order=i
            )
        
        # Verify that the project has 50 tasks
        self.assertEqual(self.project.tasks.count(), 50)
        
        # Test project detail view with 50 tasks
        start_time = timezone.now()
        response = self.client.get(reverse('projectflow:project-detail', kwargs={'slug': self.project.slug}))
        end_time = timezone.now()
        
        self.assertEqual(response.status_code, 200)
        
        # Check that the response time is reasonable (less than 1 second)
        response_time = (end_time - start_time).total_seconds()
        self.assertLess(response_time, 1.0)
        
        # Test project timeline view with 50 tasks
        start_time = timezone.now()
        response = self.client.get(reverse('projectflow:project-timeline', kwargs={'slug': self.project.slug}))
        end_time = timezone.now()
        
        self.assertEqual(response.status_code, 200)
        
        # Check that the response time is reasonable (less than 1 second)
        response_time = (end_time - start_time).total_seconds()
        self.assertLess(response_time, 1.0)
    
    def test_task_reordering_performance(self):
        """Test performance of task reordering"""
        # Create 20 tasks for the project
        for i in range(1, 21):
            Task.objects.create(
                name=f'Task {i}',
                description=f'Description for Task {i}',
                status='Todo',
                project=self.project,
                order=i
            )
        
        # Get the first and last tasks
        first_task = Task.objects.filter(project=self.project).order_by('order').first()
        last_task = Task.objects.filter(project=self.project).order_by('order').last()
        
        # Move the first task to the end
        start_time = timezone.now()
        response = self.client.post(
            reverse('projectflow:task-reorder'),
            json.dumps({
                'task_id': first_task.id,
                'new_order': last_task.order + 1
            }),
            content_type='application/json'
        )
        end_time = timezone.now()
        
        self.assertEqual(response.status_code, 200)
        
        # Check that the response time is reasonable (less than 0.5 seconds)
        response_time = (end_time - start_time).total_seconds()
        self.assertLess(response_time, 0.5)
        
        # Verify that the task was moved to the end
        first_task.refresh_from_db()
        self.assertEqual(first_task.order, last_task.order + 1)


class ErrorHandlingEdgeCaseTest(TestCase):
    """Test case for error handling edge cases"""
    
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
            description='Test team description',
            teamAuthor=self.user1,
            teamAuthor=self.user1
        )
        
        # Add user to team
        self.team_member = TeamMember.objects.create(
            user=self.user,
            team=self.team,
            role='Admin'
        )
        
        # Create test project
        self.project = Project.objects.create(
            name='Test Project',
            slug='test-project',
            description='Test project description',
            status='Todo',
            is_public=True,
            team=self.team
        )
        
        # Create test task
        self.task = Task.objects.create(
            name='Test Task',
            description='Test task description',
            status='Todo',
            project=self.project,
            order=1
        )
        
        # Create test client
        self.client = Client()
        
        # Login the user
        self.client.login(username='testuser', password='testpassword')
    
    def test_nonexistent_project(self):
        """Test accessing a nonexistent project"""
        response = self.client.get(reverse('projectflow:project-detail', kwargs={'slug': 'nonexistent-project'}))
        self.assertEqual(response.status_code, 404)
    
    def test_nonexistent_task(self):
        """Test accessing a nonexistent task"""
        response = self.client.get(reverse('projectflow:task-detail', kwargs={'task_id': 9999}))
        self.assertEqual(response.status_code, 404)
    
    def test_nonexistent_team(self):
        """Test accessing a nonexistent team"""
        response = self.client.get(reverse('teamflow:team-detail', kwargs={'url': 'nonexistent-team'}))
        self.assertEqual(response.status_code, 404)
    
    def test_invalid_task_status_update(self):
        """Test updating a task with an invalid status"""
        response = self.client.post(
            reverse('projectflow:task-update-status', kwargs={'task_id': self.task.id}),
            {'status': 'InvalidStatus'}
        )
        self.assertEqual(response.status_code, 400)  # Bad request
        
        # Verify that the task status was not changed
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'Todo')
    
    def test_delete_project_with_tasks(self):
        """Test deleting a project that has tasks"""
        # Create a task for the project
        Task.objects.create(
            name='Task to Delete',
            description='Task that should be deleted with the project',
            status='Todo',
            project=self.project,
            order=2
        )
        
        # Delete the project
        response = self.client.post(reverse('projectflow:project-delete', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        
        # Verify that the project was deleted
        self.assertFalse(Project.objects.filter(slug='test-project').exists())
        
        # Verify that the tasks were also deleted
        self.assertFalse(Task.objects.filter(project=self.project).exists())
