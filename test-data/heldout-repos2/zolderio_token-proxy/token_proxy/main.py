"""FastAPI application — Token API proxy entry point."""

from __future__ import annotations

import asyncio
import json
import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse

from token_proxy.audit import audit_log, init_audit
from token_proxy.audit import router as audit_router
from token_proxy.config import load_config
from token_proxy.config_api import router as config_router
from token_proxy.config_api import set_config_ref
from token_proxy.context import ContextEngine
from token_proxy.providers import detect_provider
from token_proxy.scanner import init_scanner, is_redaction_enabled
from token_proxy.session_store import SessionStore

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Globals (initialised at startup)
# ------------------------------------------------------------------

store = SessionStore()
ctx_engine: ContextEngine | None = None
http_client: httpx.AsyncClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global ctx_engine, http_client

    # Configure logging
    log_level = os.environ.get("LOG_LEVEL", "info").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    )

    # Load config
    config_path = os.environ.get("TOKEN_PROXY_CONFIG_PATH", "/app/config.json")
    config = load_config(config_path)
    set_config_ref(config)
    ctx_engine = ContextEngine(config)
    init_audit(store)

    # Initialize GeoIP for ASN-aware IP pseudonymization (optional)
    from token_proxy.geoip import GeoIPLookup

    geoip_path = config.get("geoip_asn_db_path")
    geoip = GeoIPLookup(db_path=geoip_path)
    store.set_geoip(geoip)

    # Initialize scanner (compiles known-entity patterns)
    init_scanner(config)

    # Load NER model if enabled
    if config.get("ner_enabled", True):
        from token_proxy.ner import load_model

        load_model(
            tech_skiplist=config.get("ner_tech_skiplist"),
            generic_it_words=config.get("ner_generic_it_words"),
        )

    # httpx client
    http_client = httpx.AsyncClient()

    # Background session eviction (every 5 minutes)
    async def _evict_loop() -> None:
        while True:
            await asyncio.sleep(300)
            try:
                store.evict_expired()
            except Exception:
                logger.warning("Session eviction failed", exc_info=False)

    evict_task = asyncio.create_task(_evict_loop())

    logger.info(
        "Token proxy started — redaction_enabled=%s, ner_enabled=%s",
        config["redaction_enabled"],
        config.get("ner_enabled", True),
    )
    yield

    # Shutdown
    evict_task.cancel()
    await http_client.aclose()
    geoip.close()
    logger.info("Token proxy shut down")


app = FastAPI(title="Token API Proxy", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(audit_router)
app.include_router(config_router)


# ------------------------------------------------------------------
# Health
# ------------------------------------------------------------------


@app.get("/health")
async def health():
    return {"status": "ok"}


# ------------------------------------------------------------------
# Catch-all proxy route
# ------------------------------------------------------------------


@app.api_route(
    "/session/{session_id}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
)
async def proxy(session_id: str, path: str, request: Request):
    """Intercept requests, redact PII, forward to upstream LLM, restore response."""
    if ctx_engine is None or http_client is None:
        return JSONResponse({"error": "proxy_not_ready"}, status_code=503)

    # Parse request body (if present)
    body = None
    if request.method in ("POST", "PUT", "PATCH"):
        try:
            body = await request.json()
        except Exception:
            raw = await request.body()
            return Response(content=raw, status_code=400)

    # Collect headers
    headers = dict(request.headers)

    # Get or create session mapping
    session = store.get(session_id)

    upstream_path = f"/{path}"
    adapter = detect_provider(upstream_path)

    # ------------------------------------------------------------------
    # Streaming path
    # ------------------------------------------------------------------
    if body and body.get("stream") is True:
        return StreamingResponse(
            _stream_proxy(session_id, upstream_path, body, headers, session, adapter),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )

    # ------------------------------------------------------------------
    # Non-streaming path (existing behaviour)
    # ------------------------------------------------------------------
    from token_proxy.proxy import forward_request

    (
        status,
        resp_headers,
        resp_body,
        out_counts,
        in_counts,
        redacted_body,
        raw_resp,
        usage,
    ) = await forward_request(
        method=request.method,
        path=upstream_path,
        headers=headers,
        body=body,
        session=session,
        ctx=ctx_engine,
        client=http_client,
        adapter=adapter,
    )

    # Audit logging
    audit_log.record(
        session_id,
        "outbound",
        upstream_path,
        out_counts,
        payload=redacted_body,
    )
    if raw_resp:
        audit_log.record(
            session_id,
            "inbound",
            upstream_path,
            in_counts,
            payload=raw_resp,
            usage=usage,
        )

    # Filter response headers
    safe_headers = {
        k: v
        for k, v in resp_headers.items()
        if k.lower()
        not in ("transfer-encoding", "content-encoding", "content-length", "connection")
    }

    return Response(
        content=resp_body,
        status_code=status,
        headers=safe_headers,
        media_type="application/json",
    )


# ------------------------------------------------------------------
# Streaming proxy generator
# ------------------------------------------------------------------


async def _stream_proxy(
    session_id: str,
    path: str,
    body: dict,
    headers: dict[str, str],
    session,
    adapter=None,
) -> AsyncGenerator[bytes, None]:
    """Wrap forward_request_streaming with audit logging."""
    from token_proxy.proxy import forward_request_streaming

    redaction = is_redaction_enabled()

    try:
        async for chunk in forward_request_streaming(
            method="POST",
            path=path,
            headers=headers,
            body=body,
            session=session,
            ctx=ctx_engine,
            client=http_client,
            redaction_enabled=redaction,
            adapter=adapter,
        ):
            yield chunk
    except httpx.RemoteProtocolError:
        logger.warning("Upstream disconnected during stream for session %s", session_id)
        error_event = {
            "type": "error",
            "error": {"type": "proxy_error", "message": "Upstream connection lost"},
        }
        yield f"event: error\ndata: {json.dumps(error_event)}\n\n".encode()
    except Exception:
        logger.exception("Error during streaming for session %s", session_id)
        error_event = {
            "type": "error",
            "error": {"type": "proxy_error", "message": "Internal proxy error"},
        }
        yield f"event: error\ndata: {json.dumps(error_event)}\n\n".encode()
    finally:
        # Record audit entries from the completed stream
        result = getattr(forward_request_streaming, "_last_result", None)
        if result:
            audit_log.record(
                session_id,
                "outbound",
                path,
                result.outbound_counts,
                payload=result.redacted_body,
            )
            # Build assembled payload for audit
            assembled_payload: dict | None = None
            if result.raw_assembled_text:
                assembled_payload = {
                    "type": "message",
                    "_streaming": True,
                    "_assembled": True,
                    "content": [
                        {"type": "text", "index": idx, "text": text}
                        for idx, text in sorted(result.raw_assembled_text.items())
                    ],
                }
            audit_log.record(
                session_id,
                "inbound",
                path,
                result.inbound_counts,
                payload=assembled_payload,
                usage=result.usage or None,
            )
            # Clean up
            forward_request_streaming._last_result = None  # type: ignore[attr-defined]
