"""Optional MaxMind GeoLite2-ASN database wrapper for context-preserving IP pseudonymization."""

from __future__ import annotations

import ipaddress
import logging
import os
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = Path("/app/data/GeoLite2-ASN.mmdb")


@dataclass(frozen=True)
class ASNInfo:
    """ASN lookup result."""

    asn: int  # e.g., 24940
    org: str  # e.g., "Hetzner Online GmbH"
    network: ipaddress.IPv4Network | ipaddress.IPv6Network  # e.g., 95.216.0.0/16


class GeoIPLookup:
    """Optional MaxMind GeoLite2-ASN database wrapper.

    If the database file is not found, all lookups return None.
    Thread-safe for concurrent reads.
    """

    def __init__(self, db_path: str | Path | None = None):
        self._reader = None

        path = self._resolve_path(db_path)
        if path and path.exists():
            try:
                import maxminddb

                self._reader = maxminddb.open_database(str(path))
                logger.info("GeoIP ASN database loaded from %s", path)
            except ImportError:
                logger.warning("maxminddb not installed — GeoIP lookups disabled")
            except Exception:
                logger.warning("Failed to open GeoIP database at %s", path, exc_info=True)
        else:
            logger.info("GeoIP ASN database not found — using fallback IP pseudonymization")

    @staticmethod
    def _resolve_path(db_path: str | Path | None) -> Path | None:
        """Resolve database path from argument, env var, or default."""
        if db_path:
            return Path(db_path)
        env_path = os.environ.get("GEOIP_ASN_DB_PATH")
        if env_path:
            return Path(env_path)
        return DEFAULT_DB_PATH

    @property
    def available(self) -> bool:
        """Check if the GeoIP database is loaded and ready."""
        return self._reader is not None

    def lookup(self, ip_str: str) -> ASNInfo | None:
        """Look up ASN info for an IP address.

        Returns None if the database is unavailable or the IP is not found.
        """
        if self._reader is None:
            return None

        try:
            result, prefix_len = self._reader.get_with_prefix_len(ip_str)
            if result is None:
                return None

            asn = result.get("autonomous_system_number")
            org = result.get("autonomous_system_organization", "Unknown")

            if asn is None:
                return None

            # Construct the network from the IP and prefix length
            addr = ipaddress.ip_address(ip_str)
            network = ipaddress.ip_network(f"{addr}/{prefix_len}", strict=False)
            return ASNInfo(asn=asn, org=org, network=network)
        except Exception:
            logger.debug("GeoIP lookup failed for %s", ip_str, exc_info=True)
            return None

    def close(self) -> None:
        """Close the database reader."""
        if self._reader is not None:
            self._reader.close()
            self._reader = None
