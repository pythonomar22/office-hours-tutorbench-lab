"""Cheap provider/key diagnostics."""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class ProviderCheck:
    provider: str
    key_env: str
    present: bool
    pinged: bool
    ok: bool | None
    status_code: int | None
    detail: str


PROVIDERS = {
    "anthropic": {
        "env": "ANTHROPIC_API_KEY",
        "url": "https://api.anthropic.com/v1/models",
        "headers": lambda key: {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
    },
    "openai": {
        "env": "OPENAI_API_KEY",
        "url": "https://api.openai.com/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
    },
    "google": {
        "env": "GOOGLE_API_KEY",
        "alt_env": "GEMINI_API_KEY",
        "url": "https://generativelanguage.googleapis.com/v1beta/models",
        "headers": lambda _key: {},
    },
    "deepseek": {
        "env": "DEEPSEEK_API_KEY",
        "url": "https://api.deepseek.com/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
    },
    "fireworks": {
        "env": "FIREWORKS_API_KEY",
        "url": "https://api.fireworks.ai/inference/v1/models",
        "headers": lambda key: {"Authorization": f"Bearer {key}"},
    },
}


def check_providers(*, ping: bool = False, timeout_s: float = 10.0) -> list[ProviderCheck]:
    checks = []
    for provider, config in PROVIDERS.items():
        env_name = config["env"]
        key = os.getenv(env_name)
        if not key and config.get("alt_env"):
            env_name = config["alt_env"]
            key = os.getenv(env_name)
        present = bool(key)
        if not present:
            checks.append(
                ProviderCheck(
                    provider=provider,
                    key_env=env_name,
                    present=False,
                    pinged=False,
                    ok=None,
                    status_code=None,
                    detail="missing",
                )
            )
            continue
        if not ping:
            checks.append(
                ProviderCheck(
                    provider=provider,
                    key_env=env_name,
                    present=True,
                    pinged=False,
                    ok=None,
                    status_code=None,
                    detail="present; ping skipped",
                )
            )
            continue

        try:
            url = config["url"]
            params = {}
            if provider == "google":
                params = {"key": key}
            with httpx.Client(timeout=timeout_s) as client:
                response = client.get(url, headers=config["headers"](key), params=params)
            checks.append(
                ProviderCheck(
                    provider=provider,
                    key_env=env_name,
                    present=True,
                    pinged=True,
                    ok=response.is_success,
                    status_code=response.status_code,
                    detail="ok" if response.is_success else _safe_error(response),
                )
            )
        except Exception as exc:  # noqa: BLE001 - diagnostics should not crash
            checks.append(
                ProviderCheck(
                    provider=provider,
                    key_env=env_name,
                    present=True,
                    pinged=True,
                    ok=False,
                    status_code=None,
                    detail=f"{type(exc).__name__}: {exc}",
                )
            )
    return checks


def _safe_error(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return response.text[:200]
    text = str(payload)
    return text[:200]
