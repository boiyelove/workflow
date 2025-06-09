from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile, InviteCode
import uuid

class InviteCodeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.invite_code = InviteCode.objects.create(
            email='invited@example.com',
            created_by=self.user
        )
    
    def test_invite_code_creation(self):
        self.assertEqual(self.invite_code.email, 'invited@example.com')
        self.assertEqual(self.invite_code.created_by, self.user)
        self.assertFalse(self.invite_code.is_used)
        self.assertIsNotNone(self.invite_code.code)
        
    def test_invite_code_str_method(self):
        self.assertEqual(str(self.invite_code), f"Invite for invited@example.com - Unused")
        
        # Test used invite code
        self.invite_code.is_used = True
        self.invite_code.save()
        self.assertEqual(str(self.invite_code), f"Invite for invited@example.com - Used")

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.invite_code = InviteCode.objects.create(
            email='test@example.com',
            created_by=self.user
        )
        
        self.profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio',
            phone='1234567890',
            position='Developer',
            invite_code=self.invite_code
        )
    
    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.bio, 'Test bio')
        self.assertEqual(self.profile.phone, '1234567890')
        self.assertEqual(self.profile.position, 'Developer')
        self.assertEqual(self.profile.invite_code, self.invite_code)
        
    def test_profile_str_method(self):
        self.assertEqual(str(self.profile), 'testuser')
        
    def test_profile_creation_signal(self):
        # Create a new user and check if profile is automatically created
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpassword'
        )
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertIsInstance(new_user.profile, UserProfile)

class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.invite_code = InviteCode.objects.create(
            email='invited@example.com',
            created_by=self.user
        )
    
    def test_login_view(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        
        # Test successful login
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.url.endswith(reverse('webcore:home')))
        
        # Test failed login
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertTemplateUsed(response, 'accounts/login.html')
        
    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertTrue(response.url.endswith(reverse('accounts:login')))
        
    def test_invite_code_view(self):
        response = self.client.get(reverse('accounts:invite_code'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/invite_code.html')
        
        # Test valid invite code
        response = self.client.post(reverse('accounts:invite_code'), {
            'invite_code': str(self.invite_code.code),
            'email': 'invited@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to registration page
        self.assertTrue(response.url.endswith(reverse('accounts:register', kwargs={'invite_code': self.invite_code.code})))
        
        # Test invalid invite code
        response = self.client.post(reverse('accounts:invite_code'), {
            'invite_code': str(uuid.uuid4()),
            'email': 'invited@example.com'
        })
        self.assertEqual(response.status_code, 200)  # Stay on invite code page
        self.assertTemplateUsed(response, 'accounts/invite_code.html')
        
    def test_register_view(self):
        response = self.client.get(reverse('accounts:register', kwargs={'invite_code': self.invite_code.code}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        
        # Test successful registration
        response = self.client.post(reverse('accounts:register', kwargs={'invite_code': self.invite_code.code}), {
            'username': 'newuser',
            'email': 'invited@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
            'invite_code': self.invite_code.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(response.url.endswith(reverse('webcore:home')))
        
        # Check if invite code is marked as used
        self.invite_code.refresh_from_db()
        self.assertTrue(self.invite_code.is_used)
        
        # Check if user is created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        new_user = User.objects.get(username='newuser')
        
        # Check if profile is created
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertEqual(new_user.profile.invite_code, self.invite_code)

class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio',
            phone='1234567890',
            position='Developer'
        )
        
        self.client.login(username='testuser', password='testpassword')
    
    def test_profile_view(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertContains(response, 'Test bio')
        self.assertContains(response, '1234567890')
        self.assertContains(response, 'Developer')
        
        # Test profile update
        response = self.client.post(reverse('accounts:profile'), {
            'bio': 'Updated bio',
            'phone': '0987654321',
            'position': 'Senior Developer'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.assertTrue(response.url.endswith(reverse('accounts:profile')))
        
        # Check if profile is updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertEqual(self.profile.phone, '0987654321')
        self.assertEqual(self.profile.position, 'Senior Developer')

class InviteUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.client.login(username='testuser', password='testpassword')
    
    def test_invite_user_view(self):
        response = self.client.get(reverse('accounts:invite_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/invite_user.html')
        
        # Test invite creation
        response = self.client.post(reverse('accounts:invite_create'), {
            'email': 'invited@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(response.url.endswith(reverse('accounts:invite_list')))
        
        # Check if invite is created
        self.assertTrue(InviteCode.objects.filter(email='invited@example.com').exists())
        invite = InviteCode.objects.get(email='invited@example.com')
        self.assertEqual(invite.created_by, self.user)
        self.assertFalse(invite.is_used)
    
    def test_invite_list_view(self):
        # Create some invites
        InviteCode.objects.create(email='invited1@example.com', created_by=self.user)
        InviteCode.objects.create(email='invited2@example.com', created_by=self.user)
        
        response = self.client.get(reverse('accounts:invite_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/invite_list.html')
        self.assertContains(response, 'invited1@example.com')
        self.assertContains(response, 'invited2@example.com')
