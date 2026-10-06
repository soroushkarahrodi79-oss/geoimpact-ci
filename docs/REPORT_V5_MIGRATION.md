# Report V5 migration record

Status: development report contract introduced after v1.1.0. The package
version and the historical `v1.1.0` release remain unchanged.

## Why V5 adds provenance

A detached V4 report describes spatial results but does not identify the exact
input bytes or qualified GeoImpact/spatial-engine versions used to produce
them. V5 adds one top-level `provenance` object so a reviewer can compare the
report's declared inputs and runtime against retained source artifacts.

V4 reports remain valid V4 documents and retain their original interpretation.
V5 adds deterministic provenance; relationship, geometry, policy, and verdict
semantics are otherwise unchanged. This is a semantic report-contract change,
not a scientific evidence change.

## V5 provenance structure

```json
{
  "provenance": {
    "hash_algorithm": "sha256",
    "inputs": {
      "config": {"sha256": "...", "size_bytes": 0},
      "primary": {
        "base": {"dataset": "...", "sha256": "...", "size_bytes": 0},
        "candidate": {"dataset": "...", "sha256": "...", "size_bytes": 0}
      },
      "dependencies": [
        {"dataset": "...", "sha256": "...", "size_bytes": 0}
      ]
    },
    "engine": {
      "geoimpact_ci": "...",
      "shapely": "...",
      "geos": "...",
      "pyproj": "...",
      "proj": "..."
    }
  }
}
```

For every input, SHA-256 is calculated over the exact raw file bytes. The
config digest identifies the original `geoimpact.yml` bytes that were decoded
and parsed for the run; it is not a digest of a resolved in-memory contract.
BASE, CANDIDATE, and dependency digests likewise identify the supplied bytes,
not parsed or normalized GeoJSON. Whitespace, key order, or feature order
changes can therefore change an input hash even when parsed content is
semantically equivalent. `size_bytes` is the number of bytes read while
hashing.

Dependencies are emitted in ascending dataset-name order, matching the
analysis engine's canonical dependency ordering. Their YAML declaration order
does not affect provenance ordering.

Engine values use installed package/runtime APIs: GeoImpact CI distribution
metadata (`importlib.metadata.version("geoimpact-ci")`), `shapely.__version__`,
`shapely.geos_version_string`, `pyproj.__version__`, and
`pyproj.proj_version_str`. For source-tree execution only, if distribution
metadata is absent, GeoImpact reads the single repository-owned package
version from `pyproject.toml`. It never substitutes `unknown`. Python and OS
versions are omitted because the qualified matrix intentionally differs in
those values.

No paths, usernames, timestamps, hostnames, runner names, working directories,
or environment values are included. The hashes identify bytes; they do not
embed the source files or independently establish who supplied them.

## V4 to V5 artifact hashes

`report.json` changes because `report_version` advances to `"5"` and the
provenance section is added. `report.md` changes to display those identities.
These are report-contract and presentation changes only. All recorded
relationship evidence and primary geometry results remain unchanged. The
relationship regression GeoJSON is byte-for-byte identical for all three
qualification cases.

| Case and artifact | V4 SHA-256 | V5 SHA-256 | Reason / evidence status |
|---|---|---|---|
| Synthetic `report.json` | `a3245fb06b1a49c9cfec7d7b46cd70871937fdcb40700ad6c9733f470f73df13` | `7c30c65f1228197e0fd457084c509911d40446f4b6e281907b167c30e47985ab` | V5 version and provenance; science unchanged |
| Synthetic `report.md` | `222d3e3da2f7dc5c1c466249746022379a1735210792e3165435e49fae40d2f4` | `0ae2da4f039b9a4dc1b7545deae2bcd968fdc401c5bb9874eaaae9648333d2ec` | Provenance summary added |
| Synthetic relationship GeoJSON | `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978` | `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978` | Unchanged |
| Madrid `report.json` | `2657b69c8e173e8997fcca10e50df36a96e80ec5226f57299039fe3c817c8d2b` | `d79a9bc7cf9780ee86fae4f4bb2302d0ed87a3e12bda64bdd9c033e67d42d374` | V5 version and provenance; science unchanged |
| Madrid `report.md` | `74ce6c7f7e614bcec7ad94203747dce0f59dbda4e4e1e4fb0522e515665531d1` | `f0a943bad800cba1360c6a74714d295dfe341de63a05f56d812de20fcac31a43` | Provenance summary added |
| Madrid relationship GeoJSON | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` | Unchanged |
| Sierra `report.json` | `41c7add0c2f55a8778671661efbc30427ab0856d2e1e68ec5a904e11b8c88fcd` | `bde8bd26982e776c589286d277e51f1ef123d7091d245a579f500c61bffec3a9` | V5 version and provenance; science unchanged |
| Sierra `report.md` | `dc522a1fc60cb083669d89b793994d57da8e996c5c667cb1b8a785f5d8beb09e` | `920a27b275147fd04cf6a17e9f64212e6bec111673798d1e0e549688bf80f834` | Provenance summary added |
| Sierra relationship GeoJSON | `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a` | `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a` | Unchanged |

The V5 reports retain the frozen scientific results: Madrid has 2,112
relationship changes across 26 transition pairs (1,768 split-like, 344
merge-like, zero gained, zero lost, and zero boundary ambiguities). Sierra has
52 relationships, zero regressions, zero boundary ambiguities, and maximum
displacement of 368.82509547712834 m. No administrative intent is inferred.
