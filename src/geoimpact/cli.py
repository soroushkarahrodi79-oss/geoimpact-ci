"""Command-line interface for a declared GeoImpact analysis."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from geoimpact.errors import GeoImpactError
from geoimpact.runner import run_from_config


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="geoimpact")
    commands = parser.add_subparsers(dest="command", required=True)
    analyze = commands.add_parser("analyze", help="analyze a declared dataset change")
    analyze.add_argument("--config", required=True, type=Path, help="v1 YAML config file")
    analyze.add_argument("--out", required=True, type=Path, help="artifact output directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run one declared analysis and return its PASS/BLOCK/ERROR exit status."""
    arguments = _parser().parse_args(argv)
    try:
        report = run_from_config(arguments.config, arguments.out)
    except (GeoImpactError, OSError, UnicodeError) as error:
        # Only expected GeoImpact domain/input failures and operational I/O
        # errors become a controlled exit 2. Unexpected programming errors
        # (including a bare ValueError) are left to propagate as a traceback.
        print(f"GeoImpact error: {error}", file=sys.stderr)
        return 2

    output = arguments.out.resolve()
    print("GeoImpact CI")
    print(f"Verdict: {report['verdict']}")
    print(f"Report: {output / 'report.json'}")
    print(f"Markdown: {output / 'report.md'}")
    print(f"Evidence: {output / 'relationship-regressions.geojson'}")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
