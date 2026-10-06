"""Stable evidence records for relationship regressions."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from shapely.geometry import mapping
from shapely.geometry.base import BaseGeometry

from geoimpact.models import RelationshipChange, RelationshipRegression


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def relationship_evidence(
    *,
    primary_dataset: str,
    dependent_dataset: str,
    dependent_id: str,
    dependent_geometry: BaseGeometry,
    before: list[str],
    after: list[str],
    change_type: RelationshipChange,
) -> RelationshipRegression:
    """Build content-addressed, reviewable evidence for one relationship delta."""
    primary_feature_ids = sorted(set(before) | set(after))
    identity = {
        "primary_dataset": primary_dataset,
        "primary_feature_ids": primary_feature_ids,
        "dependent_dataset": dependent_dataset,
        "dependent_id": dependent_id,
        "predicate": "within",
        "before": before,
        "after": after,
        "change_type": change_type,
    }
    evidence_id = "relationship-regression-" + hashlib.sha256(
        _canonical_json(identity).encode("ascii")
    ).hexdigest()
    geometry = json.loads(json.dumps(mapping(dependent_geometry), sort_keys=True))
    return {
        "evidence_id": evidence_id,
        **identity,
        "evidence_geometry_crs": "EPSG:25830",
        "evidence_geometry": geometry,
    }
