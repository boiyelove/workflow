import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from teamflow.models import Team, TeamMember
from projectflow.models import Project, Task, SubTask
from accounts.models import InviteCode, UserProfile

class Command(BaseCommand):
    help = 'Populates the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword'
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin.username}'))
        else:
            admin = User.objects.get(username='admin')
        
        # Create regular users
        users = []
        for i in range(5):
            username = fake.user_name() + str(random.randint(1, 1000))
            email = fake.email()
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))
        
        # Create invite codes
        for i in range(3):
            invite = InviteCode.objects.create(
                email=fake.email(),
                created_by=admin
            )
            self.stdout.write(self.style.SUCCESS(f'Created invite code: {invite.code} for {invite.email}'))
        
        # Create teams
        teams = []
        for i in range(3):
            team = Team.objects.create(
                name=fake.company(),
                url=fake.slug(),
                description=fake.catch_phrase(),
                teamAuthor=admin
            )
            teams.append(team)
            self.stdout.write(self.style.SUCCESS(f'Created team: {team.name}'))
            
            # Add admin as team manager
            TeamMember.objects.create(
                team=team,
                user=admin,
                handle=admin.username,
                is_manager=True,
                designation='Team Lead'
            )
            
            # Add some users to each team
            for user in random.sample(users, min(3, len(users))):
                designation = random.choice(['Developer', 'Designer', 'Product Manager', 'QA Engineer'])
                team_member = TeamMember.objects.create(
                    team=team,
                    user=user,
                    handle=user.username,
                    is_manager=random.choice([True, False]),
                    designation=designation
                )
                self.stdout.write(self.style.SUCCESS(f'Added {user.username} to team {team.name} as {designation}'))
        
        # Create projects
        projects = []
        for team in teams:
            for i in range(random.randint(1, 3)):
                project = Project.objects.create(
                    name=fake.bs(),
                    description=fake.paragraph(),
                    status=random.choice(['Todo', 'Doing', 'Done']),
                    team=team
                )
                projects.append(project)
                self.stdout.write(self.style.SUCCESS(f'Created project: {project.name} for team {team.name}'))
        
        # Create tasks
        tasks = []
        for project in projects:
            team_members = TeamMember.objects.filter(team=project.team)
            for i in range(random.randint(3, 7)):
                task = Task.objects.create(
                    name=fake.catch_phrase(),
                    description=fake.paragraph(),
                    status=random.choice(['Todo', 'Doing', 'Done']),
                    project=project
                )
                
                # Assign random team members to the task
                assigned_members = random.sample(list(team_members), min(random.randint(1, 2), team_members.count()))
                for member in assigned_members:
                    task.team_member.add(member)
                
                tasks.append(task)
                self.stdout.write(self.style.SUCCESS(f'Created task: {task.name} for project {project.name}'))
        
        # Create subtasks
        for task in tasks:
            team_members = TeamMember.objects.filter(team=task.project.team)
            for i in range(random.randint(1, 4)):
                member = random.choice(list(team_members))
                subtask = SubTask.objects.create(
                    name=fake.sentence(),
                    description=fake.paragraph(),
                    status=random.choice(['Todo', 'Doing', 'Done']),
                    task=task,
                    team_member=member
                )
                self.stdout.write(self.style.SUCCESS(f'Created subtask: {subtask.name} for task {task.name}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake data!'))
