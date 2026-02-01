# app/services/gemini_client.py
from __future__ import annotations

import hashlib
import requests
from typing import Optional

from app.core.config import settings


class GeminiClient:

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        auth_mode: Optional[str] = None,  # "x-goog" | "bearer"
    ) -> None:
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.base_url = (base_url or settings.GEMINI_BASE_URL).rstrip("/")
        self.model = model or settings.GEMINI_MODEL
        self.auth_mode = (auth_mode or getattr(settings, "GEMINI_AUTH_MODE", "x-goog")).lower()

    def generate(self, prompt: str) -> str:
        # Mock mode
        if settings.USE_MOCK_GEMINI:
            h = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:10]
            return f"[MOCK GEMINI OUTPUT hash={h}]"

        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not set. Put it into .env or environment variables.")

        url = f"{self.base_url}/chat/completions"

        headers = {"Content-Type": "application/json"}
        if self.auth_mode == "bearer":
            headers["Authorization"] = f"Bearer {self.api_key}"
        else:
            headers["x-goog-api-key"] = self.api_key

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": settings.GEMINI_TEMPERATURE,
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=settings.REQUEST_TIMEOUT)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            body = ""
            try:
                body = resp.text[:2000]
            except Exception:
                pass
            raise RuntimeError(f"Gemini HTTP error: {e}. Response: {body}") from e

        data = resp.json()
        return data["choices"][0]["message"]["content"]
