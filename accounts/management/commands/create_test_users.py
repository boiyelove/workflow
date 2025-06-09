from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Program, UserProfile
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Creates test users with email addresses ending with -test@boiyelove.website'
    
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=5, help='Number of test users to create')
        parser.add_argument('--programs', type=int, default=3, help='Number of programs to create')
    
    def handle(self, *args, **options):
        count = options['count']
        program_count = options['programs']
        
        # Create programs if they don't exist
        programs = []
        existing_programs = Program.objects.count()
        
        if existing_programs < program_count:
            self.stdout.write(self.style.SUCCESS(f'Creating {program_count} programs...'))
            for i in range(program_count):
                title = fake.catch_phrase()
                slug = fake.slug()
                description = fake.paragraph()
                
                program = Program.objects.create(
                    title=title,
                    slug=slug,
                    description=description,
                    active=True
                )
                programs.append(program)
                self.stdout.write(f'Created program: {program.title}')
        else:
            programs = list(Program.objects.all()[:program_count])
            self.stdout.write(f'Using {len(programs)} existing programs')
        
        # Create test users
        self.stdout.write(self.style.SUCCESS(f'Creating {count} test users...'))
        
        for i in range(count):
            username = fake.user_name()
            email = f"{username}-test@boiyelove.website"
            password = "password123"  # Simple password for testing
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                username = f"{username}{random.randint(1, 999)}"
            
            if User.objects.filter(email=email).exists():
                continue
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            
            # Get user profile and update it
            profile = UserProfile.objects.get(user=user)
            profile.full_name = f"{user.first_name} {user.last_name}"
            profile.country = random.choice(['NG', 'GH', 'SA'])
            profile.state = fake.state()
            profile.address = fake.address()
            profile.phone_number = fake.phone_number()
            profile.bio = fake.paragraph()
            profile.save()
            
            # Skip adding programs for now due to database issues
            # for program in random.sample(programs, min(random.randint(1, len(programs)), len(programs))):
            #     profile.programs.add(program)
            
            self.stdout.write(f'Created user: {username} ({email})')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} test users'))
