"""Evaluation of the configured relationship-regression policy."""

from __future__ import annotations

from geoimpact.models import PolicyResult


def evaluate_max_relationship_regressions(
    observed_value: int, threshold: int, evidence_ids: list[str]
) -> PolicyResult:
    """Evaluate the fixed max_relationship_regressions BLOCK rule."""
    return {
        "rule": "max_relationship_regressions",
        "observed_value": observed_value,
        "threshold": threshold,
        "evidence_ids": sorted(evidence_ids),
        "status": "PASS" if observed_value <= threshold else "BLOCK",
    }
