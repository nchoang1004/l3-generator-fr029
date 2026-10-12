"""In-memory per-session bidirectional mapping between real values and pseudonyms."""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field

from token_proxy.pseudonyms import PseudonymAllocator

logger = logging.getLogger(__name__)

DEFAULT_TTL_SECONDS = 7200  # 2 hours

_ALL_ENTITY_TYPES = ("IP", "Email", "Domain", "Person", "Org", "Hostname", "Username")


@dataclass
class SessionMapping:
    """Bidirectional map of real values ↔ pseudonyms for one session."""

    real_to_tag: dict[str, str] = field(default_factory=dict)
    tag_to_real: dict[str, str] = field(default_factory=dict)
    fake_to_type: dict[str, str] = field(default_factory=dict)
    counters: dict[str, int] = field(default_factory=lambda: {t: 0 for t in _ALL_ENTITY_TYPES})
    last_active: float = field(default_factory=time.time)
    created_at: float = field(default_factory=time.time)
    request_count: int = 0
    allocator: PseudonymAllocator = field(default_factory=PseudonymAllocator)
    _real_lower_to_key: dict[str, str] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def get_or_create_tag(self, real_value: str, entity_type: str, context: str) -> str:
        """Return existing pseudonym or create a new one for *real_value*."""
        with self._lock:
            lookup_key = real_value.lower()
            if lookup_key in self._real_lower_to_key:
                canonical = self._real_lower_to_key[lookup_key]
                return self.real_to_tag[canonical]

            # Allocate pseudonym based on entity type
            if entity_type == "Email":
                from token_proxy.scanner import is_pseudonymize_domains

                keep_domain = not is_pseudonymize_domains()
                pseudo = self.allocator.allocate_email(real_value, context, keep_domain=keep_domain)
                self._register(real_value, pseudo, "Email")
                # Auto-register domain (only when domains are pseudonymized)
                if not keep_domain:
                    real_domain = real_value.rsplit("@", 1)[-1]
                    if real_domain.lower() not in self._real_lower_to_key:
                        pseudo_domain = self.allocator.allocate_domain(real_domain, context)
                        self._register(real_domain, pseudo_domain, "Domain")
                # Auto-register bare username
                real_local = real_value.rsplit("@", 1)[0]
                if real_local.lower() not in self._real_lower_to_key:
                    pseudo_local = pseudo.rsplit("@", 1)[0]  # user_account_NNN
                    self._register(real_local, pseudo_local, "Username")
                return pseudo
            elif entity_type == "Domain":
                pseudo = self.allocator.allocate_domain(real_value, context)
            elif entity_type == "IP":
                pseudo = self.allocator.allocate_ip(real_value, context)
            elif entity_type == "Person":
                pseudo = self.allocator.allocate_person(real_value, context)
            elif entity_type == "Org":
                pseudo = self.allocator.allocate_org(real_value, context)
            elif entity_type == "Hostname":
                pseudo = self.allocator.allocate_hostname(real_value, context)
            elif entity_type == "Username":
                pseudo = self.allocator.allocate_username(real_value, context)
            else:
                pseudo = f"unknown_{real_value}"

            self._register(real_value, pseudo, entity_type)
            return pseudo

    def _register(self, real_value: str, pseudo: str, entity_type: str) -> None:
        """Register a real↔pseudo mapping (must be called under lock)."""
        self.real_to_tag[real_value] = pseudo
        self.tag_to_real[pseudo] = real_value
        self.fake_to_type[pseudo] = entity_type
        self._real_lower_to_key[real_value.lower()] = real_value
        self.counters[entity_type] = self.counters.get(entity_type, 0) + 1

    def touch(self) -> None:
        self.last_active = time.time()
        self.request_count += 1


class SessionStore:
    """Thread-safe store of per-session mappings with TTL eviction."""

    def __init__(self, ttl_seconds: int = DEFAULT_TTL_SECONDS) -> None:
        self._sessions: dict[str, SessionMapping] = {}
        self._lock = threading.Lock()
        self._ttl = ttl_seconds
        self._geoip = None  # Optional GeoIPLookup, set via set_geoip()

    def set_geoip(self, geoip) -> None:
        """Set a shared GeoIPLookup instance for ASN-aware IP pseudonymization."""
        self._geoip = geoip

    def get(self, session_id: str) -> SessionMapping:
        with self._lock:
            if session_id not in self._sessions:
                mapping = SessionMapping()
                if self._geoip:
                    mapping.allocator.set_geoip(self._geoip)
                self._sessions[session_id] = mapping
            mapping = self._sessions[session_id]
            mapping.touch()
            return mapping

    def remove(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)

    def list_sessions(self) -> dict[str, SessionMapping]:
        with self._lock:
            return dict(self._sessions)

    def evict_expired(self) -> int:
        cutoff = time.time() - self._ttl
        evicted = 0
        with self._lock:
            expired = [sid for sid, m in self._sessions.items() if m.last_active < cutoff]
            for sid in expired:
                del self._sessions[sid]
                evicted += 1
        if evicted:
            logger.info("Evicted %d expired token proxy sessions", evicted)
        return evicted
