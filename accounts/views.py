from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import uuid

def signup_view(request):
    """View for user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def invite_code_view(request):
    """View for entering invite code"""
    # Placeholder for now
    return render(request, 'accounts/invite_code.html')

def register_view(request, invite_code):
    """View for registering with an invite code"""
    # Placeholder for now
    return render(request, 'accounts/register.html', {'invite_code': invite_code})

@login_required
def invite_create_view(request):
    """View for creating invite codes"""
    # Placeholder for now
    return redirect('accounts:invite_list')

@login_required
def invite_list_view(request):
    """View for listing invite codes"""
    # Placeholder for now
    return render(request, 'accounts/invite_list.html')
