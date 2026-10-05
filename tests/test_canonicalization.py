"""Gate 3B: portable artifact-coordinate canonicalization.

These tests pin the serialization-boundary precision contract. They prove the
published artifact coordinates are bounded to a declared precision (so the
bytes are reproducible across platforms) while the underlying spatial analysis
keeps full double precision.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest
from shapely.geometry import shape

from geoimpact.artifacts import (
    GEOGRAPHIC_COORDINATE_DECIMALS,
    PROJECTED_COORDINATE_DECIMALS,
    canonical_coordinate,
    canonicalize_geojson_geometry,
)
from geoimpact.runner import run_from_config


ROOT = Path(__file__).resolve().parents[1]
BLOCK_CONFIG = ROOT / "tests" / "fixtures" / "geoimpact.yml"

_GEOMETRY_TYPES = {"Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon"}


def _coordinate_ordinates(node: object) -> list[float]:
    """Yield every numeric ordinate from every geometry embedded in ``node``."""
    ordinates: list[float] = []

    def walk_coordinates(coordinates: object) -> None:
        if isinstance(coordinates, list):
            for item in coordinates:
                walk_coordinates(item)
        else:
            assert isinstance(coordinates, (int, float))
            ordinates.append(float(coordinates))

    def walk(value: object) -> None:
        if isinstance(value, dict):
            if value.get("type") in _GEOMETRY_TYPES and "coordinates" in value:
                walk_coordinates(value["coordinates"])
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(node)
    return ordinates


def test_projected_report_coordinates_within_declared_precision(tmp_path: Path) -> None:
    run_from_config(BLOCK_CONFIG, tmp_path / "out")
    report = json.loads((tmp_path / "out" / "report.json").read_text(encoding="utf-8"))
    ordinates = _coordinate_ordinates(report)
    assert ordinates  # the fixture embeds geometry
    for ordinate in ordinates:
        assert ordinate == round(ordinate, PROJECTED_COORDINATE_DECIMALS)


def test_geographic_geojson_coordinates_within_declared_precision(tmp_path: Path) -> None:
    run_from_config(BLOCK_CONFIG, tmp_path / "out")
    geojson = json.loads(
        (tmp_path / "out" / "relationship-regressions.geojson").read_text(encoding="utf-8")
    )
    ordinates = _coordinate_ordinates(geojson)
    assert ordinates
    for ordinate in ordinates:
        assert ordinate == round(ordinate, GEOGRAPHIC_COORDINATE_DECIMALS)


def test_negative_zero_canonicalizes_to_positive_zero() -> None:
    result = canonical_coordinate(-0.0, PROJECTED_COORDINATE_DECIMALS)
    assert result == 0.0
    assert math.copysign(1.0, result) == 1.0  # not -0.0

    tiny_negative = canonical_coordinate(-0.0000000001, PROJECTED_COORDINATE_DECIMALS)
    assert tiny_negative == 0.0
    assert math.copysign(1.0, tiny_negative) == 1.0

    geometry = canonicalize_geojson_geometry(
        {"type": "Point", "coordinates": [-0.0, -0.00000001]}, PROJECTED_COORDINATE_DECIMALS
    )
    assert geometry["coordinates"] == [0.0, 0.0]
    assert json.dumps(geometry["coordinates"]) == "[0.0, 0.0]"  # no "-0.0" in bytes


def test_non_finite_coordinate_is_rejected() -> None:
    for bad in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(ValueError):
            canonical_coordinate(bad, PROJECTED_COORDINATE_DECIMALS)
    with pytest.raises(ValueError):
        canonicalize_geojson_geometry(
            {"type": "Point", "coordinates": [1.0, float("inf")]}, PROJECTED_COORDINATE_DECIMALS
        )


def test_canonicalization_preserves_type_order_and_non_coordinate_members() -> None:
    geometry = {
        "type": "Polygon",
        "coordinates": [[[1.123456789, 2.987654321], [3.5, 4.5], [1.123456789, 2.987654321]]],
        "extra": "unchanged",
    }
    result = canonicalize_geojson_geometry(geometry, PROJECTED_COORDINATE_DECIMALS)
    assert result["type"] == "Polygon"
    assert result["extra"] == "unchanged"
    assert result["coordinates"] == [[[1.123457, 2.987654], [3.5, 4.5], [1.123457, 2.987654]]]
    # ring closure (first == last) preserved
    assert result["coordinates"][0][0] == result["coordinates"][0][-1]


def test_canonicalization_touches_only_artifact_representation_not_analysis(tmp_path: Path) -> None:
    """V4 reports a valid fixed-grid footprint and preserves it at serialization."""
    report = run_from_config(BLOCK_CONFIG, tmp_path / "out")

    in_memory = shape(report["primary_change"]["changed_footprint_geometry"])
    assert in_memory.is_valid
    assert report["primary_change"]["changed_footprint_area_m2"] == in_memory.area

    serialized = json.loads((tmp_path / "out" / "report.json").read_text(encoding="utf-8"))
    assert serialized["report_version"] == "4"
    changed_footprint = shape(serialized["primary_change"]["changed_footprint_geometry"])
    assert changed_footprint.is_valid
    assert changed_footprint.equals(in_memory)
    serialized_ordinates = _coordinate_ordinates(serialized)
    for ordinate in serialized_ordinates:
        assert ordinate == round(ordinate, PROJECTED_COORDINATE_DECIMALS)
