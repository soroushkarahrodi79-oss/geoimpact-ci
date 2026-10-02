"""Fail-closed loader for the deliberately narrow Gate 2 YAML contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ContractError(ValueError):
    """A rejected or incomplete ``geoimpact.yml`` declaration."""


def _mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ContractError(f"{field} must be a YAML mapping")
    return value


def _required(mapping: dict[str, Any], name: str, parent: str) -> Any:
    field = f"{parent}.{name}"
    if name not in mapping or mapping[name] is None:
        raise ContractError(f"missing required field: {field}")
    return mapping[name]


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field} must be a non-empty string")
    return value


def _input_path(value: Any, field: str, config_directory: Path) -> Path:
    declared = Path(_text(value, field))
    path = declared if declared.is_absolute() else config_directory / declared
    path = path.resolve()
    if not path.is_file():
        raise ContractError(f"{field} file does not exist: {declared}")
    return path


def load_contract(config_path: str | Path) -> dict[str, Any]:
    """Load and validate the v1 contract; resolve inputs from its directory."""
    config = Path(config_path).expanduser().resolve()
    if not config.is_file():
        raise ContractError(f"config file does not exist: {config_path}")
    try:
        value = yaml.safe_load(config.read_text(encoding="utf-8"))
    except (yaml.YAMLError, UnicodeError) as error:
        raise ContractError(f"invalid YAML in config file: {error}") from error
    root = _mapping(value, "config")

    version = _required(root, "version", "config")
    if type(version) is not int or version != 1:
        raise ContractError("version must be the supported integer 1")

    analysis = _mapping(_required(root, "analysis", "config"), "analysis")
    crs = _text(_required(analysis, "crs", "analysis"), "analysis.crs")
    if crs != "EPSG:25830":
        raise ContractError("analysis.crs must be EPSG:25830 for Gate 2")

    primary = _mapping(_required(root, "primary", "config"), "primary")
    primary_name = _text(_required(primary, "dataset", "primary"), "primary.dataset")
    primary_id = _text(_required(primary, "id_field", "primary"), "primary.id_field")
    primary_base = _input_path(
        _required(primary, "base", "primary"), "primary.base", config.parent
    )
    primary_candidate = _input_path(
        _required(primary, "candidate", "primary"), "primary.candidate", config.parent
    )

    dependencies_value = _required(root, "dependencies", "config")
    if not isinstance(dependencies_value, list):
        raise ContractError("dependencies must be a YAML sequence")
    dependencies: list[dict[str, Any]] = []
    names: set[str] = set()
    for index, item in enumerate(dependencies_value):
        field = f"dependencies[{index}]"
        dependency = _mapping(item, field)
        name = _text(_required(dependency, "dataset", field), f"{field}.dataset")
        if name in names:
            raise ContractError(f"duplicate dependency dataset name: {name}")
        names.add(name)
        path = _input_path(
            _required(dependency, "path", field), f"{field}.path", config.parent
        )
        id_field = _text(_required(dependency, "id_field", field), f"{field}.id_field")
        predicate = _text(
            _required(dependency, "predicate", field), f"{field}.predicate"
        )
        if predicate != "within":
            raise ContractError(f"{field}.predicate must be within for Gate 2")
        dependencies.append(
            {"dataset": name, "path": path, "id_field": id_field, "predicate": predicate}
        )

    policy = _mapping(_required(root, "policy", "config"), "policy")
    rule = _mapping(
        _required(policy, "max_relationship_regressions", "policy"),
        "policy.max_relationship_regressions",
    )
    threshold = _required(rule, "threshold", "policy.max_relationship_regressions")
    if type(threshold) is not int:
        raise ContractError("policy.max_relationship_regressions.threshold must be an integer")
    if threshold < 0:
        raise ContractError("policy.max_relationship_regressions.threshold must be non-negative")
    severity = _text(
        _required(rule, "severity", "policy.max_relationship_regressions"),
        "policy.max_relationship_regressions.severity",
    )
    if severity != "block":
        raise ContractError("policy.max_relationship_regressions.severity must be block")

    return {
        "version": version,
        "analysis_crs": crs,
        "primary": {
            "dataset": primary_name,
            "id_field": primary_id,
            "base": primary_base,
            "candidate": primary_candidate,
        },
        "dependencies": dependencies,
        "threshold": threshold,
        "severity": severity,
    }
