from __future__ import annotations

import os

from config import OPENROUTER_URL
from .base import LLMProvider


def get_llm_client() -> LLMProvider:
    """Create an LLM provider based on the LLM_PROVIDER env var.

    Supported values: "openrouter" (default), "google".
    """
    provider = os.getenv("LLM_PROVIDER", "openrouter")

    if provider == "openrouter":
        from .openrouter import OpenRouterProvider

        api_key = os.getenv("OPENROUTER_API_KEY", "")
        return OpenRouterProvider(api_key=api_key, base_url=OPENROUTER_URL)

    if provider == "google":
        from .google_ai import GoogleAIProvider

        api_key = os.getenv("GOOGLE_AI_API_KEY", "")
        return GoogleAIProvider(api_key=api_key)

    raise ValueError(f"Unknown LLM_PROVIDER: {provider!r}. Use 'openrouter' or 'google'.")
