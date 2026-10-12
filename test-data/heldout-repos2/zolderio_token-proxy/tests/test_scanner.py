"""Tests for PII detection and pseudonym replacement."""

from token_proxy.context import ContextEngine
from token_proxy.scanner import (
    PATTERNS,
    redact_request,
    redact_text,
    restore_response,
    restore_text,
)
from token_proxy.session_store import SessionMapping


class TestPatterns:
    def test_email_pattern(self):
        matches = PATTERNS["email"].findall("Contact admin@contoso.com for help")
        assert matches == ["admin@contoso.com"]

    def test_ip_pattern(self):
        matches = PATTERNS["ip"].findall("Source IP: 10.0.1.5, dest: 8.8.8.8")
        assert matches == ["10.0.1.5", "8.8.8.8"]

    def test_domain_pattern(self):
        text = "Resolved evil.com and sub.contoso.com"
        matches = PATTERNS["domain"].findall(text)
        assert "evil.com" in matches
        assert "sub.contoso.com" in matches

    def test_ip_not_matched_as_domain(self):
        matches = PATTERNS["domain"].findall("Address is 192.168.1.1")
        assert "192.168.1.1" not in matches


class TestRedactText:
    def test_email_produces_structured_pseudonym(self, session: SessionMapping, ctx: ContextEngine):
        text = "User admin@contoso.com logged in"
        redacted, counts = redact_text(text, session, ctx)
        assert "admin@contoso.com" not in redacted
        assert "user_account_001@domain-internal-001.com" in redacted
        assert counts["Email"] == 1

    def test_ip_produces_safe_range(self, session: SessionMapping, ctx: ContextEngine):
        text = "Connection from 10.0.1.5 to 8.8.8.8"
        redacted, counts = redact_text(text, session, ctx)
        # Internal IPs pass through (no value in hiding them)
        assert "10.0.1.5" in redacted
        # External IPs are pseudonymized
        assert "8.8.8.8" not in redacted
        assert "198.51.100." in redacted

    def test_internal_ips_not_redacted(self, session: SessionMapping, ctx: ContextEngine):
        """RFC 1918 and other private IPs should pass through unmodified."""
        text = "Servers at 10.0.1.5, 172.16.0.1, and 192.168.1.1"
        redacted, counts = redact_text(text, session, ctx)
        assert "10.0.1.5" in redacted
        assert "172.16.0.1" in redacted
        assert "192.168.1.1" in redacted
        assert counts.get("IP", 0) == 0

    def test_domain_produces_structured_pseudonym(
        self, session: SessionMapping, ctx: ContextEngine
    ):
        text = "DNS query to evil.com"
        redacted, counts = redact_text(text, session, ctx)
        assert "evil.com" not in redacted
        assert "domain-external-001.net" in redacted

    def test_same_value_same_pseudonym(self, session: SessionMapping, ctx: ContextEngine):
        text = "From admin@contoso.com to admin@contoso.com"
        redacted, _ = redact_text(text, session, ctx)
        assert redacted.count("user_account_001@domain-internal-001.com") == 2

    def test_file_extensions_not_matched(self, session: SessionMapping, ctx: ContextEngine):
        text = "Read CLAUDE.md and settings.json and config.yaml"
        redacted, counts = redact_text(text, session, ctx)
        assert "CLAUDE.md" in redacted
        assert "settings.json" in redacted
        assert "config.yaml" in redacted
        assert counts.get("Domain", 0) == 0

    def test_dotted_properties_not_matched(self, session: SessionMapping, ctx: ContextEngine):
        text = "Permission Policy.ReadWrite.All granted to ServicePrincipal.DisplayName"
        redacted, counts = redact_text(text, session, ctx)
        assert "Policy.ReadWrite.All" in redacted
        assert "ServicePrincipal.DisplayName" in redacted
        assert counts.get("Domain", 0) == 0

    def test_email_domain_consistency(self, session: SessionMapping, ctx: ContextEngine):
        text = "User admin@contoso.com from contoso.com"
        redact_text(text, session, ctx)
        email_pseudo = session.real_to_tag["admin@contoso.com"]
        domain_pseudo = session.real_to_tag["contoso.com"]
        assert email_pseudo == "user_account_001@domain-internal-001.com"
        assert domain_pseudo == "domain-internal-001.com"

    def test_known_hostnames(self, session: SessionMapping, ctx: ContextEngine):
        text = "Connected to DC01 via RDP"
        redacted, counts = redact_text(text, session, ctx)
        assert "DC01" not in redacted
        assert "host_001" in redacted

    def test_known_orgs(self, session: SessionMapping, ctx: ContextEngine):
        text = "Report from Contoso Inc about the breach"
        redacted, counts = redact_text(text, session, ctx)
        assert "Contoso Inc" not in redacted
        assert counts.get("Org", 0) >= 1


class TestRestoreText:
    def test_round_trip(self, session: SessionMapping, ctx: ContextEngine):
        original = "User admin@contoso.com from 8.8.8.8"
        redacted, _ = redact_text(original, session, ctx)
        restored = restore_text(redacted, session)
        assert restored == original

    def test_round_trip_complex(self, session: SessionMapping, ctx: ContextEngine):
        original = (
            "Alert: admin@contoso.com connected from 192.168.1.100 "
            "to evil.com (8.8.8.8) via partnercorp.com"
        )
        redacted, _ = redact_text(original, session, ctx)
        assert "admin@contoso.com" not in redacted
        assert "192.168.1.100" in redacted  # internal IP passes through
        assert "evil.com" not in redacted
        assert "8.8.8.8" not in redacted
        assert "partnercorp.com" not in redacted
        restored = restore_text(redacted, session)
        assert restored == original

    def test_subdomain_round_trip(self, session: SessionMapping, ctx: ContextEngine):
        original = "Resolved mail.contoso.com and contoso.com"
        redacted, _ = redact_text(original, session, ctx)
        assert "mail.contoso.com" not in redacted
        assert "contoso.com" not in redacted
        restored = restore_text(redacted, session)
        assert restored == original


class TestRedactRequest:
    def test_string_content(self, session: SessionMapping, ctx: ContextEngine):
        body = {
            "model": "claude-sonnet-4-20250514",
            "messages": [{"role": "user", "content": "Check IP 8.8.8.8"}],
        }
        counts = redact_request(body, session, ctx)
        assert "8.8.8.8" not in body["messages"][0]["content"]
        assert counts.get("IP", 0) >= 1

    def test_system_prompt(self, session: SessionMapping, ctx: ContextEngine):
        body = {
            "system": "You are investigating events at contoso.com",
            "messages": [{"role": "user", "content": "hello"}],
        }
        redact_request(body, session, ctx)
        assert "contoso.com" not in body["system"]

    def test_thinking_block_in_history(self, session: SessionMapping, ctx: ContextEngine):
        """Thinking blocks in assistant message history must be redacted."""
        body = {
            "messages": [
                {"role": "user", "content": "investigate admin@contoso.com"},
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "thinking",
                            "thinking": "The user admin@contoso.com logged in from 8.8.4.4",
                        },
                        {
                            "type": "text",
                            "text": "I found some activity.",
                        },
                    ],
                },
                {"role": "user", "content": "continue"},
            ],
        }
        redact_request(body, session, ctx)
        thinking = body["messages"][1]["content"][0]["thinking"]
        assert "admin@contoso.com" not in thinking
        assert "8.8.4.4" not in thinking
        assert "domain-internal-001.com" in thinking

    def test_tool_use_input_in_history(self, session: SessionMapping, ctx: ContextEngine):
        """tool_use input fields in assistant message history must be redacted."""
        body = {
            "messages": [
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "toolu_123",
                            "name": "Bash",
                            "input": {
                                "command": (
                                    'query run "SigninLogs | where'
                                    " UserPrincipalName != 'admin@contoso.com'\""
                                    " --mode hunt"
                                ),
                                "description": "Query sign-ins excluding admin@contoso.com",
                                "timeout": 30000,
                            },
                        },
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "tool_result", "tool_use_id": "toolu_123", "content": "ok"}
                    ],
                },
            ],
        }
        redact_request(body, session, ctx)
        tool_input = body["messages"][0]["content"][0]["input"]
        assert "admin@contoso.com" not in tool_input["command"]
        assert "admin@contoso.com" not in tool_input["description"]
        assert "domain-internal-001.com" in tool_input["command"]
        # Non-string fields should be untouched
        assert tool_input["timeout"] == 30000


class TestRestoreResponse:
    def test_text_block(self, session: SessionMapping, ctx: ContextEngine):
        redact_text("admin@contoso.com", session, ctx)
        pseudo = session.real_to_tag["admin@contoso.com"]
        resp = {"content": [{"type": "text", "text": f"Found {pseudo} in logs"}]}
        restore_response(resp, session)
        assert "admin@contoso.com" in resp["content"][0]["text"]

    def test_tool_use_block(self, session: SessionMapping, ctx: ContextEngine):
        redact_text("8.8.8.8", session, ctx)
        pseudo = session.real_to_tag["8.8.8.8"]
        resp = {
            "content": [
                {
                    "type": "tool_use",
                    "input": {"query": f"search {pseudo}", "nested": {"ip": pseudo}},
                }
            ]
        }
        restore_response(resp, session)
        assert resp["content"][0]["input"]["query"] == "search 8.8.8.8"
        assert resp["content"][0]["input"]["nested"]["ip"] == "8.8.8.8"

    def test_thinking_block(self, session: SessionMapping, ctx: ContextEngine):
        redact_text("admin@contoso.com", session, ctx)
        pseudo = session.real_to_tag["admin@contoso.com"]
        resp = {"content": [{"type": "thinking", "thinking": f"Investigating {pseudo}"}]}
        restore_response(resp, session)
        assert "admin@contoso.com" in resp["content"][0]["thinking"]
