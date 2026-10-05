# Madrid census-section research fixture

This is a compact, derived subset for the Gate 5 research case. It is not a
complete Madrid boundary or address inventory. The exact selection method,
source links, version details, observed results, limits, hashes, and license
attributions are in [the Gate 5 report](../../docs/GATE_5_REAL_WORLD_CASE.md)
and [source register](../../docs/GATE_5_SOURCE_REGISTER.md).

## Attribution and data licenses

- Section geometries derive from the Instituto Nacional de Estadística annual
  census-section collections. Attribute the source as **“Seccionado cedido por
  el Instituto Nacional de Estadística”**. INE web properties expose differing
  general Creative Commons labels, and the available census-section service
  metadata does not establish a dataset-specific license. This fixture
  preserves the service's required attribution and records that ambiguity
  rather than asserting an unsupported dataset-specific share-alike
  obligation. Confirm licensing with INE before broader redistribution.
- Portal points derive from the Ayuntamiento de Madrid Callejero, resource
  `200075-1-callejero-csv`. Attribute **Ayuntamiento de Madrid** and link to
  its [Callejero dataset](https://datos.madrid.es/dataset/200075-0-callejero).
  The point subset is under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The input files total 480,444 bytes (the config is 391 bytes and the three
GeoJSON files are 480,444 bytes combined; 480,835 bytes including config).
The data licenses apply to their respective derived inputs; they do not change
the license of GeoImpact's source code.

## Rerun

From the repository root, run the installed CLI:

```text
geoimpact analyze --config research/madrid-ine-sections-2024-2025/geoimpact.yml --out <temporary-output-directory>
```

The expected completed result is `BLOCK` with exit code 1. The config's zero
threshold is an exploratory probe setting, not a policy recommendation. The
generated report artifacts should be written outside this directory.
