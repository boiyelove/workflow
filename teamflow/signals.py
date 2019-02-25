from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Team, TeamInvites

@receiver(sender=Team)
def create_member(sender, instance,  created, *args, **kwargs):
	if created:
		TeamMember.objects.create(
			user =  instance.teamAuthor,
			team = instance,
			handle = instance.teamAuthor.username,
			is_manager = True,
			designation = "Manager"
			)