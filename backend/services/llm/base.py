from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class LLMResponse:
    """Normalized response from any LLM provider."""

    content: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model: str = ""
    provider: str = ""


class LLMProvider(Protocol):
    """Protocol for LLM providers."""

    provider_name: str

    def chat(self, messages: list[dict], model: str) -> LLMResponse: ...
