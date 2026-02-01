from __future__ import annotations

import time
import requests
from app.core.config import settings


class PerplexityClient:
    def __init__(self) -> None:
        self.api_key = (getattr(settings, "PERPLEXITY_API_KEY", "") or "").strip()
        self.base_url = (getattr(settings, "PERPLEXITY_BASE_URL", "") or "https://api.perplexity.ai").rstrip("/")
        self.model = (getattr(settings, "PERPLEXITY_MODEL", "") or "sonar-deep-research").strip()

        # mock
        self.use_mock = str(getattr(settings, "USE_MOCK_PERPLEXITY", "false")).lower() == "true"

        if not self.use_mock and not self.api_key:
            raise RuntimeError(
                "PERPLEXITY_API_KEY is empty. Put it in .env or set USE_MOCK_PERPLEXITY=true."
            )

    def sonar_deep_research(self, prompt: str) -> str:

        if self.use_mock:
            return "[MOCK Perplexity]\n" + prompt[:200] + ("\n..." if len(prompt) > 200 else "")

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        retries = int(getattr(settings, "RETRY_COUNT", 3))
        timeout = int(getattr(settings, "REQUEST_TIMEOUT", 60))

        last_err = None
        for attempt in range(1, retries + 1):
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=timeout)

                if not r.ok:
                    # Make error readable
                    body_preview = (r.text or "")[:800]
                    last_err = f"Perplexity HTTP {r.status_code}. Response: {body_preview}"


                    if r.status_code in (429, 500, 502, 503, 504) and attempt < retries:
                        time.sleep(1.2 * attempt)
                        continue

                    raise RuntimeError(last_err)

                data = r.json()
                content = data["choices"][0]["message"]["content"]
                return content.strip()

            except requests.RequestException as e:
                last_err = f"Network error while calling Perplexity: {e}"
                if attempt < retries:
                    time.sleep(1.2 * attempt)
                    continue
                raise RuntimeError(last_err) from e

        raise RuntimeError(last_err or "Perplexity unknown error")
