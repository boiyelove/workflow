from django.test import TestCase
from django.contrib.auth.models import User
from invites.forms import InviteForm
from workspace.models import Workspace
from teamflow.models import Team
from projectflow.models import Project

class InviteFormTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        # Create entities
        self.workspace = Workspace.objects.create(
            name='Test Workspace',
            description='Test workspace description'
        )
        
        self.team = Team.objects.create(
            name='Test Team',
            url='test-team',
            description='Test team description',
            teamAuthor=self.user
        )
        
        self.project = Project.objects.create(
            name='Test Project',
            description='Test project description',
            status='Todo',
            team=self.team,
            workspace=self.workspace
        )

    def test_workspace_invite_form(self):
        """Test that the invite form works correctly for workspaces"""
        form_data = {
            'email': 'newuser@example.com',
            'role': 'workspace_member'
        }
        
        form = InviteForm(
            data=form_data,
            target=self.workspace,
            invited_by=self.user,
            target_type='workspace'
        )
        
        self.assertTrue(form.is_valid())
        invite = form.save()
        
        self.assertEqual(invite.email, 'newuser@example.com')
        self.assertEqual(invite.role, 'workspace_member')
        self.assertEqual(invite.target, self.workspace)
        self.assertEqual(invite.invited_by, self.user)
        
    def test_team_invite_form(self):
        """Test that the invite form works correctly for teams"""
        form_data = {
            'email': 'newuser@example.com',
            'role': 'team_member'
        }
        
        form = InviteForm(
            data=form_data,
            target=self.team,
            invited_by=self.user,
            target_type='team'
        )
        
        self.assertTrue(form.is_valid())
        invite = form.save()
        
        self.assertEqual(invite.email, 'newuser@example.com')
        self.assertEqual(invite.role, 'team_member')
        self.assertEqual(invite.target, self.team)
        self.assertEqual(invite.invited_by, self.user)
        
    def test_project_invite_form(self):
        """Test that the invite form works correctly for projects"""
        form_data = {
            'email': 'newuser@example.com',
            'role': 'project_member'
        }
        
        form = InviteForm(
            data=form_data,
            target=self.project,
            invited_by=self.user,
            target_type='project'
        )
        
        self.assertTrue(form.is_valid())
        invite = form.save()
        
        self.assertEqual(invite.email, 'newuser@example.com')
        self.assertEqual(invite.role, 'project_member')
        self.assertEqual(invite.target, self.project)
        self.assertEqual(invite.invited_by, self.user)
        
    def test_form_role_filtering(self):
        """Test that the form filters role choices based on target_type"""
        # Test workspace form
        form = InviteForm(target_type='workspace')
        role_choices = [choice[0] for choice in form.fields['role'].choices]
        
        # Should only include workspace roles
        self.assertIn('workspace_admin', role_choices)
        self.assertIn('workspace_member', role_choices)
        self.assertNotIn('team_member', role_choices)
        self.assertNotIn('project_member', role_choices)
        
        # Test team form
        form = InviteForm(target_type='team')
        role_choices = [choice[0] for choice in form.fields['role'].choices]
        
        # Should only include team roles
        self.assertIn('team_manager', role_choices)
        self.assertIn('team_member', role_choices)
        self.assertNotIn('workspace_member', role_choices)
        self.assertNotIn('project_member', role_choices)
        
        # Test project form
        form = InviteForm(target_type='project')
        role_choices = [choice[0] for choice in form.fields['role'].choices]
        
        # Should only include project roles
        self.assertIn('project_manager', role_choices)
        self.assertIn('project_member', role_choices)
        self.assertIn('project_viewer', role_choices)
        self.assertNotIn('workspace_member', role_choices)
        self.assertNotIn('team_member', role_choices)
        
    def test_invalid_email(self):
        """Test form validation with invalid email"""
        form_data = {
            'email': 'not-an-email',
            'role': 'workspace_member'
        }
        
        form = InviteForm(
            data=form_data,
            target=self.workspace,
            invited_by=self.user,
            target_type='workspace'
        )
        
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
