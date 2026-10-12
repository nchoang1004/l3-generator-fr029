"""NER-based entity extraction using spaCy.

Supplements regex detection by catching person and organization names
in natural language that regex cannot detect.

Aggressive filtering ensures only real human names and real company names
are detected — code identifiers, technical terms, acronyms, and fragments
are all skipped.
"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

_nlp = None

# ------------------------------------------------------------------
# Skiplist sets — loaded from config at startup, empty by default.
# Recommended values are in config.json.example.
# ------------------------------------------------------------------

_tech_skiplist: set[str] = set()
_generic_it_words: set[str] = set()

# Characters that indicate code/data fragments, not real names
_JUNK_CHARS = re.compile(r'[=\\{}\[\]<>|;`"\'/@#$\n\r\t]')

# CamelCase single word: e.g., "SecurityEvent", "TimeGenerated", "ResultType"
_CAMELCASE_RE = re.compile(r"^[A-Z][a-z]+(?:[A-Z][a-z]+)+$")


def load_model(
    tech_skiplist: list[str] | None = None,
    generic_it_words: list[str] | None = None,
) -> None:
    """Load the spaCy NER model. Call once at startup."""
    global _nlp

    _tech_skiplist.clear()
    if tech_skiplist:
        _tech_skiplist.update(s.lower() for s in tech_skiplist)

    _generic_it_words.clear()
    if generic_it_words:
        _generic_it_words.update(s.lower() for s in generic_it_words)

    try:
        import spacy

        _nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer"])
        logger.info("spaCy NER model loaded successfully")
    except ImportError:
        logger.warning("spaCy not installed — NER detection disabled")
    except OSError:
        logger.warning("spaCy model 'en_core_web_sm' not found — NER detection disabled")


def is_available() -> bool:
    """Check if the NER model is loaded and ready."""
    return _nlp is not None


def add_to_skiplist(terms: list[str]) -> None:
    """Add terms to the NER tech skiplist at runtime."""
    _tech_skiplist.update(t.lower() for t in terms)


def remove_from_skiplist(terms: list[str]) -> None:
    """Remove terms from the NER tech skiplist at runtime."""
    _tech_skiplist.difference_update(t.lower() for t in terms)


def get_skiplist() -> set[str]:
    """Return a copy of the current tech skiplist."""
    return set(_tech_skiplist)


def add_to_generic_it_words(terms: list[str]) -> None:
    """Add terms to the generic IT words set at runtime."""
    _generic_it_words.update(t.lower() for t in terms)


def remove_from_generic_it_words(terms: list[str]) -> None:
    """Remove terms from the generic IT words set at runtime."""
    _generic_it_words.difference_update(t.lower() for t in terms)


def get_generic_it_words() -> set[str]:
    """Return a copy of the current generic IT words set."""
    return set(_generic_it_words)


def _looks_like_name(text: str) -> bool:
    """Return True only if text plausibly looks like a real person or company name."""
    # Too short
    if len(text) < 4:
        return False

    # Contains junk characters (code fragments, JSON, paths)
    if _JUNK_CHARS.search(text):
        return False

    # ALL_CAPS = acronym or constant, not a name (e.g., CLI, API, OWASP, CRITICAL)
    if text.isupper():
        return False

    # Single CamelCase word = code identifier (e.g., SecurityEvent, TimeGenerated)
    if " " not in text and _CAMELCASE_RE.match(text):
        return False

    # Starts with a dot (file extensions like .json, .jpeg)
    if text.startswith("."):
        return False

    # Contains digits mixed in (hashes, IDs, tokens) — real names don't
    if any(c.isdigit() for c in text):
        # Allow version-like patterns in org names (e.g., "Haiku 4.5"
        # won't reach here — it's in skiplist).
        # Reject "cch=8d05a", "ba7b014d-74f8", "607c7344"
        return False

    # Single word that's all lowercase = generic word, not a proper name
    if " " not in text and text.islower():
        return False

    # Must start with an uppercase letter (proper names do)
    if not text[0].isupper():
        return False

    return True


def extract_entities(text: str) -> list[tuple[str, str]]:
    """Extract PERSON and ORG entities from text.

    Returns list of (entity_text, entity_label) tuples.
    Heavy filtering to only return real human/company names.
    """
    if _nlp is None:
        return []

    doc = _nlp(text)
    results = []
    seen = set()

    for ent in doc.ents:
        if ent.label_ not in ("PERSON", "ORG"):
            continue

        entity_text = ent.text.strip()

        # Structural filters — is this plausibly a name?
        if not _looks_like_name(entity_text):
            continue

        # Skip tech terms (exact match)
        if entity_text.lower() in _tech_skiplist:
            continue

        # Skip if ALL individual words are tech terms or generic IT words
        words = entity_text.lower().split()
        if all(w in _tech_skiplist or w in _generic_it_words for w in words):
            continue

        # Deduplicate
        key = (entity_text, ent.label_)
        if key in seen:
            continue
        seen.add(key)

        entity_type = "Person" if ent.label_ == "PERSON" else "Org"
        results.append((entity_text, entity_type))

    return results
