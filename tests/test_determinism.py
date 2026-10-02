from pathlib import Path

from geoimpact.analysis import analyze


FIXTURES = Path(__file__).parent / "fixtures"


def test_repeated_analysis_has_deep_equal_scientific_output() -> None:
    arguments = (
        FIXTURES / "districts_base.geojson",
        FIXTURES / "districts_candidate.geojson",
        {
            "tourism_pois": (FIXTURES / "tourism_pois.geojson", "poi_id"),
            "hotels": (FIXTURES / "hotels.geojson", "hotel_id"),
        },
    )

    first = analyze(*arguments, relationship_threshold=1)
    second = analyze(*arguments, relationship_threshold=1)

    assert first == second
    assert first["policy"]["status"] == "BLOCK"
    assert [(item["dependent_dataset"], item["dependent_id"]) for item in first["relationship_regressions"]] == [
        ("hotels", "hotel_813"),
        ("tourism_pois", "poi_212"),
    ]
