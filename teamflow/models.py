from django.db import models
from django.conf import settings
from webcore.models import TimestampedModel
from django.template.loader import render_to_string
from django.core.mail import send_mail

# Create your models here.

class Team(TimestampedModel):
	name = models.CharField(max_length=60)
	url = models.SlugField(unique = True)
	icon = models.ImageField(upload_to='teams')
	description = models.CharField(max_length=160)
	is_public = models.BooleanField(default = False)
	teamAuthor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="teamcreator", on_delete=models.CASCADE)


	def __str__(self):
		return self.name

	def is_author(self, user):
		if self.teamAuthor == user:
			return True
		else:
			return False

	def is_teammanager(self, user):
		obj = TeamMember.objects.filter(team=self, user=user, is_manager=True)
		if obj:
			return True
		else:
			return False



class TeamMember(TimestampedModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	team = models.ForeignKey('Team', on_delete=models.CASCADE)
	handle = models.CharField(max_length=60, null=True)
	is_manager = models.BooleanField(default = False)
	designation = models.CharField(max_length = 60, null=True)

	class Meta:
		unique_together = ('handle', 'team')

	def __str__(self):
		return self.handle



class TeamInvite(TimestampedModel):
	slug = models.SlugField(unique=True)
	email = models.EmailField()
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	accepted = models.BooleanField(default=False, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

	class Meta:
		unique_together = ('email', 'team')

	def is_pending(self):
		if self.accepted == None:
			return True
		else:
			return False

# class Organization(TimestampedModel):
# 	name = models.CharField(max_length = 60)
# 	about  = models.TextField()
# 	website = models.URLField()
# 	email = models.EmailField()
# 	phone = models.CharField()
# 	orgManagers = models.ManyToManyField(settings.AUTH_USER_MODEL)

#Email Verification
class EmailVerification(TimestampedModel):
	email = models.EmailField(default = "example@domain.ext", unique=True)
	slug = models.SlugField(null = True)
	confirmed = models.BooleanField(default=False)
	action = models.URLField()
	actiontype = models.CharField(max_length = 10, default='USER')

	def __str__(self):
		return ('%s %s' % (self.email, self.confirmed))

	def send_activation_email(self):
		verification_url = "%s%s/%s" % (settings.SITE_URL, 
			'/create', self.slug)
		message = render_to_string("accounts/newsletter/verification_message.txt", {
			"website": settings.SITE_NAME,
			"verification_url": verification_url,
		})
		subject = "Verify your email"
		self.email_user(subject, message)

	def email_user(self, subject, message):
		send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])


class Room(TimestampedModel):
	label = models.SlugField()
	team = models.ForeignKey(Team, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('label', 'team')


class Message(TimestampedModel):
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	text = models.TextField()
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
