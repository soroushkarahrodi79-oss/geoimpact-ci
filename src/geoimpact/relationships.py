"""Topological WITHIN assignments for the Gate 1 vertical slice."""

from __future__ import annotations

from typing import Mapping

from shapely.geometry.base import BaseGeometry


def derive_within_assignments(
    dependents: Mapping[str, BaseGeometry], primary: Mapping[str, BaseGeometry]
) -> dict[str, dict[str, list[str]]]:
    """Derive exact WITHIN assignments and separately report boundary touches.

    A geometry which merely touches a primary boundary is never put in
    ``within``. This is a direct GEOS topological predicate, not a bounds,
    centroid, or distance-based approximation.
    """
    result: dict[str, dict[str, list[str]]] = {}
    for dependent_id in sorted(dependents):
        geometry = dependents[dependent_id]
        result[dependent_id] = {
            "within": [
                primary_id for primary_id in sorted(primary) if geometry.within(primary[primary_id])
            ],
            "boundary_primary_ids": [
                primary_id for primary_id in sorted(primary) if geometry.touches(primary[primary_id])
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
