from django.db import models
from django.db.models import F
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.template.loader import render_to_string
from django.core.mail import send_mail
from webcore.models import TimestampedModel
from django.contrib.auth.models import User
from revprograms.models import RevenupaPrograms

# Create your models here.


User = settings.AUTH_USER_MODEL
COUNTRY = (('NG', 'Nigeria'), 
		('GH','Ghana'), 
		('SA', 'South Africa'),)

PAYCHOICE = (('LOCB', 'LOCAL BANK'),)
			# ("PAYP", 'PAYPAL'),
			# ('PAYE', 'PAYEER'),
			# ('SKRIL','SKRILL'),
			# ('PAYO', 'PAYONEER'),
			# ('BITC', 'BITCOIN'),
			# ('AIRC', 'PHONE RECHARGE')
			# )

PAYCATEGORY = (("DIGI","DIGITAL"),
	("CASH","CASH"))

def user_directory_path(instance, filename):
	return 'uploads/user_{0}/{1}'.format(instance.user.id, filename)

class UserProfile(TimestampedModel):
	user = models.OneToOneField(User)
	full_name = models.CharField(max_length = 50, null=True)
	country = models.CharField(max_length = 30, null=True, choices=COUNTRY)
	state = models.CharField(max_length =60, null=True)
	address = models.CharField(max_length=160, null=True)
	phone_number = models.CharField(max_length = 15, null=True)
	alt_address = models.CharField(max_length = 160, null=True)
	alt_phone_number = models.CharField(max_length = 15, null=True)
	headshot = models.ImageField(upload_to = user_directory_path)
	bio = models.TextField(max_length = 320, null=True)
	verified = models.BooleanField(default = False)
	referral = models.ForeignKey(User, null=True, editable=False, related_name='parent', on_delete=models.CASCADE)
	programs = models.ManyToManyField(RevenupaPrograms, related_name='programs_entered')
	lastpasswordreset = models.DateTimeField(null=True)

	def profile_to_dict(self):
		data = {'full_name': self.full_name,
		'country' : self.country,
		'state': self.state ,
		'address' :self.address ,
		'alt_address' : self.alt_address ,
		'phone_number' : self.phone_number ,
		'alt_phone_number': self.alt_phone_number ,
		'headshot': self.headshot ,
		# 'timestamp': self.timestamp ,
		# 'updated': self.updated ,
		# 'programs': self.programs ,
		}
		return data

	def profile_valid(self):
		if self.full_name and self.phone_number:
			return True
		return False

	def set_parent(self, user):
		self.parent = user
		self.save()



class UserToken(TimestampedModel):
	user = models.OneToOneField(User, null=True)
	balance = models.FloatField(default=0)

	def __str__(self):
		return str(self.balance)

	def withdraw(self, amount):
		if (self.balance <= 0):
			return "Invalid deposit amount"
		elif amount < 0:
			return "invalid withdrawal amount"
		self.balance = F("balance") - amount
		self.save()

	def deposit(self, amount):
		if amount <= 0:
			return "Invalid deposit amount"
		self.balance = F("balance") + amount
		self.save()



class DonateMethod(TimestampedModel):
	account_type= models.CharField(max_length =4, choices=PAYCHOICE)
	bank_name = models.CharField(max_length=60, null=True, blank=True)
	bank_sort_code = models.CharField(max_length = 10, null=True, blank=True)
	account_no = models.IntegerField()
	account_name = models.CharField(max_length =60)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	is_default = models.BooleanField(default = False)




