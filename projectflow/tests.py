from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from teamflow.models import Team, TeamMember
from .models import Project, Task, SubTask
from unittest.mock import patch

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        with patch('django.db.models.fields.files.ImageFieldFile'):
            self.team = Team.objects.create(
                name='Test Team',
                url='test-team',
                description='Test Team Description',
                teamAuthor=self.user
            )
            
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Project Description',
            status='Todo',
            slug='test-project',
            team=self.team
        )
    
    def test_project_creation(self):
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.description, 'Test Project Description')
        self.assertEqual(self.project.status, 'Todo')
        self.assertEqual(self.project.slug, 'test-project')
        self.assertEqual(self.project.team, self.team)
        
    def test_project_status_choices(self):
        # Test that status can only be one of the predefined choices
        self.project.status = 'Doing'
        self.project.save()
        self.assertEqual(self.project.status, 'Doing')
        
        self.project.status = 'Done'
        self.project.save()
        self.assertEqual(self.project.status, 'Done')
        
    def test_project_str_method(self):
        self.assertEqual(str(self.project), 'Test Project')
        
    def test_project_slug_generation(self):
        project = Project.objects.create(
            name='Another Project',
            description='Another Project Description',
            status='Todo',
            team=self.team
        )
        self.assertEqual(project.slug, 'another-project')

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
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
            status='Todo',
            slug='test-project',
            team=self.team
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
        
    def test_task_str_method(self):
        self.assertEqual(str(self.task), 'Test Task - Test Project')

class SubTaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
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
            status='Todo',
            slug='test-project',
            team=self.team
        )
        
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Task Description',
            status='Todo',
            project=self.project
        )
        
        self.subtask = SubTask.objects.create(
            name='Test SubTask',
            description='Test SubTask Description',
            status='Todo',
            task=self.task,
            team_member=self.team_member
        )
    
    def test_subtask_creation(self):
        self.assertEqual(self.subtask.name, 'Test SubTask')
        self.assertEqual(self.subtask.description, 'Test SubTask Description')
        self.assertEqual(self.subtask.status, 'Todo')
        self.assertEqual(self.subtask.task, self.task)
        self.assertEqual(self.subtask.team_member, self.team_member)
        
    def test_subtask_status_choices(self):
        # Test that status can only be one of the predefined choices
        self.subtask.status = 'Doing'
        self.subtask.save()
        self.assertEqual(self.subtask.status, 'Doing')
        
        self.subtask.status = 'Done'
        self.subtask.save()
        self.assertEqual(self.subtask.status, 'Done')
        
    def test_subtask_str_method(self):
        self.assertEqual(str(self.subtask), 'Test SubTask - Test Task')

class ProjectViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
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
            status='Todo',
            slug='test-project',
            team=self.team
        )
        
        self.client.login(username='testuser', password='testpassword')
    
    def test_project_list_view(self):
        response = self.client.get(reverse('projectflow:project-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/project_list.html')
        self.assertContains(response, 'Test Project')
        
    def test_project_detail_view(self):
        response = self.client.get(reverse('projectflow:project-detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/project_detail.html')
        self.assertContains(response, 'Test Project')
        self.assertContains(response, 'Test Project Description')
        
    def test_project_create_view(self):
        response = self.client.get(reverse('projectflow:project-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/project_form.html')
        
        # Test POST request
        response = self.client.post(reverse('projectflow:project-create'), {
            'name': 'New Project',
            'description': 'New Project Description',
            'status': 'Todo',
            'team': self.team.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Project.objects.filter(name='New Project').exists())
        
    def test_project_update_view(self):
        response = self.client.get(reverse('projectflow:project-update', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/project_form.html')
        
        # Test POST request
        response = self.client.post(reverse('projectflow:project-update', kwargs={'slug': self.project.slug}), {
            'name': 'Updated Project',
            'description': 'Updated Project Description',
            'status': 'Doing',
            'team': self.team.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Updated Project')
        self.assertEqual(self.project.description, 'Updated Project Description')
        self.assertEqual(self.project.status, 'Doing')
        
    def test_project_delete_view(self):
        response = self.client.get(reverse('projectflow:project-delete', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/project_confirm_delete.html')
        
        # Test POST request
        response = self.client.post(reverse('projectflow:project-delete', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Project.objects.filter(slug='test-project').exists())

class TaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
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
            status='Todo',
            slug='test-project',
            team=self.team
        )
        
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Task Description',
            status='Todo',
            project=self.project
        )
        self.task.team_member.add(self.team_member)
        
        self.client.login(username='testuser', password='testpassword')
    
    def test_task_list_view(self):
        response = self.client.get(reverse('projectflow:task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/task_list.html')
        self.assertContains(response, 'Test Task')
        
    def test_task_detail_view(self):
        response = self.client.get(reverse('projectflow:task-detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/task_detail.html')
        self.assertContains(response, 'Test Task')
        self.assertContains(response, 'Test Task Description')
        
    def test_task_create_view(self):
        response = self.client.get(reverse('projectflow:task-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/task_form.html')
        
        # Test POST request
        response = self.client.post(reverse('projectflow:task-create'), {
            'name': 'New Task',
            'description': 'New Task Description',
            'status': 'Todo',
            'project': self.project.id,
            'team_member': [self.team_member.id]
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Task.objects.filter(name='New Task').exists())
        
    def test_task_update_view(self):
        response = self.client.get(reverse('projectflow:task-update', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/task_form.html')
        
        # Test POST request
        response = self.client.post(reverse('projectflow:task-update', kwargs={'pk': self.task.pk}), {
            'name': 'Updated Task',
            'description': 'Updated Task Description',
            'status': 'Doing',
            'project': self.project.id,
            'team_member': [self.team_member.id]
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Task Description')
        self.assertEqual(self.task.status, 'Doing')
        
    def test_task_delete_view(self):
        response = self.client.get(reverse('projectflow:task-delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/task_confirm_delete.html')
        
        # Test POST request
        response = self.client.post(reverse('projectflow:task-delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        
    def test_task_status_update(self):
        response = self.client.post(reverse('projectflow:task-update-status', kwargs={'pk': self.task.pk}), {
            'status': 'Doing'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'Doing')

class SubTaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
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
            status='Todo',
            slug='test-project',
            team=self.team
        )
        
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Task Description',
            status='Todo',
            project=self.project
        )
        self.task.team_member.add(self.team_member)
        
        self.subtask = SubTask.objects.create(
            name='Test SubTask',
            description='Test SubTask Description',
            status='Todo',
            task=self.task,
            team_member=self.team_member
        )
        
        self.client.login(username='testuser', password='testpassword')
    
    def test_subtask_create_view(self):
        response = self.client.get(reverse('projectflow:subtask-create-for-task', kwargs={'task_id': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/subtask_form.html')
        
        # Test POST request
        response = self.client.post(reverse('projectflow:subtask-create-for-task', kwargs={'task_id': self.task.pk}), {
            'name': 'New SubTask',
            'description': 'New SubTask Description',
            'status': 'Todo',
            'task': self.task.id,
            'team_member': self.team_member.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(SubTask.objects.filter(name='New SubTask').exists())
        
    def test_subtask_update_view(self):
        response = self.client.get(reverse('projectflow:subtask-update', kwargs={'pk': self.subtask.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/subtask_form.html')
        
        # Test POST request
        response = self.client.post(reverse('projectflow:subtask-update', kwargs={'pk': self.subtask.pk}), {
            'name': 'Updated SubTask',
            'description': 'Updated SubTask Description',
            'status': 'Doing',
            'task': self.task.id,
            'team_member': self.team_member.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.subtask.refresh_from_db()
        self.assertEqual(self.subtask.name, 'Updated SubTask')
        self.assertEqual(self.subtask.description, 'Updated SubTask Description')
        self.assertEqual(self.subtask.status, 'Doing')
        
    def test_subtask_delete_view(self):
        response = self.client.get(reverse('projectflow:subtask-delete', kwargs={'pk': self.subtask.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projectflow/subtask_confirm_delete.html')
        
        # Test POST request
        response = self.client.post(reverse('projectflow:subtask-delete', kwargs={'pk': self.subtask.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(SubTask.objects.filter(pk=self.subtask.pk).exists())
        
    def test_subtask_status_update(self):
        response = self.client.post(reverse('projectflow:subtask-update-status', kwargs={'pk': self.subtask.pk}), {
            'status': 'Doing'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.subtask.refresh_from_db()
        self.assertEqual(self.subtask.status, 'Doing')
