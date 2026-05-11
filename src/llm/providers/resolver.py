"""Provider factory and resolver."""

from __future__ import annotations

import os

from llm.core.interface import LLMProvider
from llm.core.types import ProviderType

# Importações condicionais conforme __init__.py
try:
    from llm.providers.claude import ClaudeProvider
except ImportError:
    ClaudeProvider = None

try:
    from llm.providers.openai import OpenAIProvider
except ImportError:
    OpenAIProvider = None

try:
    from llm.providers.ollama import OllamaProvider
except ImportError:
    OllamaProvider = None

from llm.providers.gemini import GeminiProvider

_PROVIDER_MAP: dict[ProviderType, type[LLMProvider]] = {
    ProviderType.CLAUDE: ClaudeProvider,
    ProviderType.OPENAI: OpenAIProvider,
    ProviderType.OLLAMA: OllamaProvider,
    ProviderType.GEMINI: GeminiProvider,
}


def get_provider(provider_type: ProviderType | str | None = None, **kwargs: str) -> LLMProvider:
    if provider_type is None:
        provider_type = os.environ.get("LLM_PROVIDER", "gemini").lower()

    if isinstance(provider_type, str):
        try:
            provider_type = ProviderType(provider_type)
        except ValueError:
            raise ValueError(f"Unknown provider type: {provider_type}. Valid types: {[p.value for p in ProviderType]}")

    provider_cls = _PROVIDER_MAP.get(provider_type)
    
    # Validação para evitar erro se o provider for None (não instalado)
    if provider_cls is None:
        raise ValueError(f"Provedor {provider_type} não está instalado ou disponível.")

    return provider_cls(**kwargs)


def register_provider(provider_type: ProviderType, provider_cls: type[LLMProvider]) -> None:
    _PROVIDER_MAP[provider_type] = provider_cls
