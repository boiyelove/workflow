import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker

from teamflow.models import Team, TeamMember
from workspace.models import Workspace, WorkspaceUser
from projectflow.models import Project, Task, SubTask
from support.models import Ticket, TicketResponse

fake = Faker()

class Command(BaseCommand):
    help = 'Populates the database with fake data for testing'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--teams', type=int, default=5, help='Number of teams to create')
        parser.add_argument('--workspaces', type=int, default=3, help='Number of workspaces to create')
        parser.add_argument('--projects', type=int, default=15, help='Number of projects to create')
        parser.add_argument('--tasks', type=int, default=50, help='Number of tasks to create')
        parser.add_argument('--subtasks', type=int, default=100, help='Number of subtasks to create')
        parser.add_argument('--tickets', type=int, default=20, help='Number of support tickets to create')

    def handle(self, *args, **options):
        # Create admin user if it doesn't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('adminpassword')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: admin/adminpassword'))
        
        # Create regular users
        users = [admin_user]
        for i in range(options['users']):
            username = fake.user_name()
            # Avoid duplicate usernames
            while User.objects.filter(username=username).exists():
                username = fake.user_name()
                
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            users.append(user)
            self.stdout.write(f'Created user: {username}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))
        
        # Create teams
        teams = []
        for i in range(options['teams']):
            team_name = fake.company()
            # Avoid duplicate team names
            while Team.objects.filter(name=team_name).exists():
                team_name = fake.company()
                
            team = Team.objects.create(
                name=team_name,
                url=f"team-{i+1}",
                description=fake.catch_phrase(),
                teamAuthor=random.choice(users)
            )
            teams.append(team)
            
            # Add team members
            team_users = random.sample(users, min(len(users), random.randint(2, 5)))
            for user in team_users:
                TeamMember.objects.create(
                    team=team,
                    user=user,
                    handle=fake.user_name(),
                    designation=fake.job(),
                    is_manager=random.choice([True, False, False, False])  # 25% chance of being manager
                )
            
            self.stdout.write(f'Created team: {team.name} with {len(team_users)} members')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(teams)} teams'))
        
        # Create workspaces
        workspaces = []
        for i in range(options['workspaces']):
            workspace_name = fake.bs()
            # Avoid duplicate workspace names
            while Workspace.objects.filter(name=workspace_name).exists():
                workspace_name = fake.bs()
                
            workspace = Workspace.objects.create(
                name=workspace_name,
                description=fake.paragraph()
            )
            workspaces.append(workspace)
            
            # Add workspace users
            workspace_users = random.sample(users, min(len(users), random.randint(2, 6)))
            for user in workspace_users:
                WorkspaceUser.objects.create(
                    workspace=workspace,
                    user=user,
                    role=random.choice(['Admin', 'Member', 'Member', 'Member'])  # 25% chance of being admin
                )
            
            self.stdout.write(f'Created workspace: {workspace.name} with {len(workspace_users)} users')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workspaces)} workspaces'))
        
        # Create projects
        projects = []
        statuses = ['Todo', 'Doing', 'Done']
        project_types = ['standard', 'roadmap']
        
        for i in range(options['projects']):
            # Decide if it's a standard project or roadmap
            project_type = random.choice(project_types)
            project_name = fake.catch_phrase() if project_type == 'standard' else f"Roadmap: {fake.bs()}"
            
            # Decide if it has a team or workspace
            has_team = random.choice([True, False])
            team = random.choice(teams) if has_team and teams else None
            workspace = random.choice(workspaces) if not has_team and workspaces else None
            
            # Decide if it's a subproject
            is_subproject = random.choice([True, False, False, False])  # 25% chance
            parent = random.choice(projects) if is_subproject and projects and project_type == 'standard' else None
            
            # Create the project
            project = Project.objects.create(
                name=project_name,
                slug=f"project-{i+1}",
                description=fake.paragraph(),
                status=random.choice(statuses),
                team=team,
                workspace=workspace,
                is_public=random.choice([True, True, False]),  # 66% chance of being public
                project_type=project_type,
                parent=parent,
                order=i+1,
                due_date=timezone.now().date() + timedelta(days=random.randint(-10, 30)) if random.choice([True, False]) else None
            )
            projects.append(project)
            
            # Assign users to project
            if team:
                team_members = TeamMember.objects.filter(team=team)
                for member in team_members:
                    if random.choice([True, False]):
                        project.assigned_users.add(member.user)
            elif workspace:
                workspace_users = WorkspaceUser.objects.filter(workspace=workspace)
                for workspace_user in workspace_users:
                    if random.choice([True, False]):
                        project.assigned_users.add(workspace_user.user)
            
            self.stdout.write(f'Created project: {project.name} ({project_type})')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(projects)} projects'))
        
        # Create tasks
        tasks = []
        for i in range(options['tasks']):
            project = random.choice(projects)
            is_milestone = random.choice([True, False, False, False, False])  # 20% chance of being milestone
            
            task = Task.objects.create(
                project=project,
                name=fake.sentence(nb_words=4)[:-1] if not is_milestone else f"MILESTONE: {fake.sentence(nb_words=3)[:-1]}",
                description=fake.paragraph(),
                status=random.choice(statuses),
                is_milestone=is_milestone,
                order=i+1,
                due_date=timezone.now().date() + timedelta(days=random.randint(-5, 20)) if random.choice([True, False]) else None
            )
            tasks.append(task)
            
            # Assign users to task
            potential_users = list(project.assigned_users.all())
            if potential_users:
                num_assignees = random.randint(1, min(3, len(potential_users)))
                assignees = random.sample(potential_users, num_assignees)
                for user in assignees:
                    task.assigned_users.add(user)
            
            self.stdout.write(f'Created task: {task.name} for project {project.name}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(tasks)} tasks'))
        
        # Create subtasks
        subtasks = []
        for i in range(options['subtasks']):
            task = random.choice(tasks)
            
            subtask = SubTask.objects.create(
                task=task,
                name=fake.sentence(nb_words=4)[:-1],
                description=fake.paragraph(),
                status=random.choice(statuses),
                order=i+1,
                due_date=task.due_date if task.due_date and random.choice([True, False]) else None
            )
            subtasks.append(subtask)
            
            # Assign users to subtask
            if task.assigned_users.exists():
                potential_users = list(task.assigned_users.all())
                if potential_users:
                    num_assignees = random.randint(1, min(2, len(potential_users)))
                    assignees = random.sample(potential_users, num_assignees)
                    for user in assignees:
                        subtask.assigned_users.add(user)
            
            self.stdout.write(f'Created subtask: {subtask.name} for task {task.name}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(subtasks)} subtasks'))
        
        # Create support tickets
        tickets = []
        priorities = ['Low', 'Medium', 'High', 'Critical']
        statuses = ['Open', 'In Progress', 'Resolved', 'Closed']
        
        for i in range(options['tickets']):
            creator = random.choice(users)
            assigned_to = random.choice(users) if random.choice([True, False]) else None
            
            ticket = Ticket.objects.create(
                title=fake.sentence(nb_words=6)[:-1],
                description=fake.paragraph(),
                created_by=creator,
                assigned_to=assigned_to,
                status=random.choice(statuses),
                priority=random.choice(priorities)
            )
            tickets.append(ticket)
            
            # Add responses
            num_responses = random.randint(0, 3)
            for j in range(num_responses):
                responder = assigned_to if assigned_to and random.choice([True, False]) else random.choice(users)
                TicketResponse.objects.create(
                    ticket=ticket,
                    user=responder,
                    message=fake.paragraph()
                )
            
            self.stdout.write(f'Created ticket: {ticket.title} with {num_responses} responses')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(tickets)} support tickets'))
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with fake data'))
