# GeoImpact CI

**Analysis verdict: PASS**

## Primary change

- Changed primary features: chamberi, tetuan
- Added primary features: none
- Removed primary features: none
- Modified primary features: chamberi, tetuan
- Changed footprint area: 8000.0 m²
- Maximum boundary displacement (modified shared IDs only): 40.0 m

## Relationship regressions

- hotels / hotel_813: chamberi -> tetuan
- tourism_pois / poi_212: chamberi -> tetuan

## Policy

- Rule: max_relationship_regressions
- Observed: 2
- Threshold: 2
- Status: PASS

## Evidence IDs

- relationship-regression-526712f2a3cfcdb0b86e03e9b060807c34ec8909095e5bb87cd57ab47e3cde49
- relationship-regression-b9209f0fa3ca1ab124fd412de95dc593c002219a36c5053a94071855602a0c68

## Provenance

- Config SHA-256: 1ecd53d2f6ba5402d1e2f0b23de60749fa3d6de7224c10663e15685b19bca0a9
- BASE (districts) SHA-256: fe2621c4defed71287355595ecd428fd8c1f7fddee822a37dddff4fe71b23837
- CANDIDATE (districts) SHA-256: a3ef49590971c5cf5dc45c33ece307d0d77d300f4aba374a6947e56b3198e19c
- Dependency hotels SHA-256: b92889469f7c14863963ec8242b86cd215497db13af4ea60f88ece81f77b06f4
- Dependency tourism_pois SHA-256: ac93115affcf7db76f768785eb932b3d289a3d2da8d323f4d242566c96210257
- GeoImpact CI: 1.2.0
- Shapely / GEOS: 2.1.2 / 3.13.1
- PyProj / PROJ: 3.7.2 / 9.5.1
