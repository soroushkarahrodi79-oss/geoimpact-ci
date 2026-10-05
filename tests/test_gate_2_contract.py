from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path

import pytest
import yaml
from pyproj import Transformer

from geoimpact.artifacts import GEOGRAPHIC_COORDINATE_DECIMALS
from geoimpact.contract import ContractError, load_contract
from geoimpact.runner import run_from_config


FIXTURE_DIR = Path(__file__).parent / "fixtures"
CONFIG = FIXTURE_DIR / "geoimpact.yml"
ARTIFACT_NAMES = (
    "report.json",
    "report.md",
    "relationship-regressions.geojson",
)
EXPECTED_IDS = [
    "relationship-regression-526712f2a3cfcdb0b86e03e9b060807c34ec8909095e5bb87cd57ab47e3cde49",
    "relationship-regression-b9209f0fa3ca1ab124fd412de95dc593c002219a36c5053a94071855602a0c68",
]


def copy_bundle(directory: Path) -> Path:
    for name in (
        "geoimpact.yml",
        "districts_base.geojson",
        "districts_candidate.geojson",
        "hotels.geojson",
        "tourism_pois.geojson",
    ):
        shutil.copy2(FIXTURE_DIR / name, directory / name)
    return directory / "geoimpact.yml"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_valid_contract_and_paths_resolve_from_config_location(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    config_path = copy_bundle(bundle)
    other_cwd = tmp_path / "other-cwd"
    other_cwd.mkdir()
    old_cwd = Path.cwd()
    try:
        os.chdir(other_cwd)
        contract = load_contract(config_path)
    finally:
        os.chdir(old_cwd)

    assert contract["analysis_crs"] == "EPSG:25830"
    assert contract["primary"]["base"] == (bundle / "districts_base.geojson").resolve()
    assert contract["dependencies"][0]["path"] == (bundle / "hotels.geojson").resolve()


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ("version: 1", "version: 2", "version"),
        ("crs: EPSG:25830", "crs: EPSG:4326", "analysis.crs"),
        ("predicate: within", "predicate: intersects", "predicate"),
        ("threshold: 1", "threshold: 1.5", "threshold"),
        ("threshold: 1", "threshold: -1", "non-negative"),
        ("threshold: 1", "threshold: true", "threshold"),
    ],
)
def test_unsupported_or_invalid_declarations_fail_closed(
    tmp_path: Path, old: str, new: str, message: str
) -> None:
    config_path = copy_bundle(tmp_path)
    config_path.write_text(config_path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
    with pytest.raises(ContractError, match=message):
        load_contract(config_path)


def test_invalid_yaml_and_missing_config_fail_clearly(tmp_path: Path) -> None:
    with pytest.raises(ContractError, match="config file does not exist"):
        load_contract(tmp_path / "absent.yml")
    config_path = tmp_path / "bad.yml"
    config_path.write_text("version: [", encoding="utf-8")
    with pytest.raises(ContractError, match="invalid YAML"):
        load_contract(config_path)


@pytest.mark.parametrize(
    ("field", "message"),
    [
        ("primary.base", "primary.base"),
        ("primary.candidate", "primary.candidate"),
        ("primary.id_field", "primary.id_field"),
        ("dependencies[0].path", "dependencies\\[0\\].path"),
        ("dependencies[0].id_field", "dependencies\\[0\\].id_field"),
    ],
)
def test_missing_declarations_and_files_fail_clearly(
    tmp_path: Path, field: str, message: str
) -> None:
    config_path = copy_bundle(tmp_path)
    value = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if field.startswith("dependencies"):
        name = field.split(".", 1)[1]
        value["dependencies"][0].pop(name, None)
    else:
        name = field.split(".", 1)[1]
        value["primary"].pop(name, None)
    config_path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
    with pytest.raises(ContractError, match=message):
        load_contract(config_path)

    value = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    if field == "primary.base":
        value["primary"]["base"] = "missing.geojson"
    elif field == "primary.candidate":
        value["primary"]["candidate"] = "missing.geojson"
    elif field == "dependencies[0].path":
        value["dependencies"][0]["path"] = "missing.geojson"
    else:
        return
    config_path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
    with pytest.raises(ContractError, match="file does not exist"):
        load_contract(config_path)


def test_duplicate_dependency_dataset_names_fail_closed(tmp_path: Path) -> None:
    value = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    value["dependencies"][1]["dataset"] = value["dependencies"][0]["dataset"]
    config_path = copy_bundle(tmp_path)
    config_path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")
    with pytest.raises(ContractError, match="duplicate dependency dataset name"):
        load_contract(config_path)


def test_file_backed_report_preserves_gate_1_results_and_verdict(tmp_path: Path) -> None:
    report = run_from_config(CONFIG, tmp_path / "out")

    assert report["report_version"] == "3"
    assert [(item["dependent_dataset"], item["dependent_id"]) for item in report["relationship_regressions"]] == [
        ("hotels", "hotel_813"),
        ("tourism_pois", "poi_212"),
    ]
    assert all(item["before"] == ["chamberi"] for item in report["relationship_regressions"])
    assert all(item["after"] == ["tetuan"] for item in report["relationship_regressions"])
    assert [item["evidence_id"] for item in report["relationship_regressions"]] == EXPECTED_IDS
    assert report["policy"] == {
        "rule": "max_relationship_regressions",
        "observed_value": 2,
        "threshold": 1,
        "evidence_ids": EXPECTED_IDS,
        "status": "BLOCK",
    }
    assert report["verdict"] == "BLOCK"


def test_all_artifacts_repeat_byte_for_byte(tmp_path: Path) -> None:
    first = tmp_path / "run-a"
    second = tmp_path / "run-b"
    run_from_config(CONFIG, first)
    run_from_config(CONFIG, second)

    assert {name: digest(first / name) for name in ARTIFACT_NAMES} == {
        name: digest(second / name) for name in ARTIFACT_NAMES
    }
    markdown = (first / "report.md").read_text(encoding="utf-8")
    assert "Analysis verdict: BLOCK" in markdown
    assert "hotels / hotel_813: chamberi -> tetuan" in markdown
    assert "tourism_pois / poi_212: chamberi -> tetuan" in markdown


def test_outputs_independent_of_cwd_and_config_bundle_location(tmp_path: Path) -> None:
    bundle_a = tmp_path / "bundle-a"
    bundle_b = tmp_path / "bundle-b"
    cwd_a = tmp_path / "cwd-a"
    cwd_b = tmp_path / "cwd-b"
    out_a = tmp_path / "output-a"
    out_b = tmp_path / "output-b"
    for directory in (bundle_a, bundle_b, cwd_a, cwd_b):
        directory.mkdir()
    config_a = copy_bundle(bundle_a)
    config_b = copy_bundle(bundle_b)
    old_cwd = Path.cwd()
    try:
        os.chdir(cwd_a)
        run_from_config(config_a, out_a)
        os.chdir(cwd_b)
        run_from_config(config_a, out_b)
        run_from_config(config_b, tmp_path / "output-copied-config")
    finally:
        os.chdir(old_cwd)

    assert {name: digest(out_a / name) for name in ARTIFACT_NAMES} == {
        name: digest(out_b / name) for name in ARTIFACT_NAMES
    }
    copied_output = tmp_path / "output-copied-config"
    assert {name: digest(out_a / name) for name in ARTIFACT_NAMES} == {
        name: digest(copied_output / name) for name in ARTIFACT_NAMES
    }
    for name in ARTIFACT_NAMES:
        content = (out_a / name).read_bytes()
        assert str(tmp_path).encode() not in content


def test_evidence_geojson_is_crs84_and_has_no_legacy_crs_member(tmp_path: Path) -> None:
    run_from_config(CONFIG, tmp_path / "out")
    collection = json.loads(
        (tmp_path / "out" / "relationship-regressions.geojson").read_text(encoding="utf-8")
    )

    assert collection["type"] == "FeatureCollection"
    assert "crs" not in collection
    assert len(collection["features"]) == 2
    for feature in collection["features"]:
        assert "crs" not in feature
        longitude, latitude = feature["geometry"]["coordinates"]
        assert -180 <= longitude <= 180
        assert -90 <= latitude <= 90
    first = collection["features"][0]
    projected = json.loads((tmp_path / "out" / "report.json").read_text(encoding="utf-8"))
    source_point = projected["relationship_regressions"][0]["evidence_geometry"]["coordinates"]
    expected = Transformer.from_crs("EPSG:25830", "OGC:CRS84", always_xy=True).transform(
        *source_point
    )
    # Gate 3B: the inverse transform runs at full precision, then the published
    # coordinate is rounded to the declared CRS84 serialization precision.
    expected_canonical = [round(value, GEOGRAPHIC_COORDINATE_DECIMALS) for value in expected]
    assert first["geometry"]["coordinates"] == expected_canonical
