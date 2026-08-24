import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class GeminiServiceError(Exception):
    """Raised when the OpenRouter service cannot produce a valid classification response."""


class GeminiService:
    """Thin wrapper around the OpenRouter Chat Completions API for ticket classification."""

    def __init__(self) -> None:
        self.api_key = (os.getenv("OPENROUTER_API_KEY") or "").strip()
        if not self.api_key:
            raise GeminiServiceError("Missing OPENROUTER_API_KEY in Backend/.env.")

        lower_key = self.api_key.lower()
        if any(token in lower_key for token in ["your_", "your", "replace", "placeholder", "example"]):
            raise GeminiServiceError(
                "OPENROUTER_API_KEY is still a placeholder. Replace it with your real OpenRouter API key in Backend/.env."
            )

        self.model_name = (os.getenv("OPENROUTER_MODEL") or "openai/gpt-4o-mini").strip()
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def classify_ticket(self, ticket_text: str) -> Dict[str, Any]:
        """Send a ticket to OpenRouter and parse the JSON payload."""
        prompt = f"""
You are an AI support ticket classifier.
Classify the support ticket below and return ONLY valid JSON with this exact schema:
{{"category": "", "priority": "", "owner": "", "confidence": 0, "reason": "", "sentiment": "", "ai_reply": ""}}

Rules:
- category: one of Support, Billing, Technical, Account, Product, Sales, Other
- priority: one of Low, Medium, High, Critical
- owner: one of Support, Billing, Engineering, Product, Sales, Operations
- confidence: integer from 0 to 100
- reason: concise explanation in one sentence
- sentiment: one of Positive, Neutral, Negative
- ai_reply: a helpful customer-facing response

Ticket:
{ticket_text}
"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "AI Support Ticket Classifier",
        }

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a strict JSON-only classifier. Return only JSON matching the requested schema.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
        except requests.RequestException as exc:
            raise GeminiServiceError(f"OpenRouter request failed: {exc}") from exc

        if response.status_code >= 400:
            error_body = response.text
            raise GeminiServiceError(f"OpenRouter request failed with status {response.status_code}: {error_body}")

        try:
            data = response.json()
        except ValueError as exc:
            raise GeminiServiceError("OpenRouter returned invalid JSON.") from exc

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise GeminiServiceError("OpenRouter response did not contain expected content.") from exc

        return self._parse_response(content)

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        cleaned = (response_text or "").strip()
        if not cleaned:
            raise GeminiServiceError("OpenRouter returned an empty response.")

        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise GeminiServiceError("OpenRouter response was not valid JSON.") from exc

        required_keys = {"category", "priority", "owner", "confidence", "reason", "sentiment", "ai_reply"}
        if not isinstance(payload, dict) or not required_keys.issubset(payload.keys()):
            raise GeminiServiceError("OpenRouter response did not contain the expected schema.")

        return payload
