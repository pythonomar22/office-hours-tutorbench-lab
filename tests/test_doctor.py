from __future__ import annotations

from tutorbench_lab.doctor import check_providers
from tutorbench_lab.providers import _rate_limit_headers


def test_doctor_reports_missing_without_ping(monkeypatch):
    for env in [
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY",
        "GOOGLE_API_KEY",
        "GEMINI_API_KEY",
        "DEEPSEEK_API_KEY",
        "FIREWORKS_API_KEY",
    ]:
        monkeypatch.delenv(env, raising=False)

    checks = check_providers(ping=False, load_env=False)

    assert checks
    assert all(check.present is False for check in checks)
    assert all(check.pinged is False for check in checks)


def test_rate_limit_headers_filters_safe_metadata() -> None:
    headers = {
        "anthropic-ratelimit-requests-limit": "20000",
        "anthropic-ratelimit-input-tokens-remaining": "123",
        "retry-after": "2",
        "x-api-key": "secret",
    }

    captured = _rate_limit_headers(headers)

    assert captured == {
        "anthropic-ratelimit-requests-limit": "20000",
        "anthropic-ratelimit-input-tokens-remaining": "123",
        "retry-after": "2",
    }
