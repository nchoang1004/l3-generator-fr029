"""HTTP forwarding logic — redact request, forward to LLM provider, restore response."""

from __future__ import annotations

import copy
import json
import logging
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import httpx

from token_proxy.context import ContextEngine
from token_proxy.providers.base import SSEAction
from token_proxy.scanner import (
    _restore_recursive,
    redact_request,
    restore_response,
    restore_text,
)
from token_proxy.session_store import SessionMapping

if TYPE_CHECKING:
    from token_proxy.providers.base import ProviderAdapter

logger = logging.getLogger(__name__)

# Headers the proxy must NOT copy to the upstream request.
_HOP_BY_HOP = frozenset(
    {
        "host",
        "transfer-encoding",
        "connection",
        "keep-alive",
        "upgrade",
        "proxy-authorization",
        "proxy-connection",
        "content-length",  # httpx recalculates
        "cookie",  # irrelevant for API proxying, could leak session tokens
        "set-cookie",
    }
)

# Generous timeout — large completions can take a while.
_TIMEOUT = httpx.Timeout(connect=10.0, read=300.0, write=10.0, pool=10.0)

# Comfortable headroom beyond the longest pseudonym.
# Accounts for subdomain-preserving domain pseudonyms (e.g.,
# "mail.sub.domain-internal-001.com" = 40+ chars).
# We hold back 2× this value so a pseudonym straddling the emit/buffer boundary
# is always fully contained in the buffer.
MAX_PSEUDO_LEN = 60
_BUFFER_SIZE = MAX_PSEUDO_LEN * 2


# ------------------------------------------------------------------
# StreamingRestorer — buffered pseudonym restoration for SSE chunks
# ------------------------------------------------------------------


class StreamingRestorer:
    """Buffers tail of streaming text to handle pseudonyms split across chunks."""

    def __init__(self, session: SessionMapping):
        self._session = session
        self._buffer = ""
        self.raw_assembled = ""  # pre-restoration text for audit

    def feed(self, text: str) -> str:
        """Feed a new chunk. Returns safe-to-emit restored text."""
        self.raw_assembled += text
        combined = self._buffer + text
        if len(combined) <= _BUFFER_SIZE:
            self._buffer = combined
            return ""
        emit = combined[:-_BUFFER_SIZE]
        self._buffer = combined[-_BUFFER_SIZE:]
        return restore_text(emit, self._session)

    def flush(self) -> str:
        """Flush remaining buffer (call at stream end). Returns restored text."""
        result = restore_text(self._buffer, self._session)
        self._buffer = ""
        return result


# ------------------------------------------------------------------
# Streaming result container
# ------------------------------------------------------------------


@dataclass
class StreamResult:
    """Aggregated metadata from a completed stream."""

    outbound_counts: dict[str, int] = field(default_factory=dict)
    inbound_counts: dict[str, int] = field(default_factory=dict)
    redacted_body: dict | None = None
    raw_assembled_text: dict[int, str] = field(default_factory=dict)  # block_index → raw text
    usage: dict[str, int] = field(default_factory=lambda: {"input_tokens": 0, "output_tokens": 0})


# ------------------------------------------------------------------
# Non-streaming forward
# ------------------------------------------------------------------


async def forward_request(
    *,
    method: str,
    path: str,
    headers: dict[str, str],
    body: dict | None,
    session: SessionMapping,
    ctx: ContextEngine,
    client: httpx.AsyncClient,
    adapter: ProviderAdapter | None = None,
) -> tuple[
    int,
    dict[str, str],
    bytes,
    dict[str, int],
    dict[str, int],
    dict | None,
    dict | None,
    dict[str, int] | None,
]:
    """Redact, forward, restore.

    Returns (status_code, response_headers, response_body,
             outbound_counts, inbound_counts,
             redacted_body_snapshot, raw_response, usage).
    """
    if adapter is None:
        from token_proxy.providers.anthropic import AnthropicAdapter

        adapter = AnthropicAdapter()

    # ------------------------------------------------------------------
    # 1. Force non-streaming & redact outbound
    # ------------------------------------------------------------------
    outbound_counts: dict[str, int] = {}
    redacted_body_snapshot: dict | None = None
    if body is not None:
        body["stream"] = False
        outbound_counts = redact_request(body, session, ctx, adapter)
        redacted_body_snapshot = copy.deepcopy(body)

    # ------------------------------------------------------------------
    # 2. Build upstream request
    # ------------------------------------------------------------------
    upstream_url = f"{adapter.upstream_base_url()}{path}"
    upstream_headers = {k: v for k, v in headers.items() if k.lower() not in _HOP_BY_HOP}

    resp = await client.request(
        method=method,
        url=upstream_url,
        headers=upstream_headers,
        json=body,
        timeout=_TIMEOUT,
    )

    # ------------------------------------------------------------------
    # 3. Restore inbound
    # ------------------------------------------------------------------
    inbound_counts: dict[str, int] = {}
    resp_headers = dict(resp.headers)
    resp_body = resp.content
    raw_response: dict | None = None
    usage: dict[str, int] | None = None

    if resp.status_code == 200 and body is not None:
        try:
            resp_json = resp.json()
            raw_response = copy.deepcopy(resp_json)
            usage = adapter.extract_usage_response(raw_response)
            restore_response(resp_json, session, adapter)
            resp_body = json.dumps(resp_json).encode()
            # Count restored entities
            for fake_val in session.tag_to_real:
                entity_type = session.fake_to_type.get(fake_val, "Unknown")
                if fake_val in resp.text:
                    inbound_counts[entity_type] = inbound_counts.get(entity_type, 0) + 1
        except Exception:
            logger.warning("Failed to parse/restore response", exc_info=True)

    return (
        resp.status_code,
        resp_headers,
        resp_body,
        outbound_counts,
        inbound_counts,
        redacted_body_snapshot,
        raw_response,
        usage,
    )


# ------------------------------------------------------------------
# Streaming forward
# ------------------------------------------------------------------


async def forward_request_streaming(
    *,
    method: str,
    path: str,
    headers: dict[str, str],
    body: dict,
    session: SessionMapping,
    ctx: ContextEngine,
    client: httpx.AsyncClient,
    redaction_enabled: bool = True,
    adapter: ProviderAdapter | None = None,
) -> AsyncGenerator[bytes, None]:
    """Redact outbound, stream SSE from LLM provider, restore inbound.

    Yields SSE-formatted bytes. The caller wraps this in a StreamingResponse.
    """
    if adapter is None:
        from token_proxy.providers.anthropic import AnthropicAdapter

        adapter = AnthropicAdapter()

    result = StreamResult()

    # ------------------------------------------------------------------
    # 1. Redact outbound
    # ------------------------------------------------------------------
    if redaction_enabled:
        result.outbound_counts = redact_request(body, session, ctx, adapter)
        result.redacted_body = copy.deepcopy(body)

    # ------------------------------------------------------------------
    # 2. Open streaming connection
    # ------------------------------------------------------------------
    upstream_url = f"{adapter.upstream_base_url()}{path}"
    upstream_headers = {k: v for k, v in headers.items() if k.lower() not in _HOP_BY_HOP}

    async with client.stream(
        method=method,
        url=upstream_url,
        headers=upstream_headers,
        json=body,
        timeout=_TIMEOUT,
    ) as resp:
        # Non-200: yield the full error body as a single chunk and stop
        if resp.status_code != 200:
            await resp.aread()
            yield resp.content
            return

        # ------------------------------------------------------------------
        # 3. Parse SSE events and restore pseudonyms
        # ------------------------------------------------------------------
        if not redaction_enabled:
            async for chunk in resp.aiter_bytes():
                yield chunk
            return

        restorers: dict[int, StreamingRestorer] = {}
        tool_buffers: dict[int, list[str]] = {}
        block_types: dict[int, str] = {}
        current_event: str | None = None
        terminator = adapter.stream_terminator()

        async for raw_line in resp.aiter_lines():
            line = raw_line.rstrip("\r\n")

            # SSE: "event: <type>" line
            if line.startswith("event: "):
                current_event = line[7:]
                yield (line + "\n").encode()
                continue

            # SSE: blank line = event boundary
            if line == "":
                yield b"\n"
                current_event = None
                continue

            # SSE: "data: <payload>" line
            if not line.startswith("data: "):
                yield (line + "\n").encode()
                continue

            data_str = line[6:]

            # Check for stream terminator (e.g., OpenAI's "[DONE]")
            if terminator and data_str.strip() == terminator:
                yield (line + "\n").encode()
                continue

            try:
                data = json.loads(data_str)
            except json.JSONDecodeError:
                yield (line + "\n").encode()
                continue

            # Classify the event using the provider adapter
            action = adapter.classify_sse_event(current_event, data)

            # Side-read: token usage from message_start / message_delta events.
            # Anthropic carries authoritative input_tokens in message_start and
            # cumulative output_tokens in message_delta, so we overwrite rather
            # than accumulate.
            usage_partial = adapter.extract_usage_sse(current_event, data)
            if usage_partial:
                for k, v in usage_partial.items():
                    result.usage[k] = v

            # -- PASSTHROUGH --
            if action == SSEAction.PASSTHROUGH:
                yield (line + "\n").encode()
                continue

            # -- BLOCK_START --
            if action == SSEAction.BLOCK_START:
                info = adapter.extract_block_info(data)
                if info:
                    block_types[info.index] = info.block_type
                    restorers[info.index] = StreamingRestorer(session)
                    if info.block_type == "tool_use":
                        tool_buffers[info.index] = []
                yield (line + "\n").encode()
                continue

            # -- TEXT_DELTA / THINKING_DELTA --
            if action in (SSEAction.TEXT_DELTA, SSEAction.THINKING_DELTA):
                delta_info = adapter.extract_delta(data)
                if delta_info:
                    restorer = restorers.get(delta_info.index)
                    if restorer:
                        restored = restorer.feed(delta_info.text)
                        if restored:
                            # Mutate the data and re-emit
                            delta = data.get("delta", data)
                            delta[delta_info.field_name] = restored
                            yield (f"data: {json.dumps(data)}\n").encode()
                        # else: buffered, don't emit yet
                    else:
                        yield (line + "\n").encode()
                else:
                    yield (line + "\n").encode()
                continue

            # -- TOOL_DELTA --
            if action == SSEAction.TOOL_DELTA:
                tool_info = adapter.extract_tool_delta(data)
                if tool_info and tool_info.index in tool_buffers:
                    tool_buffers[tool_info.index].append(tool_info.partial_json)
                    continue  # Don't yield — will emit on BLOCK_STOP
                yield (line + "\n").encode()
                continue

            # -- BLOCK_STOP --
            if action == SSEAction.BLOCK_STOP:
                info = adapter.extract_block_info(data)
                idx = info.index if info else 0

                # Flush text/thinking restorer
                restorer = restorers.pop(idx, None)
                if restorer:
                    flushed = restorer.flush()
                    if flushed:
                        field_name = "thinking" if block_types.get(idx) == "thinking" else "text"
                        event_name, flush_data = adapter.build_flush_event(idx, field_name, flushed)
                        yield (f"event: {event_name}\n").encode()
                        yield (f"data: {json.dumps(flush_data)}\n\n").encode()
                    result.raw_assembled_text[idx] = restorer.raw_assembled

                # Emit accumulated tool-use input
                if idx in tool_buffers:
                    assembled_json_str = "".join(tool_buffers.pop(idx))
                    if assembled_json_str:
                        try:
                            tool_input = json.loads(assembled_json_str)
                            tool_input = _restore_recursive(tool_input, session)
                            restored_str = json.dumps(tool_input)
                        except (json.JSONDecodeError, Exception):
                            logger.warning(
                                "Failed to parse/restore tool JSON — emitting empty input"
                            )
                            restored_str = "{}"

                        event_name, tool_data = adapter.build_tool_event(idx, restored_str)
                        yield (f"event: {event_name}\n").encode()
                        yield (f"data: {json.dumps(tool_data)}\n\n").encode()

                block_types.pop(idx, None)
                yield (line + "\n").encode()
                continue

            # Anything else — pass through
            yield (line + "\n").encode()

    # ------------------------------------------------------------------
    # 4. Compute inbound counts from assembled raw text
    # ------------------------------------------------------------------
    all_raw = " ".join(result.raw_assembled_text.values())
    for fake_val in session.tag_to_real:
        if fake_val in all_raw:
            entity_type = session.fake_to_type.get(fake_val, "Unknown")
            result.inbound_counts[entity_type] = result.inbound_counts.get(entity_type, 0) + 1

    forward_request_streaming._last_result = result  # type: ignore[attr-defined]
