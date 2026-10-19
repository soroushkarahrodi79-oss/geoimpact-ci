"""Fail-closed verification for a GeoImpact academic-demo static package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ALLOWLIST = HERE / "package-allowlist.json"
DEFAULT_PACKAGE = HERE / "academic-demo-dist"
EXPECTED_CASES = ["synthetic-block", "synthetic-pass", "synthetic-error"]
RELEASE = "45237d7caaea2aa4b81359e46f1623918645078c"

EXPECTED_HASHES = {
    "data/synthetic-block/districts_base.geojson": "fe2621c4defed71287355595ecd428fd8c1f7fddee822a37dddff4fe71b23837",
    "data/synthetic-block/districts_candidate.geojson": "a3ef49590971c5cf5dc45c33ece307d0d77d300f4aba374a6947e56b3198e19c",
    "data/synthetic-block/geoimpact.yml": "17d97b90f4484be8b4244651441b4d5eea35e2f953b630f34429334af14f5df1",
    "data/synthetic-block/hotels.geojson": "b92889469f7c14863963ec8242b86cd215497db13af4ea60f88ece81f77b06f4",
    "data/synthetic-block/tourism_pois.geojson": "ac93115affcf7db76f768785eb932b3d289a3d2da8d323f4d242566c96210257",
    "data/synthetic-block/report.json": "d09f70d2f7fa07cef3fa87f5b1fe73d932c8f9c4619487c4a0fe8c4cc1d7b8dd",
    "data/synthetic-block/report.md": "65ca9d67dd7ff59bc148fccc003354ea3201f51707f3e73ca2fd96dac208d95a",
    "data/synthetic-block/relationship-regressions.geojson": "a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978",
    "data/synthetic-pass/districts_base.geojson": "fe2621c4defed71287355595ecd428fd8c1f7fddee822a37dddff4fe71b23837",
    "data/synthetic-pass/districts_candidate.geojson": "a3ef49590971c5cf5dc45c33ece307d0d77d300f4aba374a6947e56b3198e19c",
    "data/synthetic-pass/geoimpact-pass.yml": "1ecd53d2f6ba5402d1e2f0b23de60749fa3d6de7224c10663e15685b19bca0a9",
    "data/synthetic-pass/hotels.geojson": "b92889469f7c14863963ec8242b86cd215497db13af4ea60f88ece81f77b06f4",
    "data/synthetic-pass/tourism_pois.geojson": "ac93115affcf7db76f768785eb932b3d289a3d2da8d323f4d242566c96210257",
    "data/synthetic-pass/report.json": "187e22c76d13de6902794c92d70e633fb98f9eb0c4f76f806a47709f498df5a4",
    "data/synthetic-pass/report.md": "ad19ab07fc9bdd8e62b6f9dd9d95d952e8d1fca1540e1dacd3443e0b6d60b1f7",
    "data/synthetic-pass/relationship-regressions.geojson": "a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978",
}

FORBIDDEN_DATA_MARKERS = [
    b"madrid-ine-sections-2024-2025",
    b"ine-sections-2024-focus.geojson",
    b"ine-sections-2025-focus.geojson",
    b"madrid-portals-change-footprint.geojson",
    b"sierra-de-baza-2015-2025",
    b"sierra-local",
    b"rediam-public-use-equipment",
]
SECRET_PATTERNS = [
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(rb"\bgh[oprsu]_[A-Za-z0-9]{20,}\b"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(rb"(?i)\b(client_secret|api_key|access_token|refresh_token)\s*[:=]\s*['\"][^'\"]+"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def package_files(root: Path) -> list[str]:
    files: list[str] = []
    for path in root.rglob("*"):
        require(not path.is_symlink(), f"Symlink is forbidden: {path}")
        if path.is_file():
            files.append(path.relative_to(root).as_posix())
    return sorted(files)


def verify_network_surface(root: Path) -> None:
    html = (root / "index.html").read_text(encoding="utf-8")
    scripts = "\n".join((root / name).read_text(encoding="utf-8") for name in ["app.js", "reader.js", "onboarding.js", "onboarding-copy.js"])
    styles = "\n".join((root / name).read_text(encoding="utf-8") for name in ["style.css", "onboarding.css"])
    require(not re.search(r"(?:src|href|action)\s*=\s*['\"]https?://", html, re.I), "External HTML request target")
    require(not re.search(r"(?:fetch|import)\s*\(\s*['\"]https?://", scripts, re.I), "External JavaScript request target")
    require(not re.search(r"\b(?:XMLHttpRequest|WebSocket|EventSource|sendBeacon)\b", scripts), "Unapproved network API")
    require(not re.search(r"(?:@import|url\s*\()\s*['\"]?https?://", styles, re.I), "External CSS request target")
    require(not re.search(r"google-analytics|googletagmanager|gtag\s*\(|segment\.com|plausible\.io|sentry\.io", html + scripts, re.I), "Analytics or tracking code")


def verify(root: Path) -> None:
    root = root.resolve()
    require(root.is_dir(), f"Package directory does not exist: {root}")
    allow = json.loads(ALLOWLIST.read_text(encoding="utf-8"))["files"]
    actual = package_files(root)
    require(actual == allow, f"Unexpected package files. Expected {allow}; got {actual}")

    manifest = json.loads((root / "package-manifest.json").read_text(encoding="utf-8"))
    require(manifest["cases"] == EXPECTED_CASES, "Package manifest case drift")
    require(manifest["engine_commit"] == RELEASE and manifest["report_version"] == "5", "Engine/report identity drift")
    require(sorted(manifest["files"]) == [name for name in allow if name != "package-manifest.json"], "Manifest coverage drift")
    for relative, expected in manifest["files"].items():
        path = root / relative
        require(digest(path) == expected["sha256"], f"Package hash mismatch: {relative}")
        require(path.stat().st_size == expected["size_bytes"], f"Package size mismatch: {relative}")
    for relative, expected in EXPECTED_HASHES.items():
        require(digest(root / relative) == expected, f"Frozen synthetic byte mismatch: {relative}")

    catalog_raw = (root / "catalog.json").read_bytes()
    catalog = json.loads(catalog_raw)
    require(catalog["studio_version"] == "0.1.0-academic-demo", "Catalog version drift")
    require([item["id"] for item in catalog["cases"]] == EXPECTED_CASES, "Catalog is not the exact synthetic allowlist")
    trust = (root / "trust.js").read_text(encoding="utf-8").strip()
    require(trust == f'export const catalogHash = "{hashlib.sha256(catalog_raw).hexdigest()}";', "Catalog trust anchor mismatch")

    for entry in catalog["cases"]:
        manifest_path = root / entry["path"]
        require(digest(manifest_path) == entry["sha256"], f"Case manifest mismatch: {entry['id']}")
        case = json.loads(manifest_path.read_text(encoding="utf-8"))
        if entry["id"] == "synthetic-error":
            require(case["kind"] == "analysis-error" and case["exit_code"] == 2, "ERROR contract drift")
            require("files" not in case and "verdict" not in case, "ERROR invents analysis output")
            continue
        report = json.loads((root / case["files"]["report.json"]["path"]).read_text(encoding="utf-8"))
        require(case["kind"] == "completed" and case["category"] == "synthetic", "Non-synthetic completed case")
        require(case["release_commit"] == RELEASE, "Case release identity drift")
        require(report["report_version"] == "5" and report["provenance"]["engine"]["geoimpact_ci"] == "1.2.0", "Report V5/engine drift")
        require(report["verdict"] == ("BLOCK" if entry["id"] == "synthetic-block" else "PASS"), "Verdict drift")
        require(len(report["relationship_regressions"]) == 2, "Synthetic regression count drift")

    for relative in actual:
        raw = (root / relative).read_bytes()
        lower = raw.lower()
        for marker in FORBIDDEN_DATA_MARKERS:
            require(marker not in lower, f"Excluded dataset reference in {relative}: {marker.decode()}")
        for pattern in SECRET_PATTERNS:
            require(not pattern.search(raw), f"Possible secret in {relative}: {pattern.pattern!r}")

    headers = (root / "_headers").read_text(encoding="utf-8")
    for required in ["connect-src 'self'", "Cache-Control: no-store", "X-Robots-Tag: noindex", "X-Frame-Options: DENY"]:
        require(required in headers, f"Missing security header: {required}")
    require((root / "robots.txt").read_text(encoding="utf-8") == "User-agent: *\nDisallow: /\n", "robots.txt drift")
    verify_network_surface(root)


def self_test() -> None:
    verify(DEFAULT_PACKAGE)
    with tempfile.TemporaryDirectory(prefix="academic-demo-verifier-") as temporary:
        copy = Path(temporary) / "package"
        shutil.copytree(DEFAULT_PACKAGE, copy)
        (copy / "unexpected.txt").write_text("must fail\n", encoding="utf-8")
        try:
            verify(copy)
        except ValueError as error:
            require("Unexpected package files" in str(error), "Unexpected-file failure was not specific")
        else:
            raise ValueError("Verifier accepted an unexpected file")

        (copy / "unexpected.txt").unlink()
        manifest_path = copy / "package-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["tamper_probe"] = FORBIDDEN_DATA_MARKERS[0].decode()
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        try:
            verify(copy)
        except ValueError as error:
            require("Excluded dataset reference" in str(error), "Excluded-data failure was not specific")
        else:
            raise ValueError("Verifier accepted an excluded-data reference")


def main() -> int:
    self_test_requested = len(sys.argv) == 2 and sys.argv[1] == "--self-test"
    target = Path(sys.argv[1]) if len(sys.argv) == 2 and not self_test_requested else DEFAULT_PACKAGE
    try:
        if self_test_requested:
            self_test()
        else:
            verify(target)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Academic demo package verification failed: {error}", file=sys.stderr)
        return 1
    suffix = " (fail-closed probes passed)" if self_test_requested else ""
    print(f"Academic demo package verified: {target.resolve()}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
