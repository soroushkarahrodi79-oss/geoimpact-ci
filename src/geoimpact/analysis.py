"""Small deterministic orchestration for the Gate 1 fixture only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

from pyproj import Transformer
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry
from shapely.ops import transform

from geoimpact.evidence import relationship_evidence
from geoimpact.geometry_change import measure_primary_change
from geoimpact.policy import evaluate_max_relationship_regressions
from geoimpact.relationships import classify_assignment_change, derive_within_assignments


FIXTURE_CRS = "EPSG:25830"
PRIMARY_DATASET = "districts"
_CRS84_TO_ANALYSIS = Transformer.from_crs("OGC:CRS84", FIXTURE_CRS, always_xy=True)


def load_features(path: Path, id_field: str) -> dict[str, BaseGeometry]:
    """Load the narrow FeatureCollection fixture format with stable IDs."""
    collection = json.loads(path.read_text(encoding="utf-8"))
    if collection.get("type") != "FeatureCollection":
        raise ValueError(f"{path} is not a FeatureCollection")

    features: dict[str, BaseGeometry] = {}
    for feature in collection.get("features", []):
        feature_id = feature.get("properties", {}).get(id_field)
        if not isinstance(feature_id, str) or not feature_id:
            raise ValueError(f"{path} has a missing stable {id_field}")
        if feature_id in features:
            raise ValueError(f"{path} has duplicate stable ID {feature_id}")
        geometry = transform(_CRS84_TO_ANALYSIS.transform, shape(feature["geometry"]))
        if geometry.is_empty or not geometry.is_valid:
            raise ValueError(f"{path} has invalid or empty geometry for {feature_id}")
        features[feature_id] = geometry
    return features


def analyze(
    base_primary_path: Path,
    candidate_primary_path: Path,
    dependent_sources: Mapping[str, tuple[Path, str]],
    *,
    relationship_threshold: int,
) -> dict[str, object]:
    """Analyze the declared fixed dependencies against BASE and CANDIDATE."""
    base_primary = load_features(base_primary_path, "district_id")
    candidate_primary = load_features(candidate_primary_path, "district_id")
    relationship_records: list[dict[str, object]] = []
    regression_evidence: list[dict[str, object]] = []
    boundary_ambiguities: list[dict[str, object]] = []

    for dependent_dataset in sorted(dependent_sources):
        dependent_path, id_field = dependent_sources[dependent_dataset]
        dependents = load_features(dependent_path, id_field)
        before_assignments = derive_within_assignments(dependents, base_primary)
        after_assignments = derive_within_assignments(dependents, candidate_primary)

        for dependent_id in sorted(dependents):
            before = before_assignments[dependent_id]["within"]
            after = after_assignments[dependent_id]["within"]
            before_boundary = before_assignments[dependent_id]["boundary_primary_ids"]
            after_boundary = after_assignments[dependent_id]["boundary_primary_ids"]
            change_type = classify_assignment_change(before, after)
            relationship_records.append(
                {
                    "dependent_dataset": dependent_dataset,
                    "dependent_id": dependent_id,
                    "predicate": "within",
                    "before": before,
                    "after": after,
                    "change_type": change_type,
                }
            )
            if before_boundary or after_boundary:
                boundary_ambiguities.append(
                    {
                        "dependent_dataset": dependent_dataset,
                        "dependent_id": dependent_id,
                        "before_boundary_primary_ids": before_boundary,
                        "after_boundary_primary_ids": after_boundary,
                    }
                )
            if change_type != "unchanged":
                regression_evidence.append(
                    relationship_evidence(
                        primary_dataset=PRIMARY_DATASET,
                        dependent_dataset=dependent_dataset,
                        dependent_id=dependent_id,
                        dependent_geometry=dependents[dependent_id],
                        before=before,
                        after=after,
                        change_type=change_type,
                    )
                )

    policy = evaluate_max_relationship_regressions(
        len(regression_evidence),
        relationship_threshold,
        [str(evidence["evidence_id"]) for evidence in regression_evidence],
    )
    return {
        "analysis_crs": FIXTURE_CRS,
        "primary_dataset": PRIMARY_DATASET,
        "primary_geometry_change": measure_primary_change(base_primary, candidate_primary),
        "relationships": relationship_records,
        "relationship_regressions": regression_evidence,
        "boundary_ambiguities": boundary_ambiguities,
        "policy": policy,
    }
