from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from teamflow.models import Team, TeamMember
from projectflow.models import Project, Task
from .models import Program, TimestampedModel

class TimestampedModelTest(TestCase):
    def test_timestamped_model_fields(self):
        # Create a concrete subclass for testing
        class TestModel(TimestampedModel):
            class Meta:
                app_label = 'webcore'
        
        # Check that the fields are defined correctly
        self.assertTrue(hasattr(TestModel, 'created_at'))
        self.assertTrue(hasattr(TestModel, 'updated_at'))
        
        # Check that the Meta options are set correctly
        self.assertEqual(TestModel._meta.ordering, ['-created_at', '-updated_at'])
        self.assertTrue(TestModel._meta.abstract)

class ProgramModelTest(TestCase):
    def setUp(self):
        self.program = Program.objects.create(
            name='Test Program',
            description='Test Program Description'
        )
    
    def test_program_creation(self):
        self.assertEqual(self.program.name, 'Test Program')
        self.assertEqual(self.program.description, 'Test Program Description')
        
    def test_program_str_method(self):
        self.assertEqual(str(self.program), 'Test Program')

class HomeViewTest(TestCase):
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
    
    def test_home_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('webcore:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        
        # Check that context contains the expected data
        self.assertIn('projects', response.context)
        self.assertIn('tasks', response.context)
        self.assertIn('teams', response.context)
        self.assertEqual(list(response.context['projects']), [self.project])
        self.assertEqual(list(response.context['tasks']), [self.task])
        self.assertEqual(list(response.context['teams']), [self.team])
        
        # Check that the page contains the expected content
        self.assertContains(response, 'Test Project')
        self.assertContains(response, 'Test Task')
        self.assertContains(response, 'Test Team')
    
    def test_home_view_unauthenticated(self):
        response = self.client.get(reverse('webcore:home'))
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertTrue(response.url.startswith(reverse('accounts:login')))

class FormUtilsTest(TestCase):
    def test_bs_char_field(self):
        from webcore.forms import BsCharField
        field = BsCharField()
        self.assertEqual(field.widget.attrs['class'], 'form-control')
    
    def test_bs_email_field(self):
        from webcore.forms import BsEmailField
        field = BsEmailField()
        self.assertEqual(field.widget.attrs['class'], 'form-control')
    
    def test_bs_password_field(self):
        from webcore.forms import BsPasswordField
        field = BsPasswordField()
        self.assertEqual(field.widget.attrs['class'], 'form-control')
        self.assertEqual(field.widget.__class__.__name__, 'PasswordInput')
    
    def test_bs_choice_field(self):
        from webcore.forms import BsChoiceField
        field = BsChoiceField(choices=[('1', 'One'), ('2', 'Two')])
        self.assertEqual(field.widget.attrs['class'], 'form-control')
    
    def test_bs_phone_number_field(self):
        from webcore.forms import BsPhoneNumberField
        field = BsPhoneNumberField()
        self.assertEqual(field.widget.attrs['class'], 'form-control')
        self.assertEqual(field.widget.attrs['type'], 'tel')
    
    def test_form_link(self):
        from webcore.forms import FormLink
        form_link = FormLink(form_class='TestForm', link_field='test_field', link_value_field='test_value')
        self.assertEqual(form_link.form_class, 'TestForm')
        self.assertEqual(form_link.link_field, 'test_field')
        self.assertEqual(form_link.link_value_field, 'test_value')
    
    def test_extra_form_context(self):
        from webcore.forms import ExtraFormContext
        extra_context = ExtraFormContext(form_class='TestForm', extra_context={'test': 'value'})
        self.assertEqual(extra_context.form_class, 'TestForm')
        self.assertEqual(extra_context.extra_context, {'test': 'value'})
        
        # Test default extra_context
        extra_context = ExtraFormContext(form_class='TestForm')
        self.assertEqual(extra_context.extra_context, {})
