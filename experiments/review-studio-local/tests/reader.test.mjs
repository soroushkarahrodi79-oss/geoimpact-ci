import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { loadCatalog, loadCase, validateBundle, readVerified, rowKey, sha256 } from '../web/reader.js';
import { catalogHash } from '../web/trust.js';

const web = new URL('../web/', import.meta.url);
const fileFetch = async path => { try { return new Response(await readFile(new URL(path,web))); } catch { return new Response('',{status:404}); } };
const catalog = await loadCatalog(catalogHash,fileFetch);
const entry = catalog.cases.find(x=>x.id==='synthetic-block');
const valid = await loadCase(entry,fileFetch);
const fresh = () => {
  const data={};for(const [role,raw] of valid.bytes) if(!['config','report.md'].includes(role)) data[role]=JSON.parse(new TextDecoder().decode(raw));
  return { manifest:structuredClone(valid.manifest), data };
};
const reject = (operation,code) => assert.throws(operation,error=>error.code===code);

test('released BLOCK has complete composite joins and exact two evidence records',()=>{
  assert.equal(valid.report.verdict,'BLOCK');assert.equal(valid.rows.size,3);assert.equal(valid.evidence.size,2);
  assert.deepEqual(valid.rows.get(rowKey({dependent_dataset:'hotels',dependent_id:'hotel_813'})).before,['chamberi']);
  assert.equal(valid.bytes.get('report.json').byteLength,valid.manifest.files['report.json'].size_bytes);
});
test('real PASS report retains two regressions with a permissive configured threshold',async()=>{
  const b=await loadCase(catalog.cases.find(x=>x.id==='synthetic-pass'),fileFetch);
  assert.equal(b.report.verdict,'PASS');assert.equal(b.report.policy.threshold,2);assert.equal(b.evidence.size,2);
});
test('recorded CLI ERROR has no report, geometry, input manifest or invented verdict',async()=>{
  const b=await loadCase(catalog.cases.find(x=>x.id==='synthetic-error'),fileFetch);
  assert.equal(b.manifest.exit_code,2);assert.equal(b.report,undefined);assert.equal(b.manifest.verdict,undefined);
});
test('raw byte changes reject even semantically equivalent JSON',async()=>{
  await assert.rejects(loadCase(entry,async path=>{
    const r=await fileFetch(path);if(path.endsWith('/report.json'))return new Response((await r.text())+' ');return r;
  }),e=>e.code==='HASH_MISMATCH');
});
test('missing files are not empty valid results',async()=>{
  await assert.rejects(loadCase(entry,async path=>path.endsWith('/districts_base.geojson')?new Response('',{status:404}):fileFetch(path)),e=>e.code==='MISSING');
});
test('remote, parent-traversal, cross-case and unsafe bundle paths cannot be loaded',async()=>{
  for(const path of ['https://example.com/x','../report.json','data/synthetic-block/../report.json','data/sierra-local/report.json']){
    await assert.rejects(readVerified({...entry,path},()=>{throw Error('must not fetch');},entry.id),e=>e.code==='UNSAFE_PATH');
  }
});
test('catalog itself is bound to a retained digest',async()=>{
  await assert.rejects(loadCatalog('0'.repeat(64),fileFetch),e=>e.code==='HASH_MISMATCH');
});
test('unsupported V4 is rejected without upgrading',()=>{
  const {manifest,data}=fresh();data['report.json'].report_version='4';reject(()=>validateBundle(manifest,data),'UNSUPPORTED_REPORT');
});
test('unknown report and display CRS cannot be drawn',()=>{
  const f=fresh();f.data['report.json'].analysis.crs='OGC:CRS84';reject(()=>validateBundle(f.manifest,f.data),'UNSUPPORTED_CRS_OR_ANALYSIS');
  const g=fresh();g.manifest.display_crs='EPSG:25830';reject(()=>validateBundle(g.manifest,g.data),'UNSUPPORTED_DISPLAY_CRS');
});
test('V5 config identities are independently checked after bundle hashes',()=>{
  const {manifest,data}=fresh();data['report.json'].provenance.inputs.config.sha256='0'.repeat(64);reject(()=>validateBundle(manifest,data),'V5_INPUT_MISMATCH');
});
test('same dependent ID in different datasets remains a separate composite key',()=>{
  assert.notEqual(rowKey({dependent_dataset:'one',dependent_id:'shared'}),rowKey({dependent_dataset:'two',dependent_id:'shared'}));
});
test('duplicate and orphan relationship rows reject',()=>{
  const f=fresh();f.data['report.json'].relationships.push(f.data['report.json'].relationships[0]);reject(()=>validateBundle(f.manifest,f.data),'ORPHAN_OR_DUPLICATE_ID');
  const g=fresh();g.data['report.json'].relationships[0].dependent_id='missing';reject(()=>validateBundle(g.manifest,g.data),'ORPHAN_OR_DUPLICATE_ID');
});
test('missing records cannot silently reduce the observed inventory',()=>{
  const {manifest,data}=fresh();data['report.json'].relationships.pop();reject(()=>validateBundle(manifest,data),'INCOMPLETE_RELATIONSHIPS');
});
test('before/after cannot reference absent source primary IDs',()=>{
  const {manifest,data}=fresh();data['report.json'].relationships[0].before=['absent'];reject(()=>validateBundle(manifest,data),'ORPHAN_OR_DUPLICATE_ID');
});
test('primary added/removed declarations must agree with presence in original snapshots',()=>{
  const {manifest,data}=fresh();data['report.json'].primary_change.feature_geometry_status.chamberi='added';reject(()=>validateBundle(manifest,data),'PRIMARY_PRESENCE_MISMATCH');
});
test('regression primary dataset and referenced identity set must match the original relationship',()=>{
  const {manifest,data}=fresh();data['report.json'].relationship_regressions[0].primary_dataset='wrong-case';reject(()=>validateBundle(manifest,data),'EVIDENCE_JOIN_MISMATCH');
});
test('source geometry must be original geographic Polygon/MultiPolygon with closed rings',()=>{
  const f=fresh();f.data.base.features[0].geometry.coordinates[0][0]=[440000,4470000];reject(()=>validateBundle(f.manifest,f.data),'INVALID_FEATURE');
  const g=fresh();g.data.base.features[0].geometry.coordinates[0].pop();reject(()=>validateBundle(g.manifest,g.data),'INVALID_FEATURE');
});
test('export evidence properties must agree with report and original fixed coordinates',()=>{
  const f=fresh();f.data['relationship-regressions.geojson'].features[0].properties.before=['tetuan'];reject(()=>validateBundle(f.manifest,f.data),'EXPORT_JOIN_MISMATCH');
  const g=fresh();g.data['relationship-regressions.geojson'].features[0].geometry.coordinates[0]+=0.01;reject(()=>validateBundle(g.manifest,g.data),'EXPORT_COORDINATE_MISMATCH');
});
test('policy status contradictions fail closed, without executing threshold logic',()=>{
  const {manifest,data}=fresh();data['report.json'].policy.status='PASS';reject(()=>validateBundle(manifest,data),'INVALID_POLICY_RECORD');
});
test('regression evidence cannot be attached to an unchanged row or omitted',()=>{
  const f=fresh();f.data['report.json'].relationship_regressions[0].dependent_id='hotel_unchanged';reject(()=>validateBundle(f.manifest,f.data),'EVIDENCE_JOIN_MISMATCH');
  const g=fresh();g.data['relationship-regressions.geojson'].features.pop();reject(()=>validateBundle(g.manifest,g.data),'EXPORT_COVERAGE_MISMATCH');
});
test('Sierra: exact frozen hashes, 52 unchanged rows, 40 assigned / 12 unassigned, empty regression collection', {skip:!catalog.cases.some(x=>x.id==='sierra-local')}, async()=>{
  const b=await loadCase(catalog.cases.find(x=>x.id==='sierra-local'),fileFetch);
  assert.equal(b.report.verdict,'PASS');assert.equal(b.rows.size,52);assert.equal(b.evidence.size,0);assert.equal(b.report.boundary_ambiguities.length,0);
  assert.equal(b.report.relationships.filter(r=>r.before.length===1&&r.after.length===1&&r.before[0]==='69'&&r.after[0]==='69').length,40);
  assert.equal(b.report.relationships.filter(r=>r.before.length===0&&r.after.length===0).length,12);
  assert.equal(b.report.primary_change.feature_geometry_status['69'],'modified');
  const rights=JSON.parse(await readFile(new URL('../rights/sierra-local.json',import.meta.url)));
  for(const [role,digest] of Object.entries(rights.output_sha256))assert.equal(await sha256(b.bytes.get(role)),digest);
});

test('the browser source has no GIS or policy execution and serves only its own root',async()=>{
  const app=await readFile(new URL('../web/app.js',import.meta.url),'utf8');
  assert.doesNotMatch(app,/innerHTML|eval\(|turf\.|fetch\(|XMLHttpRequest|WebSocket|serviceWorker/);
  const files=['index.html','app.js','style.css','reader.js'];
  for(const file of files)assert.doesNotMatch(await readFile(new URL('../web/'+file,import.meta.url),'utf8'),/ine-sections-202[45]-focus|madrid-portals-change-footprint|unpkg\.com|fonts\.googleapis/);
});
