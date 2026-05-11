"""Provider adapters for multiple LLM backends."""

# Importações resilientes para evitar falhas se bibliotecas não estiverem instaladas
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
from llm.providers.resolver import get_provider, register_provider

__all__ = (
    "ClaudeProvider",
    "OpenAIProvider",
    "OllamaProvider",
    "GeminiProvider",
    "get_provider",
    "register_provider",
)
