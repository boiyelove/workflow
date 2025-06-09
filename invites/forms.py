from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import Invite

class InviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ['email', 'role']
    
    def __init__(self, *args, **kwargs):
        self.target = kwargs.pop('target', None)
        self.invited_by = kwargs.pop('invited_by', None)
        self.target_type = kwargs.pop('target_type', None)
        
        super().__init__(*args, **kwargs)
        
        # Filter role choices based on target type
        if self.target_type:
            prefix = f"{self.target_type}_"
            self.fields['role'].choices = [
                (role, label) for role, label in self.fields['role'].choices
                if role.startswith(prefix)
            ]
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.target and self.invited_by:
            instance.invited_by = self.invited_by
            
            # Set the generic foreign key
            content_type = ContentType.objects.get_for_model(self.target.__class__)
            instance.content_type = content_type
            instance.object_id = self.target.id
            
            if commit:
                instance.save()
        
        return instance
