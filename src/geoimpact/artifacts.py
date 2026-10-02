"""Canonical report and deterministic derived Gate 2 artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform


_ANALYSIS_TO_CRS84 = Transformer.from_crs(
    "EPSG:25830", "OGC:CRS84", always_xy=True
)


def canonical_json_bytes(value: Any) -> bytes:
    """UTF-8, sorted keys, two-space indentation, finite floats, final LF."""
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")


def build_report(contract: dict[str, Any], analysis_result: dict[str, Any]) -> dict[str, Any]:
    dependencies = [
        {
            "dataset": dependency["dataset"],
            "id_field": dependency["id_field"],
            "predicate": dependency["predicate"],
        }
        for dependency in contract["dependencies"]
    ]
    regressions = sorted(
        analysis_result["relationship_regressions"],
        key=lambda item: (item["dependent_dataset"], item["dependent_id"]),
    )
    relationships = sorted(
        analysis_result["relationships"],
        key=lambda item: (item["dependent_dataset"], item["dependent_id"]),
    )
    boundaries = sorted(
        analysis_result["boundary_ambiguities"],
        key=lambda item: (item["dependent_dataset"], item["dependent_id"]),
    )
    policy = analysis_result["policy"]
    return {
        "report_version": "1",
        "analysis": {
            "crs": contract["analysis_crs"],
            "primary_dataset": contract["primary"]["dataset"],
            "primary_id_field": contract["primary"]["id_field"],
            "dependencies": dependencies,
        },
        "primary_change": analysis_result["primary_geometry_change"],
        "relationships": relationships,
        "relationship_regressions": regressions,
        "boundary_ambiguities": boundaries,
        "policy": policy,
        "verdict": policy["status"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    """Render the reviewer summary solely from the canonical report object."""
    change = report["primary_change"]
    policy = report["policy"]
    lines = [
        "# GeoImpact CI",
        "",
        f"**Analysis verdict: {report['verdict']}**",
        "",
        "## Primary change",
        "",
        f"- Modified primary features: {', '.join(change['changed_feature_ids']) or 'none'}",
        f"- Changed footprint area: {change['changed_footprint_area_m2']} m²",
        f"- Maximum boundary displacement: {change['max_boundary_displacement_m']} m",
        "",
        "## Relationship regressions",
        "",
    ]
    if report["relationship_regressions"]:
        for item in report["relationship_regressions"]:
            before = ", ".join(item["before"]) or "none"
            after = ", ".join(item["after"]) or "none"
            lines.append(
                f"- {item['dependent_dataset']} / {item['dependent_id']}: {before} -> {after}"
            )
    else:
        lines.append("- none")
    lines += [
        "",
        "## Policy",
        "",
        f"- Rule: {policy['rule']}",
        f"- Observed: {policy['observed_value']}",
        f"- Threshold: {policy['threshold']}",
        f"- Status: {policy['status']}",
        "",
        "## Evidence IDs",
        "",
    ]
    lines.extend(
        f"- {item['evidence_id']}" for item in report["relationship_regressions"]
    )
    if not report["relationship_regressions"]:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def build_relationship_geojson(report: dict[str, Any]) -> dict[str, Any]:
    features: list[dict[str, Any]] = []
    for item in report["relationship_regressions"]:
        analysis_geometry = shape(item["evidence_geometry"])
        crs84_geometry = transform(_ANALYSIS_TO_CRS84.transform, analysis_geometry)
        features.append(
            {
                "type": "Feature",
                "geometry": mapping(crs84_geometry),
                "properties": {
                    "evidence_id": item["evidence_id"],
                    "dependent_dataset": item["dependent_dataset"],
                    "dependent_id": item["dependent_id"],
                    "predicate": item["predicate"],
                    "before": item["before"],
                    "after": item["after"],
                    "change_type": item["change_type"],
                },
            }
        )
    features.sort(
        key=lambda feature: (
            feature["properties"]["dependent_dataset"],
            feature["properties"]["dependent_id"],
        )
    )
    return {"type": "FeatureCollection", "features": features}


def write_artifacts(report: dict[str, Any], output_directory: str | Path) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "report.json": output / "report.json",
        "report.md": output / "report.md",
        "relationship-regressions.geojson": output / "relationship-regressions.geojson",
    }
    paths["report.json"].write_bytes(canonical_json_bytes(report))
    paths["report.md"].write_text(render_markdown(report), encoding="utf-8", newline="\n")
    paths["relationship-regressions.geojson"].write_bytes(
        canonical_json_bytes(build_relationship_geojson(report))
    )
    return paths
