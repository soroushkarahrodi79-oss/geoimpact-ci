"""Verify the installed GeoImpact CLI contract used by GitHub Actions."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
OUTPUTS = ROOT / "ci-output"
ARTIFACTS = (
    "report.json",
    "report.md",
    "relationship-regressions.geojson",
)
EXPECTED_HASHES = {
    "report.json": "2bfc39f79dbe11d9dc84d58923bba486ad29763155da905eb273cf0257433188",
    "report.md": "0a3525f5bf376fd47120175bc161de13769005cbcd194b9d350771a69a63009b",
    "relationship-regressions.geojson": "a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978",
}


def run_cli(config: Path, output: Path, expected_code: int) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [
            "geoimpact",
            "analyze",
            "--config",
            str(config),
            "--out",
            str(output),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != expected_code:
        raise RuntimeError(
            f"GeoImpact returned {result.returncode}; expected exactly {expected_code}"
        )
    return result


def require_artifacts(output: Path) -> None:
    missing = [name for name in ARTIFACTS if not (output / name).is_file()]
    if missing:
        raise RuntimeError(f"Required CLI artifacts are missing from {output}: {', '.join(missing)}")


def verify_scenario(name: str) -> None:
    if name == "pass":
        output = OUTPUTS / "pass"
        result = run_cli(FIXTURES / "geoimpact-pass.yml", output, 0)
        require_artifacts(output)
        if "Verdict: PASS" not in result.stdout:
            raise RuntimeError("PASS execution did not report Verdict: PASS")
    elif name == "block":
        output = OUTPUTS / "block"
        result = run_cli(FIXTURES / "geoimpact.yml", output, 1)
        require_artifacts(output)
        if "Verdict: BLOCK" not in result.stdout:
            raise RuntimeError("BLOCK execution did not report Verdict: BLOCK")
    elif name == "error":
        missing_config = FIXTURES / "missing_gate4.yml"
        if missing_config.exists():
            raise RuntimeError(f"Controlled missing-config path unexpectedly exists: {missing_config}")
        output = OUTPUTS / "error"
        result = run_cli(missing_config, output, 2)
        if "Verdict:" in result.stdout:
            raise RuntimeError("ERROR execution unexpectedly reported a verdict")
        if output.exists() and any(output.iterdir()):
            raise RuntimeError("ERROR execution unexpectedly produced output files")
    else:
        raise ValueError(f"Unknown contract scenario: {name}")
    print(f"Verified {name.upper()} CLI exit code and output contract.")


def verify_hashes() -> None:
    output = OUTPUTS / "block"
    require_artifacts(output)
    mismatches: list[str] = []
    for name in ARTIFACTS:
        actual = hashlib.sha256((output / name).read_bytes()).hexdigest()
        expected = EXPECTED_HASHES[name]
        print(f"SHA-256 {name}: {actual}")
        if actual != expected:
            mismatches.append(f"{name}: expected {expected}, got {actual}")
    if mismatches:
        raise RuntimeError("Canonical BLOCK artifact hash mismatch: " + "; ".join(mismatches))
    print("All canonical BLOCK artifact hashes match.")


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"pass", "block", "error", "hashes"}:
        print("Usage: python scripts/verify_ci_contract.py {pass|block|error|hashes}", file=sys.stderr)
        return 2
    try:
        if sys.argv[1] == "hashes":
            verify_hashes()
        else:
            verify_scenario(sys.argv[1])
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"CI contract verification failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
