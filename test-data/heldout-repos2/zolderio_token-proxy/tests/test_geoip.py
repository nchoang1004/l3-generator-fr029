"""Tests for the GeoIP lookup module."""

from __future__ import annotations

import ipaddress
from unittest.mock import MagicMock

from token_proxy.geoip import ASNInfo, GeoIPLookup


class TestGeoIPLookup:
    def test_unavailable_when_no_database(self, tmp_path):
        geoip = GeoIPLookup(db_path=tmp_path / "nonexistent.mmdb")
        assert geoip.available is False

    def test_lookup_returns_none_when_unavailable(self, tmp_path):
        geoip = GeoIPLookup(db_path=tmp_path / "nonexistent.mmdb")
        assert geoip.lookup("8.8.8.8") is None

    def test_lookup_with_mock_reader(self):
        mock_reader = MagicMock()
        mock_reader.get_with_prefix_len.return_value = (
            {
                "autonomous_system_number": 24940,
                "autonomous_system_organization": "Hetzner Online GmbH",
            },
            16,
        )

        geoip = GeoIPLookup(db_path="/nonexistent")  # won't load
        # Manually inject the mock reader
        geoip._reader = mock_reader

        assert geoip.available is True
        info = geoip.lookup("95.216.246.66")
        assert info is not None
        assert info.asn == 24940
        assert info.org == "Hetzner Online GmbH"
        assert info.network == ipaddress.IPv4Network("95.216.0.0/16")

    def test_lookup_returns_none_for_unknown_ip(self):
        mock_reader = MagicMock()
        mock_reader.get_with_prefix_len.return_value = (None, 0)

        geoip = GeoIPLookup(db_path="/nonexistent")
        geoip._reader = mock_reader

        assert geoip.lookup("192.0.2.1") is None

    def test_lookup_returns_none_on_missing_asn(self):
        mock_reader = MagicMock()
        mock_reader.get_with_prefix_len.return_value = (
            {
                "autonomous_system_organization": "Unknown",
                # Missing autonomous_system_number
            },
            8,
        )

        geoip = GeoIPLookup(db_path="/nonexistent")
        geoip._reader = mock_reader

        assert geoip.lookup("10.0.0.1") is None

    def test_close(self):
        mock_reader = MagicMock()
        geoip = GeoIPLookup(db_path="/nonexistent")
        geoip._reader = mock_reader

        geoip.close()
        mock_reader.close.assert_called_once()
        assert geoip.available is False


class TestASNInfo:
    def test_frozen(self):
        info = ASNInfo(asn=15169, org="Google LLC", network=ipaddress.IPv4Network("8.8.8.0/24"))
        assert info.asn == 15169
        assert info.org == "Google LLC"
