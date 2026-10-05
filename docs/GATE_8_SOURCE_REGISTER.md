# Gate 8 Source Register

Retrieval date for source bytes: **2026-10-05**. Attribution for REDIAM data:
**Fuente: Red de Información Ambiental de Andalucía (REDIAM), Junta de
Andalucía.** This register separates the complete downloaded upstream source
snapshots from the smaller derived fixture checked into the repository.

## 1. BASE: EENNPP 2015

| Field | Record |
|---|---|
| Owner / publisher | Consejería de Sostenibilidad y Medio Ambiente, Junta de Andalucía |
| Dataset | Límites de los Espacios Naturales Protegidos de Andalucía (EENNPP): 2015 |
| URL | [Official 2015 open-data record](https://www.juntadeandalucia.es/datosabiertos/portal/dataset/limites-de-los-espacios-naturales-protegidos-de-andalucia-eennpp-2015); direct archive: `https://www.juntadeandalucia.es/medioambiente/servtorrent/informacionambiental/07_PATRIMONIO_NATURAL/01_RENPA/00_RENPA/EENNPP.tar.gz` |
| Resource identifier | TAR.GZ resource `90088f41-2a6b-4b48-8e82-67326c5bdbc2` |
| Snapshot/publication date | Layer documented as updated May 2015; catalog entry date not separately shown |
| Retrieved | 2026-10-05 |
| Spatial scope / fixture scope | Andalusia; selected feature is Sierra de Baza Natural Park, `CODIGOESPA=69` |
| Source CRS | Shapefile PRJ: `ETRS_1989_UTM_Zone_30N`, equivalent to EPSG:25830 |
| Geometry | Polygon shapefile; selected feature is polygon/multipolygonal |
| Stable-ID field | `CODIGOESPA` (numeric in source); selected value `69` is unique and matches the candidate on code, name, and figure |
| Original source records | 192 in `ETRS89_30/EENNPP.shp` |
| Filtered fixture records | 1 |
| Source bytes | 23,162,313 |
| Source SHA-256 | `7c1f43a0e9adf1ccc99b66051482b7c2a3f8ffdf7f42aeb4eedd3c554a1dc67b` |
| Canonical fixture SHA-256 | `eae31120ec45e51c53b48515c0bde6e1d1c269edafea51076f862c16854d2799` (`base.geojson`) |
| License / attribution | Catalog states CC BY 4.0. Attribute Junta de Andalucía / REDIAM. |
| Redistribution | CC BY 4.0 permits reuse with attribution. Raw archive omitted from repository. |
| Filtering | Extract `ETRS89_30/EENNPP.shp`; select exact official source attributes `CODIGOESPA=69`, `NOMBRE=SIERRA DE BAZA`, `FIGURA=Parque Natural`; transform to CRS84 for GeoJSON. |
| Source limitations | The 2015 layer has 27 repeated `CODIGOESPA` values across overlapping protection figures; selected feature code 69 is unique. The source lineage is a decade before candidate. |

## 2. CANDIDATE: EENNPP, December 2025 release

| Field | Record |
|---|---|
| Owner / publisher | Red de Información Ambiental de Andalucía (REDIAM), Junta de Andalucía |
| Dataset | Límites de los Espacios Naturales Protegidos de Andalucía (EENNPP); latest published version identified as December 2025 |
| URL / resource | WFS `https://www.juntadeandalucia.es/medioambiente/mapwms/REDIAM_RENPA?service=WFS&request=GetCapabilities`, feature type `ms:eennpp`, GeoJSON output |
| Resource identifier | WFS type name `ms:eennpp`; response identifies name `eennpp` |
| Snapshot/publication date | Source page identifies latest release as December 2025 and says Sierra de Baza boundary updated after the new PORN approved in December 2025; exact WFS extraction retrieved 2026-10-05 |
| Retrieved | 2026-10-05 |
| Spatial scope / fixture scope | Andalusia service layer; selected feature Sierra de Baza Natural Park |
| Source CRS | WFS response: EPSG:3042; transformed by preparation script to CRS84 for GeoJSON and product analysis EPSG:25830 |
| Geometry | WFS polygonal geometry; selected source geometry valid and non-empty |
| Stable-ID field | `CODIGOESPA` (string in WFS); selected value `69`, unique and matching BASE name/figure |
| Original source records | `numberMatched=209` |
| Filtered fixture records | 1 |
| Source bytes | 17,823,340 |
| Source SHA-256 | `2f64c939d0052076d3bb4ddb02e9230cffeafdc606c36c673612a90686add834` |
| Canonical fixture SHA-256 | `4f4b4ff369befb14c8f1d26e902fda4b431de26432f85897d2cd77df9485cc17` (`candidate.geojson`) |
| License / attribution | WFS capabilities state the service may be used freely and without charge when authors and owners are named. The EENNPP latest-release page does not show a separate standard license label. |
| Redistribution | The repository includes only a bounded derived target feature and retains the stated attribution. It makes no claim of a separate standard license. |
| Filtering | Select exact official source attributes `CODIGOESPA=69`, `NOMBRE=SIERRA DE BAZA`, `FIGURA=Parque Natural`; do not repair geometry. |
| Source limitations | The complete WFS response has 32 repeated `CODIGOESPA` values and one invalid feature unrelated to selected code 69. Latest release page documents date, while the WFS endpoint is maintained and not advertised as an immutable archive. The exact response is protected by its SHA-256 and the compact fixture is checked in. |

## 3. DEPENDENCY: public-use equipment reference inventory

| Field | Record |
|---|---|
| Owner / publisher | REDIAM, Junta de Andalucía; provider named in WFS capabilities |
| Dataset | Equipamientos de uso público, feature type `ms:equipamientos_uso_publico` |
| URL / resource | `https://www.juntadeandalucia.es/medioambiente/mapwms/REDIAM_WFS_Patrimonio_Natural?service=WFS&request=GetCapabilities`, GeoJSON output |
| Resource identifier | WFS type name `ms:equipamientos_uso_publico` |
| Snapshot/publication date | Fixed service response retrieved 2026-10-05; not a historical snapshot |
| Retrieved | 2026-10-05 |
| Coverage / fixture scope | Complete Andalusian point layer as raw acquisition; selected 52 points from deterministic 10 km expanded envelope of the independently computed Sierra de Baza geometric change footprint |
| Source CRS | WFS response: EPSG:3042; transformed via EPSG:25830 for subset selection and CRS84 for GeoJSON fixture |
| Geometry | Point |
| Stable-ID field | `CODIGOEQUI`; selected 52 identifiers are present and unique. Two duplicate codes occur in the full raw layer but are outside the selected subset. |
| Original source records | `numberMatched=1128` |
| Filtered fixture records | 52 |
| Source bytes | 528,438 |
| Source SHA-256 | `02aadfc63c7f48ed67f84aa8b1c7c4ba5069c25b737e5f0e829d977c28b5eb5e` |
| Canonical fixture SHA-256 | `617d4b71921b8d66692f1c8457a56b9b6224abb0c044bb06ce7608e2524c0f6c` (`dependencies.geojson`) |
| License / attribution | REDIAM WFS capabilities state free use conditional on naming authors and owners. The separate dated 2016 open-data record is CC BY 4.0, but that is not asserted as the license of this 2026 response. |
| Redistribution | The 52-feature derived fixture is accompanied by required provider attribution; no standard license is newly assigned. |
| Filtering | Keep all source point features whose EPSG:25830 coordinates lie within the symmetric-difference bounding box expanded by 10,000 m on each side. This spatial selection rule was fixed before any GeoImpact result. |
| Source limitations | Inventory is 2026-10-05, potentially temporally misaligned with 2015/2025 polygons; equipment can be added, moved, removed, or reclassified. Source layer is maintained online rather than presented as an immutable historical snapshot. |

## License references

The pre-execution `geoimpact.yml` SHA-256 is
`f7e3245517cc5c16d97b34c08b0760e5055cfc25a71a39f1ee847413c0ee2520`.

- 2015 EENNPP CC BY 4.0 statement: [Open Data Andalucía record](https://www.juntadeandalucia.es/datosabiertos/portal/dataset/limites-de-los-espacios-naturales-protegidos-de-andalucia-eennpp-2015).
- 2025 EENNPP date and boundary updates: [December 2025 release page](https://www.juntadeandalucia.es/medioambiente/portal/acceso-rediam/visor-condicionantes-ambientales/fichas-descriptivas/eennpp/renpa/limites).
- WFS provider, output CRS, and access/reuse condition: `GetCapabilities` responses at the two service URLs above.
- Public-use equipment context: [official description](https://www.juntadeandalucia.es/medioambiente/portal/areas-tematicas/uso-publico/equipamientos).
