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

# Displacement is a derived measurement in EPSG:25830 metres. Conforming only
# measurement copies to this grid makes the published scalar deterministic;
# it is not a claim about the accuracy of source geometries.
BOUNDARY_DISPLACEMENT_GRID_SIZE_M = 1e-6


def _geojson_geometry(geometry: BaseGeometry) -> dict[str, object]:
    """Return a JSON-compatible geometry with deterministic key ordering."""
    return json.loads(json.dumps(mapping(geometry), sort_keys=True))


def measure_primary_change(
    base: Mapping[str, BaseGeometry], candidate: Mapping[str, BaseGeometry]
) -> dict[str, object]:
    """Measure fixed-grid footprint and precision-qualified displacement.

    The fixed precision is used for derived footprint overlays and temporary
    displacement-measurement copies. Added and removed features contribute
    their full geometry to the footprint. Feature equality and relationship
    analysis retain full-precision source geometries.
    """
    base_ids = set(base)
    candidate_ids = set(candidate)
    added_ids = sorted(candidate_ids - base_ids)
    removed_ids = sorted(base_ids - candidate_ids)
    shared_ids = sorted(base_ids & candidate_ids)
    modified_ids = [
        feature_id
        for feature_id in shared_ids
        if not base[feature_id].equals(candidate[feature_id])
    ]
    statuses: dict[str, str] = {}
    for feature_id in sorted(base_ids | candidate_ids):
        if feature_id not in base_ids:
            statuses[feature_id] = "added"
        elif feature_id not in candidate_ids:
            statuses[feature_id] = "removed"
        elif base[feature_id].equals(candidate[feature_id]):
            statuses[feature_id] = "unchanged"
        else:
            statuses[feature_id] = "modified"
    changed_ids = sorted(added_ids + removed_ids + modified_ids)

    feature_footprints = [base[feature_id] for feature_id in removed_ids]
    feature_footprints.extend(candidate[feature_id] for feature_id in added_ids)
    feature_footprints.extend(
        shapely.symmetric_difference(
            base[feature_id],
            candidate[feature_id],
            grid_size=CHANGE_FOOTPRINT_GRID_SIZE_M,
        )
        for feature_id in modified_ids
    )
    if feature_footprints:
        footprint = shapely.normalize(
            shapely.union_all(feature_footprints, grid_size=CHANGE_FOOTPRINT_GRID_SIZE_M)
        )
        footprint_area = footprint.area
        footprint_geometry = _geojson_geometry(footprint)
    else:
        footprint_area = 0.0
        footprint_geometry = None

    # A displacement is defined only for the same stable feature in both
    # snapshots. Additions and removals have no counterpart to compare.
    maximum_displacement = (
        float(
            max(
                shapely.hausdorff_distance(
                    shapely.set_precision(
                        base[feature_id], grid_size=BOUNDARY_DISPLACEMENT_GRID_SIZE_M
                    ),
                    shapely.set_precision(
                        candidate[feature_id], grid_size=BOUNDARY_DISPLACEMENT_GRID_SIZE_M
                    ),
                )
                for feature_id in modified_ids
            )
        )
        if modified_ids
        else 0.0
    )

    return {
        "feature_geometry_status": statuses,
        "changed_feature_ids": changed_ids,
        "added_feature_ids": added_ids,
        "removed_feature_ids": removed_ids,
        "modified_feature_ids": modified_ids,
        "changed_footprint_area_m2": footprint_area,
        "changed_footprint_geometry": footprint_geometry,
        "max_boundary_displacement_m": maximum_displacement,
    }
