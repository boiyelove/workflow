import re
from django import forms
from django.conf import settings
from .models import Team, EmailVerification, TeamMember, TeamInvite
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from webcore.forms import BsCharField, BsChoiceField, BsEmailField, BsPasswordField, BsPhoneNumberField
from .utils import email_password, code_generator, verify_email

user = settings.AUTH_USER_MODEL


class UserInfoForm(forms.Form):
	firstname = forms.CharField(max_length=60)
	lastname = forms.CharField(max_length=60)
	username = forms.CharField(max_length=60)
	password = forms.CharField()

	def clean_username(self):
		username = self.cleaned_data.get('username')
		try:
			User.objects.get(username=username)
			raise forms.ValidationError('Username is already taken, try another one')
		except:
			return username

	def done(self, email):
		me = User.objects.create(first_name = self.cleaned_data.get('firstname'),
							last_name = self.cleaned_data.get('lastname'),
							username = self.cleaned_data.get('username'),
							password = self.cleaned_data.get('password'),
							email = email)
		return me



class CreateTeamForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ('name', 'url', 'is_public')

	def clean_teamurl(self):
		teamurl = self.cleaned_data.get('teamurl')
		try:
			Team.objects.get(teamurl=teamurl)
			raise forms.ValidationError('Url is already taken, try another one')
		except:
			return teamurl
			

class CreateTeamMember(forms.ModelForm):
	class Meta:
		model = TeamMember
		fields = ('handle', 'designation')



class EmailSignUpForm(forms.ModelForm):
	class Meta:
		model = EmailVerification
		fields = ('email',)

	def done(self):
		email = self.cleaned_data.get('email')
		verify_email(email)



class LoginForm(forms.Form):
	username = BsCharField(min_length=6)
	password = BsPasswordField()


	def clean_username(self):
		username = self.cleaned_data.get('username')
		username = username.strip()
		try:
			this_user = User.objects.get(username = username)
		except User.DoesNotExist:
			raise forms.ValidationError('User with this username does not exist')
		if not this_user.is_active:
			raise forms.ValidationError('Sorry you are not allowed to log in, contact support team')
		return username

	def clean_password(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		try:
			this_user = User.objects.get(username = username)
		except User.DoesNotExist:
			raise forms.ValidationError('User with this username does not exist')
		if not this_user.is_active:
			raise forms.ValidationError('Sorry you are not allowed to log in, contact support team')
		if not this_user.check_password(password):
			raise forms.ValidationError('Please check that your details you provided are correct')
		return password


	def login_user(self, request):
		cleaned = super(LoginForm, self).clean()
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError("An error occcured, please check your password or call admin")
		return login(request, user)

class TeamInviteForm(forms.ModelForm):
	class Meta:
		model = TeamInvite
		fields = ('email',)