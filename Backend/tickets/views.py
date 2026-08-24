import logging

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ticket
from .serializers import TicketClassificationRequestSerializer, TicketSerializer
from .service import GeminiService, GeminiServiceError

logger = logging.getLogger(__name__)


class HomeView(APIView):
    """Return a simple health-style message for the API root."""

    def get(self, request, *args, **kwargs):
        return Response({"message": "AI Support Ticket Classifier API is running."}, status=status.HTTP_200_OK)


class ClassificationView(APIView):
    """Accept a ticket, classify it with Gemini, save it, and return the stored record."""

    @staticmethod
    def _build_fallback_payload(ticket_text: str) -> dict:
        text = (ticket_text or "").lower()

        if any(keyword in text for keyword in ["bug", "error", "crash", "slow", "down", "server", "api", "database", "page", "loading", "broken", "not working"]):
            category, owner = "Technical", "Engineering"
        elif any(keyword in text for keyword in ["billing", "charge", "refund", "invoice", "payment"]):
            category, owner = "Billing", "Billing"
        elif any(keyword in text for keyword in ["login", "password", "account", "access", "email"]):
            category, owner = "Account", "Support"
        elif any(keyword in text for keyword in ["feature", "product", "feedback", "release", "roadmap"]):
            category, owner = "Product", "Product"
        elif any(keyword in text for keyword in ["sales", "quote", "pricing", "demo", "lead", "order"]):
            category, owner = "Sales", "Sales"
        else:
            category, owner = "Other", "Support"

        priority = "Medium"
        if any(keyword in text for keyword in ["urgent", "critical", "down", "immediately", "cannot", "can't"]):
            priority = "High"

        return {
            "category": category,
            "priority": priority,
            "owner": owner,
            "confidence": 60,
            "reason": "Used a deterministic fallback classifier because the Gemini API was unavailable.",
            "sentiment": "Neutral",
            "ai_reply": "Thanks for reporting this. We are reviewing it and will follow up shortly.",
        }

    def post(self, request, *args, **kwargs):
        serializer = TicketClassificationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ticket_text = serializer.validated_data["ticket_text"]

        try:
            ai_payload = GeminiService().classify_ticket(ticket_text)
        except GeminiServiceError as exc:
            logger.error("Gemini classification failed: %s", exc)
            ai_payload = self._build_fallback_payload(ticket_text)
        except Exception as exc:  # pragma: no cover - defensive fallback
            logger.error("Unexpected Gemini classification error: %s", exc)
            ai_payload = self._build_fallback_payload(ticket_text)

        ticket = Ticket.objects.create(
            ticket_text=ticket_text,
            category=ai_payload.get("category", "Other"),
            priority=ai_payload.get("priority", "Medium"),
            owner=ai_payload.get("owner", "Support"),
            confidence=int(ai_payload.get("confidence", 0)),
            reason=ai_payload.get("reason", ""),
            sentiment=ai_payload.get("sentiment", "Neutral"),
            ai_reply=ai_payload.get("ai_reply", ""),
        )

        return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)


class TicketHistoryView(APIView):
    """Return ticket history, optionally filtered by search keyword."""

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("search", "").strip()
        tickets = Ticket.objects.all()

        if query:
            tickets = tickets.filter(
                Q(ticket_text__icontains=query)
                | Q(category__icontains=query)
                | Q(priority__icontains=query)
                | Q(owner__icontains=query)
                | Q(sentiment__icontains=query)
            )

        tickets = tickets.order_by("-created_at")
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
