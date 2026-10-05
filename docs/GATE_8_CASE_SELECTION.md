# Gate 8 Case Selection (Pre-registered)

**Selection frozen before any Gate 8 GeoImpact invocation.** This note records
the source and case-family choice only; it contains no GeoImpact relationship
counts or outcomes. Scores are research judgements made from source metadata
available on 2026-10-05, on a 1 (weak) to 5 (strong) scale.

## Candidate families

| Candidate | Jurisdiction / domain | BASE → CANDIDATE and primary ID | Fixed dependent source / ID | CRS, geometry, temporal pair | License and redistribution | Source size / reproducibility / known limitations |
|---|---|---|---|---|---|---|
| **Andalusia protected natural area limits (selected)** | Junta de Andalucía; environmental protection and management, outside Madrid | Official EENNPP polygon layer, May 2015 → latest published layer December 2025. 2015 schema exposes `CODIGOESPA`; current RENPA WFS also exposes `CODIGOESPA`. Pairwise uniqueness/common-ID status will be checked independently before qualification. | REDIAM WFS `ms:equipamientos_uso_publico`, fixed response retrieved 2026-10-05; point `CODIGOEQUI` (1128 records in the frozen service response). Visitor facilities are fixed public-use installations associated with protected areas. | Source layer is polygon, dependency is point. Both WFS layers report EPSG:3042 (ETRS89 / UTM 30N); BASE source archive includes ETRS89 UTM 30N. Reproject/declare to required EPSG:25830. Boundary updates in 2024–2025 are documented; geometry change still requires independent qualification. | BASE portal explicitly CC BY 4.0. Current EENNPP page permits free reuse with author/owner attribution; service capabilities state free use with attribution. Freeze derived files only if this evidence is retained and attribution included. | BASE official TAR.GZ is 23.2 MB; current WFS contains 209 polygon records nationally/regionally; dependency WFS returns 1128 points. Authoritative dated source version. Limitations: decade gap, boundary edits may include legal redelimitation, cartographic refinement or corrections; 2026 fixed inventory is not historical evidence and some facilities may not have existed in 2015. |
| **Red Natura 2000 protected sites** | MITECO; EU nature-conservation site boundaries | MITECO Spain-wide 2021 end-year snapshot → current release whose page describes data reported through December 2024. Candidate ID expected to be Natura 2000 site code, to be confirmed from schemas. | Official Andalusian public-use visitor equipment points or a separately documented official fixed facility inventory; not Madrid Callejero. | National geometry includes multiple UTM zones; Andalusian subset can be evaluated in EPSG:25830. Official polygon distribution; stable site codes expected. Paired dates are documented at catalogue/page level. | MITECO permits free reuse with attribution on its cartography page. Redistribution of exact frozen bytes must still be assessed for the selected distributions. | National archive is reported at 127 MB; spatially scoped derived fixture should be manageable. Strong authority and reproducible source dates. Limitation: multiple overlapping site designations can make membership multi-valued; it is a distinct but still protected-area domain. Pre-registered fallback only if the selected Andalusian EENNPP case is operationally unusable under the stated conditions. |
| **Valencian flood-risk zoning (PATRICOVA)** | Generalitat Valenciana / Institut Cartogràfic Valencià; flood-risk planning | Official flood study/zoning layer; source metadata identifies the 2015 plan review, but availability of a frozen earlier paired geometry release and a stable zone ID remains unconfirmed. | Official fixed facilities such as health centers or schools, subject to a stable ID and snapshot check. | Polygon zoning / points expected; Comunitat Valenciana fits EPSG:25830. Available official WMS/SHP is confirmed; paired snapshots need verification. | Generalitat catalogue states Creative Commons Attribution; exact redistribution terms for both paired snapshots need verification. | Current SHP service is available, but metadata says update frequency unavailable. Historical pair reproducibility is weak; plan zones also express modeled hazard categories rather than site membership as a service boundary. Not selected. |
| **Barcelona low-emission zone boundary** | Ajuntament de Barcelona; transport/environmental regulation | Open Data BCN dataset provides a GeoPackage (196 KB), temporal coverage metadata 2016–2025 and an update date in 2025; an actual two-version polygon pair and stable polygon identity are unconfirmed. | Fixed official transport assets or establishments would require a separate, stable-ID source. | Polygon / points expected; within EPSG:25830. | Datos.gob.es marks the current distribution CC BY 4.0. Historical redistribution rights remain to be verified. | Small and authoritative, but a dated pair of actual geometry states is not established; a single long temporal-coverage field does not prove version history. Not selected. |

## Pre-result scorecard

Scores are 1–5. The final column is an unweighted total out of 60; this is a
transparent screening aid, not a statistical model. No GeoImpact results are
used.

| Candidate | A Authority | B Paired snapshots | C Stable IDs | D License | E WITHIN | F Meaningful change evidence | G Dependency stability | H Reproducibility | I Gate 5 independence | J Fixture size | K Interpretation | L Scientific defensibility | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Andalusia EENNPP | 5 | 4 | 3 | 4 | 5 | 4 | 3 | 4 | 5 | 4 | 5 | 5 | **51** |
| Red Natura 2000 | 5 | 4 | 4 | 4 | 5 | 3 | 3 | 4 | 5 | 3 | 4 | 5 | **49** |
| Valencia PATRICOVA | 5 | 2 | 2 | 3 | 4 | 3 | 3 | 2 | 5 | 3 | 4 | 4 | **40** |
| Barcelona ZBE | 5 | 2 | 2 | 4 | 4 | 2 | 3 | 2 | 5 | 5 | 4 | 4 | **42** |

## Selection and fallback

**Primary: Sierra de Baza Natural Park, Andalusia EENNPP May 2015 → December
2025**, conditional on the
following source-only gates being met before GeoImpact is run: paired official
bytes are available; redistribution and attribution are clear; both layers
provide a stable polygon ID; the intended geographic scope is valid in
EPSG:25830; and a fixed dependency snapshot has stable IDs, point geometry,
and defensible reuse terms. A failure on any one of these makes the primary
operationally unusable and permits considering the named fallback.

Why selected: the source owner publishes a dated 2015 layer and a separately
dated December 2025 layer. Its release notes specifically identify the Sierra
de Baza Natural Park boundary as updated following its new PORN approved in
December 2025. The primary feature is selected by the official source code
`CODIGOESPA = 69`, name `SIERRA DE BAZA`, and figure `Parque Natural`; this
selection uses source documentation only and was fixed before any dependent
assignment analysis. The domain is environmental protection rather than census
geography; whether an official visitor equipment point is within the park is a
natural WITHIN question. The frozen 2026 inventory is a spatial
counterfactual/reference-inventory probe, not a historical account of which
facilities existed in 2015 or when any boundary change took effect. Any
selection of dependencies will be based only on the geometric change footprint
and a pre-stated spatial rule, never on GeoImpact assignments.

**Fallback, pre-registered: MITECO Red Natura 2000 2021 → latest release
reported through December 2024.** It may be used only if the primary is
operationally unusable due to unavailable source bytes, invalid geometry,
missing paired snapshot, licensing prohibition, unstable IDs, or impossible
reproduction. A low or zero relationship-regression count is not grounds to
switch.

The exact selected files, source CRS, fields, record counts, hashes, licence
evidence, actual geometry-change counts, and dependency snapshot remain
qualification work. No outcome-dependent source or dependency substitution is
permitted.

## Source evidence reviewed

- Junta de Andalucía open-data entry for the 2015 EENNPP layer states the layer
  is updated to May 2015, consists of protected-area polygons, and is CC BY
  4.0: <https://www.juntadeandalucia.es/datosabiertos/portal/dataset/limites-de-los-espacios-naturales-protegidos-de-andalucia-eennpp-2015>.
- Junta de Andalucía's December 2025 EENNPP page identifies the latest version
  and describes boundary updates tied to approved 2024–2025 planning
  instruments: <https://www.juntadeandalucia.es/medioambiente/portal/acceso-rediam/visor-condicionantes-ambientales/fichas-descriptivas/eennpp/renpa/limites>.
- REDIAM's RENPA WFS describes the protected-area data and free reuse with
  author/owner attribution: <https://www.juntadeandalucia.es/medioambiente/portal/landing-page-servicio-ogc/-/asset_publisher/1qlWV3LW9vV6/content/rediam-wms-wfs-red-de-espacios-naturales-protegidos-de-andalucia-renpa-a-escala-de-detalle-y-semidetalle/20151>.
- Official visitor equipment page describes public-use facilities as fixed
  infrastructure supporting visitors and protected-area management, while
  warning that the offered inventory varies over time:
  <https://www.juntadeandalucia.es/medioambiente/portal/areas-tematicas/uso-publico/equipamientos>.
- REDIAM WFS service endpoint for the frozen dependent source:
  <https://www.juntadeandalucia.es/medioambiente/mapwms/REDIAM_WFS_Patrimonio_Natural?service=WFS&request=GetCapabilities>.
  The service's capabilities identify Junta de Andalucía as provider, EPSG:3042
  as the layer CRS, and free reuse conditional on naming the authors and owners.
- Junta open-data entry for the independently dated 2016 public-use equipment
  collection documents a CC BY 4.0 license and locational layers, but the
  Gate 8 dependency is the response frozen from the maintained REDIAM WFS on
  2026-10-05, not a claim that its contents represent 2016:
  <https://www.juntadeandalucia.es/datosabiertos/portal/dataset/equipamientos-de-uso-publico-de-andalucia-2016>.
- MITECO's Natura 2000 page describes the official date basis and attribution
  condition: <https://www.miteco.gob.es/en/cartografia-y-sig/ide/descargas/biodiversidad/rn2000.html>.
- Generalitat Valenciana's PATRICOVA entry identifies the ICV source and its
  CC Attribution catalogue license: <https://dadesobertes.gva.es/es/dataset/patricova-estudios-de-inundabilidad-plan-de-accion-territorial-de-caracter-sectorial-sobre-prev>.
- Datos.gob.es' Barcelona ZBE record describes the sole current GeoPackage
  distribution and CC BY 4.0 metadata: <https://datos.gob.es/es/catalogo/l01080193-ambito-de-la-zona-de-bajas-emisiones-zbe-de-la-ciudad-de-barcelona>.
