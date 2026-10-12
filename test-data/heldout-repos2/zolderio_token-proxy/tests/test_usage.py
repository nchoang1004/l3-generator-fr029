"""Token usage extraction and audit integration."""

from __future__ import annotations

from token_proxy.audit import AuditLog
from token_proxy.providers.anthropic import AnthropicAdapter


class TestAnthropicUsageExtraction:
    def test_response_usage(self):
        adapter = AnthropicAdapter()
        body = {
            "id": "msg_1",
            "content": [],
            "usage": {"input_tokens": 123, "output_tokens": 45},
        }
        assert adapter.extract_usage_response(body) == {
            "input_tokens": 123,
            "output_tokens": 45,
        }

    def test_response_usage_missing(self):
        adapter = AnthropicAdapter()
        assert adapter.extract_usage_response({"content": []}) is None

    def test_sse_message_start_input_tokens(self):
        adapter = AnthropicAdapter()
        data = {
            "type": "message_start",
            "message": {"id": "msg_1", "usage": {"input_tokens": 200, "output_tokens": 1}},
        }
        usage = adapter.extract_usage_sse("message_start", data)
        assert usage == {"input_tokens": 200, "output_tokens": 1}

    def test_sse_message_delta_output_tokens(self):
        adapter = AnthropicAdapter()
        data = {"type": "message_delta", "usage": {"output_tokens": 87}}
        assert adapter.extract_usage_sse("message_delta", data) == {"output_tokens": 87}

    def test_sse_other_events_return_none(self):
        adapter = AnthropicAdapter()
        assert adapter.extract_usage_sse("ping", {}) is None
        assert adapter.extract_usage_sse(None, {"type": "content_block_delta"}) is None


class TestAuditUsageIntegration:
    def test_record_and_get_session_usage(self):
        log = AuditLog()
        log.record("s1", "outbound", "/v1/messages", {})
        log.record(
            "s1",
            "inbound",
            "/v1/messages",
            {},
            usage={"input_tokens": 100, "output_tokens": 20},
        )
        log.record(
            "s1",
            "inbound",
            "/v1/messages",
            {},
            usage={"input_tokens": 50, "output_tokens": 10},
        )
        u = log.get_session_usage("s1")
        assert u == {
            "session_id": "s1",
            "request_count": 2,
            "input_tokens": 150,
            "output_tokens": 30,
        }

    def test_global_stats_include_tokens(self):
        log = AuditLog()
        log.record(
            "s1",
            "inbound",
            "/v1/messages",
            {},
            usage={"input_tokens": 10, "output_tokens": 5},
        )
        # Outbound usage should NOT double-count.
        log.record(
            "s1",
            "outbound",
            "/v1/messages",
            {},
            usage={"input_tokens": 999, "output_tokens": 999},
        )
        stats = log.get_global_stats()
        assert stats["total_tokens"] == {"input_tokens": 10, "output_tokens": 5}

    def test_session_log_exposes_usage_counts(self):
        log = AuditLog()
        log.record(
            "s1",
            "inbound",
            "/v1/messages",
            {},
            usage={"input_tokens": 7, "output_tokens": 3},
        )
        entries = log.get_session_log("s1")
        assert entries[0]["usage_counts"] == {"input_tokens": 7, "output_tokens": 3}
