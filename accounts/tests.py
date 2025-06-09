from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from faker import Faker
from .models import UserProfile, UserToken, EmailVerification, Program
from .utils import is_test_email

fake = Faker()

class TestUserCreation(TestCase):
    def setUp(self):
        self.test_domain = settings.TEST_EMAIL_DOMAIN
        
    def test_regular_user_creation(self):
        """Test creating a regular user"""
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Check user was created
        self.assertIsNotNone(user)
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        
        # Check profile was created
        profile = UserProfile.objects.filter(user=user).first()
        self.assertIsNotNone(profile)
        self.assertFalse(profile.verified)
        
        # Check token was created
        token = UserToken.objects.filter(user=user).first()
        self.assertIsNotNone(token)
        self.assertEqual(token.balance, 0)
        
        # Check email verification was created
        verification = EmailVerification.objects.filter(email=email).first()
        self.assertIsNotNone(verification)
        self.assertFalse(verification.confirmed)
    
    def test_test_user_auto_verification(self):
        """Test creating a test user with auto verification"""
        username = fake.user_name()
        email = f"{username}-test@{self.test_domain}"
        password = fake.password()
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Check user was created
        self.assertIsNotNone(user)
        
        # Check profile was created and verified
        profile = UserProfile.objects.filter(user=user).first()
        self.assertIsNotNone(profile)
        self.assertTrue(profile.verified)
        
        # Check email verification was created and confirmed
        verification = EmailVerification.objects.filter(email=email).first()
        self.assertIsNotNone(verification)
        self.assertTrue(verification.confirmed)
    
    def test_is_test_email_function(self):
        """Test the is_test_email utility function"""
        regular_email = fake.email()
        test_email = f"user-test@{self.test_domain}"
        
        self.assertFalse(is_test_email(regular_email))
        self.assertTrue(is_test_email(test_email))

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password()
        )
        self.profile = UserProfile.objects.get(user=self.user)
        self.profile.full_name = fake.name()
        self.profile.phone_number = fake.phone_number()
        self.profile.country = 'NG'
        self.profile.state = fake.state()
        self.profile.address = fake.address()
        self.profile.save()
    
    def test_profile_to_dict(self):
        """Test the profile_to_dict method"""
        profile_dict = self.profile.profile_to_dict()
        self.assertEqual(profile_dict['full_name'], self.profile.full_name)
        self.assertEqual(profile_dict['phone_number'], self.profile.phone_number)
        self.assertEqual(profile_dict['country'], self.profile.country)
    
    def test_profile_valid(self):
        """Test the profile_valid method"""
        self.assertTrue(self.profile.profile_valid())
        
        # Test with missing data
        self.profile.full_name = None
        self.profile.save()
        self.assertFalse(self.profile.profile_valid())
    
    def test_set_parent(self):
        """Test the set_parent method"""
        parent_user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password()
        )
        
        self.profile.set_parent(parent_user)
        self.assertEqual(self.profile.referral, parent_user)

class UserTokenModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password()
        )
        self.token = UserToken.objects.get(user=self.user)
    
    def test_deposit_valid(self):
        """Test valid deposit"""
        initial_balance = self.token.balance
        amount = 100
        
        self.token.deposit(amount)
        self.token.refresh_from_db()
        
        self.assertEqual(self.token.balance, initial_balance + amount)
    
    def test_deposit_invalid(self):
        """Test invalid deposit (negative or zero)"""
        initial_balance = self.token.balance
        
        result = self.token.deposit(0)
        self.assertEqual(result, "Invalid deposit amount")
        
        result = self.token.deposit(-50)
        self.assertEqual(result, "Invalid deposit amount")
        
        self.token.refresh_from_db()
        self.assertEqual(self.token.balance, initial_balance)
    
    def test_withdraw_valid(self):
        """Test valid withdrawal"""
        self.token.balance = 100
        self.token.save()
        
        self.token.withdraw(50)
        self.token.refresh_from_db()
        
        self.assertEqual(self.token.balance, 50)
    
    def test_withdraw_zero_balance(self):
        """Test withdrawal with zero balance"""
        self.token.balance = 0
        self.token.save()
        
        result = self.token.withdraw(50)
        self.assertEqual(result, "Invalid deposit amount")
    
    def test_withdraw_invalid_negative_amount(self):
        """Test withdrawal with negative amount"""
        self.token.balance = 100
        self.token.save()
        
        result = self.token.withdraw(-50)
        self.assertEqual(result, "invalid withdrawal amount")
        
        self.token.refresh_from_db()
        self.assertEqual(self.token.balance, 100)

class ProgramModelTest(TestCase):
    def setUp(self):
        self.program = Program.objects.create(
            title=fake.sentence(nb_words=3),
            slug=fake.slug(),
            description=fake.paragraph(),
            active=True
        )
    
    def test_program_creation(self):
        """Test program creation"""
        self.assertIsNotNone(self.program)
        self.assertEqual(str(self.program), self.program.title)
    
    def test_program_assignment_to_user(self):
        """Test assigning program to user profile"""
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password()
        )
        profile = UserProfile.objects.get(user=user)
        
        profile.programs.add(self.program)
        
        self.assertEqual(profile.programs.count(), 1)
        self.assertEqual(profile.programs.first(), self.program)
        self.assertEqual(self.program.programs_entered.first(), profile)
