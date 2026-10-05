"""Topological WITHIN assignments for the Gate 1 vertical slice."""

from __future__ import annotations

from typing import Mapping

from shapely import STRtree
from shapely.geometry.base import BaseGeometry


class PrimarySpatialIndex:
    """Use STRtree bounds only to find possible exact predicate matches."""

    def __init__(self, primary: Mapping[str, BaseGeometry]) -> None:
        self._primary = primary
        self._primary_ids = tuple(sorted(primary))
        self._geometries = tuple(primary[primary_id] for primary_id in self._primary_ids)
        self._tree = STRtree(self._geometries) if self._geometries else None

    def candidate_primary_ids(self, geometry: BaseGeometry) -> list[str]:
        """Return envelope candidates in stable ID order, never as evidence."""
        if self._tree is None:
            return []
        indices = self._tree.query(geometry)
        return sorted(self._primary_ids[int(index)] for index in indices)


def derive_within_assignments(
    dependents: Mapping[str, BaseGeometry],
    primary: Mapping[str, BaseGeometry],
    *,
    spatial_index: PrimarySpatialIndex | None = None,
) -> dict[str, dict[str, list[str]]]:
    """Derive exact WITHIN assignments and separately report boundary touches.

    A geometry which merely touches a primary boundary is never put in
    ``within``. This is a direct GEOS topological predicate, not a bounds,
    centroid, or distance-based approximation.
    """
    result: dict[str, dict[str, list[str]]] = {}
    index = spatial_index or PrimarySpatialIndex(primary)
    if index._primary is not primary:
        raise ValueError("spatial_index must be built from the supplied primary mapping")
    for dependent_id in sorted(dependents):
        geometry = dependents[dependent_id]
        candidates = index.candidate_primary_ids(geometry)
        result[dependent_id] = {
            "within": [
                primary_id for primary_id in candidates if geometry.within(primary[primary_id])
            ],
            "boundary_primary_ids": [
                primary_id for primary_id in candidates if geometry.touches(primary[primary_id])
            ],
        }
    return result


def classify_assignment_change(before: list[str], after: list[str]) -> str:
    """Name a relationship delta without imposing a one-to-one assignment."""
    if before == after:
        return "unchanged"
    if before and after:
        return "assignment_changed"
    if before:
        return "assignment_lost"
    return "assignment_gained"
