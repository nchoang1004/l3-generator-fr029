"""Tests for the context classification engine."""

from token_proxy.context import ContextEngine


class TestClassifyIP:
    def test_private_rfc1918(self, ctx: ContextEngine):
        assert ctx.classify_ip("10.0.1.5") == "Internal"
        assert ctx.classify_ip("172.16.0.1") == "Internal"
        assert ctx.classify_ip("192.168.1.1") == "Internal"

    def test_public_ip(self, ctx: ContextEngine):
        assert ctx.classify_ip("8.8.8.8") == "External"

    def test_invalid_ip(self, ctx: ContextEngine):
        assert ctx.classify_ip("not-an-ip") == "External"


class TestClassifyEmail:
    def test_internal(self, ctx: ContextEngine):
        assert ctx.classify_email("admin@contoso.com") == "Internal"

    def test_partner(self, ctx: ContextEngine):
        assert ctx.classify_email("vendor@partnercorp.com") == "Partner"

    def test_external(self, ctx: ContextEngine):
        assert ctx.classify_email("attacker@evil.com") == "External"


class TestClassifyDomain:
    def test_internal(self, ctx: ContextEngine):
        assert ctx.classify_domain("contoso.com") == "Internal"
        assert ctx.classify_domain("sub.contoso.com") == "Internal"

    def test_partner(self, ctx: ContextEngine):
        assert ctx.classify_domain("partnercorp.com") == "Partner"

    def test_external(self, ctx: ContextEngine):
        assert ctx.classify_domain("google.com") == "External"


class TestClassifyNewTypes:
    def test_person_defaults_internal(self, ctx: ContextEngine):
        assert ctx.classify_person("John Smith") == "Internal"

    def test_org_matches_internal_domain(self, ctx: ContextEngine):
        assert ctx.classify_org("Contoso Inc") == "Internal"

    def test_org_defaults_external(self, ctx: ContextEngine):
        assert ctx.classify_org("Unknown Corp") == "External"

    def test_hostname_defaults_internal(self, ctx: ContextEngine):
        assert ctx.classify_hostname("DC01") == "Internal"
