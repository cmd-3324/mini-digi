from django.contrib import admin
from .models import Ticket, TicketMessage, TicketAttachment

class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 1

class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 1
    fields = ('is_staff_reply', 'body', 'created_at')
    readonly_fields = ('created_at',)
    inlines = [TicketAttachmentInline]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'user', 'status', 'created_at')
    inlines = [TicketMessageInline]