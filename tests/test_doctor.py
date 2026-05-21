from __future__ import annotations

from tutorbench_lab.doctor import check_providers


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

    checks = check_providers(ping=False)

    assert checks
    assert all(check.present is False for check in checks)
    assert all(check.pinged is False for check in checks)
