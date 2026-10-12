# FX-Service

**Async currency-exchange microservice built with FastAPI, featuring resilient caching, scheduled background refresh, and graceful fallback on upstream failure.** Rates are sourced from Frankfurter (ECB data, no API key required). Convert between 30+ currencies with integer-minor-unit precision using Decimal half-up rounding.

## Resilience & Skills Shown

- **Async HTTP client** (httpx) for non-blocking provider calls
- **Redis snapshot caching** (no TTL) to hold rates in memory
- **Background refresh loop** via FastAPI lifespan — runs every hour without blocking requests
- **Stale fallback** — when upstream is down, requests serve the cached snapshot instead of failing
- **Integer-minor-unit conversion** — amount in cents/satoshis using Decimal ROUND_HALF_UP for accuracy
- **Cross-rate computation** — derive rates between any pair even if not directly cached

## Run Locally

```bash
# 1. Start Redis (Docker)
docker compose up -d

# 2. Install dependencies
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"

# 3. Start the API
uvicorn app.main:app --reload
# Open http://localhost:8000/docs
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/rates` | GET | List all available rates for a base currency; optionally filter by symbols |
| `/convert` | GET | Convert an amount from one currency to another with rate snapshot |
| `/healthz` | GET | Health check; returns cache status and age |

## Example Requests

**Get EUR rates:**
```bash
curl "http://localhost:8000/rates?base=EUR"
```

**Convert 100 cents EUR to USD:**
```bash
curl "http://localhost:8000/convert?from=EUR&to=USD&amount_minor=100"
```

**Health check:**
```bash
curl "http://localhost:8000/healthz"
```

## Tech Stack

- **Framework:** FastAPI 0.115+
- **Runtime:** Python 3.13 + Uvicorn
- **HTTP Client:** httpx (async)
- **Cache:** Redis 5.1+
- **Data Validation:** Pydantic 2.9+
- **Code Quality:** Ruff, pytest with coverage

## Documentation

- [Architecture diagram and refresh flow](docs/architecture.md)

## Related

[PayLedger](https://github.com/gabryelvs/payledger) — flagship microservice suite for financial operations.

## License

MIT License
