from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
from invites.models import Invite
from workspace.models import Workspace, WorkspaceUser
from teamflow.models import Team, TeamMember
from projectflow.models import Project

class InviteViewsTest(TestCase):
    def setUp(self):
        # Create client
        self.client = Client()
        
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='password123'
        )
        self.new_user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='password123'
        )
        
        # Create a workspace
        self.workspace = Workspace.objects.create(
            name='Test Workspace',
            description='Test workspace description'
        )
        WorkspaceUser.objects.create(
            workspace=self.workspace,
            user=self.admin_user,
            role='admin'
        )
        
        # Create a team
        self.team = Team.objects.create(
            name='Test Team',
            url='test-team',
            description='Test team description',
            teamAuthor=self.admin_user
        )
        TeamMember.objects.create(
            team=self.team,
            user=self.admin_user,
            is_manager=True
        )
        
        # Create a project
        self.project = Project.objects.create(
            name='Test Project',
            slug='test-project',
            description='Test project description',
            status='Todo',
            team=self.team,
            workspace=self.workspace
        )
        
        # Get content types
        workspace_content_type = ContentType.objects.get_for_model(Workspace)
        team_content_type = ContentType.objects.get_for_model(Team)
        project_content_type = ContentType.objects.get_for_model(Project)
        
        # Create invites
        self.workspace_invite = Invite.objects.create(
            email='newuser@example.com',
            invited_by=self.admin_user,
            content_type=workspace_content_type,
            object_id=self.workspace.id,
            role='workspace_member'
        )
        
        self.team_invite = Invite.objects.create(
            email='newuser@example.com',
            invited_by=self.admin_user,
            content_type=team_content_type,
            object_id=self.team.id,
            role='team_member'
        )
        
        self.project_invite = Invite.objects.create(
            email='newuser@example.com',
            invited_by=self.admin_user,
            content_type=project_content_type,
            object_id=self.project.id,
            role='project_member'
        )
        
        # Create an expired invite
        self.expired_invite = Invite.objects.create(
            email='newuser@example.com',
            invited_by=self.admin_user,
            content_type=workspace_content_type,
            object_id=self.workspace.id,
            role='workspace_member',
            expires_at=timezone.now() - timedelta(days=1)
        )

    def test_send_workspace_invite_view(self):
        """Test sending a workspace invite"""
        # Login as admin
        self.client.login(username='admin', password='password123')
        
        # Send invite
        url = reverse('invites:send', kwargs={'target_type': 'workspace', 'target_id': self.workspace.id})
        response = self.client.post(url, {
            'email': 'another@example.com',
            'role': 'workspace_member'
        })
        
        # Check redirect
        self.assertRedirects(response, reverse('workspace:detail', args=[self.workspace.id]))
        
        # Check that invite was created
        self.assertTrue(Invite.objects.filter(
            email='another@example.com',
            role='workspace_member',
            object_id=self.workspace.id
        ).exists())
        
    def test_send_team_invite_view(self):
        """Test sending a team invite"""
        # Login as admin
        self.client.login(username='admin', password='password123')
        
        # Send invite
        url = reverse('invites:send', kwargs={'target_type': 'team', 'target_id': self.team.id})
        response = self.client.post(url, {
            'email': 'another@example.com',
            'role': 'team_member'
        })
        
        # Check redirect
        self.assertRedirects(response, reverse('teamflow:team-detail', args=[self.team.url]))
        
        # Check that invite was created
        self.assertTrue(Invite.objects.filter(
            email='another@example.com',
            role='team_member',
            object_id=self.team.id
        ).exists())
        
    def test_send_project_invite_view(self):
        """Test sending a project invite"""
        # Login as admin
        self.client.login(username='admin', password='password123')
        
        # Send invite
        url = reverse('invites:send', kwargs={'target_type': 'project', 'target_id': self.project.id})
        response = self.client.post(url, {
            'email': 'another@example.com',
            'role': 'project_member'
        })
        
        # Check redirect
        self.assertRedirects(response, reverse('projectflow:project-detail', args=[self.project.slug]))
        
        # Check that invite was created
        self.assertTrue(Invite.objects.filter(
            email='another@example.com',
            role='project_member',
            object_id=self.project.id
        ).exists())
        
    def test_unauthorized_invite_attempt(self):
        """Test that unauthorized users cannot send invites"""
        # Login as regular user
        self.client.login(username='regular', password='password123')
        
        # Try to send workspace invite
        url = reverse('invites:send', kwargs={'target_type': 'workspace', 'target_id': self.workspace.id})
        response = self.client.post(url, {
            'email': 'another@example.com',
            'role': 'workspace_member'
        })
        
        # Should be redirected to home with error
        self.assertRedirects(response, reverse('home'))
        
        # Check that invite was not created
        self.assertFalse(Invite.objects.filter(
            email='another@example.com',
            role='workspace_member',
            object_id=self.workspace.id
        ).exists())
        
    def test_accept_workspace_invite(self):
        """Test accepting a workspace invite"""
        # Login as new user
        self.client.login(username='newuser', password='password123')
        
        # Accept invite
        url = reverse('invites:accept', kwargs={'token': self.workspace_invite.token})
        response = self.client.get(url)
        
        # Check redirect
        self.assertRedirects(response, reverse('workspace:detail', args=[self.workspace.id]))
        
        # Check that invite is marked as accepted
        self.workspace_invite.refresh_from_db()
        self.assertTrue(self.workspace_invite.accepted)
        
        # Check that user was added to workspace
        self.assertTrue(WorkspaceUser.objects.filter(
            workspace=self.workspace,
            user=self.new_user
        ).exists())
        
    def test_accept_team_invite(self):
        """Test accepting a team invite"""
        # Login as new user
        self.client.login(username='newuser', password='password123')
        
        # Accept invite
        url = reverse('invites:accept', kwargs={'token': self.team_invite.token})
        response = self.client.get(url)
        
        # Check redirect
        self.assertRedirects(response, reverse('teamflow:team-detail', args=[self.team.url]))
        
        # Check that invite is marked as accepted
        self.team_invite.refresh_from_db()
        self.assertTrue(self.team_invite.accepted)
        
        # Check that user was added to team
        self.assertTrue(TeamMember.objects.filter(
            team=self.team,
            user=self.new_user
        ).exists())
        
    def test_accept_project_invite(self):
        """Test accepting a project invite"""
        # Login as new user
        self.client.login(username='newuser', password='password123')
        
        # Accept invite
        url = reverse('invites:accept', kwargs={'token': self.project_invite.token})
        response = self.client.get(url)
        
        # Check redirect
        self.assertRedirects(response, reverse('projectflow:project-detail', args=[self.project.slug]))
        
        # Check that invite is marked as accepted
        self.project_invite.refresh_from_db()
        self.assertTrue(self.project_invite.accepted)
        
        # Check that user was added to project
        self.assertTrue(self.new_user in self.project.assigned_users.all())
        
    def test_accept_expired_invite(self):
        """Test that expired invites cannot be accepted"""
        # Login as new user
        self.client.login(username='newuser', password='password123')
        
        # Try to accept expired invite
        url = reverse('invites:accept', kwargs={'token': self.expired_invite.token})
        response = self.client.get(url)
        
        # Should be redirected to home with error
        self.assertRedirects(response, reverse('home'))
        
        # Check that invite is still not accepted
        self.expired_invite.refresh_from_db()
        self.assertFalse(self.expired_invite.accepted)
        
        # Check that user was not added to workspace
        self.assertFalse(WorkspaceUser.objects.filter(
            workspace=self.workspace,
            user=self.new_user,
            role='member'
        ).exists())
        
    def test_wrong_user_accept_invite(self):
        """Test that only the invited user can accept an invite"""
        # Login as regular user (not the invited one)
        self.client.login(username='regular', password='password123')
        
        # Try to accept invite
        url = reverse('invites:accept', kwargs={'token': self.workspace_invite.token})
        response = self.client.get(url)
        
        # Should be redirected to home with error
        self.assertRedirects(response, reverse('home'))
        
        # Check that invite is still not accepted
        self.workspace_invite.refresh_from_db()
        self.assertFalse(self.workspace_invite.accepted)
