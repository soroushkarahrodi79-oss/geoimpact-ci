/* Bounded V5 artifact reader. Only byte checks, schema checks and identity joins.
   No spatial predicates, metrics, footprints, assignments or policy execution. */
export class EvidenceError extends Error {
  constructor(code, file, detail = '') { super(`${code}: ${file}${detail ? ' · ' + detail : ''}`); this.code = code; this.file = file; }
}
const fail = (ok, code, file, detail) => { if (!ok) throw new EvidenceError(code, file, detail); };
const array = (v) => Array.isArray(v);
const object = (v) => v !== null && typeof v === 'object' && !array(v);
const finite = (v) => typeof v === 'number' && Number.isFinite(v);
const id = (v) => typeof v === 'string' && v.length > 0;
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const setSame = (a, b) => a.size === b.size && [...a].every(x => b.has(x));
export const rowKey = (row) => JSON.stringify([row.dependent_dataset, row.dependent_id]);
export const pairKey = (row) => JSON.stringify([row.before, row.after]);
export async function sha256(bytes) {
  return [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(x => x.toString(16).padStart(2, '0')).join('');
}
function pathOK(path, caseId) {
  return typeof path === 'string' && /^data\/[a-z0-9-]+\/[a-zA-Z0-9_.-]+$/.test(path) && !path.includes('..') && (!caseId || path.startsWith(`data/${caseId}/`));
}
export async function readVerified(entry, fetcher = fetch, caseId) {
  fail(object(entry) && pathOK(entry.path, caseId), 'UNSAFE_PATH', 'manifest');
  fail(/^[a-f0-9]{64}$/.test(entry.sha256) && Number.isInteger(entry.size_bytes) && entry.size_bytes > 0, 'INVALID_IDENTITY', entry.path);
  let response;
  try { response = await fetcher(entry.path, { cache: 'no-store', redirect: 'error' }); }
  catch { throw new EvidenceError('LOAD_ERROR', entry.path); }
  fail(response.ok, response.status === 404 ? 'MISSING' : 'LOAD_ERROR', entry.path);
  const bytes = await response.arrayBuffer();
  fail(bytes.byteLength === entry.size_bytes && await sha256(bytes) === entry.sha256, 'HASH_MISMATCH', entry.path);
  return bytes;
}
function json(bytes, name) {
  try { return JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)); }
  catch { throw new EvidenceError('INVALID_JSON', name); }
}
export async function loadCatalog(expectedHash, fetcher = fetch) {
  let response;
  try { response = await fetcher('catalog.json', { cache: 'no-store', redirect: 'error' }); }
  catch { throw new EvidenceError('LOAD_ERROR', 'catalog.json'); }
  fail(response.ok, 'MISSING', 'catalog.json');
  const bytes = await response.arrayBuffer();
  fail(await sha256(bytes) === expectedHash, 'HASH_MISMATCH', 'catalog.json');
  const catalog = json(bytes, 'catalog.json');
  fail(catalog.studio_version === '0.1.0-academic-demo' && catalog.R1 === 'OPEN' && catalog.full_viewer === 'HOLD' && array(catalog.cases), 'UNSUPPORTED_CATALOG', 'catalog.json');
  const allowed = new Set(['synthetic-block', 'synthetic-pass', 'synthetic-error']);
  fail(catalog.cases.length > 0 && new Set(catalog.cases.map(x => x.id)).size === catalog.cases.length && catalog.cases.every(x => allowed.has(x.id)), 'CASE_NOT_ALLOWED', 'catalog.json');
  return catalog;
}
function position(p) { return array(p) && p.length === 2 && p.every(finite) && Math.abs(p[0]) <= 180 && Math.abs(p[1]) <= 90; }
function geometry(g, point) {
  if (!object(g)) return false;
  if (point) return g.type === 'Point' && position(g.coordinates);
  if (!['Polygon', 'MultiPolygon'].includes(g.type) || !array(g.coordinates) || g.coordinates.length === 0) return false;
  const polygons = g.type === 'Polygon' ? [g.coordinates] : g.coordinates;
  return polygons.every(p => array(p) && p.length > 0 && p.every(r => array(r) && r.length >= 4 && r.every(position) && same(r[0], r.at(-1))));
}
function features(fc, field, point, file) {
  fail(object(fc) && fc.type === 'FeatureCollection' && array(fc.features) && !fc.crs && id(field), 'INVALID_GEOJSON', file);
  const map = new Map();
  for (const f of fc.features) {
    fail(object(f) && f.type === 'Feature' && object(f.properties) && id(f.properties[field]) && !map.has(f.properties[field]) && geometry(f.geometry, point), 'INVALID_FEATURE', file);
    map.set(f.properties[field], f);
  }
  fail(map.size > 0, 'EMPTY_INPUT', file);
  return map;
}
function identitySame(entry, expected, file) {
  fail(object(expected) && entry.sha256 === expected.sha256 && entry.size_bytes === expected.size_bytes, 'V5_INPUT_MISMATCH', file);
}
export function validateBundle(manifest, data) {
  const name = 'report.json', r = data['report.json'];
  fail(object(r) && r.report_version === '5', 'UNSUPPORTED_REPORT', name);
  fail(object(r.analysis) && r.analysis.crs === 'EPSG:25830' && id(r.analysis.primary_dataset) && id(r.analysis.primary_id_field), 'UNSUPPORTED_CRS_OR_ANALYSIS', name);
  fail(manifest.display_crs === 'OGC:CRS84', 'UNSUPPORTED_DISPLAY_CRS', 'manifest');
  fail(['PASS', 'BLOCK'].includes(r.verdict) && object(r.policy) && r.policy.status === r.verdict && r.policy.rule === 'max_relationship_regressions' && finite(r.policy.threshold) && r.policy.threshold >= 0 && Number.isInteger(r.policy.observed_value) && r.policy.observed_value >= 0, 'INVALID_POLICY_RECORD', name);
  fail(object(r.provenance) && r.provenance.hash_algorithm === 'sha256' && object(r.provenance.engine) && r.provenance.engine.geoimpact_ci === '1.2.0' && ['geoimpact_ci', 'shapely', 'geos', 'pyproj', 'proj'].every(k => id(r.provenance.engine[k])), 'INVALID_PROVENANCE', name);
  const inputs = r.provenance.inputs;
  fail(object(inputs) && object(inputs.primary) && array(inputs.dependencies), 'INVALID_PROVENANCE', name);
  for (const [role, expected] of [['config', inputs.config], ['base', inputs.primary.base], ['candidate', inputs.primary.candidate]]) identitySame(manifest.files[role], expected, role);
  fail(inputs.primary.base.dataset === r.analysis.primary_dataset && inputs.primary.candidate.dataset === r.analysis.primary_dataset, 'DATASET_MISMATCH', name);
  const base = features(data.base, r.analysis.primary_id_field, false, 'base');
  const candidate = features(data.candidate, r.analysis.primary_id_field, false, 'candidate');
  const pc = r.primary_change;
  fail(object(pc) && object(pc.feature_geometry_status) && finite(pc.changed_footprint_area_m2) && pc.changed_footprint_area_m2 >= 0 && finite(pc.max_boundary_displacement_m) && pc.max_boundary_displacement_m >= 0 && object(pc.changed_footprint_geometry), 'INVALID_PRIMARY_RECORD', name);
  fail(setSame(new Set(Object.keys(pc.feature_geometry_status)), new Set([...base.keys(), ...candidate.keys()])) && Object.values(pc.feature_geometry_status).every(v => ['modified', 'unchanged', 'added', 'removed'].includes(v)), 'PRIMARY_ID_MISMATCH', name);
  for (const [key,status] of Object.entries(pc.feature_geometry_status)) {
    fail(status === 'added' ? !base.has(key) && candidate.has(key) : status === 'removed' ? base.has(key) && !candidate.has(key) : base.has(key) && candidate.has(key), 'PRIMARY_PRESENCE_MISMATCH', name);
  }
  // Validate declared lists and presence, without classifying geometry.
  for (const [field, status] of [['added_feature_ids', 'added'], ['removed_feature_ids', 'removed'], ['modified_feature_ids', 'modified']]) {
    fail(array(pc[field]) && setSame(new Set(pc[field]), new Set(Object.keys(pc.feature_geometry_status).filter(k => pc.feature_geometry_status[k] === status))), 'PRIMARY_STATUS_MISMATCH', field);
  }
  fail(array(r.analysis.dependencies) && r.analysis.dependencies.length === manifest.dependencies.length && inputs.dependencies.length === manifest.dependencies.length, 'DEPENDENCY_MISMATCH', name);
  const dependencies = new Map(), allPoints = new Map();
  r.analysis.dependencies.forEach((definition, i) => {
    const md = manifest.dependencies[i];
    fail(definition.dataset === md.dataset && inputs.dependencies[i].dataset === md.dataset && definition.predicate === 'within' && !dependencies.has(md.dataset), 'DEPENDENCY_MISMATCH', name);
    identitySame(manifest.files[`dependency-${i}`], inputs.dependencies[i], md.file);
    const indexed = features(data[`dependency-${i}`], definition.id_field, true, md.file);
    dependencies.set(md.dataset, indexed);
    for (const [key, f] of indexed) allPoints.set(JSON.stringify([md.dataset, key]), f);
  });
  fail(array(r.relationships) && array(r.relationship_regressions) && array(r.boundary_ambiguities) && array(r.policy.evidence_ids), 'MISSING_RECORDS', name);
  const rows = new Map(), rowIndices = new Map();
  r.relationships.forEach((row, index) => {
    fail(object(row) && id(row.dependent_dataset) && id(row.dependent_id) && row.predicate === 'within' && ['unchanged', 'assignment_changed', 'assignment_gained', 'assignment_lost'].includes(row.change_type), 'INVALID_RELATIONSHIP', name);
    const key = rowKey(row);
    fail(!rows.has(key) && allPoints.has(key) && array(row.before) && array(row.after) && row.before.length === new Set(row.before).size && row.after.length === new Set(row.after).size && row.before.every(x => base.has(x)) && row.after.every(x => candidate.has(x)), 'ORPHAN_OR_DUPLICATE_ID', name);
    rows.set(key, row); rowIndices.set(key, index);
  });
  fail(rows.size === allPoints.size, 'INCOMPLETE_RELATIONSHIPS', name);
  const evidence = new Map(), regressionByRow = new Map();
  for (const row of r.relationship_regressions) {
    const key = rowKey(row), related = rows.get(key);
    fail(related && id(row.evidence_id) && !evidence.has(row.evidence_id) && !regressionByRow.has(key) && row.change_type !== 'unchanged' && ['before', 'after', 'predicate', 'change_type'].every(f => same(row[f], related[f])) && row.primary_dataset === r.analysis.primary_dataset && array(row.primary_feature_ids) && setSame(new Set(row.primary_feature_ids), new Set([...row.before,...row.after])) && row.evidence_geometry_crs === 'EPSG:25830' && row.evidence_geometry?.type === 'Point', 'EVIDENCE_JOIN_MISMATCH', name);
    evidence.set(row.evidence_id, row); regressionByRow.set(key, row);
  }
  fail(setSame(new Set(r.policy.evidence_ids), new Set(evidence.keys())) && r.policy.evidence_ids.length === evidence.size && r.policy.observed_value === evidence.size && r.relationships.every(row => (row.change_type === 'unchanged') === !regressionByRow.has(rowKey(row))), 'EVIDENCE_COVERAGE_MISMATCH', name);
  const geo = data['relationship-regressions.geojson'];
  fail(object(geo) && geo.type === 'FeatureCollection' && array(geo.features) && !geo.crs, 'INVALID_GEOJSON', 'relationship-regressions.geojson');
  const seen = new Set();
  for (const f of geo.features) {
    const p = f.properties, ref = evidence.get(p?.evidence_id);
    fail(f.type === 'Feature' && ref && !seen.has(p.evidence_id) && geometry(f.geometry, true) && ['evidence_id', 'dependent_dataset', 'dependent_id', 'predicate', 'before', 'after', 'change_type'].every(k => same(p[k], ref[k])), 'EXPORT_JOIN_MISMATCH', 'relationship-regressions.geojson');
    const original = allPoints.get(rowKey(ref)).geometry.coordinates;
    fail(f.geometry.coordinates.every((c, i) => Math.abs(c - original[i]) <= 5.1e-9), 'EXPORT_COORDINATE_MISMATCH', 'relationship-regressions.geojson');
    seen.add(p.evidence_id);
  }
  fail(setSame(seen, new Set(evidence.keys())), 'EXPORT_COVERAGE_MISMATCH', 'relationship-regressions.geojson');
  const boundaries = new Map();
  for (const row of r.boundary_ambiguities) {
    const key = rowKey(row);
    fail(rows.has(key) && !boundaries.has(key) && array(row.before_boundary_primary_ids) && row.before_boundary_primary_ids.every(x => base.has(x)) && array(row.after_boundary_primary_ids) && row.after_boundary_primary_ids.every(x => candidate.has(x)), 'BOUNDARY_JOIN_MISMATCH', name);
    boundaries.set(key, row);
  }
  return { manifest, report: r, base, candidate, dependencies, allPoints, rows, rowIndices, evidence, regressionByRow, boundaries };
}
export async function loadCase(entry, fetcher = fetch) {
  const manifest = json(await readVerified(entry, fetcher, entry.id), entry.path);
  fail(manifest.bundle_version === 1 && manifest.id === entry.id, 'MIXED_CASE', 'manifest');
  if (manifest.kind === 'analysis-error') {
    fail(manifest.exit_code === 2 && typeof manifest.stderr === 'string' && !('verdict' in manifest) && !('files' in manifest), 'INVALID_ERROR_RECORD', 'manifest');
    return { manifest };
  }
  fail(manifest.kind === 'completed' && object(manifest.files) && array(manifest.dependencies) && manifest.release_commit === '45237d7caaea2aa4b81359e46f1623918645078c', 'UNSUPPORTED_BUNDLE', 'manifest');
  fail(object(manifest.title) && ['es','en'].every(k => id(manifest.title[k]) && id(manifest.limitations?.[k])) && array(manifest.editions) && manifest.editions.length === 2 && manifest.editions.every(id) && id(manifest.attribution) && id(manifest.inventory_date) && manifest.category === 'synthetic' && array(manifest.sources) && manifest.sources.every(s => id(s.title) && id(s.terms) && typeof s.url === 'string' && s.url.startsWith('https://')), 'INVALID_SOURCE_METADATA', 'manifest');
  const roles = ['config', 'base', 'candidate', 'report.json', 'report.md', 'relationship-regressions.geojson', ...manifest.dependencies.map((_, i) => `dependency-${i}`)];
  fail(setSame(new Set(roles), new Set(Object.keys(manifest.files))), 'MISSING_FILES', 'manifest');
  const data = {}, bytes = new Map();
  await Promise.all(roles.map(async role => {
    const raw = await readVerified(manifest.files[role], fetcher, manifest.id);
    bytes.set(role, raw);
    if (!['config', 'report.md'].includes(role)) data[role] = json(raw, manifest.files[role].path);
  }));
  return { ...validateBundle(manifest, data), bytes };
}
