from django import template
from support.models import Ticket

register = template.Library()

@register.simple_tag(takes_context=True)
def all_unread_tickets(context):
    request = context.get('request')
    if not request or not request.user.is_authenticated:
        return 0
    
    count = Ticket.objects.filter(user=request.user, status='open').count()
    return count