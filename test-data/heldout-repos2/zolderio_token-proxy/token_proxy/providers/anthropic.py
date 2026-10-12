"""Anthropic Messages API adapter."""

from __future__ import annotations

import logging
import os
from typing import Any

from token_proxy.providers.base import (
    BlockInfo,
    DeltaInfo,
    SSEAction,
    TextRef,
    ToolDeltaInfo,
)

logger = logging.getLogger(__name__)

_PASSTHROUGH_EVENTS = frozenset(
    {
        "message_start",
        "message_delta",
        "message_stop",
        "ping",
    }
)


class AnthropicAdapter:
    """Provider adapter for the Anthropic Messages API (/v1/messages)."""

    @property
    def name(self) -> str:
        return "anthropic"

    # ------------------------------------------------------------------
    # Request text extraction
    # ------------------------------------------------------------------

    def extract_texts(self, body: dict) -> list[TextRef]:
        """Extract all redactable text references from an Anthropic request."""
        refs: list[TextRef] = []

        # System prompt (string or list of blocks)
        if "system" in body:
            system = body["system"]
            if isinstance(system, str):
                refs.append(
                    TextRef(
                        get=lambda: body["system"],
                        set=lambda v: body.__setitem__("system", v),
                        kind="system",
                    )
                )
            elif isinstance(system, list):
                refs.extend(self._extract_from_blocks(system))

        # Messages
        for msg in body.get("messages", []):
            content = msg.get("content")
            if content is None:
                continue
            if isinstance(content, str):
                refs.append(
                    TextRef(
                        get=lambda m=msg: m["content"],
                        set=lambda v, m=msg: m.__setitem__("content", v),
                        kind="text",
                    )
                )
            elif isinstance(content, list):
                refs.extend(self._extract_from_blocks(content))

        return refs

    def _extract_from_blocks(self, blocks: list[dict]) -> list[TextRef]:
        """Extract TextRefs from Anthropic content blocks."""
        refs: list[TextRef] = []
        for block in blocks:
            bt = block.get("type")

            if bt == "text" and "text" in block:
                refs.append(
                    TextRef(
                        get=lambda b=block: b["text"],
                        set=lambda v, b=block: b.__setitem__("text", v),
                        kind="text",
                    )
                )

            elif bt == "thinking" and "thinking" in block:
                refs.append(
                    TextRef(
                        get=lambda b=block: b["thinking"],
                        set=lambda v, b=block: b.__setitem__("thinking", v),
                        kind="thinking",
                    )
                )

            elif bt == "tool_use" and "input" in block:
                # Tool input is a dict — extract all string values recursively
                self._extract_from_obj(block["input"], refs, kind="tool_input")

            elif bt == "tool_result" and "content" in block:
                content = block["content"]
                if isinstance(content, str):
                    refs.append(
                        TextRef(
                            get=lambda b=block: b["content"],
                            set=lambda v, b=block: b.__setitem__("content", v),
                            kind="text",
                        )
                    )
                elif isinstance(content, list):
                    refs.extend(self._extract_from_blocks(content))

            elif bt not in (None, "image"):
                # image blocks contain binary data (not scannable by regex/NER)
                logger.debug("Unhandled content block type: %s", bt)

        return refs

    def _extract_from_obj(self, obj: Any, refs: list[TextRef], kind: str = "tool_input") -> None:
        """Recursively extract string TextRefs from a dict/list structure."""
        if isinstance(obj, dict):
            for key in obj:
                val = obj[key]
                if isinstance(val, str):
                    refs.append(
                        TextRef(
                            get=lambda o=obj, k=key: o[k],
                            set=lambda v, o=obj, k=key: o.__setitem__(k, v),
                            kind=kind,
                        )
                    )
                else:
                    self._extract_from_obj(val, refs, kind)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, str):
                    refs.append(
                        TextRef(
                            get=lambda o=obj, idx=i: o[idx],
                            set=lambda v, o=obj, idx=i: o.__setitem__(idx, v),
                            kind=kind,
                        )
                    )
                else:
                    self._extract_from_obj(item, refs, kind)

    # ------------------------------------------------------------------
    # Response text extraction
    # ------------------------------------------------------------------

    def extract_texts_response(self, body: dict) -> list[TextRef]:
        """Extract all restorable text references from an Anthropic response."""
        refs: list[TextRef] = []
        for block in body.get("content", []):
            bt = block.get("type")

            if bt == "text" and "text" in block:
                refs.append(
                    TextRef(
                        get=lambda b=block: b["text"],
                        set=lambda v, b=block: b.__setitem__("text", v),
                        kind="text",
                    )
                )

            elif bt == "thinking" and "thinking" in block:
                refs.append(
                    TextRef(
                        get=lambda b=block: b["thinking"],
                        set=lambda v, b=block: b.__setitem__("thinking", v),
                        kind="thinking",
                    )
                )

            elif bt == "tool_use" and "input" in block:
                self._extract_from_obj(block["input"], refs, kind="tool_input")

        return refs

    # ------------------------------------------------------------------
    # Streaming SSE
    # ------------------------------------------------------------------

    def classify_sse_event(self, event_name: str | None, data: dict) -> SSEAction:
        if event_name in _PASSTHROUGH_EVENTS:
            return SSEAction.PASSTHROUGH

        event_type = data.get("type", "")

        if event_type == "content_block_start":
            return SSEAction.BLOCK_START
        if event_type == "content_block_stop":
            return SSEAction.BLOCK_STOP

        if event_type == "content_block_delta":
            delta_type = data.get("delta", {}).get("type", "")
            if delta_type == "text_delta":
                return SSEAction.TEXT_DELTA
            if delta_type == "thinking_delta":
                return SSEAction.THINKING_DELTA
            if delta_type == "input_json_delta":
                return SSEAction.TOOL_DELTA
            return SSEAction.PASSTHROUGH

        return SSEAction.PASSTHROUGH

    def extract_block_info(self, data: dict) -> BlockInfo | None:
        idx = data.get("index", 0)
        event_type = data.get("type", "")

        if event_type == "content_block_start":
            block = data.get("content_block", {})
            return BlockInfo(index=idx, block_type=block.get("type", "text"))

        if event_type == "content_block_stop":
            return BlockInfo(index=idx, block_type="")

        return None

    def extract_delta(self, data: dict) -> DeltaInfo | None:
        delta = data.get("delta", {})
        idx = data.get("index", 0)
        delta_type = delta.get("type", "")

        if delta_type == "text_delta" and "text" in delta:
            return DeltaInfo(index=idx, field_name="text", text=delta["text"])
        if delta_type == "thinking_delta" and "thinking" in delta:
            return DeltaInfo(index=idx, field_name="thinking", text=delta["thinking"])

        return None

    def extract_tool_delta(self, data: dict) -> ToolDeltaInfo | None:
        delta = data.get("delta", {})
        if delta.get("type") == "input_json_delta" and "partial_json" in delta:
            return ToolDeltaInfo(
                index=data.get("index", 0),
                partial_json=delta["partial_json"],
            )
        return None

    def build_flush_event(self, index: int, field_name: str, text: str) -> tuple[str, dict]:
        if field_name == "thinking":
            delta_type = "thinking_delta"
            delta_content = {"type": delta_type, "thinking": text}
        else:
            delta_type = "text_delta"
            delta_content = {"type": delta_type, "text": text}

        return "content_block_delta", {
            "type": "content_block_delta",
            "index": index,
            "delta": delta_content,
        }

    def build_tool_event(self, index: int, json_str: str) -> tuple[str, dict]:
        return "content_block_delta", {
            "type": "content_block_delta",
            "index": index,
            "delta": {
                "type": "input_json_delta",
                "partial_json": json_str,
            },
        }

    # ------------------------------------------------------------------
    # Usage extraction
    # ------------------------------------------------------------------

    def extract_usage_response(self, body: dict) -> dict[str, int] | None:
        usage = body.get("usage")
        if not isinstance(usage, dict):
            return None
        result: dict[str, int] = {}
        for key in ("input_tokens", "output_tokens"):
            val = usage.get(key)
            if isinstance(val, int):
                result[key] = val
        return result or None

    def extract_usage_sse(self, event_name: str | None, data: dict) -> dict[str, int] | None:
        if event_name == "message_start":
            usage = data.get("message", {}).get("usage")
            if not isinstance(usage, dict):
                return None
            result: dict[str, int] = {}
            for key in ("input_tokens", "output_tokens"):
                val = usage.get(key)
                if isinstance(val, int):
                    result[key] = val
            return result or None

        if event_name == "message_delta":
            usage = data.get("usage")
            if not isinstance(usage, dict):
                return None
            result = {}
            # message_delta carries cumulative output_tokens (and sometimes input_tokens)
            for key in ("input_tokens", "output_tokens"):
                val = usage.get(key)
                if isinstance(val, int):
                    result[key] = val
            return result or None

        return None

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def upstream_base_url(self) -> str:
        return os.environ.get("ANTHROPIC_API_BASE", "https://api.anthropic.com")

    def stream_terminator(self) -> str | None:
        return None  # Anthropic uses event types, not data terminators
