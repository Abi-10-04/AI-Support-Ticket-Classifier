from django.db import models


class Ticket(models.Model):
    """Represents a support ticket with AI-generated classification data."""

    ticket_text = models.TextField()
    category = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)
    confidence = models.IntegerField()
    reason = models.TextField()
    sentiment = models.CharField(max_length=50)
    ai_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.category} - {self.priority}"
