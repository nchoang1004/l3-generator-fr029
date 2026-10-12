# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is this?

A transparent PII redaction proxy for LLM API traffic. Sits between an application and an LLM provider (currently Anthropic), pseudonymizing sensitive data outbound and restoring it inbound. Built with FastAPI + httpx.

## Commands

```bash
# Install (dev + NER + GeoIP)
pip install -e ".[dev,ner,geoip]"
python -m spacy download en_core_web_sm

# Run locally
TOKEN_PROXY_CONFIG_PATH=config.json uvicorn token_proxy.main:app --port 8090 --reload

# Docker
docker build -t llm-token-proxy .
docker run -p 8090:8080 -v ./config.json:/app/config.json llm-token-proxy

# Tests
pytest                          # all tests
pytest tests/test_scanner.py    # single file
pytest -k "test_redact_email"   # by name pattern

# Lint
ruff check token_proxy/ tests/
ruff format token_proxy/ tests/
```

## Architecture

### Request flow

```
Client → /session/{session_id}/v1/messages → proxy() in main.py
  → scanner.redact_request() mutates body in-place (3-pass pipeline)
  → proxy.forward_request() sends to upstream LLM API
  → scanner.restore_response() replaces pseudonyms with originals
  → Response back to client
```

Streaming path uses `forward_request_streaming()` with `StreamingRestorer` — a tail-buffer that holds back `MAX_PSEUDO_LEN * 2` chars to handle pseudonyms split across SSE chunks.

### Core modules

| Module | Role |
|--------|------|
| `main.py` | FastAPI app, lifespan init, catch-all proxy route, streaming generator |
| `proxy.py` | HTTP forwarding logic — `forward_request()` (non-streaming) and `forward_request_streaming()` (SSE) |
| `scanner.py` | Three-pass PII detection pipeline (regex → NER → username extraction) and bidirectional replacement |
| `pseudonyms.py` | `PseudonymAllocator` — generates structured pseudonyms (counter-based, never exhausts) |
| `session_store.py` | `SessionMapping` (bidirectional real↔pseudo map) and `SessionStore` (per-session with TTL eviction) |
| `context.py` | `ContextEngine` — classifies entities as Internal/External/Partner using config |
| `ner.py` | spaCy NER wrapper with aggressive filtering (TECH_SKIPLIST, structural checks) |
| `geoip.py` | Optional MaxMind ASN database for context-preserving IP pseudonymization |
| `providers/base.py` | `ProviderAdapter` protocol + SSE event types (`SSEAction`, `TextRef`, `BlockInfo`, etc.) |
| `providers/anthropic.py` | Anthropic Messages API adapter |
| `audit.py` | In-memory audit log + `/token-proxy/sessions/*` inspection endpoints |
| `config_api.py` | Runtime config API — `/token-proxy/config/whitelist` and `/token-proxy/config/status` |
| `config.py` | Load/save `config.json`, atomic writes |

### Provider adapter pattern

New LLM providers implement the `ProviderAdapter` protocol (`providers/base.py`). Key methods:
- `extract_texts()` / `extract_texts_response()` — return `TextRef` objects (getter/setter) for in-place mutation
- `classify_sse_event()` → `SSEAction` enum for streaming
- Register in `providers/__init__.py` via `register_provider(path_prefix, AdapterClass)`

### Session isolation

Each `session_id` in the URL path gets its own `SessionMapping` with independent pseudonym counters. Same real value always maps to the same pseudonym within a session. Sessions auto-evict after 2 hours (TTL).

### Three-pass redaction pipeline (`scanner.redact_text`)

1. **Regex** — emails (must be first, contain domains), IPs, domains (with allowlist + file extension blocklist + dotted property detection), known hostnames/persons/orgs from config
2. **NER** — spaCy PERSON/ORG entities with heavy filtering (`_looks_like_name()`, TECH_SKIPLIST, _GENERIC_IT_WORDS)
3. **Username extraction** — bare email local parts (e.g., `j.smith` from `j.smith@contoso.com`)

### Module-level state

`scanner.py` and `ner.py` use module-level globals initialized at startup via `init_scanner()` and `load_model()`. Tests reset this state via the autouse `_init_scanner_state` fixture in `conftest.py`.

## Conventions

- Python 3.11+, type hints, Ruff (line-length=100)
- Section markers: `# ------------------------------------------------------------------`
- Private helpers prefixed with `_`
- `config.json` is the runtime config file — persisted atomically via `config.py:save_config()`
- Domain allowlist has hardcoded defaults (`_DEFAULT_DOMAIN_ALLOWLIST` in scanner.py) — security reference sites that should never be pseudonymized
- `FILE_EXTENSION_BLOCKLIST` in pseudonyms.py prevents `.json`, `.py` etc. from matching as domains
- `_looks_like_dotted_property()` in pseudonyms.py skips Azure permission scopes like `Policy.ReadWrite.All`

## Testing

- NER is disabled in tests by default (`ner_enabled: False` in conftest config) — no spaCy model dependency
- `conftest.py` provides: `config`, `ctx` (ContextEngine), `session` (SessionMapping), `store` (SessionStore)
- Scanner module state auto-resets per test via autouse fixture
- pytest asyncio_mode is `auto` — async tests just work
- Test config uses `contoso.com` as internal domain, `partnercorp.com` as partner

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `ANTHROPIC_API_BASE` | `https://api.anthropic.com` | Upstream API URL |
| `TOKEN_PROXY_CONFIG_PATH` | `/app/config.json` | Path to config file |
| `LOG_LEVEL` | `info` | Logging level |
| `GEOIP_ASN_DB_PATH` | `/app/data/GeoLite2-ASN.mmdb` | MaxMind ASN database (optional) |

## Common gotchas

1. **Email must be detected before domains** — emails contain domains; detecting domains first would break email matching.
2. **Streaming tail buffer** — `StreamingRestorer` holds back `MAX_PSEUDO_LEN * 2` (80) chars. This means short responses may be entirely buffered until `flush()`.
3. **Pseudonym length matters for streaming** — `MAX_PSEUDO_LEN` (40) must be >= the longest possible pseudonym. If you add longer pseudonym formats, update this.
4. **`_last_result` hack** — streaming audit data is passed back via `forward_request_streaming._last_result` attribute. Fragile but avoids changing the generator signature.
5. **Restore sorts by descending length** — `restore_text()` replaces longest pseudonyms first to prevent partial matches (e.g., `domain_internal_001.com` before `internal_001`).
6. **Case-insensitive dedup** — `SessionMapping` uses `_real_lower_to_key` for case-insensitive lookup but preserves the original case in mappings.
