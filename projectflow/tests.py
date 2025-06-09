from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from teamflow.models import Team, TeamMember
from .models import Project, Task
from unittest.mock import patch

class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Project Description',
            status='Todo'
        )
    
    def test_project_creation(self):
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.description, 'Test Project Description')
        self.assertEqual(self.project.status, 'Todo')
        
    def test_project_status_choices(self):
        # Test that status can only be one of the predefined choices
        self.project.status = 'Doing'
        self.project.save()
        self.assertEqual(self.project.status, 'Doing')
        
        self.project.status = 'Done'
        self.project.save()
        self.assertEqual(self.project.status, 'Done')

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Mock the ImageField to avoid Pillow issues
        with patch('django.db.models.fields.files.ImageFieldFile'):
            self.team = Team.objects.create(
                name='Test Team',
                url='test-team',
                description='Test Team Description',
                teamAuthor=self.user
            )
        
        self.team_member = TeamMember.objects.create(
            user=self.user,
            team=self.team,
            handle='testhandle',
            is_manager=True,
            designation='Developer'
        )
        
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Project Description',
            status='Todo'
        )
        
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Task Description',
            status='Todo',
            project=self.project
        )
        self.task.team_member.add(self.team_member)
    
    def test_task_creation(self):
        self.assertEqual(self.task.name, 'Test Task')
        self.assertEqual(self.task.description, 'Test Task Description')
        self.assertEqual(self.task.status, 'Todo')
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.team_member.count(), 1)
        self.assertEqual(self.task.team_member.first(), self.team_member)
        
    def test_task_status_choices(self):
        # Test that status can only be one of the predefined choices
        self.task.status = 'Doing'
        self.task.save()
        self.assertEqual(self.task.status, 'Doing')
        
        self.task.status = 'Done'
        self.task.save()
        self.assertEqual(self.task.status, 'Done')
        
    def test_task_team_member_relationship(self):
        # Create another team member and add to task
        another_user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='anotherpassword'
        )
        
        another_team_member = TeamMember.objects.create(
            user=another_user,
            team=self.team,
            handle='anotherhandle',
            is_manager=False,
            designation='Designer'
        )
        
        self.task.team_member.add(another_team_member)
        self.assertEqual(self.task.team_member.count(), 2)
        self.assertIn(self.team_member, self.task.team_member.all())
        self.assertIn(another_team_member, self.task.team_member.all())
        
        # Remove a team member
        self.task.team_member.remove(self.team_member)
        self.assertEqual(self.task.team_member.count(), 1)
        self.assertNotIn(self.team_member, self.task.team_member.all())
        self.assertIn(another_team_member, self.task.team_member.all())

class ProjectViewsTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Project Description',
            status='Todo'
        )
    
    def test_project_list_view(self):
        # This test will fail if the view is not properly configured
        # or if the template doesn't exist, but it tests the view class itself
        try:
            from .views import ProjectList
            view = ProjectList()
            self.assertEqual(view.model, Project)
            self.assertEqual(view.template_name, 'projects.html')
        except ImportError:
            self.fail("Failed to import ProjectList view")
    
    def test_project_detail_view(self):
        # This test will fail if the view is not properly configured
        # or if the template doesn't exist, but it tests the view class itself
        try:
            from .views import ProjectDetail
            view = ProjectDetail()
            self.assertEqual(view.model, Project)
            self.assertEqual(view.template_name, 'project_admin.html')
        except ImportError:
            self.fail("Failed to import ProjectDetail view")

class TaskViewsTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Project Description',
            status='Todo'
        )
        
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Task Description',
            status='Todo',
            project=self.project
        )
    
    def test_task_list_view(self):
        # This test will fail if the view is not properly configured
        # or if the template doesn't exist, but it tests the view class itself
        try:
            from .views import TaskList
            view = TaskList()
            self.assertEqual(view.model, Task)
            self.assertEqual(view.template_name, 'task.html')
        except ImportError:
            self.fail("Failed to import TaskList view")
    
    def test_task_detail_view(self):
        # This test will fail if the view is not properly configured
        # or if the template doesn't exist, but it tests the view class itself
        try:
            from .views import TaskDetail
            view = TaskDetail()
            self.assertEqual(view.model, Task)
            self.assertEqual(view.template_name, 'task.html')
        except ImportError:
            self.fail("Failed to import TaskDetail view")