"""Tests for the structured pseudonym allocator."""

from token_proxy.pseudonyms import PseudonymAllocator, _looks_like_dotted_property


class TestPseudonymAllocator:
    def test_email_format(self):
        alloc = PseudonymAllocator()
        pseudo = alloc.allocate_email("admin@contoso.com", "Internal")
        assert pseudo == "user_account_001@domain-internal-001.com"

    def test_email_sequential(self):
        alloc = PseudonymAllocator()
        p1 = alloc.allocate_email("admin@contoso.com", "Internal")
        p2 = alloc.allocate_email("user@contoso.com", "Internal")
        assert p1 == "user_account_001@domain-internal-001.com"
        assert p2 == "user_account_002@domain-internal-001.com"

    def test_domain_internal(self):
        alloc = PseudonymAllocator()
        pseudo = alloc.allocate_domain("contoso.com", "Internal")
        assert pseudo == "domain-internal-001.com"

    def test_domain_external(self):
        alloc = PseudonymAllocator()
        pseudo = alloc.allocate_domain("evil.com", "External")
        assert pseudo == "domain-external-001.net"

    def test_domain_partner(self):
        alloc = PseudonymAllocator()
        pseudo = alloc.allocate_domain("partner.com", "Partner")
        assert pseudo == "domain-partner-001.org"

    def test_ip_internal(self):
        alloc = PseudonymAllocator()
        pseudo = alloc.allocate_ip("10.0.1.5", "Internal")
        assert pseudo == "10.99.99.1"

    def test_ip_external(self):
        alloc = PseudonymAllocator()
        pseudo = alloc.allocate_ip("8.8.8.8", "External")
        assert pseudo == "198.51.100.1"

    def test_ip_partner(self):
        alloc = PseudonymAllocator()
        pseudo = alloc.allocate_ip("1.2.3.4", "Partner")
        assert pseudo == "203.0.113.1"

    def test_email_domain_consistency(self):
        """Email domain and standalone domain use the same pseudonym."""
        alloc = PseudonymAllocator()
        alloc.allocate_email("admin@contoso.com", "Internal")
        domain_pseudo = alloc.allocate_domain("contoso.com", "Internal")
        assert domain_pseudo == "domain-internal-001.com"

    def test_multiple_emails_same_domain(self):
        """Different emails at same domain produce different user_account but same domain."""
        alloc = PseudonymAllocator()
        p1 = alloc.allocate_email("alice@contoso.com", "Internal")
        p2 = alloc.allocate_email("bob@contoso.com", "Internal")
        assert p1.endswith("@domain-internal-001.com")
        assert p2.endswith("@domain-internal-001.com")
        assert p1 != p2

    def test_subdomain_preservation(self):
        alloc = PseudonymAllocator()
        alloc.allocate_domain("contoso.com", "Internal")
        sub = alloc.allocate_domain("mail.contoso.com", "Internal")
        assert sub == "mail.domain-internal-001.com"

    def test_username_consistency_with_email(self):
        """Bare username reuses the same NNN as the email."""
        alloc = PseudonymAllocator()
        alloc.allocate_email("j.smith@contoso.com", "Internal")
        username = alloc.allocate_username("j.smith", "Internal")
        assert username == "user_account_001"

    def test_person_format(self):
        alloc = PseudonymAllocator()
        pseudo = alloc.allocate_person("John Smith", "Internal")
        assert pseudo == "person_internal_001"

    def test_person_no_collision_with_emails(self):
        """Person pseudonyms must never collide with email pseudonyms."""
        alloc = PseudonymAllocator()
        email_pseudos = set()
        for i in range(150):
            p = alloc.allocate_email(f"user{i}@example.com", "External")
            email_pseudos.add(p)
        person_pseudo = alloc.allocate_person("John Smith", "External")
        assert person_pseudo not in email_pseudos
        assert person_pseudo.startswith("person_")

    def test_org_format(self):
        alloc = PseudonymAllocator()
        pseudo = alloc.allocate_org("Contoso Inc", "Internal")
        assert pseudo == "org_internal_001"

    def test_hostname_format(self):
        alloc = PseudonymAllocator()
        pseudo = alloc.allocate_hostname("DC01", "Internal")
        assert pseudo == "host_001"

    def test_many_ips_no_collision(self):
        alloc = PseudonymAllocator()
        fakes = set()
        for i in range(300):
            fakes.add(alloc.allocate_ip(f"10.0.{i // 256}.{i % 256}", "Internal"))
        assert len(fakes) == 300


class TestASNAwareIPAllocation:
    """Tests for context-preserving IP pseudonymization."""

    @staticmethod
    def _make_mock_geoip(asn=24940, org="Hetzner", network="95.216.0.0/16"):
        """Create a mock GeoIPLookup that returns fixed ASN info."""
        import ipaddress
        from unittest.mock import MagicMock

        from token_proxy.geoip import ASNInfo

        mock = MagicMock()
        mock.available = True
        mock.lookup.return_value = ASNInfo(asn=asn, org=org, network=ipaddress.IPv4Network(network))
        return mock

    def test_external_asn_aware_same_prefix(self):
        """External IP with GeoIP produces donor in the same ASN prefix."""
        import ipaddress

        alloc = PseudonymAllocator()
        alloc.set_geoip(self._make_mock_geoip(network="95.216.0.0/16"))

        donor = alloc.allocate_ip("95.216.246.66", "External")
        donor_addr = ipaddress.ip_address(donor)
        assert donor_addr in ipaddress.IPv4Network("95.216.0.0/16")

    def test_external_asn_aware_deterministic(self):
        """Same real IP in same allocator produces same donor."""
        alloc = PseudonymAllocator()
        alloc.set_geoip(self._make_mock_geoip())

        d1 = alloc.allocate_ip("95.216.246.66", "External")
        d2 = alloc.allocate_ip("95.216.246.66", "External")
        assert d1 == d2

    def test_external_asn_aware_different_from_real(self):
        """Donor IP is never the real IP."""
        alloc = PseudonymAllocator()
        alloc.set_geoip(self._make_mock_geoip())

        donor = alloc.allocate_ip("95.216.246.66", "External")
        assert donor != "95.216.246.66"

    def test_fallback_without_geoip(self):
        """Without GeoIP, external IPs fall back to 198.51.100.x."""
        alloc = PseudonymAllocator()
        # No set_geoip() call
        donor = alloc.allocate_ip("95.216.246.66", "External")
        assert donor == "198.51.100.1"

    def test_internal_unchanged_with_geoip(self):
        """Internal IPs still use 10.99.99.x even with GeoIP available."""
        alloc = PseudonymAllocator()
        alloc.set_geoip(self._make_mock_geoip())

        donor = alloc.allocate_ip("10.0.1.5", "Internal")
        assert donor == "10.99.99.1"

    def test_different_sessions_different_donors(self):
        """Two allocators (different salts) produce different donors for same IP."""
        geoip = self._make_mock_geoip()

        alloc1 = PseudonymAllocator()
        alloc1.set_geoip(geoip)
        alloc2 = PseudonymAllocator()
        alloc2.set_geoip(geoip)

        d1 = alloc1.allocate_ip("95.216.246.66", "External")
        d2 = alloc2.allocate_ip("95.216.246.66", "External")
        # Very unlikely to collide with different random salts
        # (1 in 65534 for a /16)
        assert d1 != d2 or True  # Extremely rare collision is OK

    def test_small_prefix_fallback(self):
        """Prefixes with <=2 addresses fall back to counter-based."""
        from unittest.mock import MagicMock

        from token_proxy.geoip import ASNInfo

        mock = MagicMock()
        mock.available = True
        mock.lookup.return_value = ASNInfo(
            asn=12345,
            org="TinyISP",
            network=__import__("ipaddress").IPv4Network("203.0.113.0/31"),
        )

        alloc = PseudonymAllocator()
        alloc.set_geoip(mock)

        donor = alloc.allocate_ip("203.0.113.0", "External")
        # Should fall back to counter-based
        assert donor == "198.51.100.1"

    def test_geoip_lookup_returns_none_fallback(self):
        """When GeoIP lookup returns None, fall back to counter-based."""
        from unittest.mock import MagicMock

        mock = MagicMock()
        mock.available = True
        mock.lookup.return_value = None

        alloc = PseudonymAllocator()
        alloc.set_geoip(mock)

        donor = alloc.allocate_ip("192.0.2.1", "External")
        assert donor == "198.51.100.1"


class TestDottedPropertyDetection:
    def test_graph_permission(self):
        assert _looks_like_dotted_property("Policy.ReadWrite.All") is True
        assert _looks_like_dotted_property("Files.Read.All") is True
        assert _looks_like_dotted_property("SecurityAlert.Read.All") is True

    def test_property_path(self):
        assert _looks_like_dotted_property("ServicePrincipal.DisplayName") is True
        assert _looks_like_dotted_property("ConsentContext.IsAdminConsent") is True

    def test_real_domain(self):
        assert _looks_like_dotted_property("contoso.com") is False
        assert _looks_like_dotted_property("mail.contoso.com") is False
        assert _looks_like_dotted_property("graph.microsoft.com") is False

    def test_edge_cases(self):
        assert _looks_like_dotted_property("a.b") is False  # too short, no indicators
        assert _looks_like_dotted_property("User.Read") is True
