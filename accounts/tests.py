from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserProfile, UserToken, DonateMethod, EmailVerification
from accounts.forms import LoginForm, RegisterForm, UserProfileForm, DonateMethodForm
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth import authenticate
from unittest.mock import patch, MagicMock
from accounts.utils import code_generator, verify_email, email_password

# Model Tests
class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        # Mock the ImageField to avoid Pillow issues
        with patch('django.db.models.fields.files.ImageFieldFile'):
            self.profile = UserProfile.objects.create(
                user=self.user,
                full_name='Test User',
                country='NG',
                state='Lagos',
                address='123 Test Street',
                phone_number='1234567890'
            )

    def test_profile_to_dict(self):
        # Mock the ImageField in the profile_to_dict method
        with patch.object(self.profile, 'headshot', create=True) as mock_headshot:
            profile_dict = self.profile.profile_to_dict()
            self.assertEqual(profile_dict['full_name'], 'Test User')
            self.assertEqual(profile_dict['country'], 'NG')
            self.assertEqual(profile_dict['state'], 'Lagos')
            self.assertEqual(profile_dict['address'], '123 Test Street')
            self.assertEqual(profile_dict['phone_number'], '1234567890')

    def test_profile_valid(self):
        self.assertTrue(self.profile.profile_valid())
        
        # Test invalid profile
        self.profile.full_name = None
        self.profile.save()
        self.assertFalse(self.profile.profile_valid())
        
        # Reset and test another invalid case
        self.profile.full_name = 'Test User'
        self.profile.phone_number = None
        self.profile.save()
        self.assertFalse(self.profile.profile_valid())

    def test_set_parent(self):
        parent_user = User.objects.create_user(
            username='parentuser',
            email='parent@example.com',
            password='parentpassword'
        )
        self.profile.set_parent(parent_user)
        self.assertEqual(self.profile.referral, parent_user)


class UserTokenModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.token = UserToken.objects.create(
            user=self.user,
            balance=100.0
        )

    def test_withdraw_valid(self):
        self.token.withdraw(50.0)
        # Need to refresh from DB since we're using F() expressions
        self.token.refresh_from_db()
        self.assertEqual(self.token.balance, 50.0)

    def test_withdraw_invalid_negative_amount(self):
        result = self.token.withdraw(-10.0)
        self.assertEqual(result, "invalid withdrawal amount")
        self.token.refresh_from_db()
        self.assertEqual(self.token.balance, 100.0)

    def test_withdraw_zero_balance(self):
        self.token.balance = 0
        self.token.save()
        result = self.token.withdraw(50.0)
        self.assertEqual(result, "Invalid deposit amount")

    def test_deposit_valid(self):
        self.token.deposit(50.0)
        self.token.refresh_from_db()
        self.assertEqual(self.token.balance, 150.0)

    def test_deposit_invalid(self):
        result = self.token.deposit(0)
        self.assertEqual(result, "Invalid deposit amount")
        self.token.refresh_from_db()
        self.assertEqual(self.token.balance, 100.0)

        result = self.token.deposit(-10)
        self.assertEqual(result, "Invalid deposit amount")
        self.token.refresh_from_db()
        self.assertEqual(self.token.balance, 100.0)


class DonateMethodModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.donate_method = DonateMethod.objects.create(
            account_type='LOCB',
            bank_name='Test Bank',
            account_no=1234567890,
            account_name='Test Account',
            user=self.user,
            is_default=True
        )

    def test_donate_method_creation(self):
        self.assertEqual(self.donate_method.account_type, 'LOCB')
        self.assertEqual(self.donate_method.bank_name, 'Test Bank')
        self.assertEqual(self.donate_method.account_no, 1234567890)
        self.assertEqual(self.donate_method.account_name, 'Test Account')
        self.assertEqual(self.donate_method.user, self.user)
        self.assertTrue(self.donate_method.is_default)

# Utils Tests
class UtilsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
    def test_code_generator(self):
        # Test that code_generator returns a string
        code = code_generator('test@example.com')
        self.assertIsInstance(code, str)
        
        # Test that code_generator returns different codes for different inputs
        code1 = code_generator('test1@example.com')
        code2 = code_generator('test2@example.com')
        self.assertNotEqual(code1, code2)