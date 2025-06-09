import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from projectflow.models import Project, Task, SubTask, PROJECT_TYPES, JOB_STATUS
from teamflow.models import Team, TeamMember

class Command(BaseCommand):
    help = 'Populates the database with sample timeline and roadmap data'

    def handle(self, *args, **kwargs):
        # Get or create admin user
        try:
            admin = User.objects.get(username='admin')
        except User.DoesNotExist:
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword'
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin.username}'))
        
        # Get or create a team
        team, created = Team.objects.get_or_create(
            name='Development Team',
            defaults={
                'url': 'dev-team',
                'description': 'Main development team',
                'teamAuthor': admin
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created team: {team.name}'))
        
        # Get or create team members
        team_member, created = TeamMember.objects.get_or_create(
            team=team,
            user=admin,
            defaults={
                'handle': 'admin',
                'is_manager': True,
                'designation': 'Project Manager'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Added {admin.username} to team {team.name}'))
        
        # Create a standard project with timeline
        project, created = Project.objects.get_or_create(
            name='Website Redesign',
            defaults={
                'description': 'Complete redesign of the company website with new branding',
                'status': 'Doing',
                'team': team,
                'is_public': True,
                'project_type': 'standard',
                'due_date': timezone.now().date() + timedelta(days=60)
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created project: {project.name}'))
            project.assigned_users.add(admin)
        
        # Create tasks with milestones for the project
        if created:
            # Create milestone tasks
            milestones = [
                {
                    'name': 'Project Kickoff',
                    'description': 'Initial project meeting and requirements gathering',
                    'status': 'Done',
                    'is_milestone': True,
                    'order': 0,
                    'due_date': timezone.now().date() - timedelta(days=15)
                },
                {
                    'name': 'Design Phase Complete',
                    'description': 'All design mockups approved by stakeholders',
                    'status': 'Doing',
                    'is_milestone': True,
                    'order': 3,
                    'due_date': timezone.now().date() + timedelta(days=10)
                },
                {
                    'name': 'Development Complete',
                    'description': 'All development tasks finished and ready for testing',
                    'is_milestone': True,
                    'order': 6,
                    'due_date': timezone.now().date() + timedelta(days=40)
                },
                {
                    'name': 'Website Launch',
                    'description': 'Go-live date for the new website',
                    'is_milestone': True,
                    'order': 9,
                    'due_date': timezone.now().date() + timedelta(days=60)
                }
            ]
            
            # Create regular tasks
            tasks = [
                {
                    'name': 'Gather Requirements',
                    'description': 'Interview stakeholders and document requirements',
                    'status': 'Done',
                    'order': 1,
                    'due_date': timezone.now().date() - timedelta(days=10)
                },
                {
                    'name': 'Create Wireframes',
                    'description': 'Design initial wireframes for key pages',
                    'status': 'Done',
                    'order': 2,
                    'due_date': timezone.now().date() - timedelta(days=5)
                },
                {
                    'name': 'Design UI Components',
                    'description': 'Create visual design for UI components',
                    'status': 'Doing',
                    'order': 4,
                    'due_date': timezone.now().date() + timedelta(days=15)
                },
                {
                    'name': 'Frontend Development',
                    'description': 'Implement HTML/CSS/JS for the new design',
                    'status': 'Todo',
                    'order': 5,
                    'due_date': timezone.now().date() + timedelta(days=30)
                },
                {
                    'name': 'Backend Integration',
                    'description': 'Connect frontend to backend services',
                    'status': 'Todo',
                    'order': 7,
                    'due_date': timezone.now().date() + timedelta(days=45)
                },
                {
                    'name': 'Testing & QA',
                    'description': 'Perform comprehensive testing of the website',
                    'status': 'Todo',
                    'order': 8,
                    'due_date': timezone.now().date() + timedelta(days=55)
                }
            ]
            
            # Combine and create all tasks
            all_tasks = milestones + tasks
            for task_data in all_tasks:
                task = Task.objects.create(
                    project=project,
                    name=task_data['name'],
                    description=task_data['description'],
                    status=task_data.get('status', 'Todo'),
                    is_milestone=task_data.get('is_milestone', False),
                    order=task_data['order'],
                    due_date=task_data['due_date']
                )
                task.team_member.add(team_member)
                task.assigned_users.add(admin)
                self.stdout.write(self.style.SUCCESS(f'Created task: {task.name}'))
                
                # Add subtasks for non-milestone tasks
                if not task.is_milestone:
                    for i in range(1, 4):
                        subtask = SubTask.objects.create(
                            task=task,
                            name=f'Subtask {i} for {task.name}',
                            description=f'This is subtask {i} for {task.name}',
                            status=random.choice([s[0] for s in JOB_STATUS]),
                            order=i-1,
                            due_date=task.due_date - timedelta(days=random.randint(1, 5))
                        )
                        subtask.assigned_users.add(admin)
                        self.stdout.write(self.style.SUCCESS(f'Created subtask: {subtask.name}'))
        
        # Create a roadmap project
        roadmap, created = Project.objects.get_or_create(
            name='Product Roadmap 2025',
            defaults={
                'description': 'Strategic roadmap for product features in 2025',
                'status': 'Doing',
                'team': team,
                'is_public': True,
                'project_type': 'roadmap',
                'due_date': datetime(2025, 12, 31).date()
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created roadmap: {roadmap.name}'))
            roadmap.assigned_users.add(admin)
            
            # Create feature projects (as subprojects of the roadmap)
            features = [
                {
                    'name': 'User Authentication Overhaul',
                    'description': 'Implement OAuth 2.0 and improve security',
                    'status': 'Doing',
                    'due_date': datetime(2025, 3, 15).date()
                },
                {
                    'name': 'Mobile App Integration',
                    'description': 'Connect web platform with mobile applications',
                    'status': 'Todo',
                    'due_date': datetime(2025, 5, 30).date()
                },
                {
                    'name': 'Analytics Dashboard',
                    'description': 'Real-time analytics and reporting dashboard',
                    'status': 'Todo',
                    'due_date': datetime(2025, 7, 15).date()
                },
                {
                    'name': 'AI-Powered Recommendations',
                    'description': 'Machine learning recommendation engine',
                    'status': 'Todo',
                    'due_date': datetime(2025, 9, 30).date()
                },
                {
                    'name': 'Enterprise Integration',
                    'description': 'Integration with enterprise systems and SSO',
                    'status': 'Todo',
                    'due_date': datetime(2025, 11, 15).date()
                }
            ]
            
            for feature_data in features:
                feature = Project.objects.create(
                    name=feature_data['name'],
                    description=feature_data['description'],
                    status=feature_data['status'],
                    team=team,
                    is_public=True,
                    project_type='standard',
                    parent=roadmap,
                    due_date=feature_data['due_date']
                )
                feature.assigned_users.add(admin)
                self.stdout.write(self.style.SUCCESS(f'Created feature: {feature.name}'))
                
                # Add some tasks to each feature
                for i in range(1, 4):
                    task_status = 'Done' if i == 1 and feature_data['status'] == 'Doing' else 'Todo'
                    task = Task.objects.create(
                        project=feature,
                        name=f'Task {i} for {feature.name}',
                        description=f'This is task {i} for feature {feature.name}',
                        status=task_status,
                        order=i-1,
                        due_date=feature_data['due_date'] - timedelta(days=30-i*10)
                    )
                    task.team_member.add(team_member)
                    task.assigned_users.add(admin)
                    self.stdout.write(self.style.SUCCESS(f'Created task for feature: {task.name}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully populated timeline and roadmap data!'))
