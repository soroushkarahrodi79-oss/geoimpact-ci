"""File-backed orchestration entry point for the GeoImpact CLI."""

from __future__ import annotations

from pathlib import Path

from geoimpact.analysis import analyze
from geoimpact.artifacts import build_report, write_artifacts
from geoimpact.contract import load_contract
from geoimpact.models import GeoImpactReport
from geoimpact.provenance import build_provenance


def run_from_config(
    config_path: str | Path, output_directory: str | Path
) -> GeoImpactReport:
    """Run a declared v1 analysis and write deterministic artifacts."""
    # Parse and hash the same captured config bytes so provenance identifies
    # the exact declaration used to construct the resolved contract.
    resolved_config = Path(config_path).expanduser().resolve()
    if not resolved_config.is_file():
        # Preserve the loader's concise missing-config contract.
        load_contract(resolved_config)
    config_bytes = resolved_config.read_bytes()
    contract = load_contract(config_path, source_bytes=config_bytes)
    provenance = build_provenance(config_bytes, contract)
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
    report = build_report(contract, result, provenance)
    write_artifacts(report, output_directory)
    return report
