"""Tests for audit logging."""

from token_proxy.audit import AuditLog


class TestAuditLog:
    def test_record_and_retrieve(self):
        log = AuditLog()
        log.record("session-1", "outbound", "/v1/messages", {"IP": 2, "Email": 1})
        entries = log.get_session_log("session-1")
        assert len(entries) == 1
        assert entries[0]["entity_counts"]["IP"] == 2

    def test_global_stats(self):
        log = AuditLog()
        log.record("s1", "outbound", "/v1/messages", {"IP": 2})
        log.record("s1", "outbound", "/v1/messages", {"Email": 3})
        log.record("s2", "outbound", "/v1/messages", {"IP": 1})
        stats = log.get_global_stats()
        assert stats["total_requests_proxied"] == 3
        assert stats["total_entities_redacted"]["IP"] == 3
        assert stats["total_entities_redacted"]["Email"] == 3

    def test_inbound_not_counted_as_request(self):
        log = AuditLog()
        log.record("s1", "outbound", "/v1/messages", {"IP": 1})
        log.record("s1", "inbound", "/v1/messages", {"IP": 1})
        stats = log.get_global_stats()
        assert stats["total_requests_proxied"] == 1

    def test_empty_session_log(self):
        log = AuditLog()
        entries = log.get_session_log("nonexistent")
        assert entries == []
