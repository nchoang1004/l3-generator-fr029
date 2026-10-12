# Contributing to llm-token-proxy

Thanks for your interest in contributing! This guide covers the basics.

## Development Setup

```bash
# Clone and install
git clone https://github.com/zolderio/token-proxy.git
cd token-proxy
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Optional: install NER support
pip install -e ".[ner]"
python -m spacy download en_core_web_sm

# Run tests
pytest

# Lint
ruff check token_proxy/ tests/
ruff format --check token_proxy/ tests/
```

## Adding a New LLM Provider

The proxy uses a provider adapter pattern. To add support for a new LLM API (e.g., OpenAI, Google Gemini):

1. **Create `token_proxy/providers/yourprovider.py`** implementing the `ProviderAdapter` protocol from `token_proxy/providers/base.py`. You need to implement:
   - `extract_texts(body)` — find all redactable strings in a request
   - `extract_texts_response(body)` — find all restorable strings in a response
   - `classify_sse_event()` — classify streaming events
   - `extract_delta()` / `extract_tool_delta()` — parse streaming deltas
   - `build_flush_event()` / `build_tool_event()` — construct SSE events
   - `upstream_base_url()` / `stream_terminator()`

2. **Register it** in `token_proxy/providers/__init__.py`:
   ```python
   from token_proxy.providers.yourprovider import YourAdapter
   register_provider("/v1/chat/completions", YourAdapter)
   ```

3. **Add tests** in `tests/test_providers_yourprovider.py`. See `test_providers_anthropic.py` for the pattern.

4. **Test end-to-end** with a mock upstream that returns your provider's response format.

## Code Style

- Python 3.11+, type hints throughout
- Ruff for linting and formatting (line-length=100)
- No unused imports, no star imports
- Docstrings on public functions

## Pull Requests

- One feature per PR
- Include tests for new functionality
- All tests must pass (`pytest`)
- Lint must pass (`ruff check`)
- Keep PRs focused — refactoring and features should be separate PRs

## Reporting Issues

- Use GitHub Issues for bugs and feature requests
- For security vulnerabilities, see [SECURITY.md](SECURITY.md)
