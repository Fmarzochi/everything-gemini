"""Gemini provider adapter using the official Google Generative AI SDK."""

from __future__ import annotations

import os
from typing import Any

import google.generativeai as genai
from google.generativeai.types import GenerationConfig

from llm.core.interface import (
    AuthenticationError,
    ContextLengthError,
    LLMProvider,
    RateLimitError,
)
from llm.core.types import LLMInput, LLMOutput, Message, ModelInfo, ProviderType, ToolCall


class GeminiProvider(LLMProvider):
    provider_type = ProviderType.GEMINI

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        self._models = [
            ModelInfo(
                name="gemini-1.5-pro",
                provider=ProviderType.GEMINI,
                supports_tools=True,
                supports_vision=True,
                max_tokens=8192,
                context_window=1000000,
            ),
            ModelInfo(
                name="gemini-1.5-flash",
                provider=ProviderType.GEMINI,
                supports_tools=True,
                supports_vision=True,
                max_tokens=8192,
                context_window=1000000,
            ),
        ]

    def generate(self, input: LLMInput) -> LLMOutput:
        try:
            model_name = input.model or "gemini-1.5-pro"
            # Map common internal names to actual Gemini model names
            if "sonnet" in model_name or "opus" in model_name:
                model_name = "gemini-1.5-pro"
            elif "haiku" in model_name:
                model_name = "gemini-1.5-flash"

            model = genai.GenerativeModel(model_name)
            
            # Convert messages to Gemini format
            contents = []
            for msg in input.messages:
                role = "user" if msg.role == "user" else "model"
                contents.append({"role": role, "parts": [msg.content]})

            generation_config = GenerationConfig(
                temperature=input.temperature,
                max_output_tokens=input.max_tokens or 8192,
            )

            # Note: Tool calling implementation for Gemini SDK is more complex
            # and would require a deeper refactor of the tool types.
            # This is a baseline functional adaptation.
            response = model.generate_content(
                contents,
                generation_config=generation_config
            )

            return LLMOutput(
                content=response.text,
                tool_calls=None, # Simplified for now
                model=model_name,
                usage={
                    "input_tokens": 0, # SDK doesn't expose this easily in this call
                    "output_tokens": 0,
                },
                stop_reason="end_turn",
            )
        except Exception as e:
            msg = str(e)
            if "401" in msg or "API_KEY_INVALID" in msg:
                raise AuthenticationError(msg, provider=ProviderType.GEMINI) from e
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                raise RateLimitError(msg, provider=ProviderType.GEMINI) from e
            raise

    def list_models(self) -> list[ModelInfo]:
        return self._models.copy()

    def validate_config(self) -> bool:
        return bool(self.api_key)

    def get_default_model(self) -> str:
        return "gemini-1.5-pro"
