"""Canonical report and deterministic derived Gate 2 artifacts."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform

from geoimpact.models import AnalysisResult, GeoImpactContract, GeoImpactReport


_ANALYSIS_TO_CRS84 = Transformer.from_crs(
    "EPSG:25830", "OGC:CRS84", always_xy=True
)

# Artifact-coordinate serialization precision (representation only, NOT the
# precision or accuracy of the source data or the analysis). Scientific
# computation runs at full double precision; coordinates are rounded solely
# when they cross the published-artifact boundary, so artifact bytes are
# reproducible across operating systems whose libm differs in the low-order
# digits of CRS transformations. See decision log D-022.
PROJECTED_COORDINATE_DECIMALS = 6  # EPSG:25830 metres -> 1e-6 m (one micrometre)
GEOGRAPHIC_COORDINATE_DECIMALS = 8  # OGC:CRS84 degrees -> ~mm-scale in Madrid

_GEOMETRY_TYPES = frozenset(
    {
        "Point",
        "MultiPoint",
        "LineString",
        "MultiLineString",
        "Polygon",
        "MultiPolygon",
    }
)


def canonical_coordinate(value: Any, decimals: int) -> float:
    """Round one coordinate ordinate; normalize ``-0.0`` and reject non-finite."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"coordinate ordinate must be a real number, got {value!r}")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"coordinate ordinate must be finite, got {number!r}")
    rounded = round(number, decimals)
    if rounded == 0.0:
        rounded = 0.0  # collapse -0.0 to a single canonical zero
    return rounded


def _canonicalize_coordinates(coordinates: Any, decimals: int) -> Any:
    """Recursively round a GeoJSON coordinate array, preserving its structure."""
    if isinstance(coordinates, (list, tuple)):
        return [_canonicalize_coordinates(item, decimals) for item in coordinates]
    return canonical_coordinate(coordinates, decimals)


def canonicalize_geojson_geometry(geometry: Any, decimals: int) -> Any:
    """Return a geometry mapping with coordinates rounded to ``decimals`` places.

    Geometry type, coordinate ordering, and topology representation are
    preserved; only numeric ordinates are rounded. Non-coordinate members are
    left untouched. ``None`` (an absent geometry) passes through unchanged.
    """
    if geometry is None:
        return None
    if not isinstance(geometry, dict) or "type" not in geometry:
        raise ValueError("geometry must be a GeoJSON mapping with a type member")
    result = dict(geometry)
    if "coordinates" in geometry:
        result["coordinates"] = _canonicalize_coordinates(geometry["coordinates"], decimals)
    return result


def _canonicalize_report_geometry(value: Any, decimals: int) -> Any:
    """Deep-copy-walk a report object, rounding every embedded geometry only.

    Scalar scientific measurements (areas, displacements, counts, thresholds)
    are not inside geometry mappings and are therefore never rounded here.
    """
    if isinstance(value, dict):
        if value.get("type") in _GEOMETRY_TYPES and "coordinates" in value:
            return canonicalize_geojson_geometry(value, decimals)
        return {key: _canonicalize_report_geometry(item, decimals) for key, item in value.items()}
    if isinstance(value, list):
        return [_canonicalize_report_geometry(item, decimals) for item in value]
    return value


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


def build_report(
    contract: GeoImpactContract, analysis_result: AnalysisResult
) -> GeoImpactReport:
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
        "report_version": "4",
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


def render_markdown(report: GeoImpactReport) -> str:
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
        f"- Changed primary features: {', '.join(change['changed_feature_ids']) or 'none'}",
        f"- Added primary features: {', '.join(change['added_feature_ids']) or 'none'}",
        f"- Removed primary features: {', '.join(change['removed_feature_ids']) or 'none'}",
        f"- Modified primary features: {', '.join(change['modified_feature_ids']) or 'none'}",
        f"- Changed footprint area: {change['changed_footprint_area_m2']} m²",
        f"- Maximum boundary displacement (modified shared IDs only): {change['max_boundary_displacement_m']} m",
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


def build_relationship_geojson(report: GeoImpactReport) -> dict[str, Any]:
    features: list[dict[str, Any]] = []
    for item in report["relationship_regressions"]:
        analysis_geometry = shape(item["evidence_geometry"])
        # The inverse CRS transform runs on the full-precision projected
        # geometry; only its CRS84 output is rounded for serialization.
        crs84_geometry = transform(_ANALYSIS_TO_CRS84.transform, analysis_geometry)
        geometry = canonicalize_geojson_geometry(
            mapping(crs84_geometry), GEOGRAPHIC_COORDINATE_DECIMALS
        )
        features.append(
            {
                "type": "Feature",
                "geometry": geometry,
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


def write_artifacts(report: GeoImpactReport, output_directory: str | Path) -> dict[str, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "report.json": output / "report.json",
        "report.md": output / "report.md",
        "relationship-regressions.geojson": output / "relationship-regressions.geojson",
    }
    # report.json embeds EPSG:25830 geometry; round only those coordinates for
    # serialization. The in-memory report keeps full precision, so the geojson
    # inverse transform below still runs on unrounded projected geometry.
    report_for_json = _canonicalize_report_geometry(report, PROJECTED_COORDINATE_DECIMALS)
    paths["report.json"].write_bytes(canonical_json_bytes(report_for_json))
    paths["report.md"].write_text(render_markdown(report), encoding="utf-8", newline="\n")
    paths["relationship-regressions.geojson"].write_bytes(
        canonical_json_bytes(build_relationship_geojson(report))
    )
    return paths
