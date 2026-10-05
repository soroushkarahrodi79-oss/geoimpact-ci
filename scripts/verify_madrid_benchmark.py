"""Run and verify the frozen Madrid real-world regression benchmark."""

from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

from shapely.geometry import shape


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "tests/fixtures/madrid_benchmark_expected.json"
OUTPUT_DIR = ROOT / "ci-output/madrid-benchmark"
OUTPUT_NAMES = (
    "report.json",
    "report.md",
    "relationship-regressions.geojson",
)


def canonical_json_sha256(value: Any) -> str:
    """Hash JSON data independent of object-key order and whitespace."""
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def transition_histogram(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return a stable old-CUSEC/new-CUSEC count list from CLI relationships."""
    counts: Counter[tuple[str, str]] = Counter()
    for record in records:
        before = record.get("before", [])
        after = record.get("after", [])
        if len(before) != 1 or len(after) != 1:
            continue
        counts[(str(before[0]), str(after[0]))] += 1
    return [
        {"from": old, "to": new, "count": count}
        for (old, new), count in sorted(counts.items())
    ]


def validate_transition_manifest(
    actual: list[dict[str, Any]], expected: list[dict[str, Any]]
) -> None:
    """Raise with a useful diff when observed old/new counts drift."""
    if actual != expected:
        raise AssertionError(
            "transition histogram mismatch\n"
            f"expected: {json.dumps(expected, separators=(',', ':'))}\n"
            f"actual:   {json.dumps(actual, separators=(',', ':'))}"
        )


def relationship_identity_digest(records: list[dict[str, str]]) -> str:
    """Hash sorted portal/old/new/classification identity projections."""
    ordered = sorted(
        records,
        key=lambda item: (
            item["portal_id"],
            item["old_cusec"],
            item["new_cusec"],
            item["classification"],
        ),
    )
    return canonical_json_sha256(ordered)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _check_input_hashes(manifest: dict[str, Any]) -> dict[str, str]:
    actual: dict[str, str] = {}
    for relative, expected in manifest["inputs"].items():
        path = ROOT / relative
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        actual[relative] = observed
        if observed != expected:
            raise AssertionError(
                f"input hash drift for {relative}: expected {expected}, got {observed}"
            )
    return actual


def _load_primary_features(path: Path) -> dict[str, Any]:
    collection = _read_json(path)
    features: dict[str, Any] = {}
    for feature in collection["features"]:
        feature_id = feature["properties"]["cusec"]
        features[feature_id] = shape(feature["geometry"])
    return features


def _classify_relationships(
    records: list[dict[str, Any]], base: dict[str, Any], candidate: dict[str, Any]
) -> tuple[list[dict[str, str]], Counter[str]]:
    retained = base.keys() & candidate.keys()
    changed_retained = {
        feature_id
        for feature_id in retained
        if not base[feature_id].equals(candidate[feature_id])
    }
    identities: list[dict[str, str]] = []
    counts: Counter[str] = Counter()

    for record in records:
        before = record.get("before", [])
        after = record.get("after", [])
        if len(before) != 1 or len(after) != 1:
            counts["unclassified"] += 1
            continue
        old, new = str(before[0]), str(after[0])
        if (
            old in base
            and old in candidate
            and old in changed_retained
            and new not in base
            and new in candidate
        ):
            classification = "split-like"
        elif (
            old in base
            and old not in candidate
            and new in base
            and new in candidate
            and new in changed_retained
        ):
            classification = "merge-like"
        else:
            classification = "unclassified"
        counts[classification] += 1
        if old in retained and new in retained:
            counts["both_retained"] += 1
            if old != new and old not in changed_retained and new not in changed_retained:
                counts["pure_id_only"] += 1
        identities.append(
            {
                "portal_id": str(record["dependent_id"]),
                "old_cusec": old,
                "new_cusec": new,
                "classification": classification,
            }
        )
    return identities, counts


def _assert_equal(label: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def verify_report_and_outputs(
    report: dict[str, Any], manifest: dict[str, Any], output_dir: Path
) -> dict[str, Any]:
    expected = manifest["expected"]
    relationships = report["relationships"]
    regressions = report["relationship_regressions"]
    histogram = transition_histogram(relationships)
    validate_transition_manifest(histogram, manifest["transitions"])

    base = _load_primary_features(
        ROOT / "research/madrid-ine-sections-2024-2025/ine-sections-2024-focus.geojson"
    )
    candidate = _load_primary_features(
        ROOT / "research/madrid-ine-sections-2024-2025/ine-sections-2025-focus.geojson"
    )
    identity_records, classes = _classify_relationships(relationships, base, candidate)

    _assert_equal("verdict", report["verdict"], expected["verdict"])
    _assert_equal("relationship records", len(regressions), expected["relationship_records"])
    _assert_equal("relationship list records", len(relationships), expected["relationship_records"])
    _assert_equal(
        "assignment_changed",
        sum(item["change_type"] == "assignment_changed" for item in relationships),
        expected["assignment_changed"],
    )
    _assert_equal(
        "gained",
        sum(not item.get("before") and bool(item.get("after")) for item in relationships),
        expected["gained"],
    )
    _assert_equal(
        "lost",
        sum(bool(item.get("before")) and not item.get("after") for item in relationships),
        expected["lost"],
    )
    _assert_equal(
        "boundary ambiguities",
        len(report["boundary_ambiguities"]),
        expected["boundary_ambiguities"],
    )
    _assert_equal("split-like", classes["split-like"], expected["split_like"])
    _assert_equal("merge-like", classes["merge-like"], expected["merge_like"])
    _assert_equal(
        "both IDs retained across both versions",
        classes["both_retained"],
        expected["both_ids_retained_across_both_versions"],
    )
    _assert_equal(
        "pure ID-only/renumbering",
        classes["pure_id_only"],
        expected["pure_id_only_renumbering"],
    )
    _assert_equal(
        "unclassified transition patterns",
        classes["unclassified"],
        expected["unclassified_transition_patterns"],
    )

    identity_digest = relationship_identity_digest(identity_records)
    _assert_equal(
        "relationship identity SHA-256",
        identity_digest,
        expected["relationship_identity_sha256"],
    )
    evidence_ids = sorted(item["evidence_id"] for item in regressions)
    _assert_equal("evidence ID count", len(evidence_ids), expected["evidence_id_count"])
    _assert_equal("unique evidence IDs", len(set(evidence_ids)), len(evidence_ids))
    evidence_digest = canonical_json_sha256(evidence_ids)
    _assert_equal(
        "evidence ID SHA-256", evidence_digest, expected["evidence_id_sha256"]
    )
    _assert_equal("policy verdict", report["policy"]["status"], expected["verdict"])
    _assert_equal(
        "policy evidence IDs", report["policy"]["evidence_ids"], evidence_ids
    )

    output_hashes: dict[str, str] = {}
    for name in OUTPUT_NAMES:
        observed = hashlib.sha256((output_dir / name).read_bytes()).hexdigest()
        output_hashes[name] = observed
        _assert_equal(f"output hash {name}", observed, expected["output_sha256"][name])

    return {
        "relationship_records": len(regressions),
        "transition_pairs": len(histogram),
        "transitions": histogram,
        "split_like": classes["split-like"],
        "merge_like": classes["merge-like"],
        "gained": expected["gained"],
        "lost": expected["lost"],
        "relationship_identity_sha256": identity_digest,
        "evidence_id_sha256": evidence_digest,
        "output_sha256": output_hashes,
    }


def _remove_previous_outputs(output_dir: Path) -> None:
    if output_dir.exists():
        unknown = {item.name for item in output_dir.iterdir()} - set(OUTPUT_NAMES)
        if unknown:
            raise RuntimeError(
                f"refusing to clean unexpected files in {output_dir}: {sorted(unknown)}"
            )
        for name in OUTPUT_NAMES:
            path = output_dir / name
            if path.exists():
                path.unlink()
    output_dir.mkdir(parents=True, exist_ok=True)


def run_benchmark() -> dict[str, Any]:
    manifest = _read_json(MANIFEST_PATH)
    input_hashes = _check_input_hashes(manifest)
    _remove_previous_outputs(OUTPUT_DIR)

    cli = shutil.which("geoimpact")
    if not cli:
        raise RuntimeError("installed geoimpact console entry point is not on PATH")
    command = [
        cli,
        "analyze",
        "--config",
        str(ROOT / "research/madrid-ine-sections-2024-2025/geoimpact.yml"),
        "--out",
        str(OUTPUT_DIR),
    ]
    started = time.perf_counter()
    result = subprocess.run(command, cwd=ROOT, check=False)
    duration_seconds = time.perf_counter() - started
    if result.returncode != 1:
        raise AssertionError(
            f"installed CLI exit mismatch: expected 1 (BLOCK), got {result.returncode}"
        )

    missing = [name for name in OUTPUT_NAMES if not (OUTPUT_DIR / name).is_file()]
    if missing:
        raise AssertionError(f"CLI did not produce expected artifacts: {missing}")
    report = _read_json(OUTPUT_DIR / "report.json")
    summary = verify_report_and_outputs(report, manifest, OUTPUT_DIR)
    summary.update(
        {
            "cli_exit": result.returncode,
            "duration_seconds": round(duration_seconds, 3),
            "os": platform.system(),
            "python": platform.python_version(),
            "input_sha256": input_hashes,
        }
    )
    return summary


def main() -> int:
    try:
        summary = run_benchmark()
    except Exception as exc:  # print one concise actionable failure for CI logs
        print(f"Madrid benchmark FAILED: {exc}", file=sys.stderr)
        return 1
    print("Madrid real-world benchmark PASS")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
