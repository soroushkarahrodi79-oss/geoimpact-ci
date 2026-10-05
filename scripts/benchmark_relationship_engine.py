"""PERFORMANCE / SCALE BENCHMARK for deterministic relationship workloads.

This benchmark is not scientific evidence and never writes product artifacts.
It compares the current indexed engine with a simple exhaustive measurement
reference on deterministic synthetic geometries.
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import time
from typing import Any

import pyproj
import shapely
from shapely.geometry import Point, box

from geoimpact.relationships import PrimarySpatialIndex, derive_within_assignments


WORKLOADS = {
    "small": (30, 120),
    "medium": (100, 500),
    "large": (300, 1500),
}


def _build_workload(primary_count: int, dependent_count: int):
    primary = {
        f"primary-{index:06d}": box(index * 3, 0, index * 3 + 2, 2)
        for index in range(primary_count)
    }
    dependents = {
        f"dependent-{index:06d}": Point((index % primary_count) * 3 + 1, 1)
        for index in range(dependent_count)
    }
    return dependents, primary


def _exhaustive_measurement_reference(dependents, primary):
    """Unoptimized benchmark reference; never used by product analysis."""
    result: dict[str, dict[str, list[str]]] = {}
    for dependent_id in sorted(dependents):
        geometry = dependents[dependent_id]
        result[dependent_id] = {
            "within": [key for key in sorted(primary) if geometry.within(primary[key])],
            "boundary_primary_ids": [
                key for key in sorted(primary) if geometry.touches(primary[key])
            ],
        }
    return result


def _median_runtime(call, repetitions: int) -> tuple[float, Any]:
    durations: list[float] = []
    result = None
    for _ in range(repetitions):
        started = time.perf_counter()
        result = call()
        durations.append(time.perf_counter() - started)
    return statistics.median(durations), result


def run_benchmark(repetitions: int = 3) -> dict[str, Any]:
    results = []
    for name, (primary_count, dependent_count) in WORKLOADS.items():
        dependents, primary = _build_workload(primary_count, dependent_count)
        index = PrimarySpatialIndex(primary)
        candidate_count = sum(
            len(index.candidate_primary_ids(geometry)) for geometry in dependents.values()
        )
        theoretical_pairs = primary_count * dependent_count
        naive_seconds, naive_result = _median_runtime(
            lambda: _exhaustive_measurement_reference(dependents, primary), repetitions
        )
        indexed_seconds, indexed_result = _median_runtime(
            lambda: derive_within_assignments(dependents, primary), repetitions
        )
        if indexed_result != naive_result:
            raise AssertionError(f"{name} synthetic workload changed assignment semantics")
        results.append(
            {
                "name": name,
                "primary_count": primary_count,
                "dependent_count": dependent_count,
                "theoretical_pair_count_per_assignment": theoretical_pairs,
                "naive_theoretical_predicate_calls": theoretical_pairs * 2,
                "index_candidate_count": candidate_count,
                "indexed_exact_predicate_calls": candidate_count * 2,
                "candidate_reduction_percent": round(
                    100 * (1 - candidate_count / theoretical_pairs), 3
                ),
                "naive_median_seconds": round(naive_seconds, 6),
                "indexed_median_seconds": round(indexed_seconds, 6),
                "median_speedup": round(naive_seconds / indexed_seconds, 2),
            }
        )
    return {
        "label": "PERFORMANCE / SCALE BENCHMARK — synthetic, not scientific evidence",
        "os": platform.platform(),
        "python": platform.python_version(),
        "shapely": shapely.__version__,
        "geos": shapely.geos_version_string,
        "pyproj": pyproj.__version__,
        "proj": pyproj.proj_version_str,
        "repetitions": repetitions,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--synthetic", action="store_true", help="run deterministic workloads")
    parser.add_argument("--repetitions", type=int, default=3)
    args = parser.parse_args()
    if not args.synthetic:
        parser.error("select the --synthetic performance workload")
    if args.repetitions < 3:
        parser.error("use at least three repetitions for median timing")
    print(json.dumps(run_benchmark(args.repetitions), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
