"""Shared fixtures for Token proxy tests."""

from __future__ import annotations

import pytest

from token_proxy.context import ContextEngine
from token_proxy.scanner import init_scanner
from token_proxy.session_store import SessionMapping, SessionStore


@pytest.fixture
def config() -> dict:
    return {
        "internal_domains": ["contoso.com", "contoso.onmicrosoft.com"],
        "partner_domains": ["partnercorp.com"],
        "internal_ip_ranges": ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"],
        "known_persons": ["John van der Berg"],
        "known_orgs": ["Contoso Inc"],
        "known_hostnames": ["DC01", "FS01"],
        "ner_enabled": False,  # disabled in tests by default (no spaCy model)
        "ner_tech_skiplist": [],
        "ner_generic_it_words": [],
        "domain_allowlist": [],
        "redaction_enabled": True,
    }


@pytest.fixture(autouse=True)
def _init_scanner_state(config: dict):
    """Ensure scanner module state is reset for every test."""
    init_scanner(config)


@pytest.fixture
def ctx(config: dict) -> ContextEngine:
    return ContextEngine(config)


@pytest.fixture
def session() -> SessionMapping:
    return SessionMapping()


@pytest.fixture
def store() -> SessionStore:
    return SessionStore(ttl_seconds=60)
