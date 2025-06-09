from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from projectflow.models import Project, Task, SubTask
from teamflow.models import Team, TeamMember
from workspace.models import Workspace, WorkspaceUser
from support.models import Ticket, TicketResponse

class ProjectModelTest(TestCase):
    """Test case for Project model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.team = Team.objects.create(
            name='Test Team',
            url='test-team',
            description='Test team description'
        )
        
        self.project = Project.objects.create(
            name='Test Project',
            slug='test-project',
            description='Test project description',
            status='Todo',
            is_public=True,
            team=self.team
        )
        
        # Create tasks with different statuses
        Task.objects.create(
            name='Task 1',
            description='Task 1 description',
            status='Todo',
            project=self.project,
            order=1
        )
        
        Task.objects.create(
            name='Task 2',
            description='Task 2 description',
            status='Doing',
            project=self.project,
            order=2
        )
        
        Task.objects.create(
            name='Task 3',
            description='Task 3 description',
            status='Done',
            project=self.project,
            order=3
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
    
    def test_project_get_absolute_url(self):
        """Test project get_absolute_url method"""
        self.assertEqual(self.project.get_absolute_url(), f'/projects/project/{self.project.slug}/')
    
    def test_project_completion_percentage(self):
        """Test project completion percentage calculation"""
        # 1 out of 3 tasks are done, so completion should be 33.33%
        self.assertAlmostEqual(self.project.get_completion_percentage(), 33.33, delta=0.01)
        
        # Change another task to Done
        task = Task.objects.get(name='Task 2')
        task.status = 'Done'
        task.save()
        
        # Now 2 out of 3 tasks are done, so completion should be 66.67%
        self.assertAlmostEqual(self.project.get_completion_percentage(), 66.67, delta=0.01)
    
    def test_project_is_overdue(self):
        """Test project is_overdue property"""
        # Project without due date should not be overdue
        self.assertFalse(self.project.is_overdue)
        
        # Set due date to yesterday
        yesterday = timezone.now().date() - timedelta(days=1)
        self.project.due_date = yesterday
        self.project.save()
        
        # Project should now be overdue
        self.assertTrue(self.project.is_overdue)
        
        # Set due date to tomorrow
        tomorrow = timezone.now().date() + timedelta(days=1)
        self.project.due_date = tomorrow
        self.project.save()
        
        # Project should not be overdue
        self.assertFalse(self.project.is_overdue)
    
    def test_project_roadmap_features(self):
        """Test project roadmap features"""
        # Create a roadmap project
        roadmap = Project.objects.create(
            name='Product Roadmap',
            slug='product-roadmap',
            description='Product roadmap for 2025',
            status='Todo',
            is_public=True,
            project_type='roadmap'
        )
        
        # Create feature projects (subprojects)
        feature1 = Project.objects.create(
            name='Feature 1',
            slug='feature-1',
            description='Feature 1 description',
            status='Todo',
            is_public=True,
            parent=roadmap
        )
        
        feature2 = Project.objects.create(
            name='Feature 2',
            slug='feature-2',
            description='Feature 2 description',
            status='Doing',
            is_public=True,
            parent=roadmap
        )
        
        # Test that roadmap has subprojects
        self.assertEqual(roadmap.subprojects.count(), 2)
        self.assertIn(feature1, roadmap.subprojects.all())
        self.assertIn(feature2, roadmap.subprojects.all())
        
        # Test that features have parent
        self.assertEqual(feature1.parent, roadmap)
        self.assertEqual(feature2.parent, roadmap)


class TaskModelTest(TestCase):
    """Test case for Task model"""
    
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project',
            slug='test-project',
            description='Test project description',
            status='Todo',
            is_public=True
        )
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
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
        
        # Create subtasks
        self.subtask1 = SubTask.objects.create(
            name='Subtask 1',
            description='Subtask 1 description',
            status='Todo',
            task=self.task,
            order=1
        )
        
        self.subtask2 = SubTask.objects.create(
            name='Subtask 2',
            description='Subtask 2 description',
            status='Done',
            task=self.task,
            order=2
        )
    
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
    
    def test_task_get_absolute_url(self):
        """Test task get_absolute_url method"""
        self.assertEqual(self.task.get_absolute_url(), f'/projects/task/{self.task.id}/')
    
    def test_task_completion_percentage(self):
        """Test task completion percentage calculation"""
        # 1 out of 2 subtasks are done, so completion should be 50%
        self.assertEqual(self.task.get_completion_percentage(), 50.0)
        
        # Change another subtask to Done
        self.subtask1.status = 'Done'
        self.subtask1.save()
        
        # Now 2 out of 2 subtasks are done, so completion should be 100%
        self.assertEqual(self.task.get_completion_percentage(), 100.0)
    
    def test_task_is_overdue(self):
        """Test task is_overdue property"""
        # Task without due date should not be overdue
        self.assertFalse(self.task.is_overdue)
        
        # Set due date to yesterday
        yesterday = timezone.now().date() - timedelta(days=1)
        self.task.due_date = yesterday
        self.task.save()
        
        # Task should now be overdue
        self.assertTrue(self.task.is_overdue)
        
        # Set due date to tomorrow
        tomorrow = timezone.now().date() + timedelta(days=1)
        self.task.due_date = tomorrow
        self.task.save()
        
        # Task should not be overdue
        self.assertFalse(self.task.is_overdue)
    
    def test_task_milestone_feature(self):
        """Test task milestone feature"""
        # Task should not be a milestone by default
        self.assertFalse(self.task.is_milestone)
        
        # Set task as milestone
        self.task.is_milestone = True
        self.task.save()
        
        # Task should now be a milestone
        self.assertTrue(self.task.is_milestone)


class TeamModelTest(TestCase):
    """Test case for Team model"""
    
    def setUp(self):
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
        
        self.team = Team.objects.create(
            name='Test Team',
            url='test-team',
            description='Test team description'
        )
        
        # Add members to team
        self.member1 = TeamMember.objects.create(
            user=self.user1,
            team=self.team,
            role='Admin'
        )
        
        self.member2 = TeamMember.objects.create(
            user=self.user2,
            team=self.team,
            role='Member'
        )
    
    def test_team_creation(self):
        """Test team creation"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.url, 'test-team')
        self.assertEqual(self.team.description, 'Test team description')
    
    def test_team_str_method(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')
    
    def test_team_get_absolute_url(self):
        """Test team get_absolute_url method"""
        self.assertEqual(self.team.get_absolute_url(), f'/teams/team/{self.team.url}/')
    
    def test_team_members(self):
        """Test team members"""
        self.assertEqual(self.team.members.count(), 2)
        self.assertIn(self.member1, self.team.members.all())
        self.assertIn(self.member2, self.team.members.all())
        
        # Test member roles
        self.assertEqual(self.member1.role, 'Admin')
        self.assertEqual(self.member2.role, 'Member')


class WorkspaceModelTest(TestCase):
    """Test case for Workspace model"""
    
    def setUp(self):
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
        
        # Create projects in workspace
        self.project1 = Project.objects.create(
            name='Project 1',
            slug='project-1',
            description='Project 1 description',
            status='Todo',
            is_public=True,
            workspace=self.workspace
        )
        
        self.project2 = Project.objects.create(
            name='Project 2',
            slug='project-2',
            description='Project 2 description',
            status='Doing',
            is_public=True,
            workspace=self.workspace
        )
    
    def test_workspace_creation(self):
        """Test workspace creation"""
        self.assertEqual(self.workspace.name, 'Test Workspace')
        self.assertEqual(self.workspace.description, 'Test workspace description')
    
    def test_workspace_str_method(self):
        """Test workspace string representation"""
        self.assertEqual(str(self.workspace), 'Test Workspace')
    
    def test_workspace_users(self):
        """Test workspace users"""
        self.assertEqual(self.workspace.workspaceuser_set.count(), 2)
        self.assertIn(self.workspace_user1, self.workspace.workspaceuser_set.all())
        self.assertIn(self.workspace_user2, self.workspace.workspaceuser_set.all())
        
        # Test user roles
        self.assertEqual(self.workspace_user1.role, 'Admin')
        self.assertEqual(self.workspace_user2.role, 'Member')
    
    def test_workspace_projects(self):
        """Test workspace projects"""
        self.assertEqual(self.workspace.projects.count(), 2)
        self.assertIn(self.project1, self.workspace.projects.all())
        self.assertIn(self.project2, self.workspace.projects.all())


class SupportModelTest(TestCase):
    """Test case for Support models"""
    
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
    
    def test_ticket_response_str_method(self):
        """Test ticket response string representation"""
        self.assertEqual(str(self.response), 'Response to Test Ticket by admin')
    
    def test_ticket_responses_relationship(self):
        """Test ticket responses relationship"""
        self.assertEqual(self.ticket.responses.count(), 1)
        self.assertIn(self.response, self.ticket.responses.all())
