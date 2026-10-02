from geoimpact.policy import evaluate_max_relationship_regressions


def test_policy_passes_at_threshold() -> None:
    assert evaluate_max_relationship_regressions(1, 1, ["evidence-a"]) == {
        "rule": "max_relationship_regressions",
        "observed_value": 1,
        "threshold": 1,
        "evidence_ids": ["evidence-a"],
        "status": "PASS",
    }


def test_policy_blocks_above_threshold() -> None:
    result = evaluate_max_relationship_regressions(2, 1, ["evidence-b", "evidence-a"])

    assert result == {
        "rule": "max_relationship_regressions",
        "observed_value": 2,
        "threshold": 1,
        "evidence_ids": ["evidence-a", "evidence-b"],
        "status": "BLOCK",
    }
