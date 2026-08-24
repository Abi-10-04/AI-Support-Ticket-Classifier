from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for the Ticket model."""

    class Meta:
        model = Ticket
        fields = [
            "id",
            "ticket_text",
            "category",
            "priority",
            "owner",
            "confidence",
            "reason",
            "sentiment",
            "ai_reply",
            "created_at",
        ]


class TicketClassificationRequestSerializer(serializers.Serializer):
    """Request serializer for the classification endpoint."""

    ticket_text = serializers.CharField(required=True, allow_blank=False)
