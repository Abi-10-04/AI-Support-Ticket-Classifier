import os
from unittest.mock import Mock, patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from .models import Ticket
from .service import GeminiService, GeminiServiceError
from .views import ClassificationView


class TicketApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_home_route_returns_message(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("AI Support Ticket Classifier", response.json()["message"])

    def test_classify_requires_ticket_text(self):
        response = self.client.post(reverse("classify-ticket"), {}, format="json")
        self.assertEqual(response.status_code, 400)

    @patch("tickets.views.GeminiService")
    def test_classify_saves_ticket_and_returns_record(self, mock_service):
        mock_service.return_value.classify_ticket.return_value = {
            "category": "Technical",
            "priority": "High",
            "owner": "Engineering",
            "confidence": 88,
            "reason": "The service is failing.",
            "sentiment": "Negative",
            "ai_reply": "We are looking into this.",
        }

        response = self.client.post(
            reverse("classify-ticket"),
            {"ticket_text": "My app is failing to load."},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(response.json()["category"], "Technical")

    @patch("tickets.views.GeminiService")
    def test_classify_uses_fallback_when_gemini_is_unavailable(self, mock_service):
        mock_service.side_effect = GeminiServiceError("Gemini is unavailable")

        request = self.factory.post(
            reverse("classify-ticket"),
            {"ticket_text": "My login page is broken."},
            format="json",
        )
        response = ClassificationView.as_view()(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(response.data["category"], "Technical")

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key", "OPENROUTER_MODEL": "openai/gpt-4o-mini"}, clear=False)
    @patch("tickets.service.requests.post")
    def test_classify_ticket_returns_openrouter_payload(self, mock_post):
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"category": "Technical", "priority": "High", "owner": "Engineering", "confidence": 91, "reason": "Test", "sentiment": "Negative", "ai_reply": "Thanks"}'}}]
        }
        mock_post.return_value = mock_response

        service = GeminiService()
        payload = service.classify_ticket("My app is broken")

        self.assertEqual(payload["category"], "Technical")
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args.kwargs["json"]["model"], "openai/gpt-4o-mini")

    @patch.dict(os.environ, {}, clear=True)
    def test_init_requires_openrouter_api_key(self):
        with self.assertRaisesRegex(GeminiServiceError, "OPENROUTER_API_KEY"):
            GeminiService()

    @patch.dict(os.environ, {"OPENROUTER_API_KEY": "your_real_openrouter_api_key"}, clear=False)
    def test_init_rejects_placeholder_api_key(self):
        with self.assertRaisesRegex(GeminiServiceError, "real OpenRouter API key"):
            GeminiService()

    def test_history_returns_newest_first(self):
        Ticket.objects.create(
            ticket_text="first ticket",
            category="Billing",
            priority="Low",
            owner="Billing",
            confidence=50,
            reason="Test",
            sentiment="Neutral",
            ai_reply="Thanks",
        )
        Ticket.objects.create(
            ticket_text="second ticket",
            category="Technical",
            priority="High",
            owner="Engineering",
            confidence=90,
            reason="Test 2",
            sentiment="Negative",
            ai_reply="Sorry",
        )

        response = self.client.get(reverse("ticket-history"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["ticket_text"], "second ticket")