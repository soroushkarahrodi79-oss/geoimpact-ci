"""Bounded V5 display-readiness probe. No spatial predicates or policy execution.

This is NOT a viewer, a general schema validator, or permission to redistribute
source data. It reads the two retained cases and already-generated artifacts.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

CASES = {
    "madrid": {
        "directory": "research/madrid-ine-sections-2024-2025",
        "base": "ine-sections-2024-focus.geojson",
        "candidate": "ine-sections-2025-focus.geojson",
        "dependency": "madrid-portals-change-footprint.geojson",
        "expected": "tests/fixtures/madrid_benchmark_expected.json",
        "output": "madrid-benchmark",
    },
    "sierra": {
        "directory": "research/sierra-de-baza-2015-2025",
        "base": "base.geojson",
        "candidate": "candidate.geojson",
        "dependency": "dependencies.geojson",
        "expected": "research/sierra-de-baza-2015-2025/gate8_expected.json",
        "output": "gate8",
    },
}
ARTIFACTS = ("report.json", "report.md", "relationship-regressions.geojson")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    raw = path.read_bytes()
    return {"sha256": hashlib.sha256(raw).hexdigest(), "size_bytes": len(raw)}


def indexed_features(path, field, allowed):
    collection = read_json(path)
    require(collection["type"] == "FeatureCollection", "expected FeatureCollection")
    result = {}
    for feature in collection["features"]:
        identifier = feature["properties"][field]
        require(isinstance(identifier, str) and bool(identifier), "missing stable ID")
        require(identifier not in result, "duplicate stable ID")
        require(feature["geometry"]["type"] in allowed, "unsupported display geometry")
        result[identifier] = feature
    return result


def check_joins(report, base, candidate, dependencies, geojson):
    """Identity/property joins only; never determine within from coordinates."""
    require(report["report_version"] == "5", "V5 required; do not silently upgrade")
    require(report["analysis"]["crs"] == "EPSG:25830", "unsupported report CRS")
    require(report["verdict"] == report["policy"]["status"], "verdict mismatch")
    require(report["verdict"] in {"PASS", "BLOCK"}, "unsupported verdict")
    require(set(report["primary_change"]["feature_geometry_status"]) == set(base) | set(candidate),
            "primary ID universe mismatch")
    definitions = report["analysis"]["dependencies"]
    require(len(definitions) == 1, "probe is bounded to one dependency per retained case")
    dataset = definitions[0]["dataset"]
    require(definitions[0]["predicate"] == "within", "unsupported predicate")
    rows = {}
    for row in report["relationships"]:
        key = (row["dependent_dataset"], row["dependent_id"])
        require(key not in rows, "duplicate relationship")
        require(row["dependent_dataset"] == dataset, "unknown dependency dataset")
        require(row["dependent_id"] in dependencies, "dependency ID missing from input")
        require(row["predicate"] == "within", "unexpected row predicate")
        require(set(row["before"]) <= set(base), "BASE assignment references absent ID")
        require(set(row["after"]) <= set(candidate), "CANDIDATE assignment references absent ID")
        rows[key] = row
    require(len(rows) == len(dependencies), "dependent relationship coverage mismatch")
    regressions = report["relationship_regressions"]
    evidence = {}
    for row in regressions:
        key = (row["dependent_dataset"], row["dependent_id"])
        require(key in rows, "orphan regression")
        for field in ("before", "after", "change_type", "predicate"):
            require(row[field] == rows[key][field], "regression relationship mismatch")
        require(row["evidence_id"] not in evidence, "duplicate evidence ID")
        require(row["evidence_geometry_crs"] == "EPSG:25830", "wrong evidence CRS")
        require(row["evidence_geometry"]["type"] == "Point", "regression is not a point")
        evidence[row["evidence_id"]] = row
    require(set(report["policy"]["evidence_ids"]) == set(evidence), "policy evidence mismatch")
    require(report["policy"]["observed_value"] == len(regressions), "observed count mismatch")
    require(geojson["type"] == "FeatureCollection", "invalid regression GeoJSON")
    seen = set()
    for feature in geojson["features"]:
        props = feature["properties"]
        identifier = props["evidence_id"]
        require(identifier in evidence and identifier not in seen, "orphan or duplicate GeoJSON evidence")
        require(feature["geometry"]["type"] == "Point", "unexpected geographic geometry")
        for field, value in props.items():
            require(field in evidence[identifier] and evidence[identifier][field] == value,
                    "GeoJSON property mismatch")
        require(set(props) == {"evidence_id", "dependent_dataset", "dependent_id", "predicate",
                               "before", "after", "change_type"}, "GeoJSON property set mismatch")
        seen.add(identifier)
    require(seen == set(evidence), "missing GeoJSON evidence")
    for row in report["boundary_ambiguities"]:
        require((row["dependent_dataset"], row["dependent_id"]) in rows, "orphan boundary record")
        require(set(row["before_boundary_primary_ids"]) <= set(base), "boundary BASE ID absent")
        require(set(row["after_boundary_primary_ids"]) <= set(candidate), "boundary CANDIDATE ID absent")


def probe_case(repo, output_root, case):
    definition = CASES[case]
    source = repo / definition["directory"]
    output = output_root / definition["output"]
    expected = read_json(repo / definition["expected"])
    if case == "madrid":
        expected = expected["expected"]
    actual_hashes = {name: digest(output / name)["sha256"] for name in ARTIFACTS}
    require(actual_hashes == expected["output_sha256"], "frozen artifact hash mismatch")
    report = read_json(output / "report.json")
    inputs = report["provenance"]["inputs"]
    require(report["provenance"]["hash_algorithm"] == "sha256", "unsupported digest")
    require(report["provenance"]["engine"]["geoimpact_ci"] == "1.2.0", "wrong engine release")
    require(len(inputs["dependencies"]) == 1, "unexpected input dependencies")
    for name, identity in (("geoimpact.yml", inputs["config"]),
                           (definition["base"], inputs["primary"]["base"]),
                           (definition["candidate"], inputs["primary"]["candidate"]),
                           (definition["dependency"], inputs["dependencies"][0])):
        actual = digest(source / name)
        require(all(actual[key] == identity[key] for key in actual), "input byte identity mismatch: " + name)
    primary_id = report["analysis"]["primary_id_field"]
    dependent_id = report["analysis"]["dependencies"][0]["id_field"]
    base = indexed_features(source / definition["base"], primary_id, {"Polygon", "MultiPolygon"})
    candidate = indexed_features(source / definition["candidate"], primary_id, {"Polygon", "MultiPolygon"})
    dependencies = indexed_features(source / definition["dependency"], dependent_id, {"Point"})
    check_joins(report, base, candidate, dependencies,
                read_json(output / "relationship-regressions.geojson"))
    return {
        "verdict": report["verdict"],
        "input_features": {"base": len(base), "candidate": len(candidate), "dependencies": len(dependencies)},
        "relationship_records": len(report["relationships"]),
        "relationship_regressions": len(report["relationship_regressions"]),
        "boundary_ambiguities": len(report["boundary_ambiguities"]),
        "primary_status_counts": dict(sorted(Counter(report["primary_change"]["feature_geometry_status"].values()).items())),
        "policy": {key: report["policy"][key] for key in ("rule", "observed_value", "threshold", "status")},
        "max_boundary_displacement_m": report["primary_change"]["max_boundary_displacement_m"],
        "changed_footprint_area_m2": report["primary_change"]["changed_footprint_area_m2"],
        "engine": report["provenance"]["engine"],
        "artifact_sha256": actual_hashes,
        "artifact_bytes": {name: digest(output / name)["size_bytes"] for name in ARTIFACTS},
        "input_bytes": sum(digest(source / name)["size_bytes"] for name in
                           ("geoimpact.yml", definition["base"], definition["candidate"], definition["dependency"])),
        "checks": ["frozen artifact hashes", "V5 raw input identities", "primary ID universe",
                   "complete dependent ID joins", "before/after primary references",
                   "regression and policy evidence IDs", "GeoJSON evidence property joins"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="clean v1.2.0 checkout")
    parser.add_argument("--outputs", type=Path, required=True, help="its ci-output directory")
    args = parser.parse_args()
    try:
        cases = {case: probe_case(args.repo, args.outputs, case) for case in CASES}
    except (KeyError, OSError, TypeError, ValueError) as error:
        parser.exit(1, f"Probe rejected evidence: {error}\n")
    print(json.dumps({"probe_version": 1, "scope": "two retained V5 cases; no scientific recomputation",
                      "implementation_gate": "HOLD: Madrid reuse conditions unresolved",
                      "browser_validation": "not performed; no viewer implemented",
                      "cases": cases}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
