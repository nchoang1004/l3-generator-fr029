# llm-token-proxy

A transparent PII redaction proxy for LLM API traffic. Sits between your application and the LLM provider, pseudonymizing sensitive data on the way out and restoring it on the way back.

Your LLM never sees real names, emails, IPs, or domains — it works entirely with structured pseudonyms like `user_account_001@domain-external-001.net`. Your application gets back the original values, transparently.

## Why

When using LLMs for security operations, incident response, or any task involving real customer data, you risk sending PII to third-party APIs. This proxy solves that by:

- Replacing real PII with deterministic, structured pseudonyms before it reaches the LLM
- Restoring original values in the response before it reaches your application
- Maintaining consistency within a session (same input always maps to the same pseudonym)
- Working transparently — no code changes needed in your application

## Quickstart

```bash
# 1. Create your config
cp config.json.example config.json
# Edit config.json with your internal domains, known entities, etc.

# 2. Run with Docker
docker build -t llm-token-proxy .
docker run -p 8090:8080 -v ./config.json:/app/config.json llm-token-proxy

# 3. Point your application at the proxy
export ANTHROPIC_BASE_URL=http://localhost:8090/session/my-session/
```

That's it. Your Anthropic API calls now go through the proxy with PII redacted.

## How It Works

![Token Proxy Typical Flow](./token-proxy.jpeg)

_Typical flow: Application → Token Proxy (PII redaction) → LLM API (pseudonyms only) → Token Proxy (restore originals) → Application_


### Detection Pipeline (3 passes)

1. **Regex** — emails, IP addresses, domains, and config-driven patterns (known persons, orgs, hostnames)
2. **NER** — spaCy named entity recognition catches person and organization names that regex misses
3. **Username extraction** — bare email local parts (e.g., `admin` from `admin@acme.com`)

### Pseudonym Format

| Entity Type | Internal Example | External Example |
|---|---|---|
| Email | `user_account_001@domain-internal-001.com` | `user_account_001@domain-external-001.net` |
| Domain | `domain-internal-001.com` | `domain-external-001.net` |
| IP | `10.99.99.1` (RFC1918) | ASN-aware donor IP (see below) |
| Person | `person_internal_001` | `person_external_001` |
| Org | `org_internal_001` | `org_external_001` |
| Hostname | `host_001` | `host_001` |

Pseudonyms are deterministic within a session — the same real value always maps to the same pseudonym.

### Context-preserving IP pseudonymization

When an LLM is analyzing security logs, the hosting provider and geolocation of an IP address matters — a login from a Hetzner IP in Germany tells a different story than one from a residential ISP in the US. Naive replacement with documentation-range IPs (e.g., `198.51.100.x`) destroys this context.

With the optional [MaxMind GeoLite2-ASN](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data) database, the proxy replaces real IPs with a **different IP from the same ASN and subnet**. The LLM sees a real-looking IP that resolves to the same hosting provider and approximate geography — but it's not the actual address.

- A Hetzner IP gets replaced with a different Hetzner IP from the same prefix
- A Cloudflare IP stays a Cloudflare IP
- Internal/RFC1918 IPs always map to `10.99.99.x` (no ASN context to preserve)
- Without the GeoIP database, external IPs fall back to `198.51.100.x` (documentation range)

The donor IP is chosen deterministically via HMAC with a per-session salt, so the same real IP always maps to the same donor within a session, but different sessions produce different mappings.

## Configuration

The proxy ships with an empty `config.json` — no built-in word lists or domain-specific assumptions. The included `config.json.example` is tuned for **security operations with Microsoft Sentinel and Entra ID** (8,000+ KQL table/column names, Graph API permission terms, security reference domains). If that matches your use case, copy what you need from it. If you're using the proxy for a different domain (healthcare, legal, finance, etc.), start from the empty config and build your own lists.

### `config.json`

```json
{
  "internal_domains": ["yourcompany.com"],
  "partner_domains": ["partnercorp.com"],
  "internal_ip_ranges": ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"],
  "known_persons": ["John Smith"],
  "known_orgs": ["YourCompany"],
  "known_hostnames": ["DC01", "FS01"],
  "ner_enabled": true,
  "ner_skiplist": [],
  "redaction_enabled": true
}
```

- **internal_domains** — domains classified as "internal" (get `_internal_` pseudonyms)
- **partner_domains** — domains classified as "partner"
- **internal_ip_ranges** — CIDR ranges for internal IP classification
- **known_persons/orgs/hostnames** — regex-matched entities (guaranteed detection)
- **ner_enabled** — toggle spaCy NER (requires `spacy` + `en_core_web_sm`)
- **ner_skiplist** — terms the NER model should ignore (reduces false positives)
- **redaction_enabled** — master toggle; when `false`, proxy becomes pure pass-through
- **pseudonymize_domains** — when `false`, domains pass through unmodified (emails, IPs, names are still redacted). Useful when domain names carry important context for the LLM (e.g., distinguishing `outlook.com` from `protonmail.com`) and are not considered sensitive.

### Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `ANTHROPIC_API_BASE` | `https://api.anthropic.com` | Upstream Anthropic API URL |
| `TOKEN_PROXY_CONFIG_PATH` | `/app/config.json` | Path to config file |
| `LOG_LEVEL` | `info` | Logging level |
| `GEOIP_ASN_DB_PATH` | `/app/data/GeoLite2-ASN.mmdb` | MaxMind GeoLite2-ASN database (optional) |

## Runtime Configuration API

Manage whitelists and toggle redaction without restarting:

```bash
# View all whitelists
curl http://localhost:8090/token-proxy/config/whitelist

# Add terms to NER skiplist (reduces false positives)
curl -X POST http://localhost:8090/token-proxy/config/whitelist \
  -H "Content-Type: application/json" \
  -d '{"category": "ner_skiplist", "values": ["EvoSTS", "Hetzner"]}'

# Add domains to allowlist (never pseudonymize these)
curl -X POST http://localhost:8090/token-proxy/config/whitelist \
  -H "Content-Type: application/json" \
  -d '{"category": "domain_allowlist", "values": ["github.com"]}'

# Disable redaction (pass-through mode)
curl -X POST http://localhost:8090/token-proxy/config/status \
  -H "Content-Type: application/json" \
  -d '{"redaction_enabled": false}'
```

Whitelist categories: `ner_skiplist`, `domain_allowlist`, `known_persons`, `known_orgs`, `known_hostnames`

## Audit & Inspection API

Inspect what the proxy is doing in real-time:

```bash
# List active sessions
curl http://localhost:8090/token-proxy/sessions

# View pseudonym mappings for a session
curl http://localhost:8090/token-proxy/sessions/{session_id}/mappings

# View redaction activity log
curl http://localhost:8090/token-proxy/sessions/{session_id}/log

# Search mappings
curl http://localhost:8090/token-proxy/sessions/{session_id}/search?q=admin

# View captured payloads (what the LLM actually saw)
curl http://localhost:8090/token-proxy/sessions/{session_id}/payloads

# Token usage for a session (input/output tokens across all requests)
curl http://localhost:8090/token-proxy/sessions/{session_id}/usage

# Global statistics (includes total_tokens across all sessions)
curl http://localhost:8090/token-proxy/stats
```

## Token Usage Tracking

The proxy records `input_tokens` and `output_tokens` for every request it forwards — both non-streaming (read from the response `usage` object) and streaming (parsed from `message_start` and `message_delta` SSE events). Because the proxy sits between your application and the LLM, you get a single chokepoint for measuring consumption across all clients sharing it, without instrumenting each one.

```bash
curl http://localhost:8090/token-proxy/sessions/my-session/usage
# {
#   "session_id": "my-session",
#   "request_count": 3,
#   "input_tokens": 1240,
#   "output_tokens": 587
# }

curl http://localhost:8090/token-proxy/stats | jq .total_tokens
# { "input_tokens": 48213, "output_tokens": 19044 }
```

Per-request usage is also included in `/token-proxy/sessions/{session_id}/log` under `usage_counts`. Only raw token counts are tracked — pricing is left to the caller.

## Streaming Support

The proxy supports SSE streaming (`stream: true`). Pseudonyms are restored in real-time using a tail-buffer approach that handles pseudonyms split across SSE chunks.

## Adding Provider Support

The proxy uses a provider adapter pattern. Currently supports:

- **Anthropic Messages API** (`/v1/messages`)

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add support for additional providers (OpenAI, Google Gemini, etc.).

## Limitations

- **Text only** — the proxy scans JSON text fields in the API request/response. Images, PDFs, and other binary content (e.g., base64-encoded attachments in vision requests) pass through without redaction. If your workflow sends screenshots or documents containing PII, those will reach the LLM unmodified.
- **NER is English-only** — the spaCy model (`en_core_web_sm`) detects English person/org names. Names in other languages may be missed unless added to `known_persons`/`known_orgs` in config.
- **Regex has blind spots** — PII in unusual formats (e.g., obfuscated emails like `admin [at] acme.com`, phone numbers, physical addresses) won't be caught. The detection pipeline is tuned for structured IT/security data.
- **In-memory sessions** — session mappings live in memory and are lost on restart. There is no persistent storage. Sessions auto-evict after 2 hours.
- **Anthropic only** — currently ships with an Anthropic Messages API adapter. Other providers (OpenAI, Google Gemini) require writing a provider adapter (see [CONTRIBUTING.md](CONTRIBUTING.md)).
- **No authentication on management APIs** — the `/token-proxy/config/*` and `/token-proxy/sessions/*` endpoints have no auth. The proxy is designed for trusted/internal networks — do not expose these endpoints to untrusted networks.

## Development

```bash
# Install dev dependencies
pip install -e ".[dev,ner]"
python -m spacy download en_core_web_sm

# Run tests
pytest

# Lint
ruff check token_proxy/ tests/
```

## License

Apache 2.0 — see [LICENSE](LICENSE).
