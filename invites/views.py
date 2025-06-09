from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from .models import Invite
from .forms import InviteForm

@login_required
def send_invite(request, target_type, target_id):
    """Generic view for sending invites to any entity type"""
    # Get the target model and object
    if target_type == 'workspace':
        from workspace.models import Workspace
        target = get_object_or_404(Workspace, id=target_id)
        permission_check = target.workspaceuser_set.filter(user=request.user, role='admin').exists()
        success_url = reverse('workspace:detail', args=[target_id])
    
    elif target_type == 'team':
        from teamflow.models import Team
        target = get_object_or_404(Team, id=target_id)
        permission_check = target.members.filter(user=request.user, is_manager=True).exists()
        success_url = reverse('teamflow:team-detail', args=[target.url])
    
    elif target_type == 'project':
        from projectflow.models import Project
        target = get_object_or_404(Project, id=target_id)
        permission_check = (
            target.team.members.filter(user=request.user, is_manager=True).exists() or
            target.workspace.workspaceuser_set.filter(user=request.user, role='admin').exists()
        )
        success_url = reverse('projectflow:project-detail', args=[target.slug])
    
    elif target_type == 'platform':
        # For platform invites, check if user is a superuser
        target = settings.SITE_NAME  # Just a placeholder
        permission_check = request.user.is_superuser
        success_url = reverse('admin:index')
    
    else:
        messages.error(request, "Invalid target type.")
        return redirect('home')
    
    # Check permissions
    if not permission_check:
        messages.error(request, f"You don't have permission to invite users to this {target_type}.")
        return redirect('home')
    
    if request.method == 'POST':
        form = InviteForm(
            request.POST, 
            target=target, 
            invited_by=request.user,
            target_type=target_type
        )
        
        if form.is_valid():
            invite = form.save()
            
            # Send invitation email
            invite_url = request.build_absolute_uri(
                reverse('invites:accept', kwargs={'token': invite.token})
            )
            
            target_name = getattr(target, 'name', str(target))
            
            send_mail(
                f'Invitation to join {target_name}',
                f'You have been invited to join {target_name} as {invite.get_role_display()}. '
                f'Click the link to accept: {invite_url}',
                settings.DEFAULT_FROM_EMAIL,
                [invite.email],
                fail_silently=False,
            )
            
            messages.success(request, f"Invitation sent to {invite.email}")
            return redirect(success_url)
    else:
        form = InviteForm(target_type=target_type)
    
    context = {
        'form': form,
        'target': target,
        'target_type': target_type
    }
    
    return render(request, 'invites/send_invite.html', context)

@login_required
def accept_invite(request, token):
    """View for accepting invites"""
    invite = get_object_or_404(Invite, token=token)
    
    # Check if invite is valid
    if invite.accepted:
        messages.error(request, "This invitation has already been accepted.")
        return redirect('home')
    
    if invite.is_expired:
        messages.error(request, "This invitation has expired.")
        return redirect('home')
    
    # Check if the invite is for the current user
    if invite.email != request.user.email:
        messages.error(request, "This invitation is not for your account.")
        return redirect('home')
    
    # Accept the invitation
    if invite.accept(request.user):
        target_name = getattr(invite.target, 'name', str(invite.target))
        messages.success(request, f"You have successfully joined {target_name}.")
        
        # Redirect based on target type
        if invite.target_type == 'workspace':
            return redirect('workspace:detail', workspace_id=invite.object_id)
        elif invite.target_type == 'team':
            team = invite.target
            return redirect('teamflow:team-detail', url=team.url)
        elif invite.target_type == 'project':
            project = invite.target
            return redirect('projectflow:project-detail', slug=project.slug)
        else:
            return redirect('home')
    else:
        messages.error(request, "There was a problem accepting this invitation.")
        return redirect('home')
