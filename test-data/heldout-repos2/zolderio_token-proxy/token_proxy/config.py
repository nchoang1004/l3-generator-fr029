"""Load and validate the Token proxy configuration."""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path("/app/config.json")

# Track the path used at load time so save_config can persist back to it
_active_config_path: Path = DEFAULT_CONFIG_PATH


def get_config_path() -> Path:
    """Return the config file path that was used at load time."""
    return _active_config_path


def _dedup_strip(values: list[str]) -> list[str]:
    """Strip whitespace and deduplicate (case-insensitive) preserving first occurrence."""
    seen: set[str] = set()
    result: list[str] = []
    for v in values:
        v = v.strip()
        key = v.lower()
        if key not in seen:
            seen.add(key)
            result.append(v)
    return result


def load_config(path: Path | str | None = None) -> dict:
    """Load config.json and return the parsed dict."""
    global _active_config_path
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    _active_config_path = config_path

    if not config_path.exists():
        logger.warning("Config file %s not found — using empty defaults", config_path)
        return _defaults()

    try:
        with open(config_path) as fh:
            data = json.load(fh)
    except json.JSONDecodeError:
        logger.warning("Config file %s is malformed JSON — using defaults", config_path)
        return _defaults()

    # Backward compat: old "ner_skiplist" key maps to "ner_tech_skiplist"
    tech_skiplist = data.get("ner_tech_skiplist", data.get("ner_skiplist", []))

    validated = {
        "internal_domains": [d.lower().strip() for d in data.get("internal_domains", [])],
        "partner_domains": [d.lower().strip() for d in data.get("partner_domains", [])],
        "internal_ip_ranges": [r.strip() for r in data.get("internal_ip_ranges", [])],
        "known_persons": _dedup_strip(data.get("known_persons", [])),
        "known_orgs": _dedup_strip(data.get("known_orgs", [])),
        "known_hostnames": _dedup_strip(data.get("known_hostnames", [])),
        "ner_enabled": data.get("ner_enabled", True),
        "ner_tech_skiplist": [s.lower().strip() for s in tech_skiplist],
        "ner_generic_it_words": [s.lower().strip() for s in data.get("ner_generic_it_words", [])],
        "domain_allowlist": [d.lower().strip() for d in data.get("domain_allowlist", [])],
        "redaction_enabled": data.get("redaction_enabled", True),
        "pseudonymize_domains": data.get("pseudonymize_domains", True),
        "geoip_asn_db_path": data.get("geoip_asn_db_path", None),
    }
    logger.info(
        "Loaded config: %d internal domains, %d partner domains, %d IP ranges, "
        "NER %s, %d known persons, %d known orgs, %d known hostnames, "
        "%d tech skiplist, %d generic IT words, %d domain allowlist",
        len(validated["internal_domains"]),
        len(validated["partner_domains"]),
        len(validated["internal_ip_ranges"]),
        "enabled" if validated["ner_enabled"] else "disabled",
        len(validated["known_persons"]),
        len(validated["known_orgs"]),
        len(validated["known_hostnames"]),
        len(validated["ner_tech_skiplist"]),
        len(validated["ner_generic_it_words"]),
        len(validated["domain_allowlist"]),
    )
    return validated


def save_config(config: dict, path: Path | str | None = None) -> None:
    """Persist the config dict back to disk (atomic write)."""
    target = Path(path) if path else _active_config_path
    tmp = target.with_suffix(".tmp")
    with open(tmp, "w") as fh:
        json.dump(config, fh, indent=2)
        fh.write("\n")
    tmp.replace(target)
    logger.info("Config saved to %s", target)


def _defaults() -> dict:
    return {
        "internal_domains": [],
        "partner_domains": [],
        "internal_ip_ranges": [],
        "known_persons": [],
        "known_orgs": [],
        "known_hostnames": [],
        "ner_enabled": True,
        "ner_tech_skiplist": [],
        "ner_generic_it_words": [],
        "domain_allowlist": [],
        "redaction_enabled": True,
        "pseudonymize_domains": True,
        "geoip_asn_db_path": None,
    }
