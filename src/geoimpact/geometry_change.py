"""Geometry measurements for the primary-layer change footprint."""

from __future__ import annotations

import json
from typing import Mapping

import shapely
from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry


# The derived overlay is in EPSG:25830 metres. This is a representation and
# robustness model for the footprint only, not a source-accuracy claim.
CHANGE_FOOTPRINT_GRID_SIZE_M = 1e-6


def _geojson_geometry(geometry: BaseGeometry) -> dict[str, object]:
    """Return a JSON-compatible geometry with deterministic key ordering."""
    return json.loads(json.dumps(mapping(geometry), sort_keys=True))


def measure_primary_change(
    base: Mapping[str, BaseGeometry], candidate: Mapping[str, BaseGeometry]
) -> dict[str, object]:
    """Measure the fixed-grid change footprint and full-precision displacement.

    The fixed precision is limited to the derived symmetric-difference and
    union operations. Feature equality and Hausdorff displacement retain their
    existing full-precision semantics; relationship analysis is independent.
    """
    shared_ids = sorted(set(base) & set(candidate))
    statuses = {
        feature_id: "unchanged" if base[feature_id].equals(candidate[feature_id]) else "modified"
        for feature_id in shared_ids
    }
    changed_ids = [feature_id for feature_id in shared_ids if statuses[feature_id] == "modified"]

    if not changed_ids:
        return {
            "feature_geometry_status": statuses,
            "changed_feature_ids": [],
            "changed_footprint_area_m2": 0.0,
            "changed_footprint_geometry": None,
            "max_boundary_displacement_m": 0.0,
        }

    feature_footprints = [
        shapely.symmetric_difference(
            base[feature_id],
            candidate[feature_id],
            grid_size=CHANGE_FOOTPRINT_GRID_SIZE_M,
        )
        for feature_id in changed_ids
    ]
    footprint = shapely.normalize(
        shapely.union_all(feature_footprints, grid_size=CHANGE_FOOTPRINT_GRID_SIZE_M)
    )
    maximum_displacement = max(
        base[feature_id].hausdorff_distance(candidate[feature_id]) for feature_id in changed_ids
    )

    return {
        "feature_geometry_status": statuses,
        "changed_feature_ids": changed_ids,
        "changed_footprint_area_m2": footprint.area,
        "changed_footprint_geometry": _geojson_geometry(footprint),
        "max_boundary_displacement_m": maximum_displacement,
    }
