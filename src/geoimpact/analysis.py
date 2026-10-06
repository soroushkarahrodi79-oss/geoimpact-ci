"""Small deterministic orchestration for the Gate 1 fixture only."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Literal, Mapping

from pyproj import Transformer
from pyproj.exceptions import ProjError
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry
from shapely.errors import GEOSException
from shapely.ops import transform

from geoimpact.errors import InputError
from geoimpact.evidence import relationship_evidence
from geoimpact.geometry_change import measure_primary_change
from geoimpact.models import (
    AnalysisResult,
    BoundaryAmbiguity,
    RelationshipRecord,
    RelationshipRegression,
)
from geoimpact.policy import evaluate_max_relationship_regressions
from geoimpact.relationships import (
    PrimarySpatialIndex,
    classify_assignment_change,
    derive_within_assignments,
)


FIXTURE_CRS: Literal["EPSG:25830"] = "EPSG:25830"
PRIMARY_DATASET = "districts"
_CRS84_TO_ANALYSIS = Transformer.from_crs("OGC:CRS84", FIXTURE_CRS, always_xy=True)


def _finite_coordinates(value: object, *, path: Path, feature_id: str) -> None:
    if isinstance(value, (list, tuple)):
        for item in value:
            _finite_coordinates(item, path=path, feature_id=feature_id)
        return
    try:
        valid_number = (
            not isinstance(value, bool)
            and isinstance(value, (int, float))
            and math.isfinite(float(value))
        )
    except OverflowError:
        valid_number = False
    if not valid_number:
        raise InputError(f"{path} has malformed or non-finite coordinates for {feature_id}")


def load_features(
    path: Path,
    id_field: str,
    *,
    geometry_role: str = "primary",
) -> dict[str, BaseGeometry]:
    """Load supported GeoJSON features and enforce the narrow geometry contract."""
    try:
        raw_json = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise InputError(f"{path} cannot be read as UTF-8 GeoJSON") from error
    try:
        collection = json.loads(raw_json)
    except json.JSONDecodeError as error:
        raise InputError(f"{path} contains malformed JSON: {error.msg}") from error
    except RecursionError as error:
        raise InputError(f"{path} contains excessively nested JSON") from error
    if not isinstance(collection, dict):
        raise InputError(f"{path} must contain a top-level GeoJSON object")
    if collection.get("type") != "FeatureCollection":
        raise InputError(f"{path} is not a FeatureCollection")
    if "features" not in collection:
        raise InputError(f"{path} is missing features")
    collection_features = collection["features"]
    if not isinstance(collection_features, list):
        raise InputError(f"{path} features must be a list")

    features: dict[str, BaseGeometry] = {}
    allowed_types = {"primary": {"Polygon", "MultiPolygon"}, "dependent": {"Point"}}
    if geometry_role not in allowed_types:
        raise ValueError(f"unsupported internal geometry role: {geometry_role}")
    for index, feature in enumerate(collection_features):
        if not isinstance(feature, dict):
            raise InputError(f"{path} feature at index {index} must be an object")
        if feature.get("type") != "Feature":
            raise InputError(f"{path} feature at index {index} must have type Feature")
        properties = feature.get("properties")
        if not isinstance(properties, dict):
            raise InputError(f"{path} feature at index {index} properties must be an object")
        feature_id = properties.get(id_field)
        if not isinstance(feature_id, str) or not feature_id.strip():
            raise InputError(f"{path} feature at index {index} has a missing or invalid stable {id_field}")
        if feature_id in features:
            raise InputError(f"{path} has duplicate stable ID {feature_id}")
        if "geometry" not in feature:
            raise InputError(f"{path} {geometry_role} {feature_id} is missing geometry")
        geometry_value = feature["geometry"]
        if not isinstance(geometry_value, dict):
            raise InputError(f"{path} {geometry_role} {feature_id} geometry must be an object")
        geometry_type = geometry_value.get("type")
        if not isinstance(geometry_type, str) or geometry_type not in allowed_types[geometry_role]:
            expected = "Polygon or MultiPolygon" if geometry_role == "primary" else "Point"
            raise InputError(
                f"{geometry_role} {feature_id} must be {expected}, got {geometry_type or 'unknown'}"
            )
        if geometry_value.get("coordinates") is None:
            raise InputError(f"{path} {geometry_role} {feature_id} has missing or null geometry coordinates")
        try:
            _finite_coordinates(geometry_value["coordinates"], path=path, feature_id=feature_id)
        except RecursionError as error:
            raise InputError(f"{path} has excessively nested coordinates for {feature_id}") from error
        try:
            geometry = transform(_CRS84_TO_ANALYSIS.transform, shape(geometry_value))
        except (
            KeyError,
            TypeError,
            ValueError,
            IndexError,
            RecursionError,
            GEOSException,
            ProjError,
        ) as error:
            raise InputError(f"{path} has malformed geometry for {feature_id}") from error
        if geometry.geom_type not in allowed_types[geometry_role]:
            expected = "Polygon or MultiPolygon" if geometry_role == "primary" else "Point"
            raise InputError(f"{geometry_role} {feature_id} must be {expected}, got {geometry.geom_type}")
        if geometry.is_empty or not geometry.is_valid:
            raise InputError(f"{path} has invalid or empty geometry for {feature_id}")
        features[feature_id] = geometry
    return features


def analyze(
    base_primary_path: Path,
    candidate_primary_path: Path,
    dependent_sources: Mapping[str, tuple[Path, str]],
    *,
    relationship_threshold: int,
    primary_id_field: str = "district_id",
    primary_dataset: str = PRIMARY_DATASET,
) -> AnalysisResult:
    """Analyze the declared fixed dependencies against BASE and CANDIDATE."""
    base_primary = load_features(base_primary_path, primary_id_field, geometry_role="primary")
    candidate_primary = load_features(
        candidate_primary_path, primary_id_field, geometry_role="primary"
    )
    base_index = PrimarySpatialIndex(base_primary)
    candidate_index = PrimarySpatialIndex(candidate_primary)
    relationship_records: list[RelationshipRecord] = []
    regression_evidence: list[RelationshipRegression] = []
    boundary_ambiguities: list[BoundaryAmbiguity] = []

    for dependent_dataset in sorted(dependent_sources):
        dependent_path, id_field = dependent_sources[dependent_dataset]
        dependents = load_features(dependent_path, id_field, geometry_role="dependent")
        before_assignments = derive_within_assignments(
            dependents, base_primary, spatial_index=base_index
        )
        after_assignments = derive_within_assignments(
            dependents, candidate_primary, spatial_index=candidate_index
        )

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
                        primary_dataset=primary_dataset,
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
        "primary_dataset": primary_dataset,
        "primary_geometry_change": measure_primary_change(base_primary, candidate_primary),
        "relationships": relationship_records,
        "relationship_regressions": regression_evidence,
        "boundary_ambiguities": boundary_ambiguities,
        "policy": policy,
    }
