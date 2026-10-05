"""Run the frozen Gate 8 case and compare it with an exhaustive reference."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

from pyproj import Transformer
from shapely.geometry import shape
from shapely.ops import transform


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "research/sierra-de-baza-2015-2025"
EXPECTED = json.loads((CASE / "gate8_expected.json").read_text(encoding="utf-8"))
OUT = ROOT / "ci-output/gate8"
ARTIFACTS = ("report.json", "report.md", "relationship-regressions.geojson")


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_features(path: Path, id_field: str, project) -> dict[str, Any]:
    collection = json.loads(path.read_text(encoding="utf-8"))
    features: dict[str, Any] = {}
    for feature in collection["features"]:
        identifier = str(feature["properties"][id_field])
        check(identifier not in features, f"duplicate stable ID {identifier} in {path}")
        features[identifier] = transform(project, shape(feature["geometry"]))
    return features


def exhaustive_assignments(dependencies, primary):
    """All-pairs exact GEOS reference; deliberately independent of STRtree."""
    rows = []
    boundaries = []
    for dependent_id in sorted(dependencies):
        geometry = dependencies[dependent_id]
        within = sorted(primary_id for primary_id, polygon in primary.items() if geometry.within(polygon))
        touches = sorted(primary_id for primary_id, polygon in primary.items() if geometry.touches(polygon))
        rows.append(
            {
                "dependent_dataset": "rediam-public-use-equipment-reference-2026-10-05",
                "dependent_id": dependent_id,
                "predicate": "within",
                "before": within,
                "after": within,
                "change_type": "unchanged",
            }
        )
        if touches:
            boundaries.append(
                {
                    "dependent_dataset": "rediam-public-use-equipment-reference-2026-10-05",
                    "dependent_id": dependent_id,
                    "before_boundary_primary_ids": touches,
                    "after_boundary_primary_ids": touches,
                }
            )
    return rows, boundaries


def main() -> None:
    observed_inputs = {}
    for relative, expected_hash in EXPECTED["inputs"].items():
        path = ROOT / relative
        observed_inputs[relative] = sha256(path)
        check(observed_inputs[relative] == expected_hash, f"input hash mismatch: {relative}")

    cli = os.environ.get("GEOIMPACT_CLI") or shutil.which("geoimpact")
    check(bool(cli), "installed geoimpact console script was not found")
    OUT.mkdir(parents=True, exist_ok=True)
    command = [
        cli,
        "analyze",
        "--config",
        str(CASE / "geoimpact.yml"),
        "--out",
        str(OUT),
    ]
    started = time.perf_counter()
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    runtime_seconds = time.perf_counter() - started
    check(completed.returncode == 0, f"installed CLI exit {completed.returncode}: {completed.stderr}")

    report = json.loads((OUT / "report.json").read_text(encoding="utf-8"))
    check(report["report_version"] == EXPECTED["report_version"], "report version drift")
    check(report["verdict"] == EXPECTED["verdict"], "CLI verdict drift")
    check(len(report["relationships"]) == EXPECTED["relationship_count"], "relationship count drift")
    check(len(report["relationship_regressions"]) == EXPECTED["relationship_regression_count"], "regression count drift")
    check(len(report["boundary_ambiguities"]) == EXPECTED["boundary_ambiguity_count"], "boundary count drift")

    input_crs = Transformer.from_crs("OGC:CRS84", "EPSG:25830", always_xy=True).transform
    base = read_features(CASE / "base.geojson", "CODIGOESPA", input_crs)
    candidate = read_features(CASE / "candidate.geojson", "CODIGOESPA", input_crs)
    dependencies = read_features(CASE / "dependencies.geojson", "CODIGOEQUI", input_crs)
    reference_rows, reference_boundaries = exhaustive_assignments(dependencies, base)
    candidate_rows, candidate_boundaries = exhaustive_assignments(dependencies, candidate)
    reference_by_id = {row["dependent_id"]: row for row in reference_rows}
    candidate_by_id = {row["dependent_id"]: row for row in candidate_rows}
    for row in reference_by_id.values():
        row["after"] = candidate_by_id[row["dependent_id"]]["before"]
        before = row["before"]
        after = row["after"]
        row["change_type"] = (
            "unchanged" if before == after else
            "assignment_changed" if before and after else
            "assignment_lost" if before else
            "assignment_gained"
        )
    boundaries_by_id = {
        row["dependent_id"]: row for row in reference_boundaries + candidate_boundaries
    }
    combined_boundaries = []
    for dependent_id in sorted(set(boundaries_by_id)):
        base_touch = next(
            (row["before_boundary_primary_ids"] for row in reference_boundaries if row["dependent_id"] == dependent_id),
            [],
        )
        cand_touch = next(
            (row["before_boundary_primary_ids"] for row in candidate_boundaries if row["dependent_id"] == dependent_id),
            [],
        )
        combined_boundaries.append(
            {
                "dependent_dataset": "rediam-public-use-equipment-reference-2026-10-05",
                "dependent_id": dependent_id,
                "before_boundary_primary_ids": base_touch,
                "after_boundary_primary_ids": cand_touch,
            }
        )
    check(report["relationships"] == list(reference_by_id.values()), "indexed CLI relationships differ from exhaustive all-pairs reference")
    check(report["boundary_ambiguities"] == combined_boundaries, "boundary results differ from exhaustive all-pairs reference")

    type_counts = Counter(row["change_type"] for row in report["relationships"])
    observed_types = {
        "unchanged": type_counts["unchanged"],
        "assignment_changed": type_counts["assignment_changed"],
        "assignment_gained": type_counts["assignment_gained"],
        "assignment_lost": type_counts["assignment_lost"],
    }
    check(observed_types == EXPECTED["change_type_counts"], "change-type counts drift")
    transitions = Counter(
        (tuple(row["before"]), tuple(row["after"])) for row in report["relationships"]
    )
    histogram = [
        {"from": list(before), "to": list(after), "count": count}
        for (before, after), count in sorted(transitions.items())
    ]
    check(histogram == EXPECTED["transition_histogram"], "transition histogram drift")

    identity_projection = [
        {
            "dependent_id": row["dependent_id"],
            "before": row["before"],
            "after": row["after"],
            "change_type": row["change_type"],
        }
        for row in report["relationships"]
    ]
    identity_projection.sort(
        key=lambda row: (row["dependent_id"], row["before"], row["after"], row["change_type"])
    )
    identity_digest = canonical_sha256(identity_projection)
    evidence_ids = sorted(row["evidence_id"] for row in report["relationship_regressions"])
    evidence_digest = canonical_sha256(evidence_ids)
    check(identity_digest == EXPECTED["relationship_identity_sha256"], "relationship identity digest drift")
    check(evidence_digest == EXPECTED["evidence_id_sha256"], "evidence ID digest drift")

    output_hashes = {name: sha256(OUT / name) for name in ARTIFACTS}
    check(
        output_hashes == EXPECTED["output_sha256"],
        "artifact output hash drift: "
        + json.dumps(
            {"expected": EXPECTED["output_sha256"], "observed": output_hashes},
            sort_keys=True,
        ),
    )
    result = {
        "cli_exit": completed.returncode,
        "cli_runtime_seconds": runtime_seconds,
        "report_version": report["report_version"],
        "verdict": report["verdict"],
        "relationships": len(report["relationships"]),
        "regressions": len(report["relationship_regressions"]),
        "boundary_ambiguities": len(report["boundary_ambiguities"]),
        "exhaustive_reference": "exact equality",
        "relationship_identity_sha256": identity_digest,
        "evidence_id_sha256": evidence_digest,
        "output_sha256": output_hashes,
        "runtime": sys.platform,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
