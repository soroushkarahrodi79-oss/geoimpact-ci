from pathlib import Path

import pytest

from geoimpact.analysis import load_features
from geoimpact.geometry_change import measure_primary_change


FIXTURES = Path(__file__).parent / "fixtures"


def test_controlled_boundary_mutation_has_documented_measurements() -> None:
    base = load_features(FIXTURES / "districts_base.geojson", "district_id")
    candidate = load_features(FIXTURES / "districts_candidate.geojson", "district_id")

    result = measure_primary_change(base, candidate)

    assert result["changed_feature_ids"] == ["chamberi", "tetuan"]
    assert result["changed_footprint_area_m2"] == pytest.approx(8000.0, abs=1e-6)
    assert result["max_boundary_displacement_m"] == pytest.approx(40.0, abs=1e-6)


def test_identical_primary_geometries_have_no_change_footprint() -> None:
    base = load_features(FIXTURES / "districts_base.geojson", "district_id")

    result = measure_primary_change(base, base)

    assert result == {
        "feature_geometry_status": {"chamberi": "unchanged", "tetuan": "unchanged"},
        "changed_feature_ids": [],
        "changed_footprint_area_m2": 0.0,
        "changed_footprint_geometry": None,
        "max_boundary_displacement_m": 0.0,
    }
