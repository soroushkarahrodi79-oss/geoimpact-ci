from pathlib import Path
import random

from shapely.geometry import MultiPolygon, Point, Polygon, box

from geoimpact.analysis import analyze, load_features
from geoimpact.artifacts import build_report
from geoimpact.relationships import PrimarySpatialIndex, derive_within_assignments


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


def test_custom_primary_dataset_name_flows_to_analysis_evidence_and_report() -> None:
    dataset_name = "administrative_units_2026"
    result = analyze(
        FIXTURES / "districts_base.geojson",
        FIXTURES / "districts_candidate.geojson",
        {"hotels": (FIXTURES / "hotels.geojson", "hotel_id")},
        relationship_threshold=1,
        primary_dataset=dataset_name,
    )
    contract = {
        "analysis_crs": "EPSG:25830",
        "primary": {"dataset": dataset_name, "id_field": "district_id"},
        "dependencies": [
            {"dataset": "hotels", "id_field": "hotel_id", "predicate": "within"}
        ],
    }

    report = build_report(contract, result)

    assert result["primary_dataset"] == dataset_name
    assert result["relationship_regressions"][0]["primary_dataset"] == dataset_name
    assert report["analysis"]["primary_dataset"] == dataset_name
    assert report["report_version"] == "4"
    assert report["verdict"] == "PASS"


def test_within_boundary_and_outside_semantics_are_explicit() -> None:
    districts = load_features(FIXTURES / "districts_candidate.geojson", "district_id")
    points = load_features(
        FIXTURES / "edge_case_points.geojson", "point_id", geometry_role="dependent"
    )
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


def _exhaustive_reference(dependents, primary):
    """Pre-index semantics kept in tests as a deliberately simple oracle."""
    return {
        dependent_id: {
            "within": [
                primary_id
                for primary_id in sorted(primary)
                if geometry.within(primary[primary_id])
            ],
            "boundary_primary_ids": [
                primary_id
                for primary_id in sorted(primary)
                if geometry.touches(primary[primary_id])
            ],
        }
        for dependent_id, geometry in sorted(dependents.items())
    }


def test_spatial_index_matches_exhaustive_edge_cases_and_stable_order() -> None:
    ring_with_hole = Polygon(
        [(50, 0), (60, 0), (60, 10), (50, 10), (50, 0)],
        holes=[[(53, 3), (57, 3), (57, 7), (53, 7), (53, 3)]],
    )
    primary = {
        "z-overlap": box(5, 0, 15, 10),
        "a-base": box(0, 0, 10, 10),
        "hole": ring_with_hole,
        "multi": MultiPolygon([box(20, 0, 22, 2), box(24, 0, 26, 2)]),
        "near-b": box(31.00001, 0, 32, 1),
        "near-a": box(30, 0, 31, 1),
        "duplicate-b": box(40, 0, 42, 2),
        "duplicate-a": box(40, 0, 42, 2),
        **{f"overlap-{index:02d}": box(100, 0, 110, 10) for index in range(20)},
    }
    dependents = {
        "within-one": Point(2, 2),
        "outside": Point(-100, -100),
        "boundary": Point(0, 5),
        "multiple-within": Point(7, 5),
        "inside-hole": Point(55, 5),
        "inside-multipolygon": Point(25, 1),
        "duplicate-shape": Point(41, 1),
        "between-near-envelopes": Point(31.000005, 0.5),
        "many-same-envelope": Point(105, 5),
    }

    expected = _exhaustive_reference(dependents, primary)
    index = PrimarySpatialIndex(primary)
    assert derive_within_assignments(dependents, primary, spatial_index=index) == expected
    assert derive_within_assignments(
        dict(reversed(list(dependents.items()))),
        dict(reversed(list(primary.items()))),
    ) == expected
    assert expected["boundary"] == {
        "within": [],
        "boundary_primary_ids": ["a-base"],
    }
    assert expected["multiple-within"]["within"] == ["a-base", "z-overlap"]
    assert expected["inside-hole"]["within"] == []
    assert expected["duplicate-shape"]["within"] == ["duplicate-a", "duplicate-b"]
    assert expected["outside"]["within"] == []
    assert len(expected["many-same-envelope"]["within"]) == 20


def test_spatial_index_matches_fixed_seed_randomized_cases() -> None:
    rng = random.Random(731_2026)
    primary = {
        f"cell-{index:03d}": box(index * 4, 0, index * 4 + 3, 3)
        for index in range(80)
    }
    dependents = {
        f"point-{index:04d}": Point(rng.uniform(-5, 325), rng.uniform(-2, 5))
        for index in range(350)
    }
    assert derive_within_assignments(dependents, primary) == _exhaustive_reference(
        dependents, primary
    )


def test_spatial_index_handles_no_primary_candidates() -> None:
    dependents = {"remote": Point(500, 500)}
    assert derive_within_assignments(dependents, {}) == {
        "remote": {"within": [], "boundary_primary_ids": []}
    }


def test_spatial_index_must_match_the_primary_mapping() -> None:
    primary = {"a": box(0, 0, 1, 1)}
    other_primary = {"a": box(0, 0, 1, 1)}
    try:
        derive_within_assignments(
            {"p": Point(0.5, 0.5)},
            other_primary,
            spatial_index=PrimarySpatialIndex(primary),
        )
    except ValueError as error:
        assert "built from the supplied primary mapping" in str(error)
    else:
        raise AssertionError("mismatched index mapping should fail")


def test_primary_indexes_are_built_once_and_reused_across_dependents(monkeypatch) -> None:
    import geoimpact.analysis as analysis_module

    original = analysis_module.PrimarySpatialIndex
    built = []

    def tracked_index(primary):
        index = original(primary)
        built.append(index)
        return index

    monkeypatch.setattr(analysis_module, "PrimarySpatialIndex", tracked_index)
    analyze(
        FIXTURES / "districts_base.geojson",
        FIXTURES / "districts_candidate.geojson",
        {
            "hotels": (FIXTURES / "hotels.geojson", "hotel_id"),
            "tourism_pois": (FIXTURES / "tourism_pois.geojson", "poi_id"),
        },
        relationship_threshold=1,
    )
    assert len(built) == 2


def test_spatial_index_materially_reduces_candidate_pairs() -> None:
    primary = {f"p{index:03d}": box(index * 3, 0, index * 3 + 2, 2) for index in range(50)}
    dependents = {f"d{index:03d}": Point(index * 3 + 1, 1) for index in range(50)}
    index = PrimarySpatialIndex(primary)
    candidate_count = sum(
        len(ids)
        for ids in (
            index.candidate_primary_ids(geometry)
            for geometry in dependents.values()
        )
    )
    assert candidate_count == len(dependents)
    assert candidate_count < len(dependents) * len(primary)
