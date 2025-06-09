from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import json
from projectflow.models import Project, Task, SubTask
from teamflow.models import Team, TeamMember

class TimelineViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create a team
        self.team = Team.objects.create(
            name='Test Team',
            url='test-team',
            description='Test team description',
            teamAuthor=self.user
        )
        
        # Add user to team
        self.team_member = TeamMember.objects.create(
            team=self.team,
            user=self.user,
            handle='testuser',
            is_manager=True
        )
        
        # Create a project
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            status='Doing',
            team=self.team,
            is_public=True,
            project_type='standard',
            due_date=timezone.now().date() + timedelta(days=30)
        )
        self.project.assigned_users.add(self.user)
        
        # Create tasks with different statuses and a milestone
        self.milestone = Task.objects.create(
            project=self.project,
            name='Project Milestone',
            description='A milestone task',
            status='Todo',
            is_milestone=True,
            order=0,
            due_date=timezone.now().date() + timedelta(days=15)
        )
        
        self.task1 = Task.objects.create(
            project=self.project,
            name='Completed Task',
            description='A completed task',
            status='Done',
            order=1,
            due_date=timezone.now().date() - timedelta(days=5)
        )
        
        self.task2 = Task.objects.create(
            project=self.project,
            name='In Progress Task',
            description='A task in progress',
            status='Doing',
            order=2,
            due_date=timezone.now().date() + timedelta(days=10)
        )
        
        self.task3 = Task.objects.create(
            project=self.project,
            name='Future Task',
            description='A future task',
            status='Todo',
            order=3,
            due_date=timezone.now().date() + timedelta(days=20)
        )
        
        # Create a client and log in
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_project_detail_has_timeline_tab(self):
        """Test that the project detail page has a timeline tab"""
        response = self.client.get(reverse('projectflow:project-detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        
        # Check that the timeline view exists and is accessible
        timeline_url = reverse('projectflow:project-timeline', kwargs={'slug': self.project.slug})
        timeline_response = self.client.get(timeline_url)
        self.assertEqual(timeline_response.status_code, 200)

    def test_project_timeline_view(self):
        """Test that the project timeline view works"""
        response = self.client.get(reverse('projectflow:project-timeline', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.name)
        
        # Check that all tasks are in the timeline
        self.assertContains(response, self.milestone.name)
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)
        
        # Check for timeline elements
        self.assertContains(response, 'timeline-item')
        self.assertContains(response, 'timeline-content')

    def test_reorder_tasks_api(self):
        """Test the API endpoint for reordering tasks"""
        url = reverse('projectflow:reorder-tasks', kwargs={'project_slug': self.project.slug})
        data = {
            'taskOrder': [self.task3.id, self.task2.id, self.task1.id, self.milestone.id]
        }
        response = self.client.post(
            url, 
            json.dumps(data),
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        
        # Check that tasks were reordered
        self.task3.refresh_from_db()
        self.task2.refresh_from_db()
        self.task1.refresh_from_db()
        self.milestone.refresh_from_db()
        
        self.assertEqual(self.task3.order, 0)
        self.assertEqual(self.task2.order, 1)
        self.assertEqual(self.task1.order, 2)
        self.assertEqual(self.milestone.order, 3)

class RoadmapViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create a team
        self.team = Team.objects.create(
            name='Test Team',
            url='test-team',
            description='Test team description',
            teamAuthor=self.user
        )
        
        # Add user to team
        self.team_member = TeamMember.objects.create(
            team=self.team,
            user=self.user,
            handle='testuser',
            is_manager=True
        )
        
        # Create a roadmap project
        self.roadmap = Project.objects.create(
            name='Test Roadmap',
            description='Test roadmap description',
            status='Doing',
            team=self.team,
            is_public=True,
            project_type='roadmap',
            due_date=timezone.now().date() + timedelta(days=365)
        )
        self.roadmap.assigned_users.add(self.user)
        
        # Create feature projects (subprojects of the roadmap)
        self.feature1 = Project.objects.create(
            name='Feature 1',
            description='Feature 1 description',
            status='Done',
            team=self.team,
            is_public=True,
            project_type='standard',
            parent=self.roadmap,
            due_date=timezone.now().date() + timedelta(days=30)
        )
        
        self.feature2 = Project.objects.create(
            name='Feature 2',
            description='Feature 2 description',
            status='Doing',
            team=self.team,
            is_public=True,
            project_type='standard',
            parent=self.roadmap,
            due_date=timezone.now().date() + timedelta(days=90)
        )
        
        self.feature3 = Project.objects.create(
            name='Feature 3',
            description='Feature 3 description',
            status='Todo',
            team=self.team,
            is_public=True,
            project_type='standard',
            parent=self.roadmap,
            due_date=timezone.now().date() + timedelta(days=180)
        )
        
        # Create a client and log in
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_roadmap_list_view(self):
        """Test that the roadmap list view works"""
        response = self.client.get(reverse('projectflow:roadmap-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Feature Roadmaps')
        self.assertContains(response, self.roadmap.name)

    def test_roadmap_detail_view(self):
        """Test that the roadmap detail view works"""
        response = self.client.get(reverse('projectflow:roadmap-detail', kwargs={'slug': self.roadmap.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.roadmap.name)
        self.assertContains(response, 'Feature Roadmap')
        
        # Check that all features are in the roadmap
        self.assertContains(response, self.feature1.name)
        self.assertContains(response, self.feature2.name)
        self.assertContains(response, self.feature3.name)
        
        # Check that features have the correct status classes
        self.assertContains(response, 'feature-item Done')
        self.assertContains(response, 'feature-item Doing')
        self.assertContains(response, 'feature-item Todo')

    def test_project_type_field(self):
        """Test that the project_type field works correctly"""
        self.assertEqual(self.roadmap.project_type, 'roadmap')
        self.assertEqual(self.feature1.project_type, 'standard')
        
        # Test that the roadmap view is accessible
        response = self.client.get(reverse('projectflow:roadmap-detail', kwargs={'slug': self.roadmap.slug}))
        self.assertEqual(response.status_code, 200)
