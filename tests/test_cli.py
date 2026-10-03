from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

import pytest
import yaml

from geoimpact import cli
from geoimpact.errors import InputError
from geoimpact.runner import run_from_config


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
BLOCK_CONFIG = FIXTURES / "geoimpact.yml"
PASS_CONFIG = FIXTURES / "geoimpact-pass.yml"
ARTIFACTS = (
    "report.json",
    "report.md",
    "relationship-regressions.geojson",
)
# Canonical hashes under the Gate 3B portable (precision-bounded) artifact
# serialization contract. These supersede the pre-portable Windows-only hashes
# (see docs/GATE_2_REPORT.md); report.md is unchanged because it embeds no
# coordinates. See decision log D-022.
EXPECTED_HASHES = {
    "report.json": "234d31b08c18ed45e8698af2abf7e001b489bcb7efbf34ffb058e2113447388d",
    "report.md": "d161a55cbf1441e078ce1ea3181dbc41d2ee8d73e540b311f5a52690379f202e",
    "relationship-regressions.geojson": "a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978",
}
EXPECTED_IDS = [
    "relationship-regression-526712f2a3cfcdb0b86e03e9b060807c34ec8909095e5bb87cd57ab47e3cde49",
    "relationship-regression-b9209f0fa3ca1ab124fd412de95dc593c002219a36c5053a94071855602a0c68",
]


def _environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / "src")
    return environment


def _run_cli(config: Path | str, output: Path, *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "geoimpact.cli", "analyze", "--config", str(config), "--out", str(output)],
        cwd=cwd,
        env=_environment(),
        text=True,
        capture_output=True,
        check=False,
    )


def _copy_bundle(destination: Path) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    for name in (
        "districts_base.geojson",
        "districts_candidate.geojson",
        "hotels.geojson",
        "tourism_pois.geojson",
    ):
        shutil.copy2(FIXTURES / name, destination / name)
    return destination


def _hashes(directory: Path) -> dict[str, str]:
    return {name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in ARTIFACTS}


def test_cli_accepts_analyze_config_and_out_arguments(tmp_path: Path) -> None:
    result = _run_cli(BLOCK_CONFIG, tmp_path / "accepted", cwd=tmp_path)
    assert result.returncode == 1
    assert "Verdict: BLOCK" in result.stdout


def test_cli_missing_config_or_out_is_argparse_usage_error(tmp_path: Path) -> None:
    commands = (
        ["analyze", "--out", str(tmp_path / "out")],
        ["analyze", "--config", str(BLOCK_CONFIG)],
    )
    for command in commands:
        result = subprocess.run(
            [sys.executable, "-m", "geoimpact.cli", *command],
            cwd=tmp_path,
            env=_environment(),
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 2
        assert "usage:" in result.stderr
        assert "Verdict:" not in result.stdout


def test_pass_run_returns_zero_and_writes_all_artifacts(tmp_path: Path) -> None:
    output = tmp_path / "pass-output"
    result = _run_cli(PASS_CONFIG, output, cwd=tmp_path)

    assert result.returncode == 0
    assert "Verdict: PASS" in result.stdout
    assert result.stderr == ""
    assert all((output / name).is_file() for name in ARTIFACTS)


def test_block_run_returns_one_and_writes_all_artifacts(tmp_path: Path) -> None:
    output = tmp_path / "block-output"
    result = _run_cli(BLOCK_CONFIG, output, cwd=tmp_path)

    assert result.returncode == 1
    assert "Verdict: BLOCK" in result.stdout
    assert result.stderr == ""
    assert all((output / name).is_file() for name in ARTIFACTS)


def test_missing_config_is_concise_operational_error(tmp_path: Path) -> None:
    result = _run_cli(tmp_path / "absent.yml", tmp_path / "out", cwd=tmp_path)
    assert result.returncode == 2
    assert "GeoImpact error: config file does not exist" in result.stderr
    assert result.stdout == ""
    assert "Traceback" not in result.stderr
    assert not (tmp_path / "out").exists()


def test_invalid_contract_is_concise_operational_error(tmp_path: Path) -> None:
    config = tmp_path / "invalid.yml"
    config.write_text("version: 2\n", encoding="utf-8")
    result = _run_cli(config, tmp_path / "out", cwd=tmp_path)
    assert result.returncode == 2
    assert "GeoImpact error: " in result.stderr
    assert "Traceback" not in result.stderr
    assert result.stdout == ""


def test_missing_declared_dataset_is_concise_operational_error(tmp_path: Path) -> None:
    bundle = _copy_bundle(tmp_path / "bundle")
    contract = yaml.safe_load(BLOCK_CONFIG.read_text(encoding="utf-8"))
    contract["primary"]["base"] = "missing.geojson"
    config = bundle / "bad-input.yml"
    config.write_text(yaml.safe_dump(contract, sort_keys=False), encoding="utf-8")

    result = _run_cli(config, tmp_path / "out", cwd=tmp_path)
    assert result.returncode == 2
    assert "GeoImpact error: primary.base file does not exist: missing.geojson" in result.stderr
    assert "Traceback" not in result.stderr
    assert result.stdout == ""
    assert not (tmp_path / "out").exists()


def test_cli_block_artifacts_match_direct_runner_byte_for_byte(tmp_path: Path) -> None:
    direct = tmp_path / "direct"
    via_cli = tmp_path / "cli"
    report = run_from_config(BLOCK_CONFIG, direct)
    result = _run_cli(BLOCK_CONFIG, via_cli, cwd=tmp_path)

    assert report["verdict"] == "BLOCK"
    assert result.returncode == 1
    assert {name: (direct / name).read_bytes() for name in ARTIFACTS} == {
        name: (via_cli / name).read_bytes() for name in ARTIFACTS
    }


def test_canonical_block_hashes_and_gate_1_evidence_ids_are_unchanged(tmp_path: Path) -> None:
    output = tmp_path / "canonical"
    result = _run_cli(BLOCK_CONFIG, output, cwd=tmp_path)
    report = json.loads((output / "report.json").read_text(encoding="utf-8"))

    assert result.returncode == 1
    assert _hashes(output) == EXPECTED_HASHES
    assert [item["evidence_id"] for item in report["relationship_regressions"]] == EXPECTED_IDS


def test_pass_threshold_preserves_science_and_relationship_evidence_ids(tmp_path: Path) -> None:
    block_output = tmp_path / "block"
    pass_output = tmp_path / "pass"
    block_result = _run_cli(BLOCK_CONFIG, block_output, cwd=tmp_path)
    pass_result = _run_cli(PASS_CONFIG, pass_output, cwd=tmp_path)
    block = json.loads((block_output / "report.json").read_text(encoding="utf-8"))
    passed = json.loads((pass_output / "report.json").read_text(encoding="utf-8"))

    assert block_result.returncode == 1
    assert pass_result.returncode == 0
    for section in ("analysis", "primary_change", "relationships", "relationship_regressions", "boundary_ambiguities"):
        assert passed[section] == block[section]
    assert [item["evidence_id"] for item in passed["relationship_regressions"]] == EXPECTED_IDS
    assert block["policy"]["threshold"] == 1
    assert passed["policy"]["threshold"] == 2
    assert block["verdict"] == "BLOCK"
    assert passed["verdict"] == "PASS"
    assert (pass_output / "relationship-regressions.geojson").read_bytes() == (
        block_output / "relationship-regressions.geojson"
    ).read_bytes()


def test_invocation_from_different_cwd_has_identical_scientific_output(tmp_path: Path) -> None:
    cwd = tmp_path / "elsewhere"
    cwd.mkdir()
    output = tmp_path / "output"
    result = _run_cli(BLOCK_CONFIG, output, cwd=cwd)

    assert result.returncode == 1
    assert _hashes(output) == EXPECTED_HASHES


def test_installed_console_entrypoint_works_in_clean_venv(tmp_path: Path) -> None:
    environment_path = tmp_path / "venv"
    venv.EnvBuilder(with_pip=True).create(environment_path)
    scripts = environment_path / ("Scripts" if os.name == "nt" else "bin")
    python = scripts / ("python.exe" if os.name == "nt" else "python")
    executable = scripts / ("geoimpact.exe" if os.name == "nt" else "geoimpact")
    install = subprocess.run(
        [str(python), "-m", "pip", "install", str(ROOT)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    assert install.returncode == 0, install.stdout + install.stderr

    result = subprocess.run(
        [str(executable), "analyze", "--config", str(PASS_CONFIG), "--out", str(tmp_path / "installed-output")],
        cwd=tmp_path,
        env={key: value for key, value in os.environ.items() if key != "PYTHONPATH"},
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Verdict: PASS" in result.stdout
    assert _hashes(tmp_path / "installed-output")["relationship-regressions.geojson"] == EXPECTED_HASHES[
        "relationship-regressions.geojson"
    ]


def test_expected_domain_input_error_is_controlled_exit_two(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """An expected GeoImpact domain/input failure becomes a concise exit 2."""

    def raise_input_error(*_args: object, **_kwargs: object) -> dict[str, object]:
        raise InputError("districts_base.geojson is not a FeatureCollection")

    monkeypatch.setattr(cli, "run_from_config", raise_input_error)
    exit_code = cli.main(
        ["analyze", "--config", str(BLOCK_CONFIG), "--out", str(tmp_path / "out")]
    )
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "GeoImpact error: districts_base.geojson is not a FeatureCollection" in captured.err
    assert "Traceback" not in captured.err
    assert captured.out == ""


def test_unexpected_programming_valueerror_is_not_swallowed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A bare programming ValueError must not be translated into exit 2."""

    def raise_programming_error(*_args: object, **_kwargs: object) -> dict[str, object]:
        raise ValueError("internal invariant violated")

    monkeypatch.setattr(cli, "run_from_config", raise_programming_error)
    with pytest.raises(ValueError, match="internal invariant violated"):
        cli.main(
            ["analyze", "--config", str(BLOCK_CONFIG), "--out", str(tmp_path / "out")]
        )
