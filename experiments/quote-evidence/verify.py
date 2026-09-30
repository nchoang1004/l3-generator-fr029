"""Quote check: the only evidence gate. Works on text lines, so it is the same for every language.

A quote is {file, line, text}. It passes when the file belongs to the component the statement is about,
the line exists, and the text appears verbatim on that line (whitespace-insensitive).
Passing proves the cited code exists; the meaning of the sentence stays an inference for review.
"""
from __future__ import annotations

import re

SECRET = re.compile(r"sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|"
                    r"(?<=[\"'])[A-Za-z0-9+/_=-]{32,}(?=[\"'])")
MIN_QUOTE = 8


def redact(text: str) -> str:
    """Hide literal secrets before a line leaves the machine; the same form is used when checking."""
    return SECRET.sub("***", text)


def norm(text: str) -> str:
    return " ".join(text.split())


def show(idx: dict, path: str, line: int, width: int = 150) -> str:
    return f"{path}:{line}| {redact(idx[path]['lines'][line - 1]).strip()[:width]}"


def check(idx: dict, quote: dict, files: list[str], symbols: list[str] | None = None) -> str | None:
    """Return None when the quote passes, otherwise the reason it fails."""
    path, line, text = quote.get("file"), quote.get("line"), norm(quote.get("text") or "")
    if path not in files:
        return "file outside this component"
    lines = idx[path]["lines"]
    if not isinstance(line, int) or not 1 <= line <= len(lines):
        return "line out of range"
    if len(text.replace(" ", "")) < MIN_QUOTE:
        return "quote too short"
    actual = norm(redact(lines[line - 1]))
    if text not in actual:
        return "text not on that line"
    if symbols and not any(re.search(rf"\b{re.escape(s)}\b", actual) for s in symbols):
        return "line does not use the related symbol"
    return None
