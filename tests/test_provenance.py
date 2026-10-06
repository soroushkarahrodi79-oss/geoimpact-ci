from __future__ import annotations

import hashlib
import json
import os
from importlib.metadata import version
from pathlib import Path
import tomllib

import pyproj
import pytest
import shapely

from geoimpact import cli
from geoimpact.contract import load_contract
from geoimpact.provenance import build_provenance, sha256_file
from geoimpact.runner import run_from_config


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
CONFIG = FIXTURES / "geoimpact.yml"


def test_streamed_sha256_is_stable_and_sensitive_to_one_byte(tmp_path: Path) -> None:
    source = tmp_path / "input.bin"
    source.write_bytes(b"abc" * 500_000)
    first = sha256_file(source)
    assert first == sha256_file(source)
    assert first == {
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "size_bytes": 1_500_000,
    }
    source.write_bytes(source.read_bytes() + b"!")
    assert sha256_file(source)["sha256"] != first["sha256"]


def test_raw_hash_distinguishes_equivalent_json_bytes(tmp_path: Path) -> None:
    compact = tmp_path / "compact.json"
    spaced = tmp_path / "spaced.json"
    compact.write_bytes(b'{"a":1}')
    spaced.write_bytes(b'{ "a" : 1 }\n')
    assert json.loads(compact.read_text()) == json.loads(spaced.read_text())
    assert sha256_file(compact)["sha256"] != sha256_file(spaced)["sha256"]


def test_engine_versions_match_runtime_apis_and_distribution_metadata() -> None:
    provenance = build_provenance(CONFIG.read_bytes(), load_contract(CONFIG))
    assert provenance["engine"] == {
        "geoimpact_ci": version("geoimpact-ci"),
        "shapely": shapely.__version__,
        "geos": shapely.geos_version_string,
        "pyproj": pyproj.__version__,
        "proj": pyproj.proj_version_str,
    }


def test_config_identity_is_the_exact_yaml_file_bytes() -> None:
    raw = CONFIG.read_bytes()
    provenance = build_provenance(raw, load_contract(CONFIG))
    assert provenance["inputs"]["config"] == {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
    }


def test_source_tree_version_fallback_reads_the_single_pyproject_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from importlib.metadata import PackageNotFoundError

    import geoimpact.provenance as provenance_module

    def no_installed_metadata(_name: str) -> str:
        raise PackageNotFoundError

    monkeypatch.setattr(provenance_module, "version", no_installed_metadata)
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    provenance = build_provenance(CONFIG.read_bytes(), load_contract(CONFIG))
    assert provenance["engine"]["geoimpact_ci"] == pyproject["project"]["version"]


def test_provenance_is_deep_equal_ordered_and_contains_no_local_metadata(
    tmp_path: Path,
) -> None:
    provenance = build_provenance(CONFIG.read_bytes(), load_contract(CONFIG))
    repeated = build_provenance(CONFIG.read_bytes(), load_contract(CONFIG))
    assert provenance == repeated
    names = [item["dataset"] for item in provenance["inputs"]["dependencies"]]
    assert names == sorted(names)
    serialized = json.dumps(provenance, sort_keys=True)
    assert str(ROOT) not in serialized
    assert str(tmp_path) not in serialized
    assert "timestamp" not in serialized.lower()
    assert not any("time" in key.lower() for key in provenance)


def test_provenance_and_report_bytes_are_independent_of_cwd_and_output_path(
    tmp_path: Path,
) -> None:
    cwd_a = tmp_path / "cwd-a"
    cwd_b = tmp_path / "cwd-b"
    cwd_a.mkdir()
    cwd_b.mkdir()
    output_a = tmp_path / "private-a" / "out"
    output_b = tmp_path / "private-b" / "out"
    original_cwd = Path.cwd()
    try:
        os.chdir(cwd_a)
        first = run_from_config(CONFIG, output_a)
        os.chdir(cwd_b)
        second = run_from_config(CONFIG, output_b)
    finally:
        os.chdir(original_cwd)

    assert first["provenance"] == second["provenance"]
    declared_files = [
        CONFIG,
        FIXTURES / "districts_base.geojson",
        FIXTURES / "districts_candidate.geojson",
        FIXTURES / "hotels.geojson",
        FIXTURES / "tourism_pois.geojson",
    ]
    for name in ("report.json", "report.md", "relationship-regressions.geojson"):
        first_bytes = (output_a / name).read_bytes()
        assert first_bytes == (output_b / name).read_bytes()
        assert str(tmp_path).encode() not in first_bytes
        assert all(str(path.resolve()).encode() not in first_bytes for path in declared_files)


def test_missing_file_during_provenance_fails_exit_two_without_artifacts(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    def missing_file(_path: Path) -> dict[str, int | str]:
        raise FileNotFoundError("input disappeared")

    monkeypatch.setattr("geoimpact.provenance.sha256_file", missing_file)
    output = tmp_path / "no-report"
    exit_code = cli.main(["analyze", "--config", str(CONFIG), "--out", str(output)])
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "GeoImpact error:" in captured.err
    assert captured.out == ""
    assert not output.exists()
