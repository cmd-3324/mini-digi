from .models import Ticket

def ticket_count(request):
    if not request.user.is_authenticated:
        return {'unread_ticket_count': 0}
    count = Ticket.objects.filter(user=request.user, status='open').count()
    return {'unread_ticket_count': count}