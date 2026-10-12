"""Tests for the runtime config management API."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from token_proxy.config import save_config
from token_proxy.ner import get_skiplist
from token_proxy.scanner import (
    DOMAIN_ALLOWLIST,
    is_redaction_enabled,
    set_redaction_enabled,
)


@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    """Write a test config.json and return its path."""
    data = {
        "internal_domains": ["contoso.com"],
        "partner_domains": [],
        "internal_ip_ranges": ["10.0.0.0/8"],
        "known_persons": ["John Doe"],
        "known_orgs": ["Contoso Inc"],
        "known_hostnames": ["DC01"],
        "ner_enabled": False,
        "ner_tech_skiplist": ["existing_term"],
        "ner_generic_it_words": ["access", "account"],
        "domain_allowlist": ["mitre.org", "owasp.org"],
        "redaction_enabled": True,
    }
    p = tmp_path / "config.json"
    p.write_text(json.dumps(data))
    return p


@pytest.fixture
def app_client(config_file: Path, monkeypatch: pytest.MonkeyPatch):
    """Create a TestClient with the config API wired up."""
    # Point lifespan at the test config file
    monkeypatch.setenv("TOKEN_PROXY_CONFIG_PATH", str(config_file))

    from token_proxy.main import app

    set_redaction_enabled(True)

    with TestClient(app, raise_server_exceptions=True) as client:
        yield client


class TestGetConfig:
    def test_returns_full_config(self, app_client: TestClient):
        resp = app_client.get("/token-proxy/config")
        assert resp.status_code == 200
        data = resp.json()
        assert "internal_domains" in data
        assert "redaction_enabled" in data
        assert data["redaction_enabled"] is True

    def test_includes_domain_allowlist(self, app_client: TestClient):
        resp = app_client.get("/token-proxy/config")
        data = resp.json()
        assert "domain_allowlist" in data
        assert "mitre.org" in data["domain_allowlist"]


class TestGetWhitelists:
    def test_returns_all_categories(self, app_client: TestClient):
        resp = app_client.get("/token-proxy/config/whitelist")
        assert resp.status_code == 200
        data = resp.json()
        assert "ner_skiplist" in data
        assert isinstance(data["ner_skiplist"], list)
        assert "ner_generic_it_words" in data
        assert isinstance(data["ner_generic_it_words"], list)
        assert "domain_allowlist" in data
        assert "mitre.org" in data["domain_allowlist"]
        assert "known_persons" in data
        assert "known_orgs" in data
        assert "known_hostnames" in data


class TestAddToWhitelist:
    def test_add_ner_skiplist(self, app_client: TestClient, config_file: Path):
        resp = app_client.post(
            "/token-proxy/config/whitelist",
            json={"category": "ner_skiplist", "values": ["EvoSTS", "Hetzner"]},
        )
        assert resp.status_code == 200
        assert resp.json()["added"] == ["EvoSTS", "Hetzner"]

        # Verify runtime effect
        sl = get_skiplist()
        assert "evosts" in sl
        assert "hetzner" in sl

        # Verify persisted
        persisted = json.loads(config_file.read_text())
        assert "evosts" in persisted["ner_tech_skiplist"]

    def test_add_ner_generic_it_words(self, app_client: TestClient, config_file: Path):
        resp = app_client.post(
            "/token-proxy/config/whitelist",
            json={"category": "ner_generic_it_words", "values": ["newword"]},
        )
        assert resp.status_code == 200

        persisted = json.loads(config_file.read_text())
        assert "newword" in persisted["ner_generic_it_words"]

    def test_add_domain_allowlist(self, app_client: TestClient):
        resp = app_client.post(
            "/token-proxy/config/whitelist",
            json={"category": "domain_allowlist", "values": ["example.com"]},
        )
        assert resp.status_code == 200
        assert "example.com" in DOMAIN_ALLOWLIST

    def test_add_known_persons(self, app_client: TestClient, config_file: Path):
        resp = app_client.post(
            "/token-proxy/config/whitelist",
            json={"category": "known_persons", "values": ["Jane Smith"]},
        )
        assert resp.status_code == 200
        persisted = json.loads(config_file.read_text())
        assert "Jane Smith" in persisted["known_persons"]

    def test_add_known_orgs(self, app_client: TestClient, config_file: Path):
        resp = app_client.post(
            "/token-proxy/config/whitelist",
            json={"category": "known_orgs", "values": ["Acme Corp"]},
        )
        assert resp.status_code == 200
        persisted = json.loads(config_file.read_text())
        assert "Acme Corp" in persisted["known_orgs"]

    def test_add_known_hostnames(self, app_client: TestClient, config_file: Path):
        resp = app_client.post(
            "/token-proxy/config/whitelist",
            json={"category": "known_hostnames", "values": ["WEB01"]},
        )
        assert resp.status_code == 200
        persisted = json.loads(config_file.read_text())
        assert "WEB01" in persisted["known_hostnames"]

    def test_invalid_category_returns_400(self, app_client: TestClient):
        resp = app_client.post(
            "/token-proxy/config/whitelist",
            json={"category": "bogus", "values": ["foo"]},
        )
        assert resp.status_code == 400

    def test_idempotent_add(self, app_client: TestClient, config_file: Path):
        """Adding the same value twice doesn't duplicate it."""
        for _ in range(2):
            app_client.post(
                "/token-proxy/config/whitelist",
                json={"category": "known_persons", "values": ["John Doe"]},
            )
        persisted = json.loads(config_file.read_text())
        assert persisted["known_persons"].count("John Doe") == 1


class TestRemoveFromWhitelist:
    def test_remove_ner_skiplist(self, app_client: TestClient, config_file: Path):
        # First add
        app_client.post(
            "/token-proxy/config/whitelist",
            json={"category": "ner_skiplist", "values": ["removeme"]},
        )
        assert "removeme" in get_skiplist()

        # Then remove
        resp = app_client.request(
            "DELETE",
            "/token-proxy/config/whitelist",
            json={"category": "ner_skiplist", "values": ["removeme"]},
        )
        assert resp.status_code == 200
        assert "removeme" not in get_skiplist()

    def test_remove_domain_allowlist(self, app_client: TestClient):
        # Add a custom domain first
        app_client.post(
            "/token-proxy/config/whitelist",
            json={"category": "domain_allowlist", "values": ["custom.example.com"]},
        )
        assert "custom.example.com" in DOMAIN_ALLOWLIST

        resp = app_client.request(
            "DELETE",
            "/token-proxy/config/whitelist",
            json={"category": "domain_allowlist", "values": ["custom.example.com"]},
        )
        assert resp.status_code == 200
        assert "custom.example.com" not in DOMAIN_ALLOWLIST

    def test_remove_known_persons(self, app_client: TestClient, config_file: Path):
        resp = app_client.request(
            "DELETE",
            "/token-proxy/config/whitelist",
            json={"category": "known_persons", "values": ["John Doe"]},
        )
        assert resp.status_code == 200
        persisted = json.loads(config_file.read_text())
        assert "John Doe" not in persisted["known_persons"]


class TestRedactionToggle:
    def test_get_status(self, app_client: TestClient):
        resp = app_client.get("/token-proxy/config/status")
        assert resp.status_code == 200
        assert resp.json()["redaction_enabled"] is True

    def test_disable_redaction(self, app_client: TestClient, config_file: Path):
        resp = app_client.post(
            "/token-proxy/config/status",
            json={"redaction_enabled": False},
        )
        assert resp.status_code == 200
        assert resp.json()["redaction_enabled"] is False
        assert is_redaction_enabled() is False

        # Verify persisted
        persisted = json.loads(config_file.read_text())
        assert persisted["redaction_enabled"] is False

    def test_enable_redaction(self, app_client: TestClient):
        # Disable first
        app_client.post("/token-proxy/config/status", json={"redaction_enabled": False})
        assert is_redaction_enabled() is False

        # Re-enable
        resp = app_client.post("/token-proxy/config/status", json={"redaction_enabled": True})
        assert resp.status_code == 200
        assert is_redaction_enabled() is True


class TestRedactionBypass:
    """Verify that redact_text is a no-op when redaction is disabled."""

    def test_redact_text_skips_when_disabled(self):
        from token_proxy.context import ContextEngine
        from token_proxy.scanner import init_scanner, redact_text, set_redaction_enabled
        from token_proxy.session_store import SessionMapping

        cfg = {
            "internal_domains": ["contoso.com"],
            "partner_domains": [],
            "internal_ip_ranges": ["10.0.0.0/8"],
            "known_persons": [],
            "known_orgs": [],
            "known_hostnames": [],
            "ner_enabled": False,
            "ner_tech_skiplist": [],
            "ner_generic_it_words": [],
            "domain_allowlist": [],
            "redaction_enabled": False,
        }
        init_scanner(cfg)
        set_redaction_enabled(False)

        session = SessionMapping()
        ctx = ContextEngine(cfg)
        text = "User admin@contoso.com from 10.0.1.5"
        result, counts = redact_text(text, session, ctx)
        assert result == text
        assert counts == {}


class TestSaveConfig:
    def test_save_and_reload(self, tmp_path: Path):
        cfg = {"known_orgs": ["TestOrg"], "ner_enabled": True}
        p = tmp_path / "test_save.json"
        save_config(cfg, p)

        reloaded = json.loads(p.read_text())
        assert reloaded["known_orgs"] == ["TestOrg"]

    def test_atomic_write(self, tmp_path: Path):
        """No .tmp file remains after save."""
        p = tmp_path / "atomic.json"
        save_config({"test": True}, p)
        assert p.exists()
        assert not p.with_suffix(".tmp").exists()
