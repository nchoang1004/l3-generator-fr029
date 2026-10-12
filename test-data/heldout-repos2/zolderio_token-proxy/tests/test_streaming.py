"""Tests for SSE streaming support in the Token proxy."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from token_proxy.context import ContextEngine
from token_proxy.proxy import _BUFFER_SIZE, StreamingRestorer
from token_proxy.scanner import init_scanner
from token_proxy.session_store import SessionMapping

# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


@pytest.fixture
def config() -> dict:
    return {
        "internal_domains": ["contoso.com"],
        "partner_domains": [],
        "internal_ip_ranges": ["10.0.0.0/8"],
        "known_persons": [],
        "known_orgs": [],
        "known_hostnames": [],
        "ner_enabled": False,
        "ner_skiplist": [],
        "redaction_enabled": True,
    }


@pytest.fixture(autouse=True)
def _init(config: dict):
    init_scanner(config)


@pytest.fixture
def session() -> SessionMapping:
    return SessionMapping()


@pytest.fixture
def ctx(config: dict) -> ContextEngine:
    return ContextEngine(config)


def _make_session_with_mapping() -> SessionMapping:
    """Create a session with a known email mapping for restoration tests."""
    session = SessionMapping()
    cfg = {
        "internal_domains": ["contoso.com"],
        "partner_domains": [],
        "internal_ip_ranges": ["10.0.0.0/8"],
        "known_persons": [],
        "known_orgs": [],
        "known_hostnames": [],
        "ner_enabled": False,
        "ner_skiplist": [],
        "redaction_enabled": True,
    }
    ctx = ContextEngine(cfg)
    # Trigger an allocation so we have a known mapping
    session.get_or_create_tag("admin@contoso.com", "Email", ctx.classify_email("admin@contoso.com"))
    return session


# ------------------------------------------------------------------
# StreamingRestorer unit tests
# ------------------------------------------------------------------


class TestStreamingRestorer:
    def test_feed_short_text(self, session: SessionMapping):
        """Text shorter than buffer size — nothing emitted until flush."""
        restorer = StreamingRestorer(session)
        result = restorer.feed("Hello")
        assert result == ""
        flushed = restorer.flush()
        assert flushed == "Hello"

    def test_feed_exceeds_buffer(self, session: SessionMapping):
        """Text longer than buffer — partial emission."""
        restorer = StreamingRestorer(session)
        text = "A" * (_BUFFER_SIZE + 20)
        result = restorer.feed(text)
        assert len(result) == 20
        assert result == "A" * 20
        flushed = restorer.flush()
        assert flushed == "A" * _BUFFER_SIZE

    def test_pseudonym_split_across_chunks(self):
        """Pseudonym split across two chunks is correctly restored."""
        session = _make_session_with_mapping()
        restorer = StreamingRestorer(session)

        pseudo = "user_account_001@domain-internal-001.com"
        assert pseudo in session.tag_to_real

        # Split the pseudonym across two chunks with surrounding text
        prefix = "Contact "
        # Make the first chunk long enough to emit something
        padding = "x" * (_BUFFER_SIZE + 10)
        chunk1 = padding + prefix + pseudo[:15]
        chunk2 = pseudo[15:] + " for help"

        result1 = restorer.feed(chunk1)
        result2 = restorer.feed(chunk2)
        flushed = restorer.flush()

        full_output = result1 + result2 + flushed
        assert "admin@contoso.com" in full_output
        assert pseudo not in full_output

    def test_flush_restores_remaining(self):
        """Flush returns restored tail."""
        session = _make_session_with_mapping()
        restorer = StreamingRestorer(session)

        pseudo = "user_account_001@domain-internal-001.com"
        # Feed just the pseudonym (fits in buffer)
        result = restorer.feed(pseudo)
        assert result == ""
        flushed = restorer.flush()
        assert flushed == "admin@contoso.com"

    def test_no_pseudonyms(self, session: SessionMapping):
        """Plain text passes through (with buffer delay)."""
        restorer = StreamingRestorer(session)
        text = "This is plain text with no PII at all, just a normal sentence."
        result = restorer.feed(text)
        flushed = restorer.flush()
        assert result + flushed == text

    def test_multiple_pseudonyms_in_stream(self):
        """Several pseudonyms across many small chunks."""
        session = _make_session_with_mapping()
        # Add another mapping
        cfg = {
            "internal_domains": ["contoso.com"],
            "partner_domains": [],
            "internal_ip_ranges": ["10.0.0.0/8"],
            "known_persons": [],
            "known_orgs": [],
            "known_hostnames": [],
            "ner_enabled": False,
            "ner_skiplist": [],
            "redaction_enabled": True,
        }
        ctx = ContextEngine(cfg)
        session.get_or_create_tag("10.0.1.5", "IP", ctx.classify_ip("10.0.1.5"))

        restorer = StreamingRestorer(session)

        email_pseudo = "user_account_001@domain-internal-001.com"
        # Find the IP pseudonym
        ip_pseudo = session.real_to_tag["10.0.1.5"]

        # Build a long text with both pseudonyms
        text = f"User {email_pseudo} connected from {ip_pseudo} yesterday"

        # Feed in small chunks
        chunks = [text[i : i + 10] for i in range(0, len(text), 10)]
        output_parts = []
        for chunk in chunks:
            result = restorer.feed(chunk)
            if result:
                output_parts.append(result)
        output_parts.append(restorer.flush())

        full = "".join(output_parts)
        assert "admin@contoso.com" in full
        assert "10.0.1.5" in full
        assert email_pseudo not in full
        assert ip_pseudo not in full

    def test_raw_assembled_tracks_input(self, session: SessionMapping):
        """raw_assembled accumulates all input text."""
        restorer = StreamingRestorer(session)
        restorer.feed("Hello ")
        restorer.feed("world")
        restorer.flush()
        assert restorer.raw_assembled == "Hello world"


# ------------------------------------------------------------------
# SSE event handling integration tests
# ------------------------------------------------------------------


def _sse_lines(*events: tuple[str, dict]) -> list[str]:
    """Build SSE-formatted lines from (event_type, data) tuples."""
    lines = []
    for event_type, data in events:
        lines.append(f"event: {event_type}")
        lines.append(f"data: {json.dumps(data)}")
        lines.append("")
    return lines


class TestSSEEventHandling:
    """Integration tests using mock httpx streaming."""

    @pytest.fixture
    def mock_stream_response(self):
        """Create a mock httpx streaming response."""

        def _make(sse_lines: list[str], status_code: int = 200):
            mock_resp = AsyncMock()
            mock_resp.status_code = status_code
            mock_resp.aiter_lines = self._async_line_iter(sse_lines)
            mock_resp.aread = AsyncMock(return_value=b'{"error": "bad"}')
            mock_resp.content = b'{"error": "bad"}'
            mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
            mock_resp.__aexit__ = AsyncMock(return_value=False)
            return mock_resp

        return _make

    @staticmethod
    def _async_line_iter(lines: list[str]):
        """Create an async iterator factory from a list of strings."""

        async def _iter():
            for line in lines:
                yield line

        return _iter

    async def _collect_stream(self, gen) -> list[bytes]:
        """Collect all bytes from an async generator."""
        chunks = []
        async for chunk in gen:
            chunks.append(chunk)
        return chunks

    def _decode_sse_events(self, chunks: list[bytes]) -> list[tuple[str | None, dict | None]]:
        """Parse SSE bytes back into (event_type, data) pairs."""
        text = b"".join(chunks).decode()
        events = []
        current_event = None
        for line in text.split("\n"):
            if line.startswith("event: "):
                current_event = line[7:]
            elif line.startswith("data: "):
                try:
                    data = json.loads(line[6:])
                except json.JSONDecodeError:
                    data = None
                events.append((current_event, data))
                current_event = None
        return events

    @pytest.mark.anyio
    async def test_passthrough_events_unchanged(self, mock_stream_response, session, ctx):
        """message_start, message_stop, ping pass through unchanged."""
        from token_proxy.proxy import forward_request_streaming

        lines = _sse_lines(
            ("message_start", {"type": "message_start", "message": {"id": "msg_123"}}),
            ("message_stop", {"type": "message_stop"}),
        )

        mock_resp = mock_stream_response(lines)
        mock_client = AsyncMock()
        mock_client.stream = MagicMock(return_value=mock_resp)

        chunks = await self._collect_stream(
            forward_request_streaming(
                method="POST",
                path="/v1/messages",
                headers={},
                body={"messages": [], "stream": True},
                session=session,
                ctx=ctx,
                client=mock_client,
            )
        )

        events = self._decode_sse_events(chunks)
        event_types = [e[0] for e in events]
        assert "message_start" in event_types
        assert "message_stop" in event_types

    @pytest.mark.anyio
    async def test_text_delta_restored(self, mock_stream_response, ctx):
        """Pseudonym in text_delta is restored."""
        from token_proxy.proxy import forward_request_streaming

        session = _make_session_with_mapping()
        pseudo = "user_account_001@domain-internal-001.com"

        # Build enough text so the buffer emits
        long_text = "A" * (_BUFFER_SIZE + 10) + f" contact {pseudo} please"

        lines = _sse_lines(
            (
                "content_block_start",
                {
                    "type": "content_block_start",
                    "index": 0,
                    "content_block": {"type": "text", "text": ""},
                },
            ),
            (
                "content_block_delta",
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "text_delta", "text": long_text},
                },
            ),
            ("content_block_stop", {"type": "content_block_stop", "index": 0}),
            ("message_stop", {"type": "message_stop"}),
        )

        mock_resp = mock_stream_response(lines)
        mock_client = AsyncMock()
        mock_client.stream = MagicMock(return_value=mock_resp)

        chunks = await self._collect_stream(
            forward_request_streaming(
                method="POST",
                path="/v1/messages",
                headers={},
                body={"messages": [], "stream": True},
                session=session,
                ctx=ctx,
                client=mock_client,
            )
        )

        full_text = b"".join(chunks).decode()
        assert "admin@contoso.com" in full_text
        assert pseudo not in full_text

    @pytest.mark.anyio
    async def test_content_block_stop_flushes_buffer(self, mock_stream_response, ctx):
        """Buffer is flushed as an extra delta before the stop event."""
        from token_proxy.proxy import forward_request_streaming

        session = _make_session_with_mapping()
        pseudo = "user_account_001@domain-internal-001.com"

        # Short text that stays in buffer
        lines = _sse_lines(
            (
                "content_block_start",
                {
                    "type": "content_block_start",
                    "index": 0,
                    "content_block": {"type": "text", "text": ""},
                },
            ),
            (
                "content_block_delta",
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "text_delta", "text": pseudo},
                },
            ),
            ("content_block_stop", {"type": "content_block_stop", "index": 0}),
            ("message_stop", {"type": "message_stop"}),
        )

        mock_resp = mock_stream_response(lines)
        mock_client = AsyncMock()
        mock_client.stream = MagicMock(return_value=mock_resp)

        chunks = await self._collect_stream(
            forward_request_streaming(
                method="POST",
                path="/v1/messages",
                headers={},
                body={"messages": [], "stream": True},
                session=session,
                ctx=ctx,
                client=mock_client,
            )
        )

        events = self._decode_sse_events(chunks)
        # Should have an extra content_block_delta with the flushed+restored text
        deltas = [e for e in events if e[0] == "content_block_delta" and e[1]]
        assert any("admin@contoso.com" in (d[1].get("delta", {}).get("text", "")) for d in deltas)

    @pytest.mark.anyio
    async def test_upstream_error_returns_error_body(self, mock_stream_response, session, ctx):
        """Non-200 upstream returns error body, not SSE stream."""
        from token_proxy.proxy import forward_request_streaming

        mock_resp = mock_stream_response([], status_code=400)
        mock_client = AsyncMock()
        mock_client.stream = MagicMock(return_value=mock_resp)

        chunks = await self._collect_stream(
            forward_request_streaming(
                method="POST",
                path="/v1/messages",
                headers={},
                body={"messages": [], "stream": True},
                session=session,
                ctx=ctx,
                client=mock_client,
            )
        )

        assert len(chunks) == 1
        assert b"error" in chunks[0]

    @pytest.mark.anyio
    async def test_redaction_disabled_passthrough(self, mock_stream_response, session, ctx):
        """When redaction is disabled, raw SSE bytes pass through."""
        from token_proxy.proxy import forward_request_streaming

        raw_bytes = [b"event: message_start\n", b"data: {}\n\n"]

        mock_resp = AsyncMock()
        mock_resp.status_code = 200
        mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
        mock_resp.__aexit__ = AsyncMock(return_value=False)

        async def _aiter_bytes():
            for b in raw_bytes:
                yield b

        mock_resp.aiter_bytes = _aiter_bytes

        mock_client = AsyncMock()
        mock_client.stream = MagicMock(return_value=mock_resp)

        chunks = await self._collect_stream(
            forward_request_streaming(
                method="POST",
                path="/v1/messages",
                headers={},
                body={"messages": [], "stream": True},
                session=session,
                ctx=ctx,
                client=mock_client,
                redaction_enabled=False,
            )
        )

        assert chunks == raw_bytes

    @pytest.mark.anyio
    async def test_thinking_delta_restored(self, mock_stream_response, ctx):
        """Pseudonym in thinking_delta is restored."""
        from token_proxy.proxy import forward_request_streaming

        session = _make_session_with_mapping()
        pseudo = "user_account_001@domain-internal-001.com"
        long_text = "B" * (_BUFFER_SIZE + 10) + f" thinking about {pseudo}"

        lines = _sse_lines(
            (
                "content_block_start",
                {
                    "type": "content_block_start",
                    "index": 0,
                    "content_block": {"type": "thinking", "thinking": ""},
                },
            ),
            (
                "content_block_delta",
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "thinking_delta", "thinking": long_text},
                },
            ),
            ("content_block_stop", {"type": "content_block_stop", "index": 0}),
        )

        mock_resp = mock_stream_response(lines)
        mock_client = AsyncMock()
        mock_client.stream = MagicMock(return_value=mock_resp)

        chunks = await self._collect_stream(
            forward_request_streaming(
                method="POST",
                path="/v1/messages",
                headers={},
                body={"messages": [], "stream": True},
                session=session,
                ctx=ctx,
                client=mock_client,
            )
        )

        full_text = b"".join(chunks).decode()
        assert "admin@contoso.com" in full_text
        assert pseudo not in full_text

    @pytest.mark.anyio
    async def test_tool_use_delta_assembled_and_restored(self, mock_stream_response, ctx):
        """input_json_delta chunks are accumulated and restored on content_block_stop."""
        from token_proxy.proxy import forward_request_streaming

        session = _make_session_with_mapping()
        pseudo = "user_account_001@domain-internal-001.com"

        # Tool input split across deltas
        lines = _sse_lines(
            (
                "content_block_start",
                {
                    "type": "content_block_start",
                    "index": 0,
                    "content_block": {"type": "tool_use", "id": "tool_1", "name": "search"},
                },
            ),
            (
                "content_block_delta",
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "input_json_delta", "partial_json": '{"query": "'},
                },
            ),
            (
                "content_block_delta",
                {
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "input_json_delta", "partial_json": f'{pseudo}"' + "}"},
                },
            ),
            ("content_block_stop", {"type": "content_block_stop", "index": 0}),
        )

        mock_resp = mock_stream_response(lines)
        mock_client = AsyncMock()
        mock_client.stream = MagicMock(return_value=mock_resp)

        chunks = await self._collect_stream(
            forward_request_streaming(
                method="POST",
                path="/v1/messages",
                headers={},
                body={"messages": [], "stream": True},
                session=session,
                ctx=ctx,
                client=mock_client,
            )
        )

        full_text = b"".join(chunks).decode()
        assert "admin@contoso.com" in full_text
        assert pseudo not in full_text


class TestNonStreamingUnchanged:
    """Verify the existing non-streaming path still works."""

    @pytest.mark.anyio
    async def test_stream_false_uses_existing_path(self, session, ctx):
        """stream: false still uses forward_request (non-streaming)."""
        from token_proxy.proxy import forward_request

        # Just verify forward_request still forces stream=False
        body = {"messages": [], "stream": False}

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {}
        mock_resp.content = b'{"content": []}'
        mock_resp.text = '{"content": []}'
        mock_resp.json = MagicMock(return_value={"content": []})

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_resp)

        status, _, _, _, _, _, _, _ = await forward_request(
            method="POST",
            path="/v1/messages",
            headers={},
            body=body,
            session=session,
            ctx=ctx,
            client=mock_client,
        )
        assert status == 200
        assert body["stream"] is False
