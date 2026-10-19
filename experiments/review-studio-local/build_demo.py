"""Build the deployable, synthetic-only static academic demo from an exact allowlist."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
WEB = HERE / "web"
HOST = HERE / "hosting" / "cloudflare"
OUTPUT = HERE / "academic-demo-dist"
ALLOWLIST = HERE / "package-allowlist.json"
MANIFEST = "package-manifest.json"
FROZEN_BASE = "4133c2262fb16546a0dd41f09dd5a6a92b64c100"
ENGINE_RELEASE = "45237d7caaea2aa4b81359e46f1623918645078c"


def identity(path: Path) -> dict[str, str | int]:
    raw = path.read_bytes()
    return {"sha256": hashlib.sha256(raw).hexdigest(), "size_bytes": len(raw)}


def write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    allow = json.loads(ALLOWLIST.read_text(encoding="utf-8"))["files"]
    if allow != sorted(allow) or len(allow) != len(set(allow)) or MANIFEST not in allow:
        raise ValueError("Package allowlist must be sorted, unique and include its manifest")
    catalog = json.loads((WEB / "catalog.json").read_text(encoding="utf-8"))
    case_ids = [item["id"] for item in catalog["cases"]]
    if case_ids != ["synthetic-block", "synthetic-pass", "synthetic-error"]:
        raise ValueError(f"Refusing non-synthetic catalog: {case_ids}")

    with tempfile.TemporaryDirectory(prefix="academic-demo-build-", dir=HERE) as temporary:
        stage = Path(temporary)
        for relative in allow:
            if relative == MANIFEST:
                continue
            if relative == "LICENSE.txt":
                source = REPO / "LICENSE"
            else:
                source = (HOST if relative in {"_headers", "robots.txt"} else WEB) / relative
            if not source.is_file() or source.is_symlink():
                raise FileNotFoundError(f"Allowlisted source is missing or unsafe: {source}")
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

        entries = {
            relative: identity(stage / relative)
            for relative in allow
            if relative != MANIFEST
        }
        write_json(
            stage / MANIFEST,
            {
                "schema_version": 1,
                "demo": "GeoImpact Review Studio — Private Academic Demo V1",
                "base_pr": 23,
                "base_commit": FROZEN_BASE,
                "engine_release": "GeoImpact CI 1.2.0",
                "engine_commit": ENGINE_RELEASE,
                "report_version": "5",
                "cases": case_ids,
                "runtime": "static files only; no Python server or analysis backend",
                "rights": "MIT repository code and synthetic fixtures only; no third-party media",
                "files": entries,
            },
        )

        from verify_package import verify

        verify(stage)
        if OUTPUT.exists():
            if OUTPUT.resolve().parent != HERE or OUTPUT.name != "academic-demo-dist":
                raise ValueError("Unsafe output path")
            shutil.rmtree(OUTPUT)
        shutil.copytree(stage, OUTPUT)
    verify(OUTPUT)
    print(f"Built and verified {len(allow)} allowlisted files in {OUTPUT}")


if __name__ == "__main__":
    main()
