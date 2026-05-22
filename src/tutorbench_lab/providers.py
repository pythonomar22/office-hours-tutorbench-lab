"""Provider-neutral model clients.

The lab uses explicit CLI commands for generations. Importing this module or
running tests never contacts model APIs.
"""

from __future__ import annotations

import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from anthropic import Anthropic
from google import genai
from google.genai import types as google_types
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from tutorbench_lab.config import load_environment
from tutorbench_lab.media import load_image
from tutorbench_lab.schemas import ModelUsage, TutorResponse, TutorTurnInput

RATE_LIMIT_HEADER_PREFIXES = (
    "anthropic-ratelimit-",
    "anthropic-priority-",
)


class ProviderError(RuntimeError):
    """Raised when a configured model provider cannot complete a request."""


@dataclass(frozen=True)
class ModelSpec:
    provider: str
    model: str

    @classmethod
    def parse(cls, spec: str) -> ModelSpec:
        if ":" not in spec:
            raise ValueError(
                f"model spec must be '<provider>:<model>', got {spec!r}"
            )
        provider, model = spec.split(":", 1)
        provider = provider.strip().lower()
        model = model.strip()
        if not provider or not model:
            raise ValueError(f"invalid model spec: {spec!r}")
        return cls(provider=provider, model=model)


@dataclass
class GenerateResult:
    text: str
    latency_ms: int
    usage: ModelUsage
    raw: dict[str, Any]


class ModelClient(ABC):
    def __init__(self, spec: ModelSpec, *, timeout_s: float | None = None):
        self.spec = spec
        self.timeout_s = timeout_s

    @abstractmethod
    def generate(self, turn: TutorTurnInput, *, max_tokens: int = 1200) -> GenerateResult:
        """Generate one model response."""


def make_client(model_spec: str, *, timeout_s: float | None = None) -> ModelClient:
    spec = ModelSpec.parse(model_spec)
    if spec.provider == "anthropic":
        return AnthropicClient(spec, timeout_s=timeout_s)
    if spec.provider == "openai":
        return OpenAIClient(spec, timeout_s=timeout_s)
    if spec.provider == "google":
        return GoogleClient(spec, timeout_s=timeout_s)
    if spec.provider == "deepseek":
        return OpenAICompatibleClient(
            spec,
            api_key_env="DEEPSEEK_API_KEY",
            base_url="https://api.deepseek.com",
            timeout_s=timeout_s,
        )
    if spec.provider == "fireworks":
        return OpenAICompatibleClient(
            spec,
            api_key_env="FIREWORKS_API_KEY",
            base_url="https://api.fireworks.ai/inference/v1",
            timeout_s=timeout_s,
        )
    raise ValueError(f"unsupported provider: {spec.provider}")


class AnthropicClient(ModelClient):
    def __init__(self, spec: ModelSpec, *, timeout_s: float | None = None):
        super().__init__(spec, timeout_s=timeout_s)
        load_environment()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ProviderError("ANTHROPIC_API_KEY is not set")
        self._client = Anthropic(api_key=api_key, timeout=timeout_s, max_retries=0)

    @retry(wait=wait_exponential(multiplier=1, min=1, max=20), stop=stop_after_attempt(2))
    def generate(self, turn: TutorTurnInput, *, max_tokens: int = 1200) -> GenerateResult:
        image = load_image(turn.image)
        content: list[dict[str, Any]] = []
        if image:
            content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image.media_type,
                        "data": image.data_base64,
                    },
                }
            )
        content.append({"type": "text", "text": turn.user_prompt})

        start = time.monotonic()
        raw_response = self._client.messages.with_raw_response.create(
            model=self.spec.model,
            max_tokens=max_tokens,
            system=turn.system_prompt,
            messages=[{"role": "user", "content": content}],
        )
        response = raw_response.parse()
        latency_ms = int((time.monotonic() - start) * 1000)
        text = "".join(
            block.text for block in response.content if getattr(block, "type", None) == "text"
        )
        usage = ModelUsage(
            input_tokens=getattr(response.usage, "input_tokens", None),
            output_tokens=getattr(response.usage, "output_tokens", None),
        )
        return GenerateResult(
            text=text.strip(),
            latency_ms=latency_ms,
            usage=usage,
            raw={
                "id": getattr(response, "id", None),
                "model": response.model,
                "rate_limit": _rate_limit_headers(raw_response.headers),
            },
        )


class OpenAIClient(ModelClient):
    def __init__(self, spec: ModelSpec, *, timeout_s: float | None = None):
        super().__init__(spec, timeout_s=timeout_s)
        load_environment()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ProviderError("OPENAI_API_KEY is not set")
        self._client = OpenAI(api_key=api_key, timeout=timeout_s, max_retries=0)

    @retry(wait=wait_exponential(multiplier=1, min=1, max=20), stop=stop_after_attempt(2))
    def generate(self, turn: TutorTurnInput, *, max_tokens: int = 1200) -> GenerateResult:
        image = load_image(turn.image)
        user_content: list[dict[str, Any]] = [{"type": "text", "text": turn.user_prompt}]
        if image:
            user_content.append(
                {"type": "image_url", "image_url": {"url": image.data_url}}
            )

        start = time.monotonic()
        response = self._client.chat.completions.create(
            model=self.spec.model,
            messages=[
                {"role": "system", "content": turn.system_prompt},
                {"role": "user", "content": user_content},
            ],
            max_completion_tokens=max_tokens,
        )
        latency_ms = int((time.monotonic() - start) * 1000)
        choice = response.choices[0]
        usage = ModelUsage(
            input_tokens=getattr(response.usage, "prompt_tokens", None),
            output_tokens=getattr(response.usage, "completion_tokens", None),
            total_tokens=getattr(response.usage, "total_tokens", None),
        )
        return GenerateResult(
            text=(choice.message.content or "").strip(),
            latency_ms=latency_ms,
            usage=usage,
            raw={"id": response.id, "model": response.model},
        )


class OpenAICompatibleClient(OpenAIClient):
    def __init__(
        self,
        spec: ModelSpec,
        *,
        api_key_env: str,
        base_url: str,
        timeout_s: float | None = None,
    ):
        ModelClient.__init__(self, spec, timeout_s=timeout_s)
        load_environment()
        api_key = os.getenv(api_key_env)
        if not api_key:
            raise ProviderError(f"{api_key_env} is not set")
        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout_s,
            max_retries=0,
        )


class GoogleClient(ModelClient):
    def __init__(self, spec: ModelSpec, *, timeout_s: float | None = None):
        super().__init__(spec, timeout_s=timeout_s)
        load_environment()
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ProviderError("GOOGLE_API_KEY or GEMINI_API_KEY is not set")
        http_options = None
        if timeout_s is not None:
            http_options = google_types.HttpOptions(timeout=int(timeout_s * 1000))
        self._client = genai.Client(api_key=api_key, http_options=http_options)

    @retry(wait=wait_exponential(multiplier=1, min=1, max=20), stop=stop_after_attempt(2))
    def generate(self, turn: TutorTurnInput, *, max_tokens: int = 1200) -> GenerateResult:
        image = load_image(turn.image)
        parts: list[Any] = [turn.user_prompt]
        if image:
            parts.insert(
                0,
                google_types.Part.from_bytes(
                    data=image.data,
                    mime_type=image.media_type,
                ),
            )

        start = time.monotonic()
        response = self._client.models.generate_content(
            model=self.spec.model,
            contents=parts,
            config=google_types.GenerateContentConfig(
                system_instruction=turn.system_prompt,
                max_output_tokens=max_tokens,
            ),
        )
        latency_ms = int((time.monotonic() - start) * 1000)
        usage_metadata = getattr(response, "usage_metadata", None)
        usage = ModelUsage(
            input_tokens=getattr(usage_metadata, "prompt_token_count", None),
            output_tokens=getattr(usage_metadata, "candidates_token_count", None),
            total_tokens=getattr(usage_metadata, "total_token_count", None),
        )
        return GenerateResult(
            text=(response.text or "").strip(),
            latency_ms=latency_ms,
            usage=usage,
            raw={"model": self.spec.model},
        )


def response_from_result(
    *,
    task_id: str,
    model: str,
    strategy: Any,
    prompt_version: str,
    result: GenerateResult,
    trace: dict[str, Any] | None = None,
) -> TutorResponse:
    return TutorResponse(
        task_id=task_id,
        text=result.text,
        model=model,
        strategy=strategy,
        prompt_version=prompt_version,
        latency_ms=result.latency_ms,
        usage=result.usage,
        trace=trace or result.raw,
    )


def _rate_limit_headers(headers: Any) -> dict[str, str]:
    """Return provider rate-limit headers without exposing credentials."""

    captured: dict[str, str] = {}
    for key, value in headers.items():
        lowered = key.lower()
        if lowered == "retry-after" or any(
            lowered.startswith(prefix) for prefix in RATE_LIMIT_HEADER_PREFIXES
        ):
            captured[lowered] = value
    return captured
