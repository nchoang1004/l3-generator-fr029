"""Structured pseudonym generation for PII replacement.

Generates syntactically valid pseudonyms like user_account_001@proxy-safe.local
instead of fake human names or bracket tags. Counter-based — never exhausts.
"""

from __future__ import annotations

import hashlib
import hmac
import ipaddress
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from token_proxy.geoip import ASNInfo, GeoIPLookup

# ------------------------------------------------------------------
# File extension blocklist — skip domain matches ending in these
# ------------------------------------------------------------------

FILE_EXTENSION_BLOCKLIST = frozenset(
    {
        ".md",
        ".json",
        ".yaml",
        ".yml",
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".txt",
        ".csv",
        ".log",
        ".xml",
        ".html",
        ".css",
        ".sh",
        ".toml",
        ".cfg",
        ".ini",
        ".exe",
        ".dll",
        ".zip",
        ".tar",
        ".gz",
        ".bz2",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".svg",
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".kql",
        ".kusto",
        ".sql",
        ".env",
        ".lock",
        ".bak",
        ".tmp",
        ".pyc",
    }
)

# ------------------------------------------------------------------
# Compound TLDs (treated as single TLD for base domain extraction)
# ------------------------------------------------------------------

COMPOUND_TLDS = frozenset(
    {
        "onmicrosoft.com",
        "co.uk",
        "co.jp",
        "co.nz",
        "co.za",
        "com.au",
        "com.br",
        "org.uk",
        "net.au",
        "ac.uk",
        "mail.onmicrosoft.com",
    }
)

# ------------------------------------------------------------------
# Dotted property / permission scope skiplist
# Patterns like "Policy.ReadWrite.All", "ServicePrincipal.Name",
# "ConsentContext.IsAdminConsent" — these are NOT domains.
# ------------------------------------------------------------------

DOTTED_PROPERTY_INDICATORS = frozenset(
    {
        "read",
        "write",
        "readwrite",
        "all",
        "basic",
        "scope",
        "type",
        "name",
        "displayname",
        "objectid",
        "appid",
        "tags",
        "directory",
        "grant",
        "consent",
        "action",
        "context",
        "permissions",
        "configuration",
        "settings",
        "monitoring",
        "id",
        "value",
        "datetime",
        "created",
        "modified",
        "last",
        "assignment",
        "role",
        "principal",
        "target",
        "resource",
        "enabled",
        "disabled",
        "status",
        "count",
        "result",
        "property",
        "properties",
        "nickname",
        "mail",
        "upn",
        "userprincipalname",
        "app",
        "user",
        "displayname",
        "operationalinsights",
        "securityinsights",
        "softwareoath",
        "authmethod",
        "proofup",
        "registration",
        "endpoint",
        "correlationids",
        "initiatedby",
        # Graph permission verbs
        "create",
        "delete",
        "edit",
        "send",
        "manage",
        "export",
        "import",
        "importexport",
        "upload",
        "submit",
        "evaluate",
        "process",
        "migrate",
        "migration",
        "activate",
        "initiate",
        "invite",
        "receive",
        "ingest",
        "sign",
        "start",
        "remove",
        "archive",
        "compute",
        "command",
        "join",
        "access",
        "fullcontrol",
        "selected",
        "shared",
        "hidden",
        "ownedby",
        "payload",
    }
)


def _looks_like_dotted_property(value: str) -> bool:
    """Return True if value looks like a dotted property path, not a domain.

    Examples that should return True:
      Policy.ReadWrite.ConditionalAccess
      ServicePrincipal.DisplayName
      ConsentContext.IsAdminConsent
      Files.Read.All
    """
    parts = value.split(".")
    if len(parts) < 2:
        return False
    # If any part starts with uppercase and uses PascalCase → likely a property
    has_pascal = any(p[0].isupper() and len(p) > 1 and not p.isupper() for p in parts if p)
    # If any part contains a known property indicator as substring
    has_indicator = any(
        indicator in p.lower() for p in parts for indicator in DOTTED_PROPERTY_INDICATORS
    )
    return has_pascal and has_indicator


# ------------------------------------------------------------------
# Pseudonym format constants
# ------------------------------------------------------------------

EMAIL_PREFIX = "user_account"

DOMAIN_FORMATS = {
    "Internal": "domain-internal-{nnn}.com",
    "External": "domain-external-{nnn}.net",
    "Partner": "domain-partner-{nnn}.org",
}

IP_FORMATS = {
    "Internal": "10.99.99.{n}",
    "External": "198.51.100.{n}",
    "Partner": "203.0.113.{n}",
}

PERSON_FORMATS = {
    "Internal": "person_internal_{nnn}",
    "External": "person_external_{nnn}",
    "Partner": "person_partner_{nnn}",
}

ORG_FORMATS = {
    "Internal": "org_internal_{nnn}",
    "External": "org_external_{nnn}",
    "Partner": "org_partner_{nnn}",
}


def _nnn(n: int) -> str:
    """Zero-pad counter to at least 3 digits."""
    return str(n).zfill(3)


# ------------------------------------------------------------------
# PseudonymAllocator
# ------------------------------------------------------------------


class PseudonymAllocator:
    """Allocates structured pseudonyms with domain-email-username consistency."""

    def __init__(self) -> None:
        # Counters per entity type
        self._email_counter: int = 0
        self._domain_counters: dict[str, int] = {}  # context → counter
        self._ip_counters: dict[str, int] = {}  # context → counter
        self._person_counter: int = 0
        self._org_counters: dict[str, int] = {}  # context → counter
        self._hostname_counter: int = 0

        # Consistency maps
        self._real_base_domain_to_nnn: dict[str, tuple[int, str]] = {}  # domain → (nnn, context)
        self._email_local_to_nnn: dict[str, int] = {}  # email local part → email NNN

        # ASN-aware IP pseudonymization
        self._session_salt: bytes = os.urandom(16)
        self._geoip: GeoIPLookup | None = None
        self._ip_donor_cache: dict[str, str] = {}  # real_ip → donor_ip

    def set_geoip(self, geoip: GeoIPLookup) -> None:
        """Inject a GeoIP lookup instance for ASN-aware IP pseudonymization."""
        self._geoip = geoip

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def allocate_email(self, real_email: str, context: str, keep_domain: bool = False) -> str:
        """Generate a pseudonym email. Also tracks local part for username consistency.

        If keep_domain is True, the real domain is preserved (e.g., user_account_001@contoso.com).
        """
        self._email_counter += 1
        nnn = self._email_counter

        # Track local part → NNN for bare username consistency
        local = real_email.rsplit("@", 1)[0]
        self._email_local_to_nnn[local.lower()] = nnn

        domain = real_email.rsplit("@", 1)[-1]

        if keep_domain:
            return f"{EMAIL_PREFIX}_{_nnn(nnn)}@{domain}"

        # Ensure domain is mapped and use the pseudonymized domain in the email
        domain_nnn, domain_context = self._ensure_domain_mapped(domain.lower(), context)
        fmt = DOMAIN_FORMATS.get(domain_context, DOMAIN_FORMATS["External"])
        pseudo_domain = fmt.format(nnn=_nnn(domain_nnn))
        return f"{EMAIL_PREFIX}_{_nnn(nnn)}@{pseudo_domain}"

    def allocate_domain(self, real_domain: str, context: str) -> str:
        """Generate a pseudonym domain. Preserves subdomains."""
        lower = real_domain.lower()
        base = self._get_base_domain(lower)
        prefix = lower[: -len(base)] if lower != base else ""

        nnn, mapped_context = self._ensure_domain_mapped(base, context)
        fmt = DOMAIN_FORMATS.get(mapped_context, DOMAIN_FORMATS["External"])
        fake_base = fmt.format(nnn=_nnn(nnn))
        return f"{prefix}{fake_base}"

    def allocate_ip(self, real_ip: str, context: str) -> str:
        """Generate a pseudonym IP.

        For external IPs with a GeoIP database available, picks a donor IP
        from the same ASN prefix (preserving hosting provider / geo context).
        Falls back to documentation-range IPs (198.51.100.x) otherwise.
        Internal IPs always use 10.99.99.x.
        """
        # Session-level determinism: same real IP → same donor
        if real_ip in self._ip_donor_cache:
            return self._ip_donor_cache[real_ip]

        # Internal IPs: use reserved range (no ASN context to preserve)
        if context == "Internal":
            result = self._allocate_ip_counter(real_ip, context)
            self._ip_donor_cache[real_ip] = result
            return result

        # External IPs: try ASN-aware allocation
        if self._geoip and self._geoip.available:
            info = self._geoip.lookup(real_ip)
            if info and info.network.num_addresses > 2:
                result = self._pick_donor_ip(real_ip, info)
                self._ip_donor_cache[real_ip] = result
                return result

        # Fallback: counter-based documentation range
        result = self._allocate_ip_counter(real_ip, context)
        self._ip_donor_cache[real_ip] = result
        return result

    def _allocate_ip_counter(self, real_ip: str, context: str) -> str:
        """Counter-based IP allocation (original fallback behavior)."""
        if context not in self._ip_counters:
            self._ip_counters[context] = 0
        self._ip_counters[context] += 1
        n = self._ip_counters[context]

        fmt = IP_FORMATS.get(context, IP_FORMATS["External"])
        if context == "Internal" and n > 254:
            third = 99 + (n - 1) // 254
            fourth = (n - 1) % 254 + 1
            return f"10.99.{third}.{fourth}"
        return fmt.format(n=n)

    def _pick_donor_ip(self, real_ip: str, info: ASNInfo) -> str:
        """Pick a deterministic donor IP from the same ASN prefix."""

        real_addr = ipaddress.ip_address(real_ip)
        net = info.network
        usable = net.num_addresses - 2  # exclude network + broadcast

        # /31 and /32 networks are too small for donor selection
        if usable < 2:
            return self._allocate_ip_counter(real_ip, "External")

        # Deterministic offset via HMAC
        digest = hmac.new(self._session_salt, real_addr.packed, hashlib.sha256).digest()
        offset = int.from_bytes(digest[:4], "big") % usable + 1  # skip network addr

        candidate = net.network_address + offset
        # Ensure donor != real
        if candidate == real_addr:
            offset = (offset % usable) + 1
            candidate = net.network_address + offset
        if candidate == real_addr:
            candidate = net.network_address + 1

        return str(candidate)

    def allocate_person(self, real_name: str, context: str) -> str:
        """Generate a pseudonym for a person name.

        Uses a dedicated person_* prefix to avoid collision with the email
        counter namespace (user_account_*).
        """
        # Check if this person's name matches a known email local part
        lower = real_name.lower().replace(" ", ".").replace("_", ".")
        if lower in self._email_local_to_nnn:
            return f"{EMAIL_PREFIX}_{_nnn(self._email_local_to_nnn[lower])}"

        self._person_counter += 1
        fmt = PERSON_FORMATS.get(context, PERSON_FORMATS["External"])
        return fmt.format(nnn=_nnn(self._person_counter))

    def allocate_org(self, real_org: str, context: str) -> str:
        """Generate a pseudonym for an organization name."""
        if context not in self._org_counters:
            self._org_counters[context] = 0
        self._org_counters[context] += 1
        fmt = ORG_FORMATS.get(context, ORG_FORMATS["External"])
        return fmt.format(nnn=_nnn(self._org_counters[context]))

    def allocate_hostname(self, real_hostname: str, context: str) -> str:
        """Generate a pseudonym for a hostname.

        Preserves domain suffix if the original has one
        (e.g., DC01.contoso.com → host_001.contoso.com).
        Bare hostnames (e.g., DC01) stay bare (host_001).
        """
        self._hostname_counter += 1
        prefix = f"host_{_nnn(self._hostname_counter)}"
        # Preserve domain suffix if present
        dot = real_hostname.find(".")
        if dot >= 0:
            suffix = real_hostname[dot:]
            return f"{prefix}{suffix}"
        return prefix

    def allocate_username(self, real_username: str, context: str) -> str:
        """Generate a pseudonym for a bare username.

        If the username matches a known email local part, reuses the same NNN.
        """
        lower = real_username.lower()
        if lower in self._email_local_to_nnn:
            return f"{EMAIL_PREFIX}_{_nnn(self._email_local_to_nnn[lower])}"
        # Unknown username — allocate fresh
        self._email_counter += 1
        self._email_local_to_nnn[lower] = self._email_counter
        return f"{EMAIL_PREFIX}_{_nnn(self._email_counter)}"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_domain_mapped(self, base_domain: str, context: str) -> tuple[int, str]:
        """Get or create a NNN mapping for a base domain. Returns (nnn, context)."""
        if base_domain in self._real_base_domain_to_nnn:
            return self._real_base_domain_to_nnn[base_domain]

        if context not in self._domain_counters:
            self._domain_counters[context] = 0
        self._domain_counters[context] += 1
        nnn = self._domain_counters[context]

        self._real_base_domain_to_nnn[base_domain] = (nnn, context)
        return nnn, context

    def _get_base_domain(self, domain: str) -> str:
        """Extract base domain, respecting compound TLDs."""
        for tld in sorted(COMPOUND_TLDS, key=len, reverse=True):
            if domain.endswith("." + tld):
                parts_before = domain[: -(len(tld) + 1)]
                last_label = parts_before.rsplit(".", 1)[-1]
                return f"{last_label}.{tld}"
            if domain == tld:
                return domain

        parts = domain.rsplit(".", 2)
        if len(parts) >= 2:
            return f"{parts[-2]}.{parts[-1]}"
        return domain
