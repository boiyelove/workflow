from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from webcore.forms import BsCharField, BsEmailField, BsPasswordField
from .models import UserProfile, InviteCode

class LoginForm(AuthenticationForm):
    username = BsCharField(label="Username")
    password = BsPasswordField(label="Password")

class InviteCodeForm(forms.Form):
    invite_code = BsCharField(label="Invite Code", max_length=36, help_text="Enter the invite code you received")
    email = BsEmailField(label="Email", help_text="Enter the email address associated with your invite")
    
    def clean(self):
        cleaned_data = super().clean()
        invite_code = cleaned_data.get('invite_code')
        email = cleaned_data.get('email')
        
        if invite_code and email:
            try:
                invite = InviteCode.objects.get(code=invite_code, email=email, is_used=False)
            except InviteCode.DoesNotExist:
                raise forms.ValidationError("Invalid invite code or email. Please check and try again.")
            
            cleaned_data['invite'] = invite
        
        return cleaned_data

class RegistrationForm(UserCreationForm):
    email = BsEmailField(required=True)
    first_name = BsCharField(required=True)
    last_name = BsCharField(required=True)
    invite_code = forms.ModelChoiceField(
        queryset=InviteCode.objects.filter(is_used=False),
        required=True,
        widget=forms.HiddenInput()
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'invite_code')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
            # Mark invite code as used
            invite_code = self.cleaned_data['invite_code']
            invite_code.is_used = True
            invite_code.save()
            
            # Create user profile
            UserProfile.objects.create(user=user, invite_code=invite_code)
            
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar', 'phone', 'position')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
        }

class InviteUserForm(forms.ModelForm):
    class Meta:
        model = InviteCode
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
