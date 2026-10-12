"""Audit logging and Token proxy inspection API endpoints."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from threading import Lock

from fastapi import APIRouter, Query

from token_proxy.session_store import SessionStore

router = APIRouter(prefix="/token-proxy", tags=["audit"])

# ------------------------------------------------------------------
# Audit log (in-memory ring buffer per session)
# ------------------------------------------------------------------

MAX_LOG_ENTRIES = 500


@dataclass
class AuditEntry:
    ts: float
    session_id: str
    direction: str  # "outbound" | "inbound"
    path: str
    entity_counts: dict[str, int]
    payload: dict | None = None  # captured request/response body
    usage_counts: dict[str, int] = field(default_factory=dict)


@dataclass
class AuditLog:
    _entries: dict[str, deque[AuditEntry]] = field(default_factory=dict)
    _global_counts: dict[str, int] = field(
        default_factory=lambda: {
            "IP": 0,
            "Email": 0,
            "Domain": 0,
            "Person": 0,
            "Org": 0,
            "Hostname": 0,
            "Username": 0,
        }
    )
    _total_requests: int = 0
    _global_usage: dict[str, int] = field(
        default_factory=lambda: {"input_tokens": 0, "output_tokens": 0}
    )
    _lock: Lock = field(default_factory=Lock)

    def record(
        self,
        session_id: str,
        direction: str,
        path: str,
        entity_counts: dict[str, int],
        payload: dict | None = None,
        usage: dict[str, int] | None = None,
    ) -> None:
        entry = AuditEntry(
            ts=time.time(),
            session_id=session_id,
            direction=direction,
            path=path,
            entity_counts=entity_counts,
            payload=payload,
            usage_counts=dict(usage) if usage else {},
        )
        with self._lock:
            if session_id not in self._entries:
                self._entries[session_id] = deque(maxlen=MAX_LOG_ENTRIES)
            self._entries[session_id].append(entry)
            for k, v in entity_counts.items():
                self._global_counts[k] = self._global_counts.get(k, 0) + v
            if direction == "outbound":
                self._total_requests += 1
            if usage and direction == "inbound":
                for k, v in usage.items():
                    self._global_usage[k] = self._global_usage.get(k, 0) + v

    def get_session_log(self, session_id: str) -> list[dict]:
        with self._lock:
            entries = self._entries.get(session_id, [])
            return [
                {
                    "ts": e.ts,
                    "direction": e.direction,
                    "path": e.path,
                    "entity_counts": e.entity_counts,
                    "usage_counts": e.usage_counts,
                    "has_payload": e.payload is not None,
                }
                for e in entries
            ]

    def get_session_usage(self, session_id: str) -> dict:
        with self._lock:
            entries = self._entries.get(session_id, [])
            input_tokens = 0
            output_tokens = 0
            request_count = 0
            for e in entries:
                if e.direction != "inbound" or not e.usage_counts:
                    continue
                request_count += 1
                input_tokens += e.usage_counts.get("input_tokens", 0)
                output_tokens += e.usage_counts.get("output_tokens", 0)
            return {
                "session_id": session_id,
                "request_count": request_count,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            }

    def get_payloads(self, session_id: str, direction: str | None = None) -> list[dict]:
        with self._lock:
            entries = self._entries.get(session_id, [])
            results = []
            for i, e in enumerate(entries):
                if e.payload is None:
                    continue
                if direction and e.direction != direction:
                    continue
                results.append(
                    {
                        "index": i,
                        "ts": e.ts,
                        "direction": e.direction,
                        "path": e.path,
                        "entity_counts": e.entity_counts,
                        "payload": e.payload,
                    }
                )
            return results

    def get_global_stats(self) -> dict:
        with self._lock:
            return {
                "total_requests_proxied": self._total_requests,
                "total_entities_redacted": dict(self._global_counts),
                "total_tokens": dict(self._global_usage),
                "active_sessions": len(self._entries),
            }


# Singleton — set during app startup
audit_log = AuditLog()
_store: SessionStore | None = None


def init_audit(store: SessionStore) -> None:
    global _store
    _store = store


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------


@router.get("/sessions")
async def list_sessions():
    """List all active sessions with redaction stats."""
    if _store is None:
        return []
    sessions = _store.list_sessions()
    result = []
    for sid, mapping in sessions.items():
        result.append(
            {
                "session_id": sid,
                "created_at": mapping.created_at,
                "last_active": mapping.last_active,
                "request_count": mapping.request_count,
                "entity_counts": {
                    etype: mapping.counters.get(etype, 0)
                    for etype in ("IP", "Email", "Domain", "Person", "Org", "Hostname", "Username")
                    if mapping.counters.get(etype, 0) > 0
                },
                "total_mappings": len(mapping.real_to_tag),
            }
        )
    return result


@router.get("/sessions/{session_id}/mappings")
async def get_mappings(session_id: str):
    """View all real↔tag pairs for a session."""
    if _store is None:
        return {"mappings": []}
    sessions = _store.list_sessions()
    mapping = sessions.get(session_id)
    if not mapping:
        return {"error": "session_not_found"}, 404

    return {
        "session_id": session_id,
        "mappings": [
            {
                "real_value": real,
                "tag": fake,
                "replacement": fake,
                "type": mapping.fake_to_type.get(fake, "Unknown"),
            }
            for real, fake in mapping.real_to_tag.items()
        ],
    }


@router.get("/sessions/{session_id}/search")
async def search_mappings(session_id: str, q: str = Query(..., min_length=1)):
    """Search through redacted values and tags."""
    if _store is None:
        return {"results": []}
    sessions = _store.list_sessions()
    mapping = sessions.get(session_id)
    if not mapping:
        return {"error": "session_not_found"}, 404

    q_lower = q.lower()
    results = []
    for real, fake in mapping.real_to_tag.items():
        if q_lower in real.lower() or q_lower in fake.lower():
            results.append(
                {
                    "real_value": real,
                    "tag": fake,
                    "replacement": fake,
                    "type": mapping.fake_to_type.get(fake, "Unknown"),
                }
            )
    return {"session_id": session_id, "query": q, "results": results}


@router.get("/sessions/{session_id}/log")
async def get_session_log(session_id: str):
    """Recent redaction events for a session."""
    return {"session_id": session_id, "entries": audit_log.get_session_log(session_id)}


@router.get("/sessions/{session_id}/usage")
async def get_session_usage(session_id: str):
    """Total input/output tokens consumed by a session."""
    return audit_log.get_session_usage(session_id)


@router.get("/sessions/{session_id}/payloads")
async def get_payloads(
    session_id: str,
    direction: str | None = Query(None, description="Filter: outbound or inbound"),
    index: int | None = Query(None, description="Get a specific exchange by index (0-based)"),
):
    """View captured request/response payloads (redacted form sent to upstream LLM)."""
    entries = audit_log.get_payloads(session_id, direction=direction)
    if index is not None:
        if 0 <= index < len(entries):
            return entries[index]
        return {"error": "index_out_of_range", "total": len(entries)}
    return {"session_id": session_id, "total": len(entries), "payloads": entries}


@router.get("/stats")
async def get_stats():
    """Global redaction statistics."""
    return audit_log.get_global_stats()
