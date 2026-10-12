"""Tests for session state management."""

import time

from token_proxy.session_store import SessionMapping, SessionStore


class TestSessionMapping:
    def test_email_pseudonym_format(self):
        m = SessionMapping()
        pseudo = m.get_or_create_tag("admin@contoso.com", "Email", "Internal")
        assert pseudo == "user_account_001@domain-internal-001.com"

    def test_ip_pseudonym_format(self):
        m = SessionMapping()
        pseudo = m.get_or_create_tag("10.0.1.5", "IP", "Internal")
        assert pseudo == "10.99.99.1"

    def test_domain_pseudonym_format(self):
        m = SessionMapping()
        pseudo = m.get_or_create_tag("evil.com", "Domain", "External")
        assert pseudo == "domain-external-001.net"

    def test_same_value_same_pseudonym(self):
        m = SessionMapping()
        p1 = m.get_or_create_tag("10.0.1.5", "IP", "Internal")
        p2 = m.get_or_create_tag("10.0.1.5", "IP", "Internal")
        assert p1 == p2

    def test_different_values_different_pseudonyms(self):
        m = SessionMapping()
        p1 = m.get_or_create_tag("10.0.1.5", "IP", "Internal")
        p2 = m.get_or_create_tag("10.0.1.6", "IP", "Internal")
        assert p1 != p2

    def test_bidirectional_lookup(self):
        m = SessionMapping()
        pseudo = m.get_or_create_tag("evil.com", "Domain", "External")
        assert m.real_to_tag["evil.com"] == pseudo
        assert m.tag_to_real[pseudo] == "evil.com"

    def test_fake_to_type_tracking(self):
        m = SessionMapping()
        pseudo = m.get_or_create_tag("admin@contoso.com", "Email", "Internal")
        assert m.fake_to_type[pseudo] == "Email"

    def test_case_insensitive_lookup(self):
        m = SessionMapping()
        p1 = m.get_or_create_tag("Admin@Contoso.com", "Email", "Internal")
        p2 = m.get_or_create_tag("admin@contoso.com", "Email", "Internal")
        assert p1 == p2

    def test_email_auto_registers_domain(self):
        m = SessionMapping()
        m.get_or_create_tag("admin@contoso.com", "Email", "Internal")
        assert "contoso.com" in m.real_to_tag
        assert m.real_to_tag["contoso.com"] == "domain-internal-001.com"

    def test_email_auto_registers_username(self):
        m = SessionMapping()
        m.get_or_create_tag("j.smith@contoso.com", "Email", "Internal")
        assert "j.smith" in m.real_to_tag
        assert m.real_to_tag["j.smith"] == "user_account_001"

    def test_email_domain_consistency(self):
        m = SessionMapping()
        m.get_or_create_tag("admin@contoso.com", "Email", "Internal")
        domain_pseudo = m.get_or_create_tag("contoso.com", "Domain", "Internal")
        assert domain_pseudo == "domain-internal-001.com"

    def test_subdomain_preservation(self):
        m = SessionMapping()
        m.get_or_create_tag("contoso.com", "Domain", "Internal")
        sub = m.get_or_create_tag("mail.contoso.com", "Domain", "Internal")
        assert sub == "mail.domain-internal-001.com"

    def test_person_pseudonym(self):
        m = SessionMapping()
        pseudo = m.get_or_create_tag("John Smith", "Person", "Internal")
        assert pseudo == "person_internal_001"

    def test_org_pseudonym(self):
        m = SessionMapping()
        pseudo = m.get_or_create_tag("Contoso Inc", "Org", "Internal")
        assert pseudo == "org_internal_001"

    def test_hostname_pseudonym(self):
        m = SessionMapping()
        pseudo = m.get_or_create_tag("DC01", "Hostname", "Internal")
        assert pseudo == "host_001"

    def test_all_counters_tracked(self):
        m = SessionMapping()
        m.get_or_create_tag("a@b.com", "Email", "External")
        m.get_or_create_tag("10.0.0.1", "IP", "Internal")
        m.get_or_create_tag("John", "Person", "Internal")
        assert m.counters["Email"] == 1
        assert m.counters["IP"] == 1
        assert m.counters["Person"] == 1
        # Email also auto-registers domain + username
        assert m.counters["Domain"] == 1
        assert m.counters["Username"] == 1


class TestSessionStore:
    def test_get_creates_new(self, store: SessionStore):
        m = store.get("session-1")
        assert isinstance(m, SessionMapping)

    def test_get_returns_same(self, store: SessionStore):
        m1 = store.get("session-1")
        m2 = store.get("session-1")
        assert m1 is m2

    def test_different_sessions_isolated(self, store: SessionStore):
        m1 = store.get("session-1")
        m2 = store.get("session-2")
        m1.get_or_create_tag("10.0.0.1", "IP", "Internal")
        assert len(m1.real_to_tag) == 1
        assert len(m2.real_to_tag) == 0

    def test_remove(self, store: SessionStore):
        store.get("session-1")
        store.remove("session-1")
        assert "session-1" not in store.list_sessions()

    def test_evict_expired(self):
        store = SessionStore(ttl_seconds=0)
        store.get("session-old")
        store.list_sessions()["session-old"].last_active = time.time() - 1
        assert store.evict_expired() == 1
        assert len(store.list_sessions()) == 0

    def test_evict_keeps_active(self):
        store = SessionStore(ttl_seconds=3600)
        store.get("session-active")
        assert store.evict_expired() == 0
        assert len(store.list_sessions()) == 1
