"""Deterministic identities for declared inputs and the spatial engine."""

from __future__ import annotations

import hashlib
import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import pyproj
import shapely

from geoimpact.models import (
    GeoImpactContract,
    Provenance,
)


_CHUNK_SIZE = 1024 * 1024


def _content_identity(data: bytes) -> dict[str, int | str]:
    return {"sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}


def sha256_file(path: Path) -> dict[str, int | str]:
    """Hash exact file bytes in bounded memory and return digest plus byte size."""
    digest = hashlib.sha256()
    size_bytes = 0
    with path.open("rb") as source:
        while chunk := source.read(_CHUNK_SIZE):
            digest.update(chunk)
            size_bytes += len(chunk)
    return {"sha256": digest.hexdigest(), "size_bytes": size_bytes}


def _geoimpact_version() -> str:
    """Use installed distribution metadata; source runs use pyproject's version."""
    try:
        return version("geoimpact-ci")
    except PackageNotFoundError:
        project_file = Path(__file__).resolve().parents[2] / "pyproject.toml"
        with project_file.open("rb") as source:
            project = tomllib.load(source)
        return str(project["project"]["version"])


def build_provenance(
    config_bytes: bytes, contract: GeoImpactContract
) -> Provenance:
    """Collect only reproducibility-relevant input and engine identities."""
    primary = contract["primary"]
    dependencies = [
        {
            "dataset": dependency["dataset"],
            **sha256_file(dependency["path"]),
        }
        for dependency in sorted(contract["dependencies"], key=lambda item: item["dataset"])
    ]
    return {
        "hash_algorithm": "sha256",
        "inputs": {
            "config": _content_identity(config_bytes),
            "primary": {
                "base": {
                    "dataset": primary["dataset"],
                    **sha256_file(primary["base"]),
                },
                "candidate": {
                    "dataset": primary["dataset"],
                    **sha256_file(primary["candidate"]),
                },
            },
            "dependencies": dependencies,
        },
        "engine": {
            "geoimpact_ci": _geoimpact_version(),
            "shapely": shapely.__version__,
            "geos": shapely.geos_version_string,
            "pyproj": pyproj.__version__,
            "proj": pyproj.proj_version_str,
        },
    }
