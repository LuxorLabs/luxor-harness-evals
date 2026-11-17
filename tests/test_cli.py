import pytest

from harness_evals.cli import _api_key, _missing_env


def _clear(monkeypatch):
    for var in ("LUXOR_API_KEY", "TENKI_API_KEY"):
        monkeypatch.delenv(var, raising=False)


def test_api_key_required(monkeypatch):
    _clear(monkeypatch)
    assert _missing_env([]) == ["TENKI_API_KEY"]


@pytest.mark.parametrize("key", ["lx_test", "tk_test", "  lx_test  "])
def test_luxor_api_key_accepted(monkeypatch, key):
    _clear(monkeypatch)
    monkeypatch.setenv("LUXOR_API_KEY", key)
    assert _api_key() == key.strip()
    assert _missing_env([]) == []


def test_luxor_api_key_wins_over_tenki(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("LUXOR_API_KEY", "lx_test")
    monkeypatch.setenv("TENKI_API_KEY", "tk_legacy")
    assert _api_key() == "lx_test"


def test_tenki_api_key_still_accepted(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("TENKI_API_KEY", "tk_test")
    assert _missing_env([]) == []


def test_unprefixed_luxor_api_key_falls_back_to_tenki(monkeypatch):
    _clear(monkeypatch)
    monkeypatch.setenv("LUXOR_API_KEY", "pool-key-123")
    monkeypatch.setenv("TENKI_API_KEY", "tk_test")
    assert _api_key() == "tk_test"
    assert _missing_env([]) == []


@pytest.mark.parametrize("key", ["pool-key-123", "   ", ""])
def test_unusable_luxor_api_key_counts_as_missing(monkeypatch, key):
    _clear(monkeypatch)
    monkeypatch.setenv("LUXOR_API_KEY", key)
    assert _api_key() is None
    assert _missing_env([]) == ["TENKI_API_KEY"]
