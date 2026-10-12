"""Provider adapters for different LLM API formats."""

from __future__ import annotations

from token_proxy.providers.base import ProviderAdapter

# Registry of known providers (path prefix → adapter class)
_REGISTRY: dict[str, type[ProviderAdapter]] = {}


def register_provider(path_prefix: str, adapter_cls: type[ProviderAdapter]) -> None:
    """Register a provider adapter for a URL path prefix."""
    _REGISTRY[path_prefix] = adapter_cls


def detect_provider(path: str) -> ProviderAdapter:
    """Detect the LLM provider from the request path and return an adapter instance."""
    for prefix, adapter_cls in _REGISTRY.items():
        if prefix in path:
            return adapter_cls()

    # Default to Anthropic for backward compatibility
    from token_proxy.providers.anthropic import AnthropicAdapter

    return AnthropicAdapter()


def _register_builtins() -> None:
    """Register built-in provider adapters."""
    from token_proxy.providers.anthropic import AnthropicAdapter

    register_provider("/v1/messages", AnthropicAdapter)


_register_builtins()
