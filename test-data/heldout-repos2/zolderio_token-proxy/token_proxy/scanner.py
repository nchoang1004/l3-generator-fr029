"""PII detection and bidirectional pseudonym replacement.

Three-pass redaction pipeline:
  Pass 1: Regex — emails, IPs, domains, known hostnames/persons/orgs
  Pass 2: NER — person and org names not caught by regex
  Pass 3: Username extraction — bare local parts from known emails
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from token_proxy.context import ContextEngine
from token_proxy.pseudonyms import FILE_EXTENSION_BLOCKLIST, _looks_like_dotted_property
from token_proxy.session_store import SessionMapping

if TYPE_CHECKING:
    from token_proxy.providers.base import ProviderAdapter

# ------------------------------------------------------------------
# Regex patterns
# ------------------------------------------------------------------

PATTERNS: dict[str, re.Pattern[str]] = {
    "email": re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"),
    "ip": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|1?\d\d?)\b"),
    "domain": re.compile(
        r"\b(?!(?:\d{1,3}\.){3}\d{1,3}\b)"
        r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b"
    ),
}

# ------------------------------------------------------------------
# Module-level state (initialized via init_scanner)
# ------------------------------------------------------------------

_known_persons_re: re.Pattern[str] | None = None
_known_orgs_re: re.Pattern[str] | None = None
_known_hostnames_re: re.Pattern[str] | None = None
_ner_enabled: bool = False
_redaction_enabled: bool = True
_pseudonymize_domains: bool = True

# Domains that should never be pseudonymized (reference sites, not customer PII)
# Loaded from config at startup. Recommended values in config.json.example.
DOMAIN_ALLOWLIST: set[str] = set()


def set_redaction_enabled(enabled: bool) -> None:
    """Toggle redaction on or off at runtime."""
    global _redaction_enabled
    _redaction_enabled = enabled


def is_redaction_enabled() -> bool:
    """Return the current redaction state."""
    return _redaction_enabled


def set_pseudonymize_domains(enabled: bool) -> None:
    """Toggle domain pseudonymization on or off."""
    global _pseudonymize_domains
    _pseudonymize_domains = enabled


def is_pseudonymize_domains() -> bool:
    """Return whether domains are being pseudonymized."""
    return _pseudonymize_domains


def add_to_domain_allowlist(domains: list[str]) -> None:
    """Add domains to the allowlist at runtime."""
    DOMAIN_ALLOWLIST.update(d.lower() for d in domains)


def remove_from_domain_allowlist(domains: list[str]) -> None:
    """Remove domains from the allowlist at runtime."""
    DOMAIN_ALLOWLIST.difference_update(d.lower() for d in domains)


def init_scanner(config: dict) -> None:
    """Compile known-entity regex patterns from config. Call once at startup.

    Builds regex objects locally first, then assigns to globals in single
    statements so concurrent readers always see a complete (old or new) regex.
    """
    global _known_persons_re, _known_orgs_re, _known_hostnames_re
    global _ner_enabled, _redaction_enabled, _pseudonymize_domains

    _ner_enabled = config.get("ner_enabled", True)
    _redaction_enabled = config.get("redaction_enabled", True)
    _pseudonymize_domains = config.get("pseudonymize_domains", True)

    # Load domain allowlist from config
    DOMAIN_ALLOWLIST.clear()
    DOMAIN_ALLOWLIST.update(d.lower() for d in config.get("domain_allowlist", []))

    new_persons_re: re.Pattern[str] | None = None
    persons = config.get("known_persons", [])
    if persons:
        escaped = [re.escape(p) for p in persons]
        new_persons_re = re.compile(r"\b(" + "|".join(escaped) + r")\b", re.IGNORECASE)

    new_orgs_re: re.Pattern[str] | None = None
    orgs = config.get("known_orgs", [])
    if orgs:
        escaped = [re.escape(o) for o in orgs]
        new_orgs_re = re.compile(r"\b(" + "|".join(escaped) + r")\b", re.IGNORECASE)

    new_hostnames_re: re.Pattern[str] | None = None
    hostnames = config.get("known_hostnames", [])
    if hostnames:
        escaped = [re.escape(h) for h in hostnames]
        new_hostnames_re = re.compile(r"\b(" + "|".join(escaped) + r")\b", re.IGNORECASE)

    # Atomic swap — Python's GIL makes single-attribute assignment atomic
    _known_persons_re = new_persons_re
    _known_orgs_re = new_orgs_re
    _known_hostnames_re = new_hostnames_re


# ------------------------------------------------------------------
# Text-level redaction / restoration
# ------------------------------------------------------------------


def redact_text(
    text: str, session: SessionMapping, ctx: ContextEngine
) -> tuple[str, dict[str, int]]:
    """Replace PII in *text* with structured pseudonyms (three-pass pipeline).

    Returns (redacted_text, counts_by_type).
    """
    if not _redaction_enabled:
        return text, {}

    counts: dict[str, int] = {}

    # ── Pass 1: Regex ──────────────────────────────────────────────

    # 1a. Emails (must come first — contain domain)
    for m in list(PATTERNS["email"].finditer(text)):
        val = m.group()
        context = ctx.classify_email(val)
        pseudo = session.get_or_create_tag(val, "Email", context)
        text = text.replace(val, pseudo)
        counts["Email"] = counts.get("Email", 0) + 1

    # 1b. IPs (skip internal/private — no value in hiding them from the LLM)
    for m in list(PATTERNS["ip"].finditer(text)):
        val = m.group()
        if val in session.tag_to_real:
            continue
        context = ctx.classify_ip(val)
        if context == "Internal":
            continue
        pseudo = session.get_or_create_tag(val, "IP", context)
        text = text.replace(val, pseudo)
        counts["IP"] = counts.get("IP", 0) + 1

    # 1c. Domains (skip entirely when domain pseudonymization is disabled)
    if _pseudonymize_domains:
        for m in list(PATTERNS["domain"].finditer(text)):
            val = m.group()
            lower = val.lower()
            # Skip file extensions
            dot_pos = lower.rfind(".")
            if dot_pos >= 0 and lower[dot_pos:] in FILE_EXTENSION_BLOCKLIST:
                continue
            # Skip already-known pseudonyms
            if val in session.tag_to_real:
                continue
            # Skip reference/security domains (mitre.org, learn.microsoft.com, etc.)
            if lower in DOMAIN_ALLOWLIST:
                continue
            # Skip dotted property paths (Policy.ReadWrite.All, etc.)
            if _looks_like_dotted_property(val):
                continue
            context = ctx.classify_domain(val)
            pseudo = session.get_or_create_tag(val, "Domain", context)
            text = text.replace(val, pseudo)
            counts["Domain"] = counts.get("Domain", 0) + 1

    # 1d. Known hostnames (config-driven)
    if _known_hostnames_re:
        for m in list(_known_hostnames_re.finditer(text)):
            val = m.group()
            if val.lower() in session._real_lower_to_key:
                continue
            context = ctx.classify_hostname(val)
            pseudo = session.get_or_create_tag(val, "Hostname", context)
            text = text.replace(val, pseudo)
            counts["Hostname"] = counts.get("Hostname", 0) + 1

    # 1e. Known persons (config-driven)
    if _known_persons_re:
        for m in list(_known_persons_re.finditer(text)):
            val = m.group()
            if val.lower() in session._real_lower_to_key:
                continue
            context = ctx.classify_person(val)
            pseudo = session.get_or_create_tag(val, "Person", context)
            text = text.replace(val, pseudo)
            counts["Person"] = counts.get("Person", 0) + 1

    # 1f. Known orgs (config-driven)
    if _known_orgs_re:
        for m in list(_known_orgs_re.finditer(text)):
            val = m.group()
            if val.lower() in session._real_lower_to_key:
                continue
            context = ctx.classify_org(val)
            pseudo = session.get_or_create_tag(val, "Org", context)
            text = text.replace(val, pseudo)
            counts["Org"] = counts.get("Org", 0) + 1

    # ── Pass 2: NER ────────────────────────────────────────────────

    if _ner_enabled:
        from token_proxy.ner import extract_entities, is_available

        if is_available():
            for entity_text, entity_type in extract_entities(text):
                # Skip if already pseudonymized
                if entity_text.lower() in session._real_lower_to_key:
                    continue
                if entity_text in session.tag_to_real:
                    continue

                if entity_type == "Person":
                    context = ctx.classify_person(entity_text)
                else:
                    context = ctx.classify_org(entity_text)

                pseudo = session.get_or_create_tag(entity_text, entity_type, context)
                text = text.replace(entity_text, pseudo)
                counts[entity_type] = counts.get(entity_type, 0) + 1

    # ── Pass 3: Bare username extraction ───────────────────────────

    # For each email local part known to the session, check if it appears
    # standalone in the text. This catches "j.smith" used without "@contoso.com".
    for real_val, pseudo_val in list(session.real_to_tag.items()):
        if session.fake_to_type.get(pseudo_val) != "Email":
            continue
        real_local = real_val.rsplit("@", 1)[0]
        if len(real_local) < 3:
            continue
        # Build word-boundary pattern for the local part
        pattern = re.compile(r"\b" + re.escape(real_local) + r"\b", re.IGNORECASE)
        if pattern.search(text):
            # Get the pseudo local part (already registered by email allocation)
            pseudo_local = session.real_to_tag.get(real_local)
            if pseudo_local and pseudo_local not in text:
                # Only replace if the pseudo isn't already present (avoid double-replace)
                text = pattern.sub(pseudo_local, text)
                counts["Username"] = counts.get("Username", 0) + 1

    return text, counts


def restore_text(text: str, session: SessionMapping) -> str:
    """Replace all known pseudonyms in *text* with original values.

    Sorts replacements by descending length to prevent partial matches.
    """
    for pseudo, real in sorted(session.tag_to_real.items(), key=lambda x: -len(x[0])):
        text = text.replace(pseudo, real)
    return text


# ------------------------------------------------------------------
# JSON-structure walkers (provider-generic via adapter)
# ------------------------------------------------------------------


def redact_request(
    body: dict,
    session: SessionMapping,
    ctx: ContextEngine,
    adapter: ProviderAdapter | None = None,
) -> dict[str, int]:
    """Redact PII in an LLM API request body *in-place*.

    Uses the provider adapter to locate redactable text fields.
    Falls back to Anthropic format if no adapter is provided.
    """
    if adapter is None:
        from token_proxy.providers.anthropic import AnthropicAdapter

        adapter = AnthropicAdapter()

    totals: dict[str, int] = {}
    for ref in adapter.extract_texts(body):
        text = ref.get()
        redacted, counts = redact_text(text, session, ctx)
        if redacted != text:
            ref.set(redacted)
        _merge(totals, counts)
    return totals


def restore_response(
    body: dict,
    session: SessionMapping,
    adapter: ProviderAdapter | None = None,
) -> None:
    """Restore pseudonyms → real values in an LLM API response *in-place*.

    Uses the provider adapter to locate restorable text fields.
    Falls back to Anthropic format if no adapter is provided.
    """
    if adapter is None:
        from token_proxy.providers.anthropic import AnthropicAdapter

        adapter = AnthropicAdapter()

    for ref in adapter.extract_texts_response(body):
        text = ref.get()
        restored = restore_text(text, session)
        if restored != text:
            ref.set(restored)


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------


def _restore_recursive(obj: Any, session: SessionMapping) -> Any:
    if isinstance(obj, str):
        return restore_text(obj, session)
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = _restore_recursive(v, session)
        return obj
    if isinstance(obj, list):
        return [_restore_recursive(item, session) for item in obj]
    return obj


def _merge(totals: dict[str, int], counts: dict[str, int]) -> None:
    for k, v in counts.items():
        totals[k] = totals.get(k, 0) + v
