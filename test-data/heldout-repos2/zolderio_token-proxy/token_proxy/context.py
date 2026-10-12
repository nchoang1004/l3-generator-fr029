"""Context engine — classify detected entities as Internal / External / Partner."""

from __future__ import annotations

import ipaddress
import logging

logger = logging.getLogger(__name__)


class ContextEngine:
    """Uses a static config to determine entity context."""

    def __init__(self, config: dict) -> None:
        self.internal_domains: set[str] = set(config.get("internal_domains", []))
        self.partner_domains: set[str] = set(config.get("partner_domains", []))
        self.internal_ranges: list[ipaddress.IPv4Network | ipaddress.IPv6Network] = [
            ipaddress.ip_network(r, strict=False) for r in config.get("internal_ip_ranges", [])
        ]
        self.known_persons: set[str] = {p.lower() for p in config.get("known_persons", [])}
        self.known_orgs: set[str] = {o.lower() for o in config.get("known_orgs", [])}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify_ip(self, ip_str: str) -> str:
        try:
            addr = ipaddress.ip_address(ip_str)
        except ValueError:
            return "External"

        for net in self.internal_ranges:
            if addr in net:
                return "Internal"
        if addr.is_private:
            return "Internal"
        return "External"

    def classify_email(self, email: str) -> str:
        domain = email.rsplit("@", 1)[-1].lower()
        return self._classify_domain(domain)

    def classify_domain(self, domain: str) -> str:
        return self._classify_domain(domain.lower())

    def classify_person(self, name: str) -> str:
        """Persons default to Internal (conservative assumption)."""
        return "Internal"

    def classify_org(self, org: str) -> str:
        """Check if org matches any known internal/partner domain hints."""
        lower = org.lower()
        for d in self.internal_domains:
            base = d.split(".")[0]
            if base and base in lower:
                return "Internal"
        for d in self.partner_domains:
            base = d.split(".")[0]
            if base and base in lower:
                return "Partner"
        return "External"

    def classify_hostname(self, hostname: str) -> str:
        """Hostnames default to Internal (short names are internal by convention)."""
        return "Internal"

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _classify_domain(self, domain: str) -> str:
        for d in self.internal_domains:
            if domain == d or domain.endswith("." + d):
                return "Internal"
        for d in self.partner_domains:
            if domain == d or domain.endswith("." + d):
                return "Partner"
        return "External"
