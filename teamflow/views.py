from django.shortcuts import render, Http404
from django.views.generic.base import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, FormView
from .models import Team, TeamMember, EmailVerification, TeamInvite
from .forms import CreateTeamForm, EmailSignUpForm, UserInfoForm, LoginForm, TeamInviteForm
from webcore.forms import FormLink, ExtraFormContext
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse_lazy


class LoginRqMixin(LoginRequiredMixin):
	login_url = '/'
	redirect_field_name = 'rdr_to'

class LoginView(FormView):
	form_class = LoginForm
	template_name = 'webcore/form_inside.html'
	success_url = '/'


	def form_valid(self, form):
		form.login_user(self.request)
		messages.success(self.request, 'You are now logged in')
		return super(LoginView, self).form_valid(form)


class LogoutView(LoginRqMixin, View):

	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, 'You are now logged out')
		return HttpResponseRedirect('/')



# Create your views here.
class NewUnconfirmedUser(SuccessMessageMixin, FormView):
	form_class = EmailSignUpForm
	template_name = 'form_inside.html'
	success_url = '/'
	success_message = "An invitation has been sent to %(email)s"

	def form_valid(self, form):
		form.done()
		return super(NewUnconfirmedUser, self).form_valid(form)

class CreateAccount(SuccessMessageMixin, FormView):
	form_class =  UserInfoForm
	template_name = 'webcore/form_inside.html'
	success_url = '/'
	success_message = "Account Has Been Created Successfully"

	def dispatch(self, request, *args, **kwargs):
		slug  = kwargs.pop('slug')
		emailver = EmailVerification.objects.get(slug=slug)
		self.email = emailver.email
		return super(CreateAccount, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		form.done(self.email)
		return super(CreateAccount, self).form_valid(form)


class CreateTeam(SuccessMessageMixin, CreateView):
	form_class = CreateTeamForm
	template_name = 'form.html'
	success_message = "%(name)s was created successfully"

	def form_valid(self, form):
		form.instance.teamAuthor = self.request.user
		return super(CreateTeam, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('teamflows:team-single', kwargs={'team_slug': self.object.url})


class TeamList(ListView):
	model = Team
	template_name = 'teamlist.html'
	context_object_name = "teamlist"

class TeamDetail(DetailView):
	model = Team
	slug_field = 'url'
	slug_url_kwarg = 'team_slug'
	template_name = 'teamflow/teams_admin.html'
	context_object_name = "teamdetail"

class TeamMemberList(ListView):
	model = TeamMember
	slug_url_kwarg = 'member_slug'
	template_name = 'teammember.html'
	context_object_name = "teammemberlist"

class TeamMemberDetail(DetailView):
	model = TeamMember
	template_name = 'teammember.html'
	context_object_name = "teammemberdetail"

class TeamInviteDetail(DetailView):
	model = TeamInvite
	template_name = 'teaminvite.html'
	context_object_name = 'teaminvite'

class CreateTeamInvite(SuccessMessageMixin, CreateView):
	template_name = 'form.html'
	form_class = TeamInviteForm
	success_url = '/'
	success_message = 'An invitation has been sent to %(email)s'



class JoinTeam(View):
	pass

	# 		slug = models.SlugField(unique=True)
	# email = models.EmailField()
	# team = models.ForeignKey(Team)
	# accepted = models.BooleanField(null=True,default=False)
	# user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

# class chat_room(request, label):
# 	room, created = Room.objects.get_or_create(label=label)
# 	messages = reversed(room.messages.order_by('-timestamp')[:50])

# 	return render(request, "form.html", {
# 		"room": room,
# 		"mesg": messages,
# 		})

# class JSONResponseMixin(object):
# 	def render_to_json_response(self, context, **response_kwargs):
# 		return JsonResponse(
# 			self.get_data(context),
# 			**response_kwargs
# 			)

# 	def get_data(self, context):
# 		return context

# class JSONView(JSONResponseMixin, TemplateView):
# 	def render_to_response(self, context, **response_kwargs):
# 		return render_to_json_reponse(context, **response_kwargs)


# from django.views.generic.detail import SingleObjectTemplateResponseMixin

# class HybridDetailView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
#     def render_to_response(self, context):
#         # Look for a 'format=json' GET argument
#         if self.request.GET.get('format') == 'json':
#             return self.render_to_json_response(context)
#         else:
#             return super(HybridDetailView, self).render_to_response(context)