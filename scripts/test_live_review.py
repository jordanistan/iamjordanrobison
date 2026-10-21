#!/usr/bin/env python3
"""Offline tests for the bounded professional-site live verifier."""

from email.message import Message
import io
from pathlib import Path
import tempfile
import unittest
from urllib.request import Request

from scripts.live_review import (
    BoundedRedirectHandler,
    EXPECTED_H1,
    EXPECTED_RESUME_PATH,
    EXPECTED_TITLE,
    HTML_LIMIT,
    ROOT_URL,
    VerificationError,
    fetch_url,
    validate_endpoint,
    verify_resume,
    verify_root,
)


def valid_html(extra: str = "") -> bytes:
    return f"""<!doctype html>
<html lang="en"><head>
<title>{EXPECTED_TITLE}</title>
<link rel="canonical" href="{ROOT_URL}">
<script type="application/ld+json">{{"name":"Jordan"}}</script>
</head><body>
<h1>{EXPECTED_H1}</h1>
<a href="{EXPECTED_RESUME_PATH}">Resume</a>
<script src="assets/js/jquery.js"></script>
<script src="assets/bootstrap/js/bootstrap.min.js"></script>
{extra}
</body></html>""".encode()


class FakeResponse:
    def __init__(
        self,
        body: bytes,
        *,
        url: str = ROOT_URL,
        status: int = 200,
        content_type: str = "text/html; charset=utf-8",
        content_length: str | None = None,
    ) -> None:
        self.status = status
        self._url = url
        self._stream = io.BytesIO(body)
        self.headers = Message()
        self.headers["Content-Type"] = content_type
        if content_length is not None:
            self.headers["Content-Length"] = content_length

    def getcode(self) -> int:
        return self.status

    def geturl(self) -> str:
        return self._url

    def read(self, size: int = -1) -> bytes:
        return self._stream.read(size)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:  # noqa: ANN001
        return None


class FakeOpener:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.requests: list[tuple[Request, int | float | None]] = []

    def open(self, request: Request, timeout=None):  # noqa: ANN001
        self.requests.append((request, timeout))
        return self.response


class EndpointTests(unittest.TestCase):
    def test_accepts_only_exact_fixed_endpoint(self) -> None:
        validate_endpoint(ROOT_URL, ROOT_URL)
        invalid = [
            "http://iamjordanrobison.com/",
            "https://evil.example/",
            "https://user@iamjordanrobison.com/",
            "https://iamjordanrobison.com:443/",
            "https://iamjordanrobison.com/other",
            "https://iamjordanrobison.com/?source=test",
            "https://iamjordanrobison.com/#top",
        ]
        for url in invalid:
            with self.subTest(url=url), self.assertRaises(VerificationError):
                validate_endpoint(url, ROOT_URL)

    def test_redirect_revalidates_target(self) -> None:
        handler = BoundedRedirectHandler(ROOT_URL)
        request = Request(ROOT_URL)
        redirected = handler.redirect_request(
            request, None, 302, "Found", {}, ROOT_URL
        )
        self.assertEqual(redirected.full_url, ROOT_URL)
        with self.assertRaises(VerificationError):
            handler.redirect_request(
                request, None, 302, "Found", {}, "https://evil.example/"
            )


class FetchTests(unittest.TestCase):
    def test_fetches_with_bounded_headers_and_timeout(self) -> None:
        opener = FakeOpener(FakeResponse(valid_html()))
        result = fetch_url(
            ROOT_URL,
            expected_type="text/html",
            limit=HTML_LIMIT,
            opener=opener,
        )
        self.assertEqual(result, valid_html())
        self.assertEqual(len(opener.requests), 1)
        request, timeout = opener.requests[0]
        headers = {name.lower(): value for name, value in request.header_items()}
        self.assertEqual(request.full_url, ROOT_URL)
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(timeout, 10)
        self.assertEqual(headers["accept-encoding"], "identity")
        self.assertNotIn("authorization", headers)
        self.assertNotIn("cookie", headers)

    def test_rejects_status_type_final_url_and_declared_size(self) -> None:
        cases = [
            FakeResponse(b"x", status=503),
            FakeResponse(b"x", content_type="application/json"),
            FakeResponse(b"x", url="https://evil.example/"),
            FakeResponse(b"x", content_length=str(HTML_LIMIT + 1)),
            FakeResponse(b"x", content_length="invalid"),
        ]
        for response in cases:
            with self.subTest(response=response), self.assertRaises(VerificationError):
                fetch_url(
                    ROOT_URL,
                    expected_type="text/html",
                    limit=HTML_LIMIT,
                    opener=FakeOpener(response),
                )

    def test_rejects_streamed_body_over_limit(self) -> None:
        with self.assertRaises(VerificationError):
            fetch_url(
                ROOT_URL,
                expected_type="text/html",
                limit=4,
                opener=FakeOpener(FakeResponse(b"12345")),
            )


class RootTests(unittest.TestCase):
    def test_accepts_reviewed_semantic_markers(self) -> None:
        verify_root(valid_html())

    def test_checked_in_root_matches_live_contract(self) -> None:
        root = Path(__file__).resolve().parents[1]
        verify_root((root / "index.html").read_bytes())

    def test_rejects_empty_invalid_utf8_and_missing_markers(self) -> None:
        for data in [b"", b"\xff", b"<html><body>missing</body></html>"]:
            with self.subTest(data=data), self.assertRaises(VerificationError):
                verify_root(data)

    def test_rejects_active_or_redirecting_content(self) -> None:
        extras = [
            '<base href="https://evil.example/">',
            "<form></form>",
            "<iframe></iframe>",
            '<img src="x" onerror="alert(1)">',
            '<svg onload="alert(1)"></svg>',
            '<meta http-equiv="refresh" content="0; url=https://evil.example">',
            '<script src="https://example.com/tracker.js"></script>',
            '<script src="//assets/js/jquery.js"></script>',
            '<script src="/cdn-cgi/scripts/loader.js"></script>',
            "<script>alert(1)</script>",
            '<img src="https://example.com/tracker.gif">',
            '<img srcset="local.jpg 1x, https://example.com/tracker.gif 2x">',
            '<link rel="stylesheet" href="https://example.com/tracker.css">',
            '<link rel="preload" href="//example.com/tracker.js">',
            '<video poster="//example.com/tracker.gif"></video>',
        ]
        for extra in extras:
            with self.subTest(extra=extra), self.assertRaises(VerificationError):
                verify_root(valid_html(extra))

    def test_rejects_changed_title_canonical_h1_and_resume_link(self) -> None:
        replacements = [
            (EXPECTED_TITLE, "Changed title"),
            (ROOT_URL, "https://example.com/"),
            (EXPECTED_H1, "Changed heading"),
            (EXPECTED_RESUME_PATH, "/different.pdf"),
        ]
        source = valid_html().decode()
        for old, new in replacements:
            with self.subTest(old=old), self.assertRaises(VerificationError):
                verify_root(source.replace(old, new).encode())


class ResumeTests(unittest.TestCase):
    def test_requires_exact_checked_in_pdf(self) -> None:
        data = b"%PDF-1.7\nreviewed\n%%EOF\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "resume.pdf"
            path.write_bytes(data)
            digest = verify_resume(data, path)
            self.assertEqual(len(digest), 64)
            for changed in [b"not-a-pdf", data + b"appended", b"%PDF-1.7\nother"]:
                with self.subTest(changed=changed), self.assertRaises(VerificationError):
                    verify_resume(changed, path)


if __name__ == "__main__":
    unittest.main()
