from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, TicketResponse
from .forms import TicketForm, TicketResponseForm

@login_required
def ticket_list(request):
    """View for listing support tickets"""
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'support/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, ticket_id):
    """View for ticket details"""
    ticket = get_object_or_404(Ticket, id=ticket_id, created_by=request.user)
    
    if request.method == 'POST':
        form = TicketResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ticket = ticket
            response.user = request.user
            response.save()
            messages.success(request, "Your response has been added.")
            return redirect('support:ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketResponseForm()
    
    responses = ticket.responses.all().order_by('created_at')
    return render(request, 'support/ticket_detail.html', {
        'ticket': ticket,
        'responses': responses,
        'form': form
    })

@login_required
def ticket_create(request):
    """View for creating a support ticket"""
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, "Your support ticket has been created.")
            return redirect('support:ticket_list')
    else:
        form = TicketForm()
    
    return render(request, 'support/ticket_form.html', {'form': form})
