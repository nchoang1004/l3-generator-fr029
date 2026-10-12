"""Tests for the Anthropic provider adapter."""

from __future__ import annotations

from token_proxy.providers.anthropic import AnthropicAdapter
from token_proxy.providers.base import SSEAction


class TestExtractTexts:
    def setup_method(self):
        self.adapter = AnthropicAdapter()

    def test_string_system_prompt(self):
        body = {"system": "You are helpful", "messages": []}
        refs = self.adapter.extract_texts(body)
        assert any(r.get() == "You are helpful" and r.kind == "system" for r in refs)
        # Mutate via setter
        for r in refs:
            if r.kind == "system":
                r.set("REDACTED")
        assert body["system"] == "REDACTED"

    def test_string_message_content(self):
        body = {"messages": [{"role": "user", "content": "Hello admin@contoso.com"}]}
        refs = self.adapter.extract_texts(body)
        assert len(refs) == 1
        assert refs[0].get() == "Hello admin@contoso.com"
        refs[0].set("Hello REDACTED")
        assert body["messages"][0]["content"] == "Hello REDACTED"

    def test_text_block(self):
        body = {
            "messages": [
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": "Found the user"},
                    ],
                }
            ]
        }
        refs = self.adapter.extract_texts(body)
        assert len(refs) == 1
        assert refs[0].kind == "text"

    def test_thinking_block(self):
        body = {
            "messages": [
                {
                    "role": "assistant",
                    "content": [
                        {"type": "thinking", "thinking": "Let me think about admin@contoso.com"},
                    ],
                }
            ]
        }
        refs = self.adapter.extract_texts(body)
        assert len(refs) == 1
        assert refs[0].kind == "thinking"
        assert "admin@contoso.com" in refs[0].get()

    def test_tool_use_input(self):
        body = {
            "messages": [
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "tool_use",
                            "id": "t1",
                            "name": "Bash",
                            "input": {
                                "command": "query admin@contoso.com",
                                "description": "Find admin@contoso.com",
                                "timeout": 30000,
                            },
                        },
                    ],
                }
            ]
        }
        refs = self.adapter.extract_texts(body)
        # Should find the two string fields but not the int
        text_values = [r.get() for r in refs]
        assert "query admin@contoso.com" in text_values
        assert "Find admin@contoso.com" in text_values
        assert len(refs) == 2

    def test_tool_result_string(self):
        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "t1",
                            "content": "result with admin@contoso.com",
                        },
                    ],
                }
            ]
        }
        refs = self.adapter.extract_texts(body)
        assert len(refs) == 1

    def test_tool_result_blocks(self):
        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "t1",
                            "content": [
                                {"type": "text", "text": "result text"},
                            ],
                        },
                    ],
                }
            ]
        }
        refs = self.adapter.extract_texts(body)
        assert len(refs) == 1
        assert refs[0].get() == "result text"

    def test_mixed_blocks(self):
        """Full conversation with all block types."""
        body = {
            "system": "sys prompt",
            "messages": [
                {"role": "user", "content": "question"},
                {
                    "role": "assistant",
                    "content": [
                        {"type": "thinking", "thinking": "hmm"},
                        {"type": "text", "text": "answer"},
                        {"type": "tool_use", "id": "t1", "name": "X", "input": {"q": "val"}},
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "tool_result", "tool_use_id": "t1", "content": "result"},
                    ],
                },
            ],
        }
        refs = self.adapter.extract_texts(body)
        # system + question + thinking + text + tool_input(q) + tool_result
        assert len(refs) == 6

    def test_in_place_mutation(self):
        """Verify setter mutates the original body dict."""
        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "original"},
                    ],
                }
            ]
        }
        refs = self.adapter.extract_texts(body)
        refs[0].set("modified")
        assert body["messages"][0]["content"][0]["text"] == "modified"


class TestExtractTextsResponse:
    def setup_method(self):
        self.adapter = AnthropicAdapter()

    def test_text_block(self):
        body = {"content": [{"type": "text", "text": "hello"}]}
        refs = self.adapter.extract_texts_response(body)
        assert len(refs) == 1
        assert refs[0].get() == "hello"

    def test_thinking_block(self):
        body = {"content": [{"type": "thinking", "thinking": "internal"}]}
        refs = self.adapter.extract_texts_response(body)
        assert len(refs) == 1
        assert refs[0].kind == "thinking"

    def test_tool_use_block(self):
        body = {
            "content": [
                {"type": "tool_use", "id": "t1", "name": "X", "input": {"key": "value"}},
            ]
        }
        refs = self.adapter.extract_texts_response(body)
        assert len(refs) == 1
        assert refs[0].get() == "value"


class TestSSEClassification:
    def setup_method(self):
        self.adapter = AnthropicAdapter()

    def test_passthrough_events(self):
        for event in ["message_start", "message_delta", "message_stop", "ping"]:
            assert self.adapter.classify_sse_event(event, {}) == SSEAction.PASSTHROUGH

    def test_block_start(self):
        data = {"type": "content_block_start", "index": 0, "content_block": {"type": "text"}}
        assert self.adapter.classify_sse_event("content_block_start", data) == SSEAction.BLOCK_START

    def test_block_stop(self):
        data = {"type": "content_block_stop", "index": 0}
        assert self.adapter.classify_sse_event("content_block_stop", data) == SSEAction.BLOCK_STOP

    def test_text_delta(self):
        data = {
            "type": "content_block_delta",
            "index": 0,
            "delta": {"type": "text_delta", "text": "hi"},
        }
        assert self.adapter.classify_sse_event("content_block_delta", data) == SSEAction.TEXT_DELTA

    def test_thinking_delta(self):
        data = {
            "type": "content_block_delta",
            "index": 0,
            "delta": {"type": "thinking_delta", "thinking": "hmm"},
        }
        assert (
            self.adapter.classify_sse_event("content_block_delta", data) == SSEAction.THINKING_DELTA
        )

    def test_tool_delta(self):
        data = {
            "type": "content_block_delta",
            "index": 0,
            "delta": {"type": "input_json_delta", "partial_json": "{"},
        }
        assert self.adapter.classify_sse_event("content_block_delta", data) == SSEAction.TOOL_DELTA


class TestDeltaExtraction:
    def setup_method(self):
        self.adapter = AnthropicAdapter()

    def test_extract_text_delta(self):
        data = {
            "type": "content_block_delta",
            "index": 2,
            "delta": {"type": "text_delta", "text": "hello"},
        }
        info = self.adapter.extract_delta(data)
        assert info is not None
        assert info.index == 2
        assert info.field_name == "text"
        assert info.text == "hello"

    def test_extract_thinking_delta(self):
        data = {
            "type": "content_block_delta",
            "index": 0,
            "delta": {"type": "thinking_delta", "thinking": "hmm"},
        }
        info = self.adapter.extract_delta(data)
        assert info is not None
        assert info.field_name == "thinking"

    def test_extract_tool_delta(self):
        data = {
            "type": "content_block_delta",
            "index": 1,
            "delta": {"type": "input_json_delta", "partial_json": '{"q":'},
        }
        info = self.adapter.extract_tool_delta(data)
        assert info is not None
        assert info.index == 1
        assert info.partial_json == '{"q":'


class TestFlushEvent:
    def setup_method(self):
        self.adapter = AnthropicAdapter()

    def test_build_text_flush(self):
        event_name, data = self.adapter.build_flush_event(0, "text", "flushed")
        assert event_name == "content_block_delta"
        assert data["delta"]["type"] == "text_delta"
        assert data["delta"]["text"] == "flushed"
        assert data["index"] == 0

    def test_build_thinking_flush(self):
        event_name, data = self.adapter.build_flush_event(1, "thinking", "thought")
        assert data["delta"]["type"] == "thinking_delta"
        assert data["delta"]["thinking"] == "thought"

    def test_build_tool_event(self):
        event_name, data = self.adapter.build_tool_event(0, '{"key": "val"}')
        assert data["delta"]["type"] == "input_json_delta"
        assert data["delta"]["partial_json"] == '{"key": "val"}'


class TestConfig:
    def test_name(self):
        assert AnthropicAdapter().name == "anthropic"

    def test_upstream_url_default(self):
        a = AnthropicAdapter()
        assert "anthropic" in a.upstream_base_url()

    def test_no_stream_terminator(self):
        assert AnthropicAdapter().stream_terminator() is None
