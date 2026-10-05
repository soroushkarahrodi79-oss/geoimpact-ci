# Sierra de Baza protected-area boundary update (Gate 8)

## What changed and why this case was selected

The Junta de Andalucía's EENNPP release for December 2025 specifically states
that the Sierra de Baza Natural Park boundary was updated after approval of its
new Plan de Ordenación de los Recursos Naturales (PORN) in December 2025. The
BASE snapshot is the official EENNPP polygon layer updated to May 2015. This is
an environmental protection-management case outside Madrid and differs from
Gate 5/6 census-section boundary change.

The target feature is identified from the official source attributes as
`CODIGOESPA = 69`, `NOMBRE = SIERRA DE BAZA`, `FIGURA = Parque Natural`. Its
official feature code is stable and unique in both selected snapshots. The
fixed dependent source consists of public-use equipment points maintained by
REDIAM, including visitor centres, recreation areas, viewpoints, and trails.
For points, `within` means that the point lies in the Sierra de Baza park
polygon. It is a spatial membership observation, not a legal assignment or
statement about access, operational service, or actual visitor use.

## Sources, dates, and provenance

- BASE: EENNPP 2015 archive, layer date May 2015, shape file in
  `ETRS89_30` (`ETRS_1989_UTM_Zone_30N`, EPSG:25830). Official archive URL:
  <https://www.juntadeandalucia.es/medioambiente/servtorrent/informacionambiental/07_PATRIMONIO_NATURAL/01_RENPA/00_RENPA/EENNPP.tar.gz>.
- CANDIDATE: REDIAM RENPA WFS `ms:eennpp`, latest release identified by the
  source page as December 2025; response retrieved 2026-10-05. WFS reported
  EPSG:3042. Endpoint:
  <https://www.juntadeandalucia.es/medioambiente/mapwms/REDIAM_RENPA?service=WFS&request=GetCapabilities>.
- DEPENDENCY: REDIAM WFS `ms:equipamientos_uso_publico`, response retrieved
  2026-10-05; WFS reported EPSG:3042. Endpoint:
  <https://www.juntadeandalucia.es/medioambiente/mapwms/REDIAM_WFS_Patrimonio_Natural?service=WFS&request=GetCapabilities>.
- The selected inventory date is not historically aligned with both boundary
  states. Interpret this as a spatial counterfactual using a fixed reference
  inventory. The dependency is not evidence that each listed facility existed
  in 2015 or at the date of the boundary update.

## Reuse and attribution

The 2015 EENNPP Open Data Andalucía record specifies CC BY 4.0. The current
EENNPP catalogue page does not display a separate standard license label; the
REDIAM WFS capabilities state that service use is free and gratuitous provided
the authors and owners are named. We preserve that condition as
`Fuente: Red de Información Ambiental de Andalucía (REDIAM), Junta de
Andalucía` and do not assign a new license to source data. Raw snapshots are
not included; only the bounded fixture derived under these attribution
conditions is checked in.

The 2015 dataset's catalog record is at
<https://www.juntadeandalucia.es/datosabiertos/portal/dataset/limites-de-los-espacios-naturales-protegidos-de-andalucia-eennpp-2015>.
The latest boundary release and its PORN update notes are at
<https://www.juntadeandalucia.es/medioambiente/portal/acceso-rediam/visor-condicionantes-ambientales/fichas-descriptivas/eennpp/renpa/limites>.
The dependent layer is described at
<https://www.juntadeandalucia.es/medioambiente/portal/areas-tematicas/uso-publico/equipamientos>.

## Frozen source and fixture hashes

SHA-256 of downloaded original snapshots:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `EENNPP_2015.tar.gz` | 23,162,313 | `7c1f43a0e9adf1ccc99b66051482b7c2a3f8ffdf7f42aeb4eedd3c554a1dc67b` |
| `EENNPP_current_WFS.geojson` | 17,823,340 | `2f64c939d0052076d3bb4ddb02e9230cffeafdc606c36c673612a90686add834` |
| `equipamientos_2026-10-05_WFS.geojson` | 528,438 | `02aadfc63c7f48ed67f84aa8b1c7c4ba5069c25b737e5f0e829d977c28b5eb5e` |

SHA-256 of canonical compact RFC 7946 GeoJSON fixture bytes:

| File | Features | SHA-256 |
|---|---:|---|
| `base.geojson` | 1 | `eae31120ec45e51c53b48515c0bde6e1d1c269edafea51076f862c16854d2799` |
| `candidate.geojson` | 1 | `4f4b4ff369befb14c8f1d26e902fda4b431de26432f85897d2cd77df9485cc17` |
| `dependencies.geojson` | 52 | `617d4b71921b8d66692f1c8457a56b9b6224abb0c044bb06ce7608e2524c0f6c` |

## Deterministic subset recipe

The source-only primary qualification is the single protected-area feature
selected by the three official source attributes above. No dependency results
were used to select it. Its change footprint is the planar symmetric
difference of its BASE and CANDIDATE geometries after projection to
EPSG:25830. The dependent subset retains every point feature whose projected
coordinates fall inside the change-footprint bounding box expanded by exactly
10,000 metres on every side. The same filter is rerun from the complete frozen
dependency snapshot. This context envelope is a fixture selection rule only;
it is not an analysis buffer or GeoImpact policy predicate.

The preparation utility verifies SHA-256 for all three raw source files,
selects the primary feature by official source attributes, validates its
geometries, applies the fixed spatial recipe, transforms output to CRS84 for
GeoJSON input, and writes canonical compact JSON. To reproduce after acquiring
the exact snapshots above, install project dependencies and
`requirements-research.txt`, then run:

```powershell
python research/sierra-de-baza-2015-2025/prepare_case.py `
  --raw-dir work/gate8-src `
  --out-dir research/sierra-de-baza-2015-2025
```

The script aborts if a downloaded source hash differs. The current WFS is
maintained online, so an upstream update will require a transparently
documented new snapshot and hashes rather than being silently accepted.

## Limitations and claims not made

This is an approximately ten-year boundary comparison. The administrative
PORN approval is documented, but geometry alone cannot identify administrative
intent, causal effects, legal impact, access, service availability,
socioeconomic consequences, or individual historical impact. Equipment points
were retrieved from the maintained source on 2026-10-05 and may have been
added, retired, moved, or reclassified since either boundary snapshot. This
test asks only whether fixed reference-inventory points change `within`
membership between two source boundary geometries. Source accuracy and scale
remain those of the supplied official cartography.
