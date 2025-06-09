from django.shortcuts import render, Http404, redirect, get_object_or_404
from django.views.generic.base import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.conf import settings

from .models import Team, TeamMember, TeamInvite
from .forms import CreateTeamForm, TeamInviteForm

import uuid

class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'teamflow/team_list.html'
    context_object_name = 'teams'
    
    def get_queryset(self):
        # Get teams where user is a member
        user_teams = Team.objects.filter(teammember__user=self.request.user)
        return user_teams

class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teamflow/team_detail.html'
    context_object_name = 'team'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = TeamMember.objects.filter(team=self.object)
        context['is_manager'] = self.object.is_teammanager(self.request.user)
        context['is_author'] = self.object.is_author(self.request.user)
        return context

class TeamCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Team
    form_class = CreateTeamForm
    template_name = 'teamflow/team_form.html'
    success_url = reverse_lazy('team_list')
    success_message = "Team %(name)s was created successfully"
    
    def form_valid(self, form):
        form.instance.teamAuthor = self.request.user
        response = super().form_valid(form)
        
        # Create team member for the author
        TeamMember.objects.create(
            team=self.object,
            user=self.request.user,
            handle=self.request.user.username,
            is_manager=True,
            designation="Team Lead"
        )
        
        return response

class TeamInviteView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = TeamInviteForm
    template_name = 'teamflow/team_invite_form.html'
    success_message = "Invitation sent to %(email)s"
    
    def get_success_url(self):
        return reverse_lazy('team_detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = get_object_or_404(Team, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])
        
        # Check if user is a manager
        if not team.is_teammanager(self.request.user):
            messages.error(self.request, "You don't have permission to invite members to this team")
            return redirect('team_detail', pk=team.pk)
        
        email = form.cleaned_data['email']
        
        # Check if invitation already exists
        if TeamInvite.objects.filter(team=team, email=email, accepted=False).exists():
            messages.warning(self.request, f"An invitation has already been sent to {email}")
            return redirect('team_detail', pk=team.pk)
        
        # Create invitation
        invite = TeamInvite.objects.create(
            team=team,
            email=email,
            sender=self.request.user,
            token=str(uuid.uuid4())
        )
        
        # Send invitation email
        invite.send_invite_email()
        
        return super().form_valid(form)
