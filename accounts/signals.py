from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from .models import DonateMethod, UserProfile, UserToken
from .utils import verify_email

@receiver(pre_save, sender=DonateMethod)
def set_defaultDonateMethodForUser(instance, *args, **kwargs):
	if instance.is_default:
		former_default = DonateMethod.objects.filter(user = instance.user, is_default=True)
		for m in former_default:
			m.is_default = False
			m.save()

@receiver(post_save, sender=User)
def verifyandcreateprofile(instance, created, sender, **kwargs):
	if created:
		up = UserProfile.objects.create(user = instance)
		UserToken.objects.create(user = instance)
		if not instance.is_staff and settings.VERIFY_EMAILS:
			instance.is_active = False
			instance.save()
	verify_email(instance.email, action=reverse_lazy('accounts:dashboard'))




