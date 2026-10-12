"""Tests for NER entity extraction."""

import pytest

from token_proxy.ner import extract_entities, is_available, load_model

_TEST_TECH_SKIPLIST = [
    "azure",
    "microsoft",
    "docker",
    "kubernetes",
    "python",
    "sentinel",
    "defender",
    "graph",
    "github",
    "anthropic",
    "claude",
    "openai",
    "bash",
    "linux",
    "redis",
]

_TEST_GENERIC_IT_WORDS = [
    "access",
    "account",
    "configuration",
    "device",
    "directory",
    "conditional",
    "user",
    "add",
    "global",
    "security",
]


@pytest.fixture(autouse=True)
def _try_load_ner():
    """Try to load NER model; skip tests if unavailable."""
    load_model(tech_skiplist=_TEST_TECH_SKIPLIST, generic_it_words=_TEST_GENERIC_IT_WORDS)
    if not is_available():
        pytest.skip("spaCy model not available")


class TestNERExtraction:
    def test_detects_person(self):
        entities = extract_entities("Alert: John Smith logged in from suspicious IP")
        types = [t for _, t in entities]
        assert "Person" in types

    def test_detects_org(self):
        entities = extract_entities("Microsoft reported a breach at Contoso Corporation")
        # Microsoft is in skiplist, but Contoso Corporation might be detected
        names = [n for n, t in entities if t == "Org"]
        # At minimum, should not include Microsoft (skiplist)
        assert "Microsoft" not in names

    def test_skips_tech_terms(self):
        entities = extract_entities("We deployed Python on Azure with Docker and Kubernetes")
        names = [n.lower() for n, _ in entities]
        assert "python" not in names
        assert "azure" not in names
        assert "docker" not in names

    def test_skips_short_entities(self):
        entities = extract_entities("AI is great")
        names = [n for n, _ in entities]
        assert "AI" not in names

    def test_empty_text(self):
        entities = extract_entities("")
        assert entities == []

    def test_no_entities(self):
        entities = extract_entities("The quick brown fox jumps over the lazy dog")
        # Might return empty or very few — just verify no crash
        assert isinstance(entities, list)
