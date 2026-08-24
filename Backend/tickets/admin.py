from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("category", "priority", "owner", "confidence", "created_at")
    search_fields = ("ticket_text", "category", "owner", "sentiment")
