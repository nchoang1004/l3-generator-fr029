"""Runtime configuration API — manage whitelists and redaction toggle."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from token_proxy.config import get_config_path, save_config
from token_proxy.ner import (
    add_to_generic_it_words,
    add_to_skiplist,
    get_generic_it_words,
    get_skiplist,
    remove_from_generic_it_words,
    remove_from_skiplist,
)
from token_proxy.scanner import (
    DOMAIN_ALLOWLIST,
    add_to_domain_allowlist,
    init_scanner,
    is_pseudonymize_domains,
    is_redaction_enabled,
    remove_from_domain_allowlist,
    set_pseudonymize_domains,
    set_redaction_enabled,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/token-proxy/config", tags=["config"])

# ------------------------------------------------------------------
# Module-level reference to the live config dict (set by main.py)
# ------------------------------------------------------------------

_config: dict = {}

WHITELIST_CATEGORIES = {
    "ner_skiplist",
    "ner_generic_it_words",
    "domain_allowlist",
    "known_persons",
    "known_orgs",
    "known_hostnames",
}


def set_config_ref(config: dict) -> None:
    """Store a reference to the live config dict. Called once at startup."""
    global _config
    _config = config


# ------------------------------------------------------------------
# Pydantic models
# ------------------------------------------------------------------


class WhitelistRequest(BaseModel):
    category: str
    values: list[str]


class RedactionToggle(BaseModel):
    redaction_enabled: bool | None = None
    pseudonymize_domains: bool | None = None


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------


@router.get("")
async def get_config():
    """Return the full live config (whitelists + state)."""
    return {
        **_config,
        "redaction_enabled": is_redaction_enabled(),
        "domain_allowlist": sorted(DOMAIN_ALLOWLIST),
        "ner_tech_skiplist": sorted(get_skiplist()),
        "ner_generic_it_words": sorted(get_generic_it_words()),
    }


@router.get("/whitelist")
async def get_whitelists():
    """Return all whitelist entries grouped by category."""
    return {
        "ner_skiplist": sorted(get_skiplist()),
        "ner_generic_it_words": sorted(get_generic_it_words()),
        "domain_allowlist": sorted(DOMAIN_ALLOWLIST),
        "known_persons": _config.get("known_persons", []),
        "known_orgs": _config.get("known_orgs", []),
        "known_hostnames": _config.get("known_hostnames", []),
    }


@router.post("/whitelist")
async def add_to_whitelist(req: WhitelistRequest):
    """Add term(s) to a whitelist category."""
    if req.category not in WHITELIST_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown category '{req.category}'. Valid: {sorted(WHITELIST_CATEGORIES)}",
        )

    if req.category == "ner_skiplist":
        add_to_skiplist(req.values)
        existing = set(_config.get("ner_tech_skiplist", []))
        existing.update(v.lower() for v in req.values)
        _config["ner_tech_skiplist"] = sorted(existing)

    elif req.category == "ner_generic_it_words":
        add_to_generic_it_words(req.values)
        existing = set(_config.get("ner_generic_it_words", []))
        existing.update(v.lower() for v in req.values)
        _config["ner_generic_it_words"] = sorted(existing)

    elif req.category == "domain_allowlist":
        add_to_domain_allowlist(req.values)
        existing = set(_config.get("domain_allowlist", []))
        existing.update(v.lower() for v in req.values)
        _config["domain_allowlist"] = sorted(existing)

    elif req.category in ("known_persons", "known_orgs", "known_hostnames"):
        existing = {v.lower(): v for v in _config.get(req.category, [])}
        for v in req.values:
            v = v.strip()
            existing[v.lower()] = v  # dedup by case
        _config[req.category] = sorted(existing.values())
        # Re-compile scanner regex patterns with updated config
        init_scanner(_config)

    _persist()
    logger.info("Added %d entries to %s", len(req.values), req.category)
    return {"status": "ok", "category": req.category, "added": req.values}


@router.delete("/whitelist")
async def remove_from_whitelist(req: WhitelistRequest):
    """Remove term(s) from a whitelist category."""
    if req.category not in WHITELIST_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown category '{req.category}'. Valid: {sorted(WHITELIST_CATEGORIES)}",
        )

    if req.category == "ner_skiplist":
        remove_from_skiplist(req.values)
        existing = set(_config.get("ner_tech_skiplist", []))
        existing.difference_update(v.lower() for v in req.values)
        _config["ner_tech_skiplist"] = sorted(existing)

    elif req.category == "ner_generic_it_words":
        remove_from_generic_it_words(req.values)
        existing = set(_config.get("ner_generic_it_words", []))
        existing.difference_update(v.lower() for v in req.values)
        _config["ner_generic_it_words"] = sorted(existing)

    elif req.category == "domain_allowlist":
        remove_from_domain_allowlist(req.values)
        existing = set(_config.get("domain_allowlist", []))
        existing.difference_update(v.lower() for v in req.values)
        _config["domain_allowlist"] = sorted(existing)

    elif req.category in ("known_persons", "known_orgs", "known_hostnames"):
        existing = set(_config.get(req.category, []))
        existing.difference_update(req.values)
        _config[req.category] = sorted(existing)
        init_scanner(_config)

    _persist()
    logger.info("Removed %d entries from %s", len(req.values), req.category)
    return {"status": "ok", "category": req.category, "removed": req.values}


@router.get("/status")
async def get_status():
    """Return the current redaction state."""
    return {
        "redaction_enabled": is_redaction_enabled(),
        "pseudonymize_domains": is_pseudonymize_domains(),
    }


@router.post("/status")
async def set_status(req: RedactionToggle):
    """Toggle redaction settings."""
    if req.redaction_enabled is not None:
        set_redaction_enabled(req.redaction_enabled)
        _config["redaction_enabled"] = req.redaction_enabled
        logger.info("Redaction %s", "enabled" if req.redaction_enabled else "disabled")

    if req.pseudonymize_domains is not None:
        set_pseudonymize_domains(req.pseudonymize_domains)
        _config["pseudonymize_domains"] = req.pseudonymize_domains
        logger.info(
            "Domain pseudonymization %s",
            "enabled" if req.pseudonymize_domains else "disabled",
        )

    _persist()
    return {
        "redaction_enabled": is_redaction_enabled(),
        "pseudonymize_domains": is_pseudonymize_domains(),
    }


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def _persist() -> None:
    """Write the current config dict back to disk."""
    try:
        save_config(_config, get_config_path())
    except Exception:
        logger.exception("Failed to persist config to disk")
