from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
from invites.models import Invite
from workspace.models import Workspace, WorkspaceUser
from teamflow.models import Team, TeamMember
from projectflow.models import Project

class InviteModelTest(TestCase):
    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
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
            description='Test project description',
            status='Todo',
            team=self.team,
            workspace=self.workspace
        )
        
        # Create invites
        workspace_content_type = ContentType.objects.get_for_model(Workspace)
        self.workspace_invite = Invite.objects.create(
            email='newuser@example.com',
            invited_by=self.admin_user,
            content_type=workspace_content_type,
            object_id=self.workspace.id,
            role='workspace_member'
        )
        
        team_content_type = ContentType.objects.get_for_model(Team)
        self.team_invite = Invite.objects.create(
            email='newuser@example.com',
            invited_by=self.admin_user,
            content_type=team_content_type,
            object_id=self.team.id,
            role='team_member'
        )
        
        project_content_type = ContentType.objects.get_for_model(Project)
        self.project_invite = Invite.objects.create(
            email='newuser@example.com',
            invited_by=self.admin_user,
            content_type=project_content_type,
            object_id=self.project.id,
            role='project_member'
        )
        
        # Create an expired invite
        self.expired_invite = Invite.objects.create(
            email='expired@example.com',
            invited_by=self.admin_user,
            content_type=workspace_content_type,
            object_id=self.workspace.id,
            role='workspace_member',
            expires_at=timezone.now() - timedelta(days=1)
        )

    def test_invite_creation(self):
        """Test that invites are created correctly"""
        self.assertEqual(Invite.objects.count(), 4)
        self.assertEqual(self.workspace_invite.target, self.workspace)
        self.assertEqual(self.team_invite.target, self.team)
        self.assertEqual(self.project_invite.target, self.project)
        
    def test_invite_expiration(self):
        """Test that invite expiration works correctly"""
        self.assertTrue(self.expired_invite.is_expired)
        self.assertFalse(self.workspace_invite.is_expired)
        
    def test_invite_target_type(self):
        """Test that target_type property returns correct values"""
        self.assertEqual(self.workspace_invite.target_type, 'workspace')
        self.assertEqual(self.team_invite.target_type, 'team')
        self.assertEqual(self.project_invite.target_type, 'project')
        
    def test_workspace_invite_accept(self):
        """Test accepting a workspace invite"""
        new_user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='password123'
        )
        
        # Accept the invite
        self.workspace_invite.accept(new_user)
        
        # Check that the invite is marked as accepted
        self.workspace_invite.refresh_from_db()
        self.assertTrue(self.workspace_invite.accepted)
        self.assertIsNotNone(self.workspace_invite.accepted_at)
        
        # Check that the user was added to the workspace
        self.assertTrue(WorkspaceUser.objects.filter(
            workspace=self.workspace,
            user=new_user,
            role='member'
        ).exists())
        
    def test_team_invite_accept(self):
        """Test accepting a team invite"""
        new_user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='password123'
        )
        
        # Accept the invite
        self.team_invite.accept(new_user)
        
        # Check that the invite is marked as accepted
        self.team_invite.refresh_from_db()
        self.assertTrue(self.team_invite.accepted)
        
        # Check that the user was added to the team
        self.assertTrue(TeamMember.objects.filter(
            team=self.team,
            user=new_user
        ).exists())
        
    def test_project_invite_accept(self):
        """Test accepting a project invite"""
        new_user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='password123'
        )
        
        # Accept the invite
        self.project_invite.accept(new_user)
        
        # Check that the invite is marked as accepted
        self.project_invite.refresh_from_db()
        self.assertTrue(self.project_invite.accepted)
        
        # Check that the user was added to the project
        self.assertTrue(new_user in self.project.assigned_users.all())
        
    def test_expired_invite_accept(self):
        """Test that expired invites cannot be accepted"""
        new_user = User.objects.create_user(
            username='expired',
            email='expired@example.com',
            password='password123'
        )
        
        # Try to accept the expired invite
        result = self.expired_invite.accept(new_user)
        
        # Check that the accept method returned False
        self.assertFalse(result)
        
        # Check that the invite is still not accepted
        self.expired_invite.refresh_from_db()
        self.assertFalse(self.expired_invite.accepted)
        
        # Check that the user was not added to the workspace
        self.assertFalse(WorkspaceUser.objects.filter(
            workspace=self.workspace,
            user=new_user
        ).exists())
