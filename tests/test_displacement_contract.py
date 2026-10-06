import json
from pathlib import Path

from geoimpact.analysis import analyze
from geoimpact.artifacts import build_report, write_artifacts


ROOT = Path(__file__).parent
FIXTURES = ROOT / "fixtures"
PROVENANCE = {
    "hash_algorithm": "sha256",
    "inputs": {
        "config": {"sha256": "0" * 64, "size_bytes": 0},
        "primary": {
            "base": {"dataset": "districts", "sha256": "0" * 64, "size_bytes": 0},
            "candidate": {"dataset": "districts", "sha256": "0" * 64, "size_bytes": 0},
        },
        "dependencies": [],
    },
    "engine": {"geoimpact_ci": "1.1.0", "shapely": "x", "geos": "x", "pyproj": "x", "proj": "x"},
}


def _gate4_report() -> dict[str, object]:
    analysis = analyze(
        FIXTURES / "districts_base.geojson",
        FIXTURES / "districts_candidate.geojson",
        {
            "tourism_pois": (FIXTURES / "tourism_pois.geojson", "poi_id"),
            "hotels": (FIXTURES / "hotels.geojson", "hotel_id"),
        },
        relationship_threshold=1,
    )
    return build_report(
        {
            "analysis_crs": "EPSG:25830",
            "primary": {"dataset": "districts", "id_field": "district_id"},
            "dependencies": [
                {"dataset": "tourism_pois", "id_field": "poi_id", "predicate": "within"},
                {"dataset": "hotels", "id_field": "hotel_id", "predicate": "within"},
            ],
        },
        analysis,
        PROVENANCE,
    )


def test_displacement_contract_is_report_version_five() -> None:
    assert _gate4_report()["report_version"] == "5"


def test_json_serializes_the_computed_displacement_without_reformatting(tmp_path: Path) -> None:
    report = _gate4_report()
    expected = report["primary_change"]["max_boundary_displacement_m"]

    write_artifacts(report, tmp_path)
    serialized = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))

    assert serialized["primary_change"]["max_boundary_displacement_m"] == expected
    assert serialized["report_version"] == "5"
