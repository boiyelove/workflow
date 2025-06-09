from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import LoginForm, RegistrationForm, UserProfileForm, InviteCodeForm, InviteUserForm
from .models import UserProfile, InviteCode

def login_view(request):
    if request.user.is_authenticated:
        return redirect('webcore:home')
        
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('webcore:home')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def invite_code_view(request):
    if request.user.is_authenticated:
        return redirect('webcore:home')
        
    if request.method == 'POST':
        form = InviteCodeForm(request.POST)
        if form.is_valid():
            invite = form.cleaned_data['invite']
            return redirect('accounts:register', invite_code=invite.code)
    else:
        form = InviteCodeForm()
    
    return render(request, 'accounts/invite_code.html', {'form': form})

def register_view(request, invite_code):
    if request.user.is_authenticated:
        return redirect('webcore:home')
    
    try:
        invite = InviteCode.objects.get(code=invite_code, is_used=False)
    except InviteCode.DoesNotExist:
        messages.error(request, "Invalid or expired invite code.")
        return redirect('accounts:invite_code')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form.fields['invite_code'].queryset = InviteCode.objects.filter(code=invite_code)
        form.initial = {'invite_code': invite.id, 'email': invite.email}
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('webcore:home')
    else:
        form = RegistrationForm()
        form.fields['invite_code'].queryset = InviteCode.objects.filter(code=invite_code)
        form.initial = {'invite_code': invite.id, 'email': invite.email}
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

class InviteUserView(LoginRequiredMixin, CreateView):
    model = InviteCode
    form_class = InviteUserForm
    template_name = 'accounts/invite_user.html'
    success_url = reverse_lazy('accounts:invite_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Invitation sent to {form.instance.email}")
        return super().form_valid(form)

class InviteListView(LoginRequiredMixin, ListView):
    model = InviteCode
    template_name = 'accounts/invite_list.html'
    context_object_name = 'invites'
    
    def get_queryset(self):
        return InviteCode.objects.filter(created_by=self.request.user)
