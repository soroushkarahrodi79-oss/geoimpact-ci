# Deterministic change model

## Preconditions and canonical analysis space

An input dataset is an immutable file plus a layer declaration:

`Dataset = (logical_name, path, SHA-256, format, id_field, geometry_field,
source_crs, analysis_crs, attribute_projection)`.

The SHA-256 is for report provenance, not equality. `logical_name` and
`id_field` are configuration, not inferred from a filename. IDs must be
present, non-null, scalar, unique after conversion to the declared canonical
string representation, and stable across versions. A duplicate, missing, or
changed representation is an analysis error. V0 does not match probable
renames: unmatched IDs are additions/removals. It may emit a *diagnostic*
possible-ID-instability pairing based on geometry, but never reclassifies it.

All spatial computation happens in an explicitly configured projected
`analysis_crs` whose horizontal unit is metres. The engine verifies that both
source CRSs are known and transformable to it, records PROJ/GEOS versions, and
uses `always_xy` axis order. It rejects CRS mismatch when `analysis_crs` is
absent or transformations fail. GeoJSON is interpreted as RFC 7946 CRS84
(longitude, latitude); it must still be transformed before metre thresholds.
Z and M are ignored in V0 and reported as such.

Before comparison, geometry is transformed once to `analysis_crs`, checked
for non-nullness, non-emptiness, validity, and an allowed simple-feature
family. Invalid, empty, null, GeometryCollection, or unsupported dimensional
geometry causes an analysis error. `MultiPoint`, `MultiLineString`, and
`MultiPolygon` are allowed; their parts are kept as one feature. Automatic
repair, precision snapping, and collection flattening are forbidden because
they change the candidate under review.

## Feature transition

Let `B` and `C` be maps from a canonical ID to `(attributes, geometry)`;
attribute comparison excludes the ID and geometry fields and uses a declared
canonical JSON encoding: sorted object keys, compact separators, UTF-8,
normalised datetimes, and exact typed scalar representation. Arrays remain
ordered. Floating-point attributes are exact in V0; a later explicit
per-field tolerance may be added.

For an ID `i`:

- **added**: `i ∈ C \ B`.
- **removed**: `i ∈ B \ C`.
- **attribute modification**: `i ∈ B ∩ C` and canonical attributes differ.
- **geometry modification**: `i ∈ B ∩ C`, the geometries are not
  topologically equal, and normalised structural comparison differs under the
  configured absolute coordinate tolerance `t_m`.
- **modified**: either attribute or geometry modification is true.
- **unchanged**: neither is true.

One modified feature may have both dimensions. Addition/removal has no
geometry-difference metric against a counterpart; its entire non-empty
geometry contributes to the footprint.

## Geometry equality and tolerance

Binary WKB equality is never the semantic test. For each valid transformed
geometry, the engine records WKB only as an evidence fingerprint and computes:

1. `topologically_equal = B.equals(C)`. This ignores vertex and ring/part
   ordering when they occupy the same point set.
2. `normalised_structurally_equal = equals_exact(B, C, t_m, normalize=True)`.
   This detects coordinate/vertex representation changes after normalisation;
   it does not by itself make a safety finding.
3. A geometry is spatially unchanged if it is topologically equal **or**
   `equals_exact(..., tolerance=t_m, normalize=True)` is true. V0 fixes
   `t_m = 0` by default. Tolerance is in analysis-CRS metres and is never
   applied by independently rounding coordinates. A topologically equal but
   structurally different feature is reported as a representation change, not
   a changed footprint or relationship event.

The report preserves both equality flags so a harmless ordering change is not
confused with a geometric motion. Equality is evaluated before metrics.

## Metrics and units

All figures below use two-dimensional planar operations after the CRS
precondition. Values are emitted as unrounded IEEE-754 values in JSON plus a
display rounding rule in Markdown; threshold comparison uses the unrounded
value. This prevents a display rounding boundary from changing a verdict.

| Geometry family | Required metrics | Interpretation / limits |
|---|---|---|
| Point / MultiPoint | point coordinate displacement, centroid displacement, discrete Hausdorff | Maximum counterpart displacement requires equal point-part count and deterministic lexicographic coordinate matching; otherwise `null`. Centroid is an aggregate, not a replacement for part movement. All metres. |
| LineString / MultiLineString | centroid displacement, length delta, discrete Hausdorff, symmetric-difference footprint | Length/distance metres; symmetric difference is areal only after the configured `footprint_buffer_m` is applied. A line has zero area, so raw symmetric difference is not a useful area metric. |
| Polygon / MultiPolygon | centroid displacement, area delta, perimeter delta, discrete Hausdorff, symmetric-difference area | Area m², lengths/metres. Symmetric difference is the changed area. |

`centroid_displacement_m = distance(centroid(B), centroid(C))`;
`length_delta_m = length(C)-length(B)`; and
`area_delta_m2 = area(C)-area(B)`. The (discrete) Hausdorff distance is the
maximum of each geometry's sampled vertices to the closest point of the other,
in metres; it is a maximum boundary/shape displacement, not necessarily a
one-to-one vertex movement. The optional fixed `densify_fraction` must be in
configuration and recorded; V0 default is no densification.

For a modified area geometry, `symmetric_difference(B,C)` is its changed
area. For an added/removed area geometry it is that geometry. For point/line
features, the footprint contribution is
`buffer(union(B,C), footprint_buffer_m)` (or the existing counterpart when
added/removed). `footprint_buffer_m` is required and must be positive for
non-area geometries. This means footprint is deliberately an impact-search
envelope, not a claim that every location inside changed.

The dataset **spatial change footprint** is the deterministic unary union of
all feature contributions, canonicalised by `normalize()` for evidence
serialization. Its area and bounds are reported. If no geometry changes,
the footprint is empty even if attribute changes exist.

## Numerical and topology safeguards

- Transformation, GEOS, PROJ, Shapely, and engine versions are evidence
  fields. Cross-platform bit-for-bit WKB is not promised; semantic and
  numeric results are tested within a documented `1e-9 m` test tolerance.
- Inputs must be valid before predicates or overlay. V0 never attempts
  `make_valid`, because it could make relationship regression an artefact of
  repair.
- Polygons that cross the antimeridian or are unsuitable for the selected
  projected CRS are rejected in V0; selecting a local analysis CRS is an
  explicit user responsibility.
- Geometry collections are rejected rather than silently flattening a mixed
  semantic object. Empty/null geometries have no relation and are errors,
  rather than being treated as disjoint.
- The configured `t_m`, buffer, CRS, and density are part of the report
  identity. Changing them is a changed analysis, not a rerun of the same one.
