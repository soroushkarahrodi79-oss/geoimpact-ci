"""Build and qualify GeoImpact wheel and sdist in fresh environments."""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import venv
import zipfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "1.1.0"
ARTIFACT_NAMES = (
    "report.json",
    "report.md",
    "relationship-regressions.geojson",
)
EXPECTED_BLOCK_HASHES = {
    "report.json": "a3245fb06b1a49c9cfec7d7b46cd70871937fdcb40700ad6c9733f470f73df13",
    "report.md": "222d3e3da2f7dc5c1c466249746022379a1735210792e3165435e49fae40d2f4",
    "relationship-regressions.geojson": "a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978",
}


def run(
    command: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, check=False)
    if result.returncode:
        raise RuntimeError(f"Command exited {result.returncode}: {command!r}")
    return result


def require_release_metadata() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    if metadata["project"]["version"] != EXPECTED_VERSION:
        raise RuntimeError(
            f"pyproject.toml version is not {EXPECTED_VERSION}"
        )
    if metadata["project"].get("readme") != "README.md":
        raise RuntimeError("README.md is not configured as package metadata")
    for relative in (
        "README.md",
        "CHANGELOG.md",
        "CITATION.cff",
        "docs/RELEASE_V1_1_0.md",
        "docs/ARCHITECTURE_V1.md",
        "docs/REPORT_V4_MIGRATION.md",
        "docs/TEST_STRATEGY.md",
    ):
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"Required release file is missing: {relative}")
    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    if citation.get("cff-version") != "1.2.0" or citation.get("version") != EXPECTED_VERSION:
        raise RuntimeError("CITATION.cff version contract is invalid")


def verify_archives(wheel: Path, sdist: Path) -> None:
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        required = {
            "geoimpact/analysis.py",
            "geoimpact/cli.py",
            "geoimpact/contract.py",
            "geoimpact/geometry_change.py",
            "geoimpact/relationships.py",
        }
        if not required.issubset(names):
            raise RuntimeError(f"Wheel is missing modules: {sorted(required - names)}")
        metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
        metadata = archive.read(metadata_name).decode("utf-8")
        if f"Version: {EXPECTED_VERSION}" not in metadata or "# GeoImpact CI" not in metadata:
            raise RuntimeError("Wheel metadata lacks version or embedded README")

    with tarfile.open(sdist, "r:gz") as archive:
        names = set(archive.getnames())
        required = (
            "/pyproject.toml",
            "/README.md",
            "/src/geoimpact/cli.py",
            "/src/geoimpact/analysis.py",
        )
        missing = [suffix for suffix in required if not any(name.endswith(suffix) for name in names)]
        if missing:
            raise RuntimeError(f"Source distribution is missing required files: {missing}")


def python_in(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def cli_in(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "geoimpact.exe"
    return environment / "bin" / "geoimpact"


def install_and_check(archive: Path, label: str, work: Path) -> None:
    environment = work / f"venv-{label}"
    venv.EnvBuilder(with_pip=True).create(environment)
    python = python_in(environment)
    run([str(python), "-m", "pip", "install", "--disable-pip-version-check", str(archive)])

    version = subprocess.check_output(
        [str(python), "-c", "from importlib.metadata import version; print(version('geoimpact-ci'))"],
        cwd=ROOT,
        text=True,
    ).strip()
    if version != EXPECTED_VERSION:
        raise RuntimeError(
            f"Installed {label} reports version {version!r}, expected {EXPECTED_VERSION}"
        )

    executable = cli_in(environment)
    if not executable.is_file():
        raise RuntimeError(f"Installed CLI executable is missing: {executable}")

    cases = (
        ("PASS", ROOT / "tests/fixtures/geoimpact-pass.yml", 0),
        ("BLOCK", ROOT / "tests/fixtures/geoimpact.yml", 1),
        ("ERROR", work / "release-candidate-missing-config.yml", 2),
    )
    for name, config, expected_code in cases:
        output = work / f"{label}-{name.lower()}"
        result = subprocess.run(
            [str(executable), "analyze", "--config", str(config), "--out", str(output)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != expected_code:
            raise RuntimeError(
                f"Installed {label} CLI {name} exit {result.returncode}; expected {expected_code}\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )
        if name in {"PASS", "BLOCK"}:
            missing = [item for item in ARTIFACT_NAMES if not (output / item).is_file()]
            if missing:
                raise RuntimeError(f"Installed {label} CLI {name} omitted artifacts: {missing}")
        elif "Verdict:" in result.stdout:
            raise RuntimeError("Installed ERROR CLI unexpectedly reported a policy verdict")

        if name == "BLOCK":
            for artifact, expected_hash in EXPECTED_BLOCK_HASHES.items():
                digest = hashlib.sha256((output / artifact).read_bytes()).hexdigest()
                if digest != expected_hash:
                    raise RuntimeError(f"Installed {label} {artifact} hash mismatch: {digest}")

        print(f"Verified {label} installed CLI {name}: exit {expected_code}")
    if (work / f"{label}-error").exists() and any((work / f"{label}-error").iterdir()):
        raise RuntimeError("Installed ERROR CLI unexpectedly wrote output files")
    print(f"Installed {label} package version: {version}")
    if label == "wheel":
        environment_vars = os.environ.copy()
        environment_vars["PATH"] = str(executable.parent) + os.pathsep + environment_vars["PATH"]
        for script in ("verify_madrid_benchmark.py", "verify_gate8_case.py"):
            run([str(python), str(ROOT / "scripts" / script)], env=environment_vars)
            print(f"Verified wheel-installed {script} contract")


def main() -> int:
    try:
        require_release_metadata()
        with tempfile.TemporaryDirectory(prefix="geoimpact-release-") as temporary:
            work = Path(temporary)
            distribution = work / "dist"
            distribution.mkdir()
            run([sys.executable, "-m", "build", "--outdir", str(distribution)])
            wheels = list(distribution.glob("*.whl"))
            sdists = list(distribution.glob("*.tar.gz"))
            if len(wheels) != 1 or len(sdists) != 1:
                raise RuntimeError("Expected exactly one wheel and one sdist")
            wheel, sdist = wheels[0], sdists[0]
            verify_archives(wheel, sdist)
            for archive in (wheel, sdist):
                digest = hashlib.sha256(archive.read_bytes()).hexdigest()
                print(f"SHA-256 {archive.name}: {digest}")
            install_and_check(wheel, "wheel", work)
            install_and_check(sdist, "sdist", work)
    except Exception as error:
        print(f"Release candidate qualification FAILED: {error}", file=sys.stderr)
        return 1
    print("Release candidate qualification PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
