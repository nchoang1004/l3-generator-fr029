"""CMP-002 GitHub intake (API-002 §1, API-001 §2.1). Off by default: API-002 §1 asks for a Security review of the
host list and connection pinning before use, so the web launcher only enables it with `--enable-github`.

Steps: repository metadata -> default branch -> commit SHA -> zipball of that SHA (one revision only).
Rules kept here: HTTPS only; hosts `api.github.com` and `codeload.github.com` only, checked again after every
redirect; every resolved address must be public; no credential is ever sent; 120 seconds for the whole operation;
the archive is read with the ZIP rules of `snapshot.take_zip`, after removing the one wrapper folder GitHub adds.
Not done: pinning the TCP connection to the checked address (DNS could change between check and connect).
"""
from __future__ import annotations

import ipaddress
import json
import socket
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit

from . import snapshot
from .snapshot import IntakeError

ALLOWED_HOSTS = {"api.github.com", "codeload.github.com"}
DEADLINE_S = 120
MAX_REDIRECTS = 3


def _public(host: str, resolve) -> bool:
    try:
        addrs = {info[4][0] for info in resolve(host, 443, proto=socket.IPPROTO_TCP)}
    except OSError:
        return False
    return bool(addrs) and all(ipaddress.ip_address(a.split("%")[0]).is_global for a in addrs)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # redirects are followed by hand so each hop is checked


def http_get(url: str, timeout: float):
    """Default transport: (status, headers, body bytes). Never sends credentials or cookies."""
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "l3slice"})
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(req, timeout=timeout) as resp:
            return resp.status, dict(resp.headers), resp.read(snapshot.ZIP_MAX_COMPRESSED + 1)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), b""


class Fetcher:
    def __init__(self, run_id: str, get=http_get, resolve=socket.getaddrinfo, clock=time.monotonic):
        self.run_id, self.get, self.resolve, self.clock = run_id, get, resolve, clock
        self.start = clock()

    def _err(self, code, message, action):
        return IntakeError(code, message, action, self.run_id)

    def fetch(self, url: str) -> bytes:
        for _ in range(MAX_REDIRECTS + 1):
            left = DEADLINE_S - (self.clock() - self.start)
            if left <= 0:
                raise self._err("FETCH_TIMEOUT", "Không lấy xong source GitHub trong 120 giây.",
                                "Kiểm kết nối và URL public, rồi bắt đầu lần chạy mới.")
            parts = urlsplit(url)
            if parts.scheme != "https" or parts.hostname not in ALLOWED_HOSTS or parts.username or parts.port:
                raise self._err("GITHUB_FETCH_FAILED", "GitHub chuyển hướng tới host ngoài danh sách cho phép.",
                                "Báo người bảo trì; không thử host khác.")
            if not _public(parts.hostname, self.resolve):
                raise self._err("GITHUB_FETCH_FAILED", "Địa chỉ của host GitHub không phải địa chỉ public.",
                                "Kiểm DNS của máy; không chạy tiếp.")
            try:
                status, headers, body = self.get(url, min(left, 30))
            except (urllib.error.URLError, TimeoutError, OSError):
                raise self._err("GITHUB_FETCH_FAILED", "Không kết nối được GitHub.", "Kiểm mạng rồi tạo run mới.") from None
            if status in (301, 302, 303, 307, 308):
                url = headers.get("Location") or headers.get("location") or ""
                continue
            if status == 404:
                raise self._err("GITHUB_NOT_FOUND_OR_PRIVATE", "Repository không tồn tại hoặc là private; GitHub "
                                "trả cùng một mã cho cả hai trường hợp.", "Kiểm URL; chỉ hỗ trợ repository public.")
            if status in (401, 403, 429, 451):
                raise self._err("GITHUB_ACCESS_DENIED", f"GitHub từ chối truy cập (HTTP {status}).",
                                "Chờ hạn mức của GitHub rồi tạo run mới; không nhập credential.")
            if status != 200:
                raise self._err("GITHUB_FETCH_FAILED", f"GitHub trả HTTP {status}.", "Thử lại bằng run mới.")
            if len(body) > snapshot.ZIP_MAX_COMPRESSED:
                raise self._err("INTAKE_LIMIT", "ZIP từ GitHub vượt 100.000.000 byte nén", "Chọn repository nhỏ hơn")
            return body
        raise self._err("GITHUB_FETCH_FAILED", "GitHub chuyển hướng quá nhiều lần.", "Thử lại bằng run mới.")

    def json(self, url: str) -> dict:
        try:
            value = json.loads(self.fetch(url))
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise self._err("GITHUB_FETCH_FAILED", "GitHub trả dữ liệu không đọc được.", "Thử lại bằng run mới.") from None
        if not isinstance(value, dict):
            raise self._err("GITHUB_FETCH_FAILED", "GitHub trả dữ liệu sai dạng.", "Thử lại bằng run mới.")
        return value


def take_github(normalized_url: str, run_id: str, **transport) -> tuple[dict, dict[str, bytes], str]:
    """`normalized_url` is `https://github.com/<owner>/<repo>` (web.normalize_github). Returns (snapshot, sources,
    commit SHA). The SHA is runtime metadata; snapshot_id stays the hash of paths and bytes (API-002 §1)."""
    owner, repo = urlsplit(normalized_url).path.strip("/").split("/")
    f = Fetcher(run_id, **transport)
    meta = f.json(f"https://api.github.com/repos/{owner}/{repo}")
    branch = meta.get("default_branch")
    if not isinstance(branch, str) or not branch or meta.get("private") is True:
        raise IntakeError("GITHUB_NOT_FOUND_OR_PRIVATE", "Repository không public hoặc không có nhánh mặc định.",
                          "Chỉ hỗ trợ repository public.", run_id)
    commit = f.json(f"https://api.github.com/repos/{owner}/{repo}/commits/{urllib.request.quote(branch, safe='')}")
    sha = commit.get("sha")
    if not (isinstance(sha, str) and len(sha) == 40 and all(c in "0123456789abcdef" for c in sha)):
        raise IntakeError("GITHUB_FETCH_FAILED", "Không xác định được commit SHA.", "Thử lại bằng run mới.", run_id)
    data = f.fetch(f"https://api.github.com/repos/{owner}/{repo}/zipball/{sha}")
    snap, sources = snapshot.take_zip(data, run_id, strip_wrapper=True)
    return snap, sources, sha
