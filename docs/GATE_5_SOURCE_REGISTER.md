# Gate 5 — Madrid case source register

Retrieval and probing date: **2026-10-03**. Live source metadata and API results
can change. The derived inputs in `research/madrid-ine-sections-2024-2025/`
freeze the exact small subset used for the CLI probe.

## Selected sources

| Role | Source and version | License / attribution | Findings |
|---|---|---|---|
| BASE primary polygons | INE `Secciones_2024`, `CUMUN=28079`, `TIPO=SECCIONADO` | The service requires attribution: “Seccionado cedido por el Instituto Nacional de Estadística”. Dataset-specific license remains ambiguous; see note below. | 2,450 valid non-empty MultiPolygons; ID `CUSEC`; OGC GeoJSON coordinates are CRS84. |
| CANDIDATE primary polygons | INE `Secciones_2025`, same filters | Same required attribution; dataset-specific license remains ambiguous. | 2,462 valid non-empty MultiPolygons; same `CUSEC` schema. Compared with 2024: 2,443 common IDs, 30 common geometries changed, 19 added IDs, 7 removed IDs. |
| Fixed dependency points | Ayuntamiento de Madrid Callejero resource `200075-1-callejero-csv`, filter `Tipologia del numero = Portal`; retrieved snapshot 2026-10-03 (published metadata update 2026-09-14) | CC BY 4.0; attribute Ayuntamiento de Madrid and link the dataset. | 161,190 rows; all `Codigo de numero` values unique; coordinate fields are ETRS89/WGS84 longitude/latitude. 2,112 points fell in the derived change footprint. |

Official links:

- [INE annual-section collection index](https://www.ine.es/geoserver/ogc/features/v1/collections)
- [INE `Secciones_2024` collection and schema](https://www.ine.es/geoserver/ogc/features/v1/collections/WMS_INE_SECCIONES_G01%3ASecciones_2024)
- [INE `Secciones_2025` collection and schema](https://www.ine.es/geoserver/ogc/features/v1/collections/WMS_INE_SECCIONES_G01%3ASecciones_2025)
- [Ayuntamiento Callejero dataset metadata](https://datos.madrid.es/dataset/200075-0-callejero/information)
- [Ayuntamiento address resource metadata and data dictionary](https://datos.madrid.es/dataset/200075-0-callejero/resource/200075-1-callejero-csv)
- [Ayuntamiento Callejero field definitions](https://datos.madrid.es/dataset/200075-0-callejero/resource/200075-5-callejero)

The INE filtered source responses were canonicalized locally for hashing after
selecting Madrid section features, then sorted/serialized as compact UTF-8 JSON
with sorted keys and one trailing LF. They were not committed:

| Retrieved source subset | Bytes | SHA-256 |
|---|---:|---|
| INE Madrid sections 2024 | 3,704,907 | `120692f71460f8cfd12f6542d4d7917337d916a781cac29e918bbd1b0e8946e8` |
| INE Madrid sections 2025 | 3,712,462 | `3ce9184cf5f2ff3f0f9bcaf9211a50ea5826487d2320ee96976d53e00b8eb70d` |
| Canonical retrieved Callejero portal snapshot (source, retrieval date, filter, and all 161,190 rows sorted by `Codigo de numero`) | 156,109,727 | `84a0324f4e4172b75f6749a57e99ecc45e895a9b1ca1c2f7a38063d1fb538004` |

The full point snapshot is intentionally not committed. The four compact,
attributed GeoJSON/config inputs committed for the probe total 480,835 bytes.
The Ayuntamiento Callejero source and point subset are CC BY 4.0. The INE
census-section service requires attribution as “Seccionado cedido por el
Instituto Nacional de Estadística”. INE web properties expose differing
general Creative Commons labels, so this research record preserves the
dataset-specific required attribution and records the licensing ambiguity
rather than asserting an unsupported dataset-specific share-alike obligation.
Confirm INE licensing before broader redistribution. The data terms are
separate from the project's source-code licensing.

## Derived input files

| File | Bytes | SHA-256 |
|---|---:|---|
| `ine-sections-2024-focus.geojson` | 93,124 | `9987b42293ffdda93b3cb5a1d897bccea4b084ed1ba0e1bd5eaf7f4eb303c453` |
| `ine-sections-2025-focus.geojson` | 97,139 | `18956b960c4b8adf5d750c04cf51a5db638ed8054e5e83988003ea59ce4d9da3` |
| `madrid-portals-change-footprint.geojson` | 290,181 | `a8ad452cb74dcc77cdfe43fb040b5e4b6ecee38c63710932e3de4209f74f6ec0` |
| `geoimpact.yml` | 390 | `7395510b1bc4b760dd606f1998d2ec317af0512768d223198544c7b6e52fc5b1` |

## Other candidates investigated

| Candidate family | Sources examined | Disposition and reason |
|---|---|---|
| Madrid districts | [Municipal district boundaries](https://datos.madrid.es/dataset/300497-0-distritos-municipales-madrid); [2021 boundary agreement](https://www.bocm.es/boletin/CM_Orden_BOCM/2021/07/12/BOCM-20210712-41.PDF) | Official boundaries and a real 2021 Hortaleza/Barajas administrative agreement exist, but the available historical download was not a paired, contemporary before/after boundary snapshot for that agreement. Not selected. |
| Madrid barrios | [Municipal barrio boundaries](https://datos.madrid.es/dataset/300496-0-barrios-madrid/information) | The metadata documents 2017 Vicálvaro neighborhood creation/changes and a rename; current version is documented. The available historical archive did not provide a paired 2016/2017 boundary release. Not selected. |
| Census sections | [INE annual series](https://www.ine.es/geoserver/ogc/features/v1/collections) | Selected: paired annual official versions, stable ID field for retained sections, valid polygon geometry, published CRS/schema, and an observed non-zero event against fixed address locations. |
| Health service zones | [Comunidad de Madrid zoning description](https://gestiona.comunidad.madrid/iestadis/fijas/clasificaciones/cozousalu.htm); [map downloads](https://gestiona.comunidad.madrid/iestadis/fijas/estructu/general/territorio/estructucartemzbs.htm) | The documented zoning version is 2009 and the available maps are not a paired recent boundary transition. Not selected. |
| Mobility / regulatory zones | [ZBEDEP Plaza Elíptica](https://datos.madrid.es/dataset/300530-0-zona-bajas-emisiones-eliptica); [SER streets](https://datos.madrid.es/dataset/218228-0-ser-calles) | No paired historic polygon transition was established for the ZBE dataset. SER is street/segment-oriented, while the current primary-layer case requires polygons and `WITHIN`; regulatory access also has road and exemption semantics outside that predicate. Not selected. |
| Tourism points | [Madrid accommodation points](https://datos.madrid.es/dataset/300032-0-turismo-alojamientos) | The directory is updated daily and has reuse conditions different from the standard municipal CC BY datasets; a stable historical snapshot pair was not established. Not selected. |

## Probe derivation

The source collections were queried through the official INE OGC API for
`CUMUN='28079'`, with `filter-lang=cql2-text`, `f=application/geo+json`, and
`limit=5000`; only records whose `TIPO` equals `SECCIONADO` were retained.
`CUSEC` was retained as the primary ID. The Ayuntamiento CKAN DataStore was
queried for resource `200075-1-callejero-csv`, using the portal filter and
offsets 0, 32,000, 64,000, 96,000, 128,000, and 160,000 (limit 32,000), stopping
after the final 1,190 records. `Codigo de numero` was the point ID. The documented
longitude/latitude DMS values were converted to decimal CRS84 coordinates.

The selection recipe is deterministic: identify common section IDs whose
geometries are not topologically equal, plus IDs added or removed; compute the
union of each common changed geometry's symmetric difference and each added or
removed full geometry; keep all points intersecting that footprint; retain all
those section IDs in BASE/CANDIDATE. No point was selected by looking at a CLI
verdict or relationship output. The 2,112 point records are all unique and
their assignment transitions match the complete-source exploratory join.
Across all source features and points, the independent join found 2,112
transitions and 197 points unassigned in both versions. A broader installed-CLI
attempt (5,480 points, complete section layers) was stopped after about 2.5
minutes without output; completed CLI evidence is limited to the deterministic
change-footprint subset.

The transition-type audit classified 1,768 relationships as split-like (the
old CUSEC is retained with changed geometry and the destination CUSEC is newly
added in 2025) and 344 as merge-like (the old CUSEC disappears and the
destination CUSEC is retained with changed geometry). There were no gained,
lost, both-retained-ID, or pure ID-only/renumbering transitions. These labels
describe the observed ID/geometry pattern and do not state INE's intention or
cause.
