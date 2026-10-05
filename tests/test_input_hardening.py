from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from geoimpact.analysis import analyze, load_features
from geoimpact.contract import ContractError, load_contract
from geoimpact.errors import InputError


def feature(identifier: str, geometry: dict[str, object]) -> dict[str, object]:
    return {
        "type": "Feature",
        "properties": {"id": identifier},
        "geometry": geometry,
    }


def collection(*features: object) -> dict[str, object]:
    return {"type": "FeatureCollection", "features": list(features)}


def polygon(left: float, bottom: float, right: float, top: float) -> dict[str, object]:
    return {
        "type": "Polygon",
        "coordinates": [[
            [left, bottom], [right, bottom], [right, top], [left, top], [left, bottom]
        ]],
    }


def write_geojson(path: Path, value: object) -> Path:
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


@pytest.mark.parametrize(
    "value",
    [
        [],
        {"type": "Feature"},
        {"type": "FeatureCollection"},
        {"type": "FeatureCollection", "features": {}},
        collection(None),
        collection({"type": "Feature", "properties": None, "geometry": polygon(0, 0, 1, 1)}),
        collection({"type": "Feature", "properties": {}, "geometry": polygon(0, 0, 1, 1)}),
        collection(feature("", polygon(0, 0, 1, 1))),
        collection({"type": "Feature", "properties": {"id": 7}, "geometry": polygon(0, 0, 1, 1)}),
        collection({"type": "Feature", "properties": {"id": "x"}}),
        collection(feature("x", None)),
        collection(feature("x", {"type": "Polygon", "coordinates": None})),
        collection(feature("x", {"type": "Polygon", "coordinates": [[[0, 0], [float("nan"), 0]]]})),
        collection(feature("x", polygon(0, 0, 1, 1)), feature("x", polygon(2, 2, 3, 3))),
        collection(feature("x", {
            "type": "Polygon",
            "coordinates": [[[0, 0], [1, 1], [1, 0], [0, 1], [0, 0]]],
        })),
    ],
)
def test_malformed_and_invalid_geojson_is_controlled(tmp_path: Path, value: object) -> None:
    path = write_geojson(tmp_path / "input.geojson", value)
    with pytest.raises(InputError):
        load_features(path, "id", geometry_role="primary")


@pytest.mark.parametrize(
    ("role", "geometry", "message"),
    [
        ("primary", {"type": "Point", "coordinates": [0, 0]}, "Polygon or MultiPolygon"),
        ("primary", {"type": "GeometryCollection", "geometries": []}, "Polygon or MultiPolygon"),
        ("dependent", polygon(0, 0, 1, 1), "must be Point"),
        ("dependent", {"type": "LineString", "coordinates": [[0, 0], [1, 1]]}, "must be Point"),
    ],
)
def test_unsupported_geometry_types_are_rejected(
    tmp_path: Path, role: str, geometry: dict[str, object], message: str
) -> None:
    path = write_geojson(tmp_path / "input.geojson", collection(feature("zone-1", geometry)))
    with pytest.raises(InputError, match=message):
        load_features(path, "id", geometry_role=role)


def test_malformed_json_and_invalid_utf8_are_controlled(tmp_path: Path) -> None:
    path = tmp_path / "bad.geojson"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(InputError, match="malformed JSON"):
        load_features(path, "id", geometry_role="primary")
    path.write_bytes(b"\xff")
    with pytest.raises(InputError, match="cannot be read as UTF-8"):
        load_features(path, "id", geometry_role="primary")
    with pytest.raises(InputError, match="cannot be read as UTF-8"):
        load_features(tmp_path / "missing.geojson", "id", geometry_role="primary")


def test_top_level_non_mapping_and_missing_feature_collection_fields_fail(tmp_path: Path) -> None:
    path = write_geojson(tmp_path / "input.geojson", "not an object")
    with pytest.raises(InputError, match="top-level GeoJSON object"):
        load_features(path, "id", geometry_role="primary")
    path = write_geojson(path, {"type": "FeatureCollection"})
    with pytest.raises(InputError, match="missing features"):
        load_features(path, "id", geometry_role="primary")


def test_unknown_contract_keys_are_rejected(tmp_path: Path) -> None:
    fixture_root = Path(__file__).parent / "fixtures"
    config = yaml.safe_load((fixture_root / "geoimpact.yml").read_text(encoding="utf-8"))
    config["analysis"]["predicat"] = "within"
    path = tmp_path / "unknown.yml"
    for filename in ("districts_base.geojson", "districts_candidate.geojson", "hotels.geojson", "tourism_pois.geojson"):
        (tmp_path / filename).write_bytes((fixture_root / filename).read_bytes())
    path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    with pytest.raises(ContractError, match="unknown field.*predicat"):
        load_contract(path)


def test_added_and_removed_primary_features_drive_expected_relationships(tmp_path: Path) -> None:
    point = collection(feature("P", {"type": "Point", "coordinates": [0.005, 0.005]}))
    points_path = write_geojson(tmp_path / "points.geojson", point)
    base_path = write_geojson(
        tmp_path / "base.geojson", collection(feature("A", polygon(0, 0, 0.01, 0.01)))
    )
    absent_path = write_geojson(tmp_path / "absent.geojson", collection())
    added_path = write_geojson(
        tmp_path / "added.geojson", collection(feature("B", polygon(0, 0, 0.01, 0.01)))
    )

    removed = analyze(
        base_path, absent_path, {"points": (points_path, "id")},
        relationship_threshold=0, primary_id_field="id"
    )
    gained = analyze(
        absent_path, added_path, {"points": (points_path, "id")},
        relationship_threshold=0, primary_id_field="id"
    )
    replaced = analyze(
        base_path, added_path, {"points": (points_path, "id")},
        relationship_threshold=0, primary_id_field="id"
    )

    assert removed["relationships"][0]["before"] == ["A"]
    assert removed["relationships"][0]["after"] == []
    assert removed["relationships"][0]["change_type"] == "assignment_lost"
    assert gained["relationships"][0]["before"] == []
    assert gained["relationships"][0]["after"] == ["B"]
    assert gained["relationships"][0]["change_type"] == "assignment_gained"
    assert replaced["relationships"][0]["before"] == ["A"]
    assert replaced["relationships"][0]["after"] == ["B"]
    assert replaced["relationships"][0]["change_type"] == "assignment_changed"
    assert all(result["boundary_ambiguities"] == [] for result in (removed, gained, replaced))
