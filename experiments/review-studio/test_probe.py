"""Failure-mode tests against regenerated retained cases; no spatial recomputation."""
import argparse
from pathlib import Path
import shutil
import tempfile
import unittest

import probe

def join_inputs(case):
    spec = probe.CASES[case]
    report = probe.read_json(args.outputs / spec["output"] / "report.json")
    folder = args.repo / spec["directory"]
    primary_id = report["analysis"]["primary_id_field"]
    dep_id = report["analysis"]["dependencies"][0]["id_field"]
    base = probe.indexed_features(folder / spec["base"], primary_id, {"Polygon", "MultiPolygon"})
    candidate = probe.indexed_features(folder / spec["candidate"], primary_id, {"Polygon", "MultiPolygon"})
    deps = probe.indexed_features(folder / spec["dependency"], dep_id, {"Point"})
    geojson = probe.read_json(args.outputs / spec["output"] / "relationship-regressions.geojson")
    return report, base, candidate, deps, geojson


class ReadinessFailures(unittest.TestCase):
    def test_both_frozen_cases_and_empty_sierra_are_accepted(self):
        madrid = probe.probe_case(args.repo, args.outputs, "madrid")
        sierra = probe.probe_case(args.repo, args.outputs, "sierra")
        self.assertEqual((madrid["verdict"], madrid["relationship_regressions"]), ("BLOCK", 2112))
        self.assertEqual((sierra["verdict"], sierra["relationship_records"], sierra["relationship_regressions"]),
                         ("PASS", 52, 0))

    def test_whitespace_change_to_original_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            spec = probe.CASES["sierra"]
            shutil.copytree(args.repo / spec["directory"], root / spec["directory"])
            path = root / spec["directory"] / spec["base"]
            path.write_bytes(path.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "input byte identity mismatch"):
                probe.probe_case(root, args.outputs, "sierra")

    def test_changed_artifact_is_rejected_even_if_json_is_equivalent(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(args.outputs / "gate8", root / "gate8")
            path = root / "gate8/report.json"
            path.write_bytes(path.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "frozen artifact hash mismatch"):
                probe.probe_case(args.repo, root, "sierra")

    def test_missing_artifact_is_not_treated_as_zero(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(args.outputs / "gate8", root / "gate8")
            (root / "gate8/relationship-regressions.geojson").unlink()
            with self.assertRaises(FileNotFoundError):
                probe.probe_case(args.repo, root, "sierra")

    def test_unknown_report_version_is_rejected(self):
        parts = list(join_inputs("sierra"))
        parts[0]["report_version"] = "4"
        with self.assertRaisesRegex(ValueError, "V5 required"):
            probe.check_joins(*parts)

    def test_missing_fixed_dependent_is_rejected(self):
        parts = list(join_inputs("madrid"))
        parts[3].pop(next(iter(parts[3])))
        with self.assertRaisesRegex(ValueError, "dependency ID missing"):
            probe.check_joins(*parts)

    def test_nonexistent_before_primary_id_is_rejected(self):
        parts = list(join_inputs("madrid"))
        parts[0]["relationships"][0]["before"] = ["not-a-retained-id"]
        with self.assertRaisesRegex(ValueError, "BASE assignment references absent ID"):
            probe.check_joins(*parts)

    def test_mismatched_geojson_evidence_is_rejected(self):
        parts = list(join_inputs("madrid"))
        parts[4]["features"][0]["properties"]["after"] = []
        with self.assertRaisesRegex(ValueError, "GeoJSON property mismatch"):
            probe.check_joins(*parts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--outputs", type=Path, required=True)
    args, unittest_args = parser.parse_known_args()
    unittest.main(argv=[__file__, *unittest_args])
