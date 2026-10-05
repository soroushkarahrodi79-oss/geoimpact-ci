# Gate 9 — deterministic boundary displacement

## Finding and scope

Gate 8's frozen Sierra de Baza case had identical input hashes, relationship
assignments, relationship identity, evidence identity, regression GeoJSON, and
footprint area on hosted Windows and Linux. Its 52 fixed equipment relationships
were all unchanged, with zero regressions and zero boundary ambiguities. The
only observed artifact difference came from
`primary_change.max_boundary_displacement_m`:

| Hosted environment | Full-precision displacement |
|---|---:|
| Windows | 368.8250959451751 m |
| Linux | 368.82509594532814 m |
| Absolute difference | 0.00000000015304 m |

The observed discrepancy is confined to the displacement scalar. This finding
does not identify a lower-level platform cause beyond the full-precision
Hausdorff measurement path. Relationship analysis, evidence, and footprint
overlay are outside the change.

## Existing measurement semantics

The project pins Shapely 2.1.2. Both hosted CI runners used GEOS 3.13.1. In Shapely
2.1.2, `Geometry.hausdorff_distance(other)` delegates to
`shapely.hausdorff_distance(self, other)`, so these spellings use the same
operation for this code path. Shapely documents the result as *discrete*
Hausdorff distance: it evaluates vertices (unless densification is requested),
so it approximates the continuous Hausdorff metric. The operation accepts
`densify`, but does not expose a `grid_size` parameter. The footprint's
OverlayNG operations do accept `grid_size`; their precision contract does not
automatically apply to Hausdorff distance.

References: [Shapely 2.1.2 `hausdorff_distance`](https://shapely.readthedocs.io/en/2.1.2/reference/shapely.hausdorff_distance.html),
[Shapely 2.1.2 `set_precision`](https://shapely.readthedocs.io/en/2.1.2/reference/shapely.set_precision.html),
[Shapely 2.1.2 overlay precision](https://shapely.readthedocs.io/en/2.1.2/reference/shapely.intersection.html),
[GEOS DiscreteHausdorffDistance](https://libgeos.org/doxygen/classgeos_1_1algorithm_1_1distance_1_1DiscreteHausdorffDistance.html).

## Candidate model and decision

The selected model conforms temporary measurement copies to a separate
`BOUNDARY_DISPLACEMENT_GRID_SIZE_M = 1e-6` metre grid, then calls
`shapely.hausdorff_distance`. The footprint continues to use its independently
named `CHANGE_FOOTPRINT_GRID_SIZE_M = 1e-6` metre grid. Source geometries used
for equality, relationships, STRtree lookup, evidence, and boundary ambiguity
remain untouched and full precision.

The one-micrometre grid is a derived-computation precision model in the
EPSG:25830 metre CRS. It is far below meaningful source-data accuracy and makes
no claim about source accuracy. The same numerical grid is used for the
footprint because the existing Gate 6 footprint contract provides an established
scale for stable derived geometry measurements; the two constants retain
separate semantics and can evolve independently.

The frozen Sierra case was used only to make a small engineering reproducer and
to qualify the result. The checked-in
[`displacement_portability_pair.geojson`](../tests/fixtures/displacement_portability_pair.geojson)
contains two 400 m crops around the maximum-displacement witness pair. The
cropped geometries are stored in OGC:CRS84 and projected to EPSG:25830 by the
test, preserving the production transformation step. It has 71 coordinates in
total and is 7,517 bytes. It contains no dependent inventory or full research
case. On Windows, the reproducer's full-precision value is
368.8250959451751 m and the grid-qualified value is 368.82509547712834 m.

## Scientific delta

| Case | Full precision | 1e-6 m grid | Absolute delta | Relative delta |
|---|---:|---:|---:|---:|
| Synthetic Gate 4 | 40.0 m | 40.0 m | 0 m | 0 |
| Madrid Gate 6 | 2937.635066209976 m | 2937.635066605893 m | 0.00000039591714084963314 m | 1.347741063563863e-10 |
| Sierra, Windows | 368.8250959451751 m | 368.82509547712834 m | 0.00000046804676 m | 1.2690209130171932e-9 |
| Sierra, Linux old value | 368.82509594532814 m | 368.82509547712834 m | 0.00000046819980 m | 1.269435852243098e-9 |

The largest observed change is below one micrometre. It is the expected effect
of applying the declared measurement grid; it does not change the Gate 4
measurement at its exact control value or the interpretation of the Madrid or
Sierra results.

## Contract migration and results

The report contract is now V3: V2's fixed-precision footprint overlay plus an
explicitly precision-qualified displacement. Config schema version remains
unchanged. The JSON scalar is the computed value from the measurement path;
Markdown renders that same report value. No platform-specific formatting or
hash allowances are used.

Gate 4 remains 3 relationship records, 2 regressions, 0 boundary ambiguities,
with the existing evidence identities unchanged. Its V3 hashes are:

| Artifact | SHA-256 |
|---|---|
| `report.json` | `2bfc39f79dbe11d9dc84d58923bba486ad29763155da905eb273cf0257433188` |
| `report.md` | `0a3525f5bf376fd47120175bc161de13769005cbcd194b9d350771a69a63009b` |
| `relationship-regressions.geojson` | `a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978` |

Madrid retains 2,112 assignment changes, 26 transition pairs, 1,768 split-like
and 344 merge-like patterns, zero gained, zero lost, and zero boundary
ambiguities. Its relationship identity remains
`4b1eac48876a66599a4eb0a8013625f81a64a1f7fedf47539324d4556d85ee38`; the
evidence digest remains
`d221ee2e751af2b46062fd0cd76581b2aff5307061919e0ba3f6e0f69bfe7cd8`.

| Madrid V3 artifact | SHA-256 |
|---|---|
| `report.json` | `9a04ee2dc5c3ec52a55fc12451edc23a573f0030e730d0947c3f1c602d6fadb8` |
| `report.md` | `87528179d747c430dfe6726237dfa5510c787329c632e29fb4117e151e667e21` |
| `relationship-regressions.geojson` | `0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf` |

The former active V2 Gate 4 hashes are retained as history: `report.json`
`3c34e46927f20864438455bf6bf94daf4c247ffe86bab88e2206ec40642bb076`,
`report.md` `0a3525f5bf376fd47120175bc161de13769005cbcd194b9d350771a69a63009b`,
and regression GeoJSON
`a3557416a5a6f7c6eb5c3fa5d4b14a48864249f208981138e6d21bc542318978`.
The former active Madrid V2 hashes are retained as history: `report.json`
`7cb57ae5b8d4c4fdf33e1e359002ac8cb2c30d05ee5f9509d47f8408a8ee9733`,
`report.md` `8173dee60053deea746185bf12f3d1caa560907701ee9377db2e5ee78604e57f`,
and regression GeoJSON
`0689f0983441f4c3c745690c9f7bf409347862f93d94754a2ef15826c49e6bcf`.

The frozen Sierra source hashes remain those recorded by Gate 8:

| Input | SHA-256 |
|---|---|
| `base.geojson` | `eae31120ec45e51c53b48515c0bde6e1d1c269edafea51076f862c16854d2799` |
| `candidate.geojson` | `4f4b4ff369befb14c8f1d26e902fda4b431de26432f85897d2cd77df9485cc17` |
| `dependencies.geojson` | `617d4b71921b8d66692f1c8457a56b9b6224abb0c044bb06ce7608e2524c0f6c` |
| `geoimpact.yml` | `f7e3245517cc5c16d97b34c08b0760e5055cfc25a71a39f1ee847413c0ee2520` |

Hosted qualification passed on Linux/Python 3.11 and Windows/Python 3.14, both
with Shapely 2.1.2 and GEOS 3.13.1. The compact CRS84 fixture reproduced the
original drift in the full-precision metric:

| Hosted environment | Compact pair, full precision | Compact pair, 1e-6 m grid |
|---|---:|---:|
| Windows | 368.8250959451751 m | 368.82509547712834 m |
| Linux | 368.82509594532814 m | 368.82509547712834 m |

The full frozen case yielded byte-identical V3 reports and regression
GeoJSON on both systems:

| Sierra V3 artifact | SHA-256 on both systems |
|---|---|
| `report.json` | `be2176458956834eebadb83c422b0e9496d496f3fa6cd1af54b00cec30748cbb` |
| `report.md` | `0884e42afc3c3327d1456cf055b9308e1540a8e7259c05cf9ed020fd1d763be7` |
| `relationship-regressions.geojson` | `a55b431e78049bb7fdc7330ffdf2c9f8e87712545ebba199445408d48694225a` |

The qualification yielded 52 relationships, all unchanged, zero regressions
and zero boundary ambiguities, relationship identity
`d57c99dd3f497d57ec3538c66b6aed2be2ef053a638d3fc68962690c8a50539a`, and
evidence digest `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`.
The Gate 8 source fixture itself remains external to the permanent Gate 9 CI
contract. The PR workflow passed on both matrix legs in
[run 37319963966](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37319963966).
The separate frozen Sierra qualification passed on both legs in
[run 37321556884](https://github.com/soroushkarahrodi79-oss/geoimpact-ci/actions/runs/37321556884).

## Decision D-032

Derived maximum boundary displacement is evaluated on measurement copies
conformed to an explicit 1e-6 metre precision grid; relationship geometries
retain their existing full-precision semantics. This makes the published
derived scalar reproducible while limiting the numerical model to measurement
copies. The grid is not a source-accuracy claim. Gate 4 and Madrid relationship
and evidence contracts remain unchanged. Gate 8 is the external cross-platform
qualification for the same scalar.

## Limitations

The guarantee applies to the pinned Shapely version and the Linux/Python 3.11
and Windows/Python 3.14 hosted CI environments after their final matrix run.
It does not establish reproducibility for other Shapely or GEOS versions,
CRSs, precision grids, architectures, or all valid geometries. Precision
reduction can remove vertices or collapse narrow geometric components; this
contract applies to the valid polygon fixtures and cases qualified here.
