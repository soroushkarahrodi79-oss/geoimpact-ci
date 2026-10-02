"""File-backed Gate 2 orchestration entry point."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from geoimpact.analysis import analyze
from geoimpact.artifacts import build_report, write_artifacts
from geoimpact.contract import load_contract


def run_from_config(config_path: str | Path, output_directory: str | Path) -> dict[str, Any]:
    """Run Gate 1 from a declared v1 contract and write deterministic files."""
    contract = load_contract(config_path)
    dependency_sources = {
        item["dataset"]: (item["path"], item["id_field"])
        for item in contract["dependencies"]
    }
    result = analyze(
        contract["primary"]["base"],
        contract["primary"]["candidate"],
        dependency_sources,
        relationship_threshold=contract["threshold"],
        primary_id_field=contract["primary"]["id_field"],
        primary_dataset=contract["primary"]["dataset"],
    )
    report = build_report(contract, result)
    write_artifacts(report, output_directory)
    return report
