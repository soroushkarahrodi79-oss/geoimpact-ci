from pathlib import Path

from geoimpact.analysis import analyze, load_features
from geoimpact.relationships import derive_within_assignments


FIXTURES = Path(__file__).parent / "fixtures"


def test_controlled_mutation_reassigns_declared_dependents() -> None:
    result = analyze(
        FIXTURES / "districts_base.geojson",
        FIXTURES / "districts_candidate.geojson",
        {
            "hotels": (FIXTURES / "hotels.geojson", "hotel_id"),
            "tourism_pois": (FIXTURES / "tourism_pois.geojson", "poi_id"),
        },
        relationship_threshold=1,
    )

    regressions = result["relationship_regressions"]
    assert [(item["dependent_dataset"], item["dependent_id"]) for item in regressions] == [
        ("hotels", "hotel_813"),
        ("tourism_pois", "poi_212"),
    ]
    assert all(item["before"] == ["chamberi"] for item in regressions)
    assert all(item["after"] == ["tetuan"] for item in regressions)
    assert all(item["change_type"] == "assignment_changed" for item in regressions)
    assert all(item["primary_dataset"] == "districts" for item in regressions)
    assert all(item["primary_feature_ids"] == ["chamberi", "tetuan"] for item in regressions)
    assert all(item["evidence_geometry_crs"] == "EPSG:25830" for item in regressions)
    assert all(item["evidence_geometry"]["type"] == "Point" for item in regressions)
    assert result["boundary_ambiguities"] == []


def test_within_boundary_and_outside_semantics_are_explicit() -> None:
    districts = load_features(FIXTURES / "districts_candidate.geojson", "district_id")
    points = load_features(FIXTURES / "edge_case_points.geojson", "point_id")
    shared_boundary = districts["chamberi"].boundary.intersection(districts["tetuan"].boundary)
    points["on_shared_boundary"] = shared_boundary.interpolate(0.5, normalized=True)

    result = derive_within_assignments(points, districts)

    assert result["strictly_inside"] == {
        "within": ["tetuan"],
        "boundary_primary_ids": [],
    }
    assert result["on_shared_boundary"] == {
        "within": [],
        "boundary_primary_ids": ["chamberi", "tetuan"],
    }
    assert result["outside_both"] == {
        "within": [],
        "boundary_primary_ids": [],
    }


def test_identical_primary_versions_have_no_relationship_regressions() -> None:
    result = analyze(
        FIXTURES / "districts_base.geojson",
        FIXTURES / "districts_base.geojson",
        {"hotels": (FIXTURES / "hotels.geojson", "hotel_id")},
        relationship_threshold=1,
    )

    assert result["relationship_regressions"] == []
