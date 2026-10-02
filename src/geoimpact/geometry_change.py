"""Geometry measurements for the Gate 1 controlled polygon mutation."""

from __future__ import annotations

import json
from typing import Mapping

from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union


def _geojson_geometry(geometry: BaseGeometry) -> dict[str, object]:
    """Return a JSON-compatible geometry with deterministic key ordering."""
    return json.loads(json.dumps(mapping(geometry), sort_keys=True))


def measure_primary_change(
    base: Mapping[str, BaseGeometry], candidate: Mapping[str, BaseGeometry]
) -> dict[str, object]:
    """Measure changed polygon footprint and discrete Hausdorff displacement.

    The Gate 1 fixture contains the same two stable primary IDs in both states.
    A feature is spatially unchanged exactly when Shapely's topological
    ``equals`` predicate is true, matching the Gate 0 change model.
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
        base[feature_id].symmetric_difference(candidate[feature_id])
        for feature_id in changed_ids
    ]
    footprint = unary_union(feature_footprints)
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
