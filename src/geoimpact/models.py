"""Standard-library type contracts for GeoImpact's internal dictionaries.

These types describe the existing in-memory and serialized structures. They
do not validate data at runtime or transform values during serialization.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal, TypedDict


FeatureGeometryStatus = Literal["unchanged", "modified", "added", "removed"]
RelationshipChange = Literal[
    "unchanged", "assignment_changed", "assignment_lost", "assignment_gained"
]
Predicate = Literal["within"]
Verdict = Literal["PASS", "BLOCK"]
EvidenceGeometry = dict[str, object]


class PrimaryContract(TypedDict):
    dataset: str
    id_field: str
    base: Path
    candidate: Path


class DependencyContract(TypedDict):
    dataset: str
    path: Path
    id_field: str
    predicate: Predicate


class GeoImpactContract(TypedDict):
    version: Literal[1]
    analysis_crs: Literal["EPSG:25830"]
    primary: PrimaryContract
    dependencies: list[DependencyContract]
    threshold: int
    severity: Literal["block"]


class PrimaryChange(TypedDict):
    feature_geometry_status: dict[str, FeatureGeometryStatus]
    changed_feature_ids: list[str]
    added_feature_ids: list[str]
    removed_feature_ids: list[str]
    modified_feature_ids: list[str]
    changed_footprint_area_m2: float
    changed_footprint_geometry: EvidenceGeometry | None
    max_boundary_displacement_m: float


class RelationshipRecord(TypedDict):
    dependent_dataset: str
    dependent_id: str
    predicate: Predicate
    before: list[str]
    after: list[str]
    change_type: RelationshipChange


class RelationshipRegression(TypedDict):
    evidence_id: str
    primary_dataset: str
    primary_feature_ids: list[str]
    dependent_dataset: str
    dependent_id: str
    predicate: Predicate
    before: list[str]
    after: list[str]
    change_type: RelationshipChange
    evidence_geometry_crs: Literal["EPSG:25830"]
    evidence_geometry: EvidenceGeometry


class BoundaryAmbiguity(TypedDict):
    dependent_dataset: str
    dependent_id: str
    before_boundary_primary_ids: list[str]
    after_boundary_primary_ids: list[str]


class PolicyResult(TypedDict):
    rule: Literal["max_relationship_regressions"]
    observed_value: int
    threshold: int
    evidence_ids: list[str]
    status: Verdict


class AnalysisResult(TypedDict):
    analysis_crs: Literal["EPSG:25830"]
    primary_dataset: str
    primary_geometry_change: PrimaryChange
    relationships: list[RelationshipRecord]
    relationship_regressions: list[RelationshipRegression]
    boundary_ambiguities: list[BoundaryAmbiguity]
    policy: PolicyResult


class ReportAnalysisSection(TypedDict):
    crs: Literal["EPSG:25830"]
    primary_dataset: str
    primary_id_field: str
    dependencies: list["ReportDependency"]


class ReportDependency(TypedDict):
    dataset: str
    id_field: str
    predicate: Predicate


class GeoImpactReport(TypedDict):
    report_version: Literal["4"]
    analysis: ReportAnalysisSection
    primary_change: PrimaryChange
    relationships: list[RelationshipRecord]
    relationship_regressions: list[RelationshipRegression]
    boundary_ambiguities: list[BoundaryAmbiguity]
    policy: PolicyResult
    verdict: Verdict


class WithinAssignment(TypedDict):
    within: list[str]
    boundary_primary_ids: list[str]
