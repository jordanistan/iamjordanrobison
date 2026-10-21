#!/usr/bin/env python3
"""Verify the public portfolio and resume without credentials or site writes."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urlsplit
from urllib.request import (
    HTTPRedirectHandler,
    Request,
    build_opener,
)


ROOT_URL = "https://iamjordanrobison.com/"
RESUME_URL = "https://iamjordanrobison.com/Jordan_Robison_2026-Resume.pdf"
EXPECTED_TITLE = "Jordan Robison | Security, Cloud, AppSec & DevSecOps Engineer"
EXPECTED_H1 = "I build secure, reliable systems and investigate the difficult problems when they fail."
EXPECTED_RESUME_PATH = "/Jordan_Robison_2026-Resume.pdf"
ALLOWED_SCRIPT_PATHS = {
    "assets/js/jquery.js",
    "assets/bootstrap/js/bootstrap.min.js",
}
HTML_LIMIT = 2 * 1024 * 1024
PDF_LIMIT = 5 * 1024 * 1024
TIMEOUT_SECONDS = 10


class VerificationError(RuntimeError):
    """A public response crossed a fixed verification boundary."""


def validate_endpoint(actual: str, expected: str) -> None:
    """Require the exact HTTPS endpoint, without credentials or URL extras."""
    parsed = urlsplit(actual)
    wanted = urlsplit(expected)
    try:
        port = parsed.port
    except ValueError as exc:
        raise VerificationError(f"invalid endpoint port: {exc}") from exc
    if parsed.scheme != "https":
        raise VerificationError("endpoint must use HTTPS")
    if parsed.username is not None or parsed.password is not None:
        raise VerificationError("endpoint must not contain credentials")
    if port is not None:
        raise VerificationError("endpoint must not contain an explicit port")
    if parsed.hostname != wanted.hostname:
        raise VerificationError("endpoint hostname changed")
    if parsed.path != wanted.path:
        raise VerificationError("endpoint path changed")
    if parsed.query or parsed.fragment:
        raise VerificationError("endpoint must not contain a query or fragment")


class BoundedRedirectHandler(HTTPRedirectHandler):
    """Allow at most three redirects, revalidating every destination."""

    max_redirections = 3
    max_repeats = 1

    def __init__(self, expected_url: str):
        super().__init__()
        self.expected_url = expected_url

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        validate_endpoint(newurl, self.expected_url)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _read_bounded(response, limit: int) -> bytes:  # noqa: ANN001
    length = response.headers.get("Content-Length")
    if length is not None:
        try:
            declared = int(length)
        except ValueError as exc:
            raise VerificationError("invalid Content-Length") from exc
        if declared < 0 or declared > limit:
            raise VerificationError("declared response exceeds byte limit")
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(64 * 1024, limit + 1 - total))
        if not chunk:
            return b"".join(chunks)
        total += len(chunk)
        if total > limit:
            raise VerificationError("streamed response exceeds byte limit")
        chunks.append(chunk)


def fetch_url(
    url: str,
    *,
    expected_type: str,
    limit: int,
    opener=None,
) -> bytes:
    """Fetch one fixed endpoint using a bounded, credential-free GET."""
    validate_endpoint(url, url)
    if opener is None:
        opener = build_opener(BoundedRedirectHandler(url))
    request = Request(
        url,
        method="GET",
        headers={
            "Accept": expected_type,
            "Accept-Encoding": "identity",
            "User-Agent": "iamjordanrobison-live-review/1.0",
        },
    )
    with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
        status = getattr(response, "status", None)
        if status is None:
            status = response.getcode()
        if status != 200:
            raise VerificationError(f"unexpected HTTP status {status}")
        validate_endpoint(response.geturl(), url)
        content_type = response.headers.get_content_type()
        if content_type != expected_type:
            raise VerificationError(
                f"expected {expected_type}, received {content_type}"
            )
        return _read_bounded(response, limit)


def _is_external_resource(value: str) -> bool:
    parsed = urlsplit(value)
    return bool(parsed.scheme or parsed.netloc or value.startswith("//"))


class RootDocument(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._capture_title = False
        self._capture_h1 = False
        self._title_parts: list[str] = []
        self._h1_parts: list[str] = []
        self.titles: list[str] = []
        self.h1s: list[str] = []
        self.canonicals: list[str] = []
        self.resume_links = 0
        self.errors: list[str] = []

    @staticmethod
    def _clean(parts: list[str]) -> str:
        return " ".join("".join(parts).split())

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        attributes = dict(attrs)
        if any(name.lower().startswith("on") for name, _ in attrs):
            self.errors.append(f"unexpected event handler on {tag}")
        if tag == "base":
            self.errors.append("unexpected base element")
        elif tag == "title":
            self._capture_title = True
            self._title_parts = []
        elif tag == "h1":
            self._capture_h1 = True
            self._h1_parts = []
        elif tag == "link":
            rel = {item.lower() for item in attributes.get("rel", "").split()}
            if "canonical" in rel:
                self.canonicals.append(attributes.get("href", ""))
            if rel.intersection({"stylesheet", "preload", "modulepreload"}):
                resource = attributes.get("href", "")
                if not resource or _is_external_resource(resource):
                    self.errors.append(f"unexpected external resource: {resource}")
        elif tag == "a" and attributes.get("href") == EXPECTED_RESUME_PATH:
            self.resume_links += 1
        elif tag in {"form", "iframe", "object", "embed"}:
            self.errors.append(f"unexpected active element: {tag}")
        elif tag == "meta" and attributes.get("http-equiv", "").lower() == "refresh":
            self.errors.append("unexpected meta refresh")
        elif tag == "script":
            source = attributes.get("src")
            if source is None:
                if attributes.get("type", "").lower() != "application/ld+json":
                    self.errors.append("unexpected inline script")
            else:
                parsed = urlsplit(source)
                local_path = parsed.path[1:] if parsed.path.startswith("/") else parsed.path
                if (
                    parsed.scheme
                    or parsed.netloc
                    or parsed.query
                    or parsed.fragment
                    or parsed.path.startswith("//")
                    or local_path not in ALLOWED_SCRIPT_PATHS
                ):
                    self.errors.append(f"unexpected script source: {source}")
        elif tag in {"img", "source", "video", "audio"}:
            resource_values = [
                attributes.get("src", ""),
                attributes.get("poster", ""),
            ]
            resource_values.extend(
                candidate.strip().split()[0]
                for candidate in attributes.get("srcset", "").split(",")
                if candidate.strip()
            )
            for resource in resource_values:
                if resource and _is_external_resource(resource):
                    self.errors.append(f"unexpected external resource: {resource}")
    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self._capture_title:
            self.titles.append(self._clean(self._title_parts))
            self._capture_title = False
        elif tag == "h1" and self._capture_h1:
            self.h1s.append(self._clean(self._h1_parts))
            self._capture_h1 = False

    def handle_data(self, data: str) -> None:
        if self._capture_title:
            self._title_parts.append(data)
        if self._capture_h1:
            self._h1_parts.append(data)


def verify_root(data: bytes) -> None:
    if not data:
        raise VerificationError("root response is empty")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise VerificationError("root response is not strict UTF-8") from exc
    document = RootDocument()
    document.feed(text)
    document.close()
    if document.errors:
        raise VerificationError("; ".join(document.errors))
    if document.titles != [EXPECTED_TITLE]:
        raise VerificationError("root title changed")
    if document.canonicals != [ROOT_URL]:
        raise VerificationError("root canonical URL changed")
    if document.h1s != [EXPECTED_H1]:
        raise VerificationError("root H1 changed")
    if document.resume_links < 1:
        raise VerificationError("root resume link is missing")


def verify_resume(data: bytes, checked_in: Path) -> str:
    expected = checked_in.read_bytes()
    if not data.startswith(b"%PDF-"):
        raise VerificationError("resume response is not a PDF")
    if data != expected:
        raise VerificationError("live resume bytes differ from the checked-in PDF")
    return hashlib.sha256(data).hexdigest()


def run(checked_in_resume: Path, opener=None) -> str:
    root = fetch_url(
        ROOT_URL,
        expected_type="text/html",
        limit=HTML_LIMIT,
        opener=opener,
    )
    verify_root(root)
    resume = fetch_url(
        RESUME_URL,
        expected_type="application/pdf",
        limit=PDF_LIMIT,
        opener=opener,
    )
    return verify_resume(resume, checked_in_resume)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify the fixed professional portfolio and resume endpoints."
    )
    parser.add_argument(
        "--resume",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "Jordan_Robison_2026-Resume.pdf",
        help="Reviewed local PDF that the live resume must match byte-for-byte.",
    )
    args = parser.parse_args(argv)
    try:
        digest = run(args.resume.resolve())
    except (OSError, VerificationError) as exc:
        print(f"Live review failed: {exc}", file=sys.stderr)
        return 1
    print(f"Live review passed: root markers valid; resume sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
