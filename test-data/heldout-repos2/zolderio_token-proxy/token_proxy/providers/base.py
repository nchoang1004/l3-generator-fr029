"""Base types and protocol for LLM provider adapters."""

from __future__ import annotations

import enum
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


class SSEAction(enum.Enum):
    """Classification of an SSE event for the streaming proxy."""

    PASSTHROUGH = "passthrough"  # Forward unchanged (message_start, ping, etc.)
    BLOCK_START = "block_start"  # New content block starting
    BLOCK_STOP = "block_stop"  # Content block ending (flush restorer)
    TEXT_DELTA = "text_delta"  # Text chunk to restore
    THINKING_DELTA = "thinking_delta"  # Thinking chunk to restore
    TOOL_DELTA = "tool_delta"  # Tool input chunk (accumulate)
    STREAM_END = "stream_end"  # Stream terminated


@dataclass
class TextRef:
    """Reference to a redactable string in a request/response body.

    Provides getter/setter for in-place mutation without copying.
    """

    get: Callable[[], str]
    set: Callable[[str], None]
    kind: str = "text"  # "text", "thinking", "tool_input", "system"


@dataclass
class BlockInfo:
    """Metadata about a content block extracted from an SSE event."""

    index: int
    block_type: str  # "text", "thinking", "tool_use"


@dataclass
class DeltaInfo:
    """Text delta extracted from an SSE event."""

    index: int
    field_name: str  # "text" or "thinking"
    text: str


@dataclass
class ToolDeltaInfo:
    """Tool input delta extracted from an SSE event."""

    index: int
    partial_json: str


@runtime_checkable
class ProviderAdapter(Protocol):
    """Protocol for LLM provider adapters.

    Implement this to add support for a new LLM API format.
    See docs/adding-a-provider.md for a step-by-step guide.
    """

    @property
    def name(self) -> str:
        """Human-readable provider name (e.g., 'anthropic', 'openai')."""
        ...

    # ------------------------------------------------------------------
    # Request / Response text extraction (for redaction and restoration)
    # ------------------------------------------------------------------

    def extract_texts(self, body: dict) -> list[TextRef]:
        """Extract all redactable text references from a request body.

        Returns TextRef objects with getters/setters so the caller can
        redact strings in-place without knowing the message format.
        """
        ...

    def extract_texts_response(self, body: dict) -> list[TextRef]:
        """Extract all restorable text references from a response body."""
        ...

    # ------------------------------------------------------------------
    # Streaming SSE event handling
    # ------------------------------------------------------------------

    def classify_sse_event(self, event_name: str | None, data: dict) -> SSEAction:
        """Classify an SSE event into an action for the streaming proxy."""
        ...

    def extract_block_info(self, data: dict) -> BlockInfo | None:
        """Extract block metadata from a BLOCK_START or BLOCK_STOP event."""
        ...

    def extract_delta(self, data: dict) -> DeltaInfo | None:
        """Extract text delta from a TEXT_DELTA or THINKING_DELTA event."""
        ...

    def extract_tool_delta(self, data: dict) -> ToolDeltaInfo | None:
        """Extract tool input delta from a TOOL_DELTA event."""
        ...

    def build_flush_event(self, index: int, field_name: str, text: str) -> tuple[str, dict]:
        """Build an SSE event line pair (event_name, data_dict) for flushed text."""
        ...

    def build_tool_event(self, index: int, json_str: str) -> tuple[str, dict]:
        """Build an SSE event for assembled tool input."""
        ...

    # ------------------------------------------------------------------
    # Usage extraction (token accounting)
    # ------------------------------------------------------------------

    def extract_usage_response(self, body: dict) -> dict[str, int] | None:
        """Extract token usage from a non-streaming response body."""
        ...

    def extract_usage_sse(self, event_name: str | None, data: dict) -> dict[str, int] | None:
        """Extract (partial) token usage from an SSE event, or None."""
        ...

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def upstream_base_url(self) -> str:
        """Return the upstream API base URL for this provider."""
        ...

    def stream_terminator(self) -> str | None:
        """Return the SSE data string that signals end of stream, or None.

        For example, OpenAI uses '[DONE]'. Anthropic uses event types instead.
        """
        ...
