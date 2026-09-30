"""Groq chat client over plain HTTP: budget ledger, token-per-minute pacing, response cache.
Also OpenRouter (same request shape): no pacing, no request cap, its own ledger with the cost in USD.

The key travels only in the Authorization header. It is never written to the ledger, cache or output.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

MODEL = "openai/gpt-oss-120b"
TPM = 8_000                 # free-tier tokens per minute
REQUEST_CAP = 7_000         # estimated prompt + max completion; above TPM the provider refuses
STATE = Path(__file__).resolve().parents[2] / "evaluation" / "quote-evidence"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class BudgetExceeded(RuntimeError):
    pass


class ModelError(RuntimeError):
    pass


def estimate(text: str) -> int:
    return len(text) // 3 + 1          # conservative for code mixed with Vietnamese


def cost(row: dict) -> int:
    """Tokens of one ledger row; a failed request reports none, so its estimate is counted instead."""
    return row.get("total_tokens") or (row.get("estimated", 0) if row.get("status") not in (0, 200, 429) else 0)


def _first_object(text: str) -> dict | None:
    """The leading JSON object of a generation the provider rejected, when it is complete."""
    try:
        value, _ = json.JSONDecoder().raw_decode(text.strip())
    except ValueError:
        return None
    return value if isinstance(value, dict) else None


def _parse_error(error: dict) -> str:
    """Why a generation was rejected: where its JSON breaks, with the text around it, else the provider's message."""
    text = str(error.get("failed_generation") or "")
    try:
        json.loads(text)
    except ValueError as exc:
        pos = getattr(exc, "pos", None)
        if text and pos is not None:
            return f"{getattr(exc, 'msg', exc)} at character {pos}: ...{text[max(0, pos - 60):pos + 20]}..."
    return str(error.get("message", ""))[:200]


def load_key(env_file: Path, name: str = "GROQ_API_KEY") -> str:
    key = os.environ.get(name, "")
    if not key and env_file.exists():
        for line in env_file.read_text(encoding="utf-8-sig").splitlines():
            if line.strip().startswith(name) and "=" in line:
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        raise ModelError(f"{name} missing; no request sent")
    return key


class Groq:
    def __init__(self, key: str, budget: int, state: Path = STATE, model: str = MODEL, url: str = GROQ_URL):
        self.key, self.budget, self.model, self.url = key, budget, model, url
        self.open = url == OPENROUTER_URL   # OpenRouter: no pacing, no request cap, its own ledger
        self.cache, self.usage = state / "cache", state / ("usage-openrouter.jsonl" if self.open else "usage.jsonl")
        self.cache.mkdir(parents=True, exist_ok=True)
        self.window: list[tuple[float, int]] = []
        self.calls: list[dict] = []
        self.reasoning: dict[str, str] = {}

    def spent(self) -> int:
        """Reported tokens; a failed request reports none, so count its estimate to stay on the safe side."""
        if not self.usage.exists():
            return 0
        rows = [json.loads(l) for l in self.usage.read_text(encoding="utf-8").splitlines() if l]
        return sum(map(cost, rows))

    def _record(self, row: dict) -> None:
        row = {"at": time.strftime("%Y-%m-%dT%H:%M:%S"), **row}
        self.calls.append(row)
        with self.usage.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    def _pace(self, need: int) -> None:
        while not self.open:
            now = time.time()
            self.window = [(t, n) for t, n in self.window if now - t < 60]
            if not self.window or sum(n for _, n in self.window) + need <= TPM:
                return
            time.sleep(max(1.0, 61 - (now - self.window[0][0])))

    def _effort(self, body: dict, effort: str) -> dict:
        """How long the model reasons before it answers (gpt-oss: low, medium, high; it cannot be switched off)."""
        if "gpt-oss" not in self.model:
            return body
        if self.open:
            return {**body, "reasoning": {"effort": effort}}
        return {**body, "reasoning_effort": effort}

    def effort_of(self, body: dict) -> str:
        return (body.get("reasoning") or {}).get("effort") or body.get("reasoning_effort") or ""

    def json(self, system: str, user: str, schema: dict, *, step: str, max_tokens: int, effort: str = "medium") -> dict:
        """The answer object. The model's reasoning text, when the provider returns it, is kept in
        self.reasoning[step] and in the cache: it shows why the model answered so, for review."""
        est = estimate(system + user) + max_tokens
        if est > REQUEST_CAP and not self.open:
            raise BudgetExceeded(f"{step}: request estimated at {est} tokens, above cap {REQUEST_CAP}")
        body = {"model": self.model, "temperature": 0, "max_completion_tokens": max_tokens,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                "response_format": {"type": "json_schema",
                                    "json_schema": {"name": "out", "strict": True, "schema": schema}}}
        body = self._effort(body, effort)
        if self.open:              # only providers that honour the schema; report the cost
            body.update(max_tokens=max_tokens, provider={"require_parameters": True}, usage={"include": True})
        digest = hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:24]
        cached = self.cache / f"{digest}.json"
        if cached.exists():
            self.calls.append({"step": step, "cached": digest, "total_tokens": 0})
            saved = json.loads(cached.read_text(encoding="utf-8"))
            if saved.get("reasoning"):
                self.reasoning[step] = saved["reasoning"]
            return json.loads(saved["content"])
        if self.spent() + est > self.budget:
            raise BudgetExceeded(f"{step}: budget {self.budget} would be exceeded ({self.spent()} spent)")
        resent = False
        for attempt in range(4):
            self._pace(est)
            started = time.time()
            status, headers, data = self._post(body)
            usage = data.get("usage", {}) if status == 200 else {}
            self.window.append((time.time(), usage.get("total_tokens", est)))
            error = (data.get("error") or {}) if status != 200 else {}
            self._record({"step": step, "status": status, "seconds": round(time.time() - started, 2),
                          "estimated": est, "prompt_tokens": usage.get("prompt_tokens", 0),
                          "completion_tokens": usage.get("completion_tokens", 0),
                          "reasoning_tokens": (usage.get("completion_tokens_details") or {}).get("reasoning_tokens", 0),
                          "total_tokens": usage.get("total_tokens", 0), "error": str(error.get("message", ""))[:200],
                          "effort": self.effort_of(body),
                          **({"model": self.model, "usd": usage.get("cost", 0)} if self.open else {}),
                          **({"mode": "resent with the parse error"} if resent else {})})
            if status == 400:
                (self.cache / f"error-{digest}-{attempt}.json").write_text(json.dumps(data, ensure_ascii=False),
                                                                          encoding="utf-8")
            if status == 200:
                choice = data["choices"][0]
                reasoning = str((choice.get("message") or {}).get("reasoning") or "")
                if reasoning:
                    self.reasoning[step] = reasoning
                if choice.get("finish_reason") == "length" and self.effort_of(body) not in ("", "low") and attempt < 3:
                    # The reasoning used up the answer's room: ask again, reasoning less.
                    body = self._effort(body, "low")
                    self.calls[-1]["note"] = "cut by length; retry with low reasoning"
                    continue
                if choice.get("finish_reason") != "stop":
                    raise ModelError(f"{step}: incomplete answer ({choice.get('finish_reason')})")
                answer = _first_object(choice["message"]["content"])
                if answer is None:
                    raise ModelError(f"{step}: answer is not a JSON object")
                cached.write_text(json.dumps({"content": json.dumps(answer, ensure_ascii=False), "usage": usage,
                                              "mode": "json_schema, resent" if resent else "json_schema",
                                              "reasoning": reasoning}, ensure_ascii=False), encoding="utf-8")
                return answer
            truncated = "max completion tokens" in str(error.get("message", ""))
            if status == 400 and error.get("failed_generation"):
                text = str(error["failed_generation"])
                (self.cache / f"failed-{digest}-{attempt}.txt").write_text(text, encoding="utf-8")
                salvaged = None if truncated else _first_object(text)
                if salvaged is not None:      # e.g. one stray '}' at the end; ids and quotes are checked later anyway
                    self.calls[-1]["salvaged"] = True
                    cached.write_text(json.dumps({"content": json.dumps(salvaged, ensure_ascii=False),
                                                  "salvaged": True}, ensure_ascii=False), encoding="utf-8")
                    return salvaged
            if status == 0 and attempt < 3:
                time.sleep(20)                # DNS or connection failure: wait, then try again
                continue
            if status == 429 and attempt < 3:
                time.sleep(float(headers.get("retry-after", "20")) + 1)
                continue
            if status == 400 and "failed_generation" in error and not error["failed_generation"] \
                    and self.effort_of(body) not in ("", "low"):
                # Nothing was written: the reasoning used up the completion budget. Retry with less reasoning.
                body = self._effort(body, "low")
                self.calls[-1]["note"] = "empty answer; retry with low reasoning"
                continue
            if status == 400 and not resent and not truncated and "JSON" in str(error.get("message", "")):
                # The provider rejected the answer as broken JSON or against the strict schema. Send it once more
                # with the parse error; it counts against the budget like any request.
                resent = True
                again = user + f"\n\nYour previous answer was rejected: {_parse_error(error)}\n" \
                               "Answer again with one JSON object that matches the schema."
                body = {**body, "messages": [body["messages"][0], {"role": "user", "content": again}]}
                est = estimate(system + again) + max_tokens
                if (est > REQUEST_CAP + 1000 and not self.open) or self.spent() + est > self.budget:
                    raise BudgetExceeded(f"{step}: resent request ({est} tokens) exceeds a cap")
                continue
            raise ModelError(f"{step}: HTTP {status}: {str(error.get('message', ''))[:200]}")
        raise ModelError(f"{step}: out of retries")

    def _post(self, body: dict) -> tuple[int, dict, dict]:
        req = urllib.request.Request(self.url,
                                     data=json.dumps(body).encode(),
                                     headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json",
                                              "User-Agent": "l3gen-quote-evidence/1"})
        try:
            with urllib.request.urlopen(req, timeout=300 if self.open else 120) as resp:
                status, headers, raw = resp.status, dict(resp.headers), resp.read()
            try:
                return status, headers, json.loads(raw)
            except ValueError:
                # OpenRouter keeps a slow answer's connection alive with blank lines; a body of only those is a
                # connection cut before the answer (run v8, 30/09): treat it as a network failure, so it is retried
                return 0, {}, {"error": {"message": f"network: the answer was not JSON ({len(raw)} bytes)"}}
        except urllib.error.HTTPError as exc:
            try:
                return exc.code, dict(exc.headers), json.load(exc)
            except ValueError:
                return exc.code, dict(exc.headers), {}
        except (urllib.error.URLError, TimeoutError, OSError) as exc:   # never reached the provider
            return 0, {}, {"error": {"message": f"network: {exc}"}}
