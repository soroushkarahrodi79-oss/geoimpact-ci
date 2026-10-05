import json
from pathlib import Path

import pytest

from scripts.verify_madrid_benchmark import (
    canonical_json_sha256,
    relationship_identity_digest,
    transition_histogram,
    validate_transition_manifest,
)


MANIFEST = Path(__file__).parent / "fixtures" / "madrid_benchmark_expected.json"


def test_canonical_json_digest_ignores_key_order_and_whitespace() -> None:
    assert canonical_json_sha256({"a": 1, "b": 2}) == canonical_json_sha256(
        {"b": 2, "a": 1}
    )


def test_transition_histogram_is_sorted_and_counts_all_pairs() -> None:
    records = [
        {"before": ["old-b"], "after": ["new-b"]},
        {"before": ["old-a"], "after": ["new-a"]},
        {"before": ["old-b"], "after": ["new-b"]},
    ]
    assert transition_histogram(records) == [
        {"from": "old-a", "to": "new-a", "count": 1},
        {"from": "old-b", "to": "new-b", "count": 2},
    ]


def test_transition_manifest_freezes_complete_madrid_pair_set() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pairs = manifest["transitions"]
    assert len(pairs) == 26
    assert sum(pair["count"] for pair in pairs) == 2112
    assert {pair["from"]: pair["count"] for pair in pairs if pair["from"] == "2807918058"} == {
        "2807918058": 328
    }
    assert {pair["to"]: pair["count"] for pair in pairs if pair["to"] == "2807919059"} == {
        "2807919059": 269
    }
    validate_transition_manifest(pairs, pairs)


def test_transition_manifest_mismatch_fails_loudly() -> None:
    with pytest.raises(AssertionError, match="transition histogram mismatch"):
        validate_transition_manifest(
            [{"from": "old", "to": "new", "count": 2}],
            [{"from": "old", "to": "new", "count": 1}],
        )


def test_relationship_identity_digest_is_order_independent_and_sensitive() -> None:
    first = {
        "portal_id": "portal-1",
        "old_cusec": "old",
        "new_cusec": "new",
        "classification": "split-like",
    }
    second = {
        "portal_id": "portal-2",
        "old_cusec": "old-2",
        "new_cusec": "new-2",
        "classification": "merge-like",
    }
    assert relationship_identity_digest([first, second]) == relationship_identity_digest(
        [second, first]
    )
    changed = {**second, "classification": "split-like"}
    assert relationship_identity_digest([first, second]) != relationship_identity_digest(
        [first, changed]
    )
