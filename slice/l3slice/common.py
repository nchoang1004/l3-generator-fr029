"""Helpers shared by the slice stages: hashing and FieldValue builders (API-004 §2)."""
from __future__ import annotations

import hashlib
import json
import re

SCHEMA_VERSION = "0.1.0"
SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"), re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"), re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"gsk_[A-Za-z0-9]{20,}"), re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S),
    re.compile(r"(?i)((?:password|passwd|secret|token|api_key|apikey)\s*[=:]\s*)(['\"])[^'\"]{4,}\2"),
    # password in URL userinfo: scheme://user:PASSWORD@host
    re.compile(r"(?i)([a-z][a-z0-9+.-]*://[^/\s:@'\"]*:)([^@\s/'\"]+)(@)"),
    # credential-like query parameter: ?password=..., &token=...
    re.compile(r"(?i)([?&;](?:password|passwd|pwd|secret|token|access_token|api_key|apikey|key|sig|signature)=)([^&;#\s'\"]+)()"),
]


def mask(text: str) -> str:
    """Hide credential-looking values. Fails closed: callers treat an exception as "do not send / do not publish"."""
    out = text
    for p in SECRET_PATTERNS:
        if p.groups == 3:
            out = p.sub(lambda m: m.group(1) + "***" + m.group(3), out)
        elif p.groups == 2:
            out = p.sub(lambda m: m.group(1) + m.group(2) + "***" + m.group(2), out)
        else:
            out = p.sub("***", out)
    return out


def has_secret(value) -> bool:
    if isinstance(value, str):
        return mask(value) != value
    if isinstance(value, dict):
        return any(has_secret(k) or has_secret(v) for k, v in value.items())
    if isinstance(value, list):
        return any(has_secret(v) for v in value)
    return False


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(value) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def known(value, *evidence_ids: str) -> dict:
    return {"state": "known", "value": value, "evidence_ids": sorted(set(evidence_ids))}


def unknown(reason: str) -> dict:
    return {"state": "unknown", "reason": reason}


def not_applicable(reason: str) -> dict:
    return {"state": "not_applicable", "reason": reason}


def is_known(field) -> bool:
    return isinstance(field, dict) and field.get("state") == "known"
