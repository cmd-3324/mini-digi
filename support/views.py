from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Ticket, TicketMessage, TicketAttachment

@login_required
def ticket_list(request):
    """User's ticket list with search, sort, filter"""
    tickets = Ticket.objects.filter(user=request.user)

    q = request.GET.get("q", "").strip()
    if q:
        tickets = tickets.filter(subject__icontains=q)

    status = request.GET.get("status", "")
    if status in ("open", "replied", "closed"):
        tickets = tickets.filter(status=status)

    sort = request.GET.get("sort", "-created_at")
    if sort not in ("-created_at", "created_at", "subject", "-subject"):
        sort = "-created_at"
    tickets = tickets.order_by(sort)

    return render(request, 'dashboard/ticket_list.html', {
        'tickets': tickets, 'q': q, 'status': status, 'sort': sort,
    })

@login_required
def ticket_detail(request, pk):
    """Single ticket chat view"""
    ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
    
    if request.method == 'POST':
        body = request.POST.get('body')
        message = TicketMessage.objects.create(
            ticket=ticket, 
            is_staff_reply=False, 
            body=body
        )
        
        files = request.FILES.getlist('attachments')
        for f in files:
            TicketAttachment.objects.create(message=message, file=f)
        
        # Notify staff
        send_mail(
            subject=f"New reply on Ticket #{ticket.pk}",
            message=f"User replied. Check: {request.build_absolute_uri('/admin/support/ticket/' + str(ticket.pk) + '/change/')}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['miniwicket@gmail.com'],
            fail_silently=True,
        )
        
        return redirect('support:ticket_detail', pk=ticket.pk)
    
    return render(request, 'dashboard/ticket_detail.html', {'ticket': ticket})

@login_required
def create_ticket(request):
    """Create new ticket"""
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('body', '').strip()

        if not subject or not body:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"ok": False, "error": "Subject and message are required."})
            return render(request, 'dashboard/ticket_create.html')

        ticket = Ticket.objects.create(user=request.user, subject=subject)
        message = TicketMessage.objects.create(ticket=ticket, is_staff_reply=False, body=body)

        files = request.FILES.getlist('attachments')
        for f in files:
            TicketAttachment.objects.create(message=message, file=f)

        # Notify staff
        send_mail(
            subject=f"New Ticket: {subject}",
            message=f"User: {request.user.email}\n\n{body}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['miniwicket@gmail.com'],
            fail_silently=True,
        )

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "ok": True,
                "message": "Ticket created successfully!",
                "ticket": {
                    "id": ticket.pk,
                    "subject": ticket.subject,
                    "status": ticket.get_status_display(),
                    "status_key": ticket.status,
                    "created_at": ticket.created_at.strftime("%b %d, %Y"),
                    "url": request.build_absolute_uri(f"/support/tickets/{ticket.pk}/"),
                }
            })

        return redirect('support:ticket_list')

    return render(request, 'dashboard/ticket_create.html')