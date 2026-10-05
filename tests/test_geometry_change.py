from pathlib import Path

import pytest
import shapely
from shapely.geometry import box, shape

from geoimpact.analysis import load_features
from geoimpact.geometry_change import (
    BOUNDARY_DISPLACEMENT_GRID_SIZE_M,
    CHANGE_FOOTPRINT_GRID_SIZE_M,
    measure_primary_change,
)
from geoimpact.relationships import derive_within_assignments


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


def test_change_footprint_uses_explicit_one_micrometre_grid() -> None:
    assert CHANGE_FOOTPRINT_GRID_SIZE_M == 1e-6


def test_displacement_uses_its_explicit_one_micrometre_grid() -> None:
    assert BOUNDARY_DISPLACEMENT_GRID_SIZE_M == 1e-6


def test_displacement_is_canonical_on_its_measurement_grid() -> None:
    base = {"section": box(0.12345641, 0, 1, 1)}
    candidate = {"section": box(0.12345649, 0, 1, 1)}

    result = measure_primary_change(base, candidate)

    assert result["changed_feature_ids"] == ["section"]
    assert result["max_boundary_displacement_m"] == 0.0


def test_displacement_is_independent_of_mapping_order() -> None:
    base = {"west": box(0, 0, 1, 1), "east": box(10, 0, 11, 1)}
    candidate = {"west": box(0, 0, 1.25, 1), "east": box(10, 0, 11.5, 1)}

    forward = measure_primary_change(base, candidate)["max_boundary_displacement_m"]
    reverse = measure_primary_change(
        dict(reversed(list(base.items()))),
        dict(reversed(list(candidate.items()))),
    )["max_boundary_displacement_m"]

    assert forward == reverse == 0.5


def test_sub_grid_boundary_variations_have_the_same_canonical_footprint() -> None:
    base = {"section": box(0, 0, 1, 1)}
    candidate_a = {"section": box(0, 0, 1.0000021, 1)}
    candidate_b = {"section": box(0, 0, 1.0000022, 1)}

    footprint_a = measure_primary_change(base, candidate_a)["changed_footprint_geometry"]
    footprint_b = measure_primary_change(base, candidate_b)["changed_footprint_geometry"]

    assert footprint_a == footprint_b


def test_normalized_multipart_footprint_is_stable_to_input_order() -> None:
    base = {
        "west": box(0, 0, 1, 1),
        "east": box(10, 0, 11, 1),
    }
    candidate = {
        "west": box(0, 0, 1.25, 1),
        "east": box(10, 0, 11.25, 1),
    }

    forward = measure_primary_change(base, candidate)["changed_footprint_geometry"]
    reverse = measure_primary_change(
        dict(reversed(list(base.items()))),
        dict(reversed(list(candidate.items()))),
    )["changed_footprint_geometry"]

    assert shape(forward).geom_type == "MultiPolygon"
    assert forward == reverse


def test_changed_footprint_area_is_measured_from_its_fixed_precision_geometry() -> None:
    result = measure_primary_change(
        {"section": box(0, 0, 1, 1)},
        {"section": box(0, 0, 1.125, 1)},
    )

    assert result["changed_footprint_area_m2"] == shape(
        result["changed_footprint_geometry"]
    ).area


def test_fixed_precision_overlay_does_not_mutate_source_geometries() -> None:
    base_geometry = box(0, 0, 1.0000004, 1)
    candidate_geometry = box(0, 0, 1.1250004, 1)
    base = {"section": base_geometry}
    candidate = {"section": candidate_geometry}
    original_base_wkb = base_geometry.wkb
    original_candidate_wkb = candidate_geometry.wkb

    measure_primary_change(base, candidate)

    assert base_geometry.wkb == original_base_wkb
    assert candidate_geometry.wkb == original_candidate_wkb


def test_relationship_within_assignments_keep_full_precision() -> None:
    dependent = {"portal": shapely.Point(1e-7, 0.5)}
    base = {"section": box(0, 0, 1, 1)}
    candidate = {"section": box(2e-7, 0, 1.0000002, 1)}

    before = derive_within_assignments(dependent, base)
    after = derive_within_assignments(dependent, candidate)
    measure_primary_change(base, candidate)
    after_measurement = derive_within_assignments(dependent, candidate)

    assert before["portal"]["within"] == ["section"]
    assert after["portal"]["within"] == []
    assert after_measurement == after
