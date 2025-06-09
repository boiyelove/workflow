from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Team, TeamMember, TeamInvite, Room, Message, EmailVerification
from .forms import CreateTeamForm, EmailSignUpForm, UserInfoForm, LoginForm, TeamInviteForm
from .utils import code_generator, verify_email
from unittest.mock import patch, MagicMock

class TeamModelTest(TestCase):
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
    
    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.url, 'test-team')
        self.assertEqual(self.team.description, 'Test Team Description')
        self.assertEqual(self.team.teamAuthor, self.user)
        
    def test_is_author(self):
        self.assertTrue(self.team.is_author(self.user))
        
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )
        self.assertFalse(self.team.is_author(other_user))
        
    def test_is_teammanager(self):
        self.assertTrue(self.team.is_teammanager(self.user))
        
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )
        self.assertFalse(self.team.is_teammanager(other_user))
        
        # Create a non-manager team member
        non_manager = User.objects.create_user(
            username='nonmanager',
            email='nonmanager@example.com',
            password='nonmanagerpassword'
        )
        TeamMember.objects.create(
            user=non_manager,
            team=self.team,
            handle='nonmanagerhandle',
            is_manager=False,
            designation='Developer'
        )
        self.assertFalse(self.team.is_teammanager(non_manager))

class TeamMemberModelTest(TestCase):
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
    
    def test_team_member_creation(self):
        self.assertEqual(self.team_member.user, self.user)
        self.assertEqual(self.team_member.team, self.team)
        self.assertEqual(self.team_member.handle, 'testhandle')
        self.assertTrue(self.team_member.is_manager)
        self.assertEqual(self.team_member.designation, 'Developer')
        
    def test_team_member_str(self):
        self.assertEqual(str(self.team_member), 'testhandle')
        
    def test_unique_together_constraint(self):
        # Try to create another team member with the same handle in the same team
        with self.assertRaises(Exception):
            TeamMember.objects.create(
                user=self.user,
                team=self.team,
                handle='testhandle',
                is_manager=False,
                designation='Designer'
            )

class TeamInviteModelTest(TestCase):
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
        
        self.team_invite = TeamInvite.objects.create(
            slug='test-invite',
            email='invite@example.com',
            team=self.team,
            accepted=None,
            user=None
        )
    
    def test_team_invite_creation(self):
        self.assertEqual(self.team_invite.slug, 'test-invite')
        self.assertEqual(self.team_invite.email, 'invite@example.com')
        self.assertEqual(self.team_invite.team, self.team)
        self.assertIsNone(self.team_invite.accepted)
        self.assertIsNone(self.team_invite.user)
        
    def test_is_pending(self):
        self.assertTrue(self.team_invite.is_pending())
        
        self.team_invite.accepted = True
        self.team_invite.save()
        self.assertFalse(self.team_invite.is_pending())
        
        self.team_invite.accepted = False
        self.team_invite.save()
        self.assertFalse(self.team_invite.is_pending())

class RoomModelTest(TestCase):
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
        
        self.room = Room.objects.create(
            label='test-room',
            team=self.team
        )
    
    def test_room_creation(self):
        self.assertEqual(self.room.label, 'test-room')
        self.assertEqual(self.room.team, self.team)
        
    def test_unique_together_constraint(self):
        # Try to create another room with the same label in the same team
        with self.assertRaises(Exception):
            Room.objects.create(
                label='test-room',
                team=self.team
            )

class MessageModelTest(TestCase):
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
        
        self.room = Room.objects.create(
            label='test-room',
            team=self.team
        )
        
        self.message = Message.objects.create(
            room=self.room,
            text='Test message',
            sender=self.user
        )
    
    def test_message_creation(self):
        self.assertEqual(self.message.room, self.room)
        self.assertEqual(self.message.text, 'Test message')
        self.assertEqual(self.message.sender, self.user)

class EmailVerificationModelTest(TestCase):
    def setUp(self):
        self.email_verification = EmailVerification.objects.create(
            email='test@example.com',
            slug='test-verification',
            confirmed=False,
            action='/',
            actiontype='USER'
        )
    
    def test_email_verification_creation(self):
        self.assertEqual(self.email_verification.email, 'test@example.com')
        self.assertEqual(self.email_verification.slug, 'test-verification')
        self.assertFalse(self.email_verification.confirmed)
        self.assertEqual(self.email_verification.action, '/')
        self.assertEqual(self.email_verification.actiontype, 'USER')
        
    def test_email_verification_str(self):
        self.assertEqual(str(self.email_verification), 'test@example.com False')
        
    @patch('teamflow.models.send_mail')
    def test_send_activation_email(self, mock_send_mail):
        self.email_verification.send_activation_email()
        self.assertTrue(mock_send_mail.called)
        
    @patch('teamflow.models.send_mail')
    def test_email_user(self, mock_send_mail):
        self.email_verification.email_user('Test Subject', 'Test Message')
        mock_send_mail.assert_called_once()

class UtilsTest(TestCase):
    def test_code_generator(self):
        code1 = code_generator('test@example.com')
        code2 = code_generator('test@example.com')
        
        self.assertIsInstance(code1, str)
        self.assertNotEqual(code1, code2)  # Should be different due to random and time
        
    @patch('teamflow.utils.EmailVerification')
    @patch('teamflow.utils.code_generator')
    def test_verify_email(self, mock_code_generator, mock_email_verification):
        mock_code_generator.return_value = 'test-code'
        mock_email_verification_instance = MagicMock()
        mock_email_verification.objects.get_or_create.return_value = (mock_email_verification_instance, True)
        mock_email_verification.objects.filter.return_value = False
        
        verify_email('test@example.com', actiontype='TEST', action='/test')
        
        mock_email_verification.objects.get_or_create.assert_called_once_with(email='test@example.com')
        self.assertEqual(mock_email_verification_instance.slug, 'test-code')
        self.assertEqual(mock_email_verification_instance.action, '/test')
        self.assertEqual(mock_email_verification_instance.actiontype, 'TEST')
        mock_email_verification_instance.save.assert_called_once()
        mock_email_verification_instance.send_activation_email.assert_called_once()

class CreateTeamFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
    def test_create_team_form_valid(self):
        form_data = {
            'name': 'Test Team',
            'url': 'test-team',
            'is_public': True
        }
        form = CreateTeamForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_create_team_form_missing_data(self):
        form_data = {
            'name': 'Test Team',
            'is_public': True
        }
        form = CreateTeamForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('url', form.errors)

class EmailSignUpFormTest(TestCase):
    def test_email_signup_form_valid(self):
        form_data = {
            'email': 'test@example.com'
        }
        form = EmailSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_email_signup_form_invalid_email(self):
        form_data = {
            'email': 'invalid-email'
        }
        form = EmailSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        
    @patch('teamflow.forms.verify_email')
    def test_done_method(self, mock_verify_email):
        form_data = {
            'email': 'test@example.com'
        }
        form = EmailSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        form.done()
        mock_verify_email.assert_called_once_with('test@example.com')

class UserInfoFormTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpassword'
        )
        
    def test_user_info_form_valid(self):
        form_data = {
            'firstname': 'Test',
            'lastname': 'User',
            'username': 'testuser',
            'password': 'testpassword'
        }
        form = UserInfoForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_user_info_form_existing_username(self):
        form_data = {
            'firstname': 'Test',
            'lastname': 'User',
            'username': 'existinguser',
            'password': 'testpassword'
        }
        form = UserInfoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
    def test_done_method(self):
        form_data = {
            'firstname': 'Test',
            'lastname': 'User',
            'username': 'testuser',
            'password': 'testpassword'
        }
        form = UserInfoForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.done('test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')

class LoginFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
    def test_login_form_valid(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_login_form_invalid_username(self):
        form_data = {
            'username': 'nonexistentuser',
            'password': 'testpassword'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
    def test_login_form_invalid_password(self):
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

class TeamInviteFormTest(TestCase):
    def test_team_invite_form_valid(self):
        form_data = {
            'email': 'test@example.com'
        }
        form = TeamInviteForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_team_invite_form_invalid_email(self):
        form_data = {
            'email': 'invalid-email'
        }
        form = TeamInviteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)