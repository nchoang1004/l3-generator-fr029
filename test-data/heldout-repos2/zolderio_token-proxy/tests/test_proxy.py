"""Integration tests — mock Anthropic, verify full redact→forward→restore cycle."""

from __future__ import annotations

import copy
import json

import httpx
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def app_client(monkeypatch, config):
    """TestClient with mocked Anthropic upstream."""
    import token_proxy.proxy as proxy_mod
    from token_proxy.audit import init_audit
    from token_proxy.context import ContextEngine
    from token_proxy.main import app, store
    from token_proxy.scanner import init_scanner

    for sid in list(store.list_sessions()):
        store.remove(sid)

    monkeypatch.setenv("TOKEN_PROXY_CONFIG_PATH", "")

    async def mock_forward(*, method, path, headers, body, session, ctx, client, adapter=None):
        from token_proxy.scanner import redact_request, restore_response

        outbound_counts = {}
        redacted_snapshot = None
        if body is not None:
            body["stream"] = False
            outbound_counts = redact_request(body, session, ctx)
            redacted_snapshot = copy.deepcopy(body)

        echo_text = "Analysis complete."
        resp_json = {
            "id": "msg_123",
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": echo_text}],
            "model": "claude-sonnet-4-20250514",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 50, "output_tokens": 30},
        }
        raw_resp = copy.deepcopy(resp_json)
        restore_response(resp_json, session)
        resp_body = json.dumps(resp_json).encode()
        return (
            200,
            {"content-type": "application/json"},
            resp_body,
            outbound_counts,
            {},
            redacted_snapshot,
            raw_resp,
            {"input_tokens": 50, "output_tokens": 30},
        )

    monkeypatch.setattr(proxy_mod, "forward_request", mock_forward)

    import token_proxy.main as main_mod

    main_mod.ctx_engine = ContextEngine(config)
    main_mod.http_client = httpx.AsyncClient()
    init_audit(store)
    init_scanner(config)

    with TestClient(app, raise_server_exceptions=True) as client:
        yield client


class TestProxyEndToEnd:
    def test_redaction(self, app_client):
        resp = app_client.post(
            "/session/test-session/v1/messages",
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 100,
                "messages": [{"role": "user", "content": "Check admin@contoso.com at 10.0.1.5"}],
            },
        )
        assert resp.status_code == 200

    def test_health(self, app_client):
        resp = app_client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


class TestAuditEndpoints:
    def test_list_sessions(self, app_client):
        app_client.post(
            "/session/audit-test/v1/messages",
            json={
                "model": "claude-sonnet-4-20250514",
                "messages": [{"role": "user", "content": "Test 10.0.1.5"}],
            },
        )
        resp = app_client.get("/token-proxy/sessions")
        assert resp.status_code == 200
        assert any(s["session_id"] == "audit-test" for s in resp.json())

    def test_search_mappings(self, app_client):
        app_client.post(
            "/session/search-test/v1/messages",
            json={
                "model": "claude-sonnet-4-20250514",
                "messages": [{"role": "user", "content": "Check admin@contoso.com"}],
            },
        )
        resp = app_client.get("/token-proxy/sessions/search-test/search?q=contoso")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["results"]) > 0
        assert "replacement" in data["results"][0]

    def test_get_stats(self, app_client):
        resp = app_client.get("/token-proxy/stats")
        assert resp.status_code == 200
        assert "total_requests_proxied" in resp.json()
