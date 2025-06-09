from django import forms
from .models import Ticket, TicketResponse

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class TicketResponseForm(forms.ModelForm):
    class Meta:
        model = TicketResponse
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your response here...'}),
        }
        labels = {
            'message': '',
        }
