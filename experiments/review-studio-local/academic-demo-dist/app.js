import { catalogHash } from './trust.js';
import { loadCatalog, loadCase, rowKey, pairKey } from './reader.js';
import { installOnboarding } from './onboarding.js';

const $ = id => document.getElementById(id);
const words = {
  es: { skip:'Ir a la revisión', local:'DEMO ACADÉMICA · DATOS SINTÉTICOS', language:'Idioma', eyebrow:'EVIDENCIA ESPACIAL / DEMOSTRACIÓN ACADÉMICA', heading:'Un cambio de límite. La evidencia, a la vista.', intro:'Compara las geometrías originales y sigue cada relación hasta su informe.', case:'Caso de revisión', scope:'Demo académica privada · datos sintéticos', loading:'Verificando archivos…', policyResult:'RESULTADO DE LA POLÍTICA', auditLink:'Ver procedencia ↗', compare:'COMPARAR', originalGeometry:'Geometrías originales', zoomIn:'Acercar', zoomOut:'Alejar', fitAll:'Encuadrar todo', fitSelection:'Ver selección', polygons:'Polígonos', points:'Inventario fijo', primary:'Geometría primaria', regression:'Regresión', regressions:'Regresiones', unchanged:'Sin cambio', boundary:'Frontera', mapHelp:'Sin mapa base · coordenadas originales. Flechas para desplazar con el mapa enfocado; +/− para zoom. Lista equivalente debajo.', inspect:'INSPECCIONAR', relationships:'Relaciones espaciales', search:'Buscar ID o dataset', show:'Mostrar', all:'Todas', transition:'Transición before → after', filtersHelp:'Los filtros cambian las filas visibles; el resultado científico permanece intacto.', identity:'IDENTIDAD', state:'ESTADO', previous:'Anterior', next:'Siguiente', trace:'TRAZAR', evidence:'Evidencia de relación', clear:'Limpiar selección', geometryRecord:'Registro geométrico', verify:'VERIFICAR', provenance:'Procedencia y límites', verified:'Bytes verificados', hashMeaning:'Coincidencia con el manifiesto retenido y las identidades V5. No autentica al proveedor ni acredita derechos o exactitud.', config:'Configuración original · solo lectura', sources:'Fuentes y condiciones', limitations:'Límites de interpretación', footprint:'Huella EPSG:25830 no representada. No se calculan métricas ni relaciones en este visor.', scientificMeaning:'La modificación de una geometría no implica una relación alterada. El resultado no acredita efectos reales ni corrección de los datos.', prototype:'demostración académica privada con datos sintéticos', fullHold:'visor completo HOLD', synthetic:'SINTÉTICO', assignments:'relaciones evaluadas', primaryChanged:'IDs primarios modificados', threshold:'Umbral configurado', observed:'Regresiones observadas', recordCount:'Registros del informe', fromJSON:'Fuente: report.json', passMeaning:'PASS: la política no bloqueó las regresiones observadas bajo el umbral configurado. No acredita corrección de datos ni ausencia de efectos reales.', blockMeaning:'BLOCK: el análisis terminó y superó el umbral configurado. No significa que los datos sean incorrectos ni demuestra daños reales.', selectHint:'Selecciona un punto o una relación para consultar sus asignaciones y evidencia original.', noEvidence:'Sin ID de evidencia de regresión', noWithin:'Sin asignación within', openRecord:'Abrir registro original ↗', boundaryNone:'Sin ambigüedad de frontera registrada', total:'total', visible:'visibles', page:'Página', of:'de', noMatches:'Ninguna relación coincide con los filtros.', zero:'0 regresiones; el inventario fijo sigue disponible en el mapa.', reviewed:'relaciones evaluadas. El export de regresiones vacío es válido.', download:'Archivo original ↓', selected:'Relación seleccionada', unsupported:'Evidencia no disponible', loadError:'ERROR · CARGA O INTEGRIDAD', analysisError:'ERROR · ANÁLISIS SIN RESULTADO', analysisMeaning:'El CLI terminó con exit 2. No produjo un informe ni un veredicto científico. Este caso es un fallo controlado de configuración ausente.', loadMeaning:'No se puede revisar este paquete. No hay un veredicto válido para esta carga; la vista anterior se ha retirado.', retry:'Reintentar', before:'ASIGNACIÓN BEFORE', after:'ASIGNACIÓN AFTER', versions:'Versiones registradas en V5', report:'Informe V5', unchangedGeometry:'Geometría primaria y relación son conceptos distintos.', exactValues:'Valores exactos del informe', mismatch:'Archivo no verificado', panLeft:'Desplazar a la izquierda', panRight:'Desplazar a la derecha', panUp:'Desplazar arriba', panDown:'Desplazar abajo', primaryState:'Estado de la geometría seleccionada', identityOK:'Identidad verificada · V5', noScientific:'Sin resultado científico', bytes:'bytes', modified:'modificada', added:'añadida', removed:'eliminada', assignment_changed:'Cambio de asignación', assignment_gained:'Asignación ganada', assignment_lost:'Asignación perdida' },
  en: { skip:'Skip to review', local:'ACADEMIC DEMO · SYNTHETIC DATA', language:'Language', eyebrow:'SPATIAL EVIDENCE / ACADEMIC DEMONSTRATION', heading:'A boundary changes. The evidence is here.', intro:'Compare original geometries and trace each relationship to its report.', case:'Review case', scope:'Private academic demo · synthetic data', loading:'Verifying files…', policyResult:'CONFIGURED POLICY RESULT', auditLink:'Inspect provenance ↗', compare:'COMPARE', originalGeometry:'Original geometries', zoomIn:'Zoom in', zoomOut:'Zoom out', fitAll:'Fit all', fitSelection:'Fit selection', polygons:'Polygons', points:'Fixed inventory', primary:'Primary geometry', regression:'Regression', regressions:'Regressions', unchanged:'Unchanged', boundary:'Boundary', mapHelp:'No basemap · original coordinates. Arrow keys pan while the map has focus; +/− zoom. Equivalent list below.', inspect:'INSPECT', relationships:'Spatial relationships', search:'Search ID or dataset', show:'Show', all:'All', transition:'Transition before → after', filtersHelp:'Filters change visible rows; the scientific result stays unchanged.', identity:'IDENTITY', state:'STATE', previous:'Previous', next:'Next', trace:'TRACE', evidence:'Relationship evidence', clear:'Clear selection', geometryRecord:'Geometry record', verify:'VERIFY', provenance:'Provenance and limits', verified:'Bytes verified', hashMeaning:'Matches the retained manifest and V5 input identities. Does not authenticate the publisher or establish rights or accuracy.', config:'Original configuration · read only', sources:'Sources and conditions', limitations:'Interpretation limits', footprint:'EPSG:25830 footprint is not mapped. No metrics or relationships are computed in this viewer.', scientificMeaning:'Modified geometry does not imply a changed relationship. The result does not establish real-world effects or data correctness.', prototype:'private academic demonstration with synthetic data', fullHold:'full viewer HOLD', synthetic:'SYNTHETIC', assignments:'relationships evaluated', primaryChanged:'Modified primary IDs', threshold:'Configured threshold', observed:'Observed regressions', recordCount:'Report records', fromJSON:'Source: report.json', passMeaning:'PASS: the configured policy did not block the observed regressions. This does not establish data correctness or absence of real-world effects.', blockMeaning:'BLOCK: analysis completed and exceeded the configured threshold. This does not mean the data are incorrect or demonstrate real-world harm.', selectHint:'Select a point or relationship to inspect its original assignments and evidence.', noEvidence:'No regression evidence ID', noWithin:'No within assignment', openRecord:'Open original record ↗', boundaryNone:'No recorded boundary ambiguity', total:'total', visible:'visible', page:'Page', of:'of', noMatches:'No relationships match the filters.', zero:'0 regressions; the fixed inventory remains available on the map.', reviewed:'relationships evaluated. An empty regression export is valid.', download:'Original file ↓', selected:'Relationship selected', unsupported:'Evidence unavailable', loadError:'ERROR · LOAD OR INTEGRITY', analysisError:'ERROR · ANALYSIS WITHOUT A RESULT', analysisMeaning:'The CLI ended with exit 2. It produced no report and no scientific verdict. This is a controlled missing-configuration failure.', loadMeaning:'This bundle cannot be reviewed. No valid verdict exists for this load; the previous view has been cleared.', retry:'Retry', before:'BEFORE ASSIGNMENT', after:'AFTER ASSIGNMENT', versions:'Versions recorded in V5', report:'V5 report', unchangedGeometry:'Primary geometry and relationships are distinct concepts.', exactValues:'Exact report values', mismatch:'File not verified', panLeft:'Pan left', panRight:'Pan right', panUp:'Pan up', panDown:'Pan down', primaryState:'Selected geometry status', identityOK:'Identity verified · V5', noScientific:'No scientific result', bytes:'bytes', modified:'modified', added:'added', removed:'removed', assignment_changed:'Assignment changed', assignment_gained:'Assignment gained', assignment_lost:'Assignment lost' }
};
const state = { lang:'es', catalog:null, bundle:null, selected:null, primary:null, page:0, snapshot:'base', view:null, error:null, epoch:0, returnKey:null };
const t = key => words[state.lang][key] ?? key;
const number = v => new Intl.NumberFormat(state.lang, { maximumFractionDigits:0 }).format(v);
function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key.startsWith('on')) node.addEventListener(key.slice(2), value);
    else if (value !== null && value !== undefined) node.setAttribute(key, String(value));
  }
  for (const child of children.flat()) if (child !== null && child !== undefined) node.append(child instanceof Node ? child : document.createTextNode(String(child)));
  return node;
}
const svg = (tag, attrs = {}) => { const node = document.createElementNS('http://www.w3.org/2000/svg', tag); for (const [k,v] of Object.entries(attrs)) node.setAttribute(k, String(v)); return node; };
// Read-only UI bridge: onboarding observes existing verified records; it cannot edit them.
const onboarding = installOnboarding({
  language: () => state.lang,
  setLanguage: language => {
    if (!['es','en'].includes(language)) return;
    $('language').value = language;
    $('language').dispatchEvent(new Event('change', { bubbles:true }));
  },
  returnToCase: id => {
    if (!state.catalog?.cases.some(entry => entry.id === id)) return;
    $('case').value = id;
    $('case').dispatchEvent(new Event('change', { bubbles:true }));
  },
  snapshot: () => {
    const b = state.bundle, row = b?.rows?.get(state.selected);
    const source = document.querySelector('[data-source-file="report.json"]');
    const rect = source?.getBoundingClientRect(), dock = $('guide-panel');
    return {
      valid: Boolean(b?.report && !$('completed').hidden && !state.error),
      caseId: b?.manifest?.id || $('case').value,
      caseIds: state.catalog?.cases.map(entry => entry.id) || [],
      reportVersion: b?.report?.report_version, verdict:b?.report?.verdict,
      observed:b?.report?.policy.observed_value, threshold:b?.report?.policy.threshold,
      search:$('search').value, visibleKeys:[...document.querySelectorAll('[data-row-key]')].map(element => element.dataset.rowKey),
      selected:row ? { dependent_dataset:row.dependent_dataset, dependent_id:row.dependent_id, before:[...row.before], after:[...row.after] } : null,
      evidenceId:b?.regressionByRow?.get(state.selected)?.evidence_id || null,
      sourceIdentityVisible:Boolean(rect && rect.bottom > 0 && rect.top < (dock && !dock.hidden ? dock.getBoundingClientRect().top : innerHeight)),
      versionCount:$('versions').children.length
    };
  }
});
function localize() {
  document.documentElement.lang = state.lang;
  document.querySelectorAll('[data-i18n]').forEach(node => { node.textContent = t(node.dataset.i18n); });
  document.querySelectorAll('[data-i18n-aria]').forEach(node => node.setAttribute('aria-label', t(node.dataset.i18nAria)));
  if (state.catalog) for (const option of $('case').options) option.textContent = state.catalog.cases.find(c => c.id === option.value).title[state.lang];
  if (state.bundle?.report) render();
  else if (state.error) showProblem(state.error);
  else if (state.bundle) showAnalysisError();
  onboarding.languageChanged();
}
function download(role, label) {
  const entry = state.bundle.manifest.files[role];
  return el('a', { href:entry.path, download:entry.path.split('/').at(-1) }, label || t('download'));
}
function field(label, value, code = false) { return el('div', {class:'field'}, el('dt',{},label), el('dd',{}, code ? el('code',{},value) : value)); }
function showProblem(error) {
  $('completed').hidden = true; $('loading').hidden = true; $('problem').hidden = false;
  $('problem').replaceChildren(el('span',{class:'eyebrow'},t('loadError')),el('h2',{},t('unsupported')),el('p',{},t('loadMeaning')),el('p',{},el('code',{},`${error.code || 'LOAD_ERROR'} · ${error.file || 'catalog.json'}`)),el('button',{type:'button',onclick:() => state.catalog ? changeCase() : location.reload()},t('retry')));
  onboarding.update();
}
function showAnalysisError() {
  $('completed').hidden = true; $('loading').hidden = true; $('problem').hidden = false;
  $('problem').replaceChildren(el('span',{class:'eyebrow'},t('analysisError')),el('h2',{},t('noScientific')),el('p',{},t('analysisMeaning')),el('p',{},el('code',{},state.bundle.manifest.stderr)));
  onboarding.update();
}
async function changeCase() {
  const epoch = ++state.epoch;
  state.bundle = null; state.selected = null; state.primary = null; state.view = null; state.page = 0; state.error = null; state.returnKey = null;
  $('completed').hidden = true; $('problem').hidden = true; $('loading').hidden = false;
  onboarding.update();
  // Clear stale scientific content immediately, including elements hidden from view.
  for (const id of ['verdict','stats','base-map','candidate-map','relation-list','evidence-body','geometry-body','input-files','versions','sources','config-raw']) $(id).replaceChildren();
  $('search').value = ''; $('filter').value = 'all'; $('points-toggle').checked = true; $('polygons-toggle').checked = true;
  try {
    const loaded = await loadCase(state.catalog.cases.find(c => c.id === $('case').value));
    if (state.epoch !== epoch) return;
    state.bundle = loaded;
    if (!loaded.report) { showAnalysisError(); return; }
    const pairs = [...new Set(loaded.report.relationships.map(pairKey))];
    $('transition').replaceChildren(el('option',{value:''},t('all')), ...pairs.map(pair => { const [before,after] = JSON.parse(pair); return el('option',{value:pair},`${JSON.stringify(before)} → ${JSON.stringify(after)}`); }));
    state.view = fullExtent(); render(); $('loading').hidden = true; $('completed').hidden = false;
    $('live').textContent = `${loaded.manifest.title[state.lang]}. ${loaded.report.verdict}. ${loaded.report.relationships.length} ${t('assignments')}.`;
    onboarding.update();
  } catch (error) { if (state.epoch === epoch) { state.error = error; showProblem(error); } }
}
function stat(label, value, pointer) { return el('div',{class:'stat'},el('strong',{},number(value)),el('span',{},label),el('small',{},pointer)); }
function render() {
  const {report:r,manifest:m} = state.bundle;
  $('category').textContent = t('synthetic');
  $('editions').textContent = m.editions.join(' / '); $('inventory').textContent = m.inventory_date;
  $('identity-status').textContent = t('identityOK'); $('verdict').textContent = r.verdict;
  document.querySelector('.verdict-strip').classList.toggle('pass',r.verdict === 'PASS');
  $('verdict-meaning').textContent = t(r.verdict === 'PASS' ? 'passMeaning' : 'blockMeaning');
  $('stats').replaceChildren(stat(t('observed'),r.policy.observed_value,'/policy/observed_value'),stat(t('threshold'),r.policy.threshold,'/policy/threshold'),stat(t('assignments'),r.relationships.length,'/relationships · records'),stat(t('primaryChanged'),r.primary_change.modified_feature_ids.length,'/primary_change/modified_feature_ids'));
  const chosen = $('primary').value;
  $('primary').replaceChildren(el('option',{value:''},t('all')),...Object.entries(r.primary_change.feature_geometry_status).map(([id,status])=>el('option',{value:id},`${id} · ${t(status)}`)));
  $('primary').value = state.primary || chosen || '';
  $('transition').options[0].textContent = t('all');
  $('base-date').textContent = m.editions[0]; $('candidate-date').textContent = m.editions[1];
  $('map-credit').textContent = m.attribution;
  renderMaps(); renderList(); renderEvidence(); renderGeometry(); renderProvenance();
}
function filteredRows() {
  const query = $('search').value.trim().toLowerCase(), filter = $('filter').value, pair = $('transition').value;
  return state.bundle.report.relationships.filter(row => (!query || `${row.dependent_dataset} ${row.dependent_id}`.toLowerCase().includes(query)) && (filter === 'all' || (filter === 'regressions' ? row.change_type !== 'unchanged' : row.change_type === 'unchanged')) && (!pair || pairKey(row) === pair));
}
function renderList() {
  const rows = filteredRows(), pages = Math.max(1,Math.ceil(rows.length / 8)); state.page = Math.min(state.page,pages-1);
  $('row-count').textContent = `${rows.length} ${t('visible')} / ${state.bundle.rows.size} ${t('total')}`;
  $('relation-list').replaceChildren(...rows.slice(state.page*8,state.page*8+8).map(row => el('li',{},el('button', {type:'button',class:'row', 'data-row-key':rowKey(row),'data-dependent-dataset':row.dependent_dataset,'data-dependent-id':row.dependent_id,'aria-pressed':state.selected === rowKey(row),onclick:() => selectRow(rowKey(row),true)},
    el('span',{},el('strong',{},row.dependent_id),el('small',{},row.dependent_dataset)), el('span',{class:'transition-code'},`${JSON.stringify(row.before)} → ${JSON.stringify(row.after)}`),el('span',{class:`state-pill ${row.change_type}`},t(row.change_type))))));
  $('page-label').textContent = `${t('page')} ${state.page+1} ${t('of')} ${pages}`;
  $('previous').disabled = state.page === 0; $('next').disabled = state.page+1 >= pages;
  $('empty').hidden = rows.length !== 0;
  if (!rows.length) $('empty').replaceChildren(el('strong',{},t('noMatches')),state.bundle.report.policy.observed_value === 0 ? el('p',{},`${t('zero')} ${state.bundle.rows.size} ${t('reviewed')}`) : el('p',{},`${state.bundle.rows.size} ${t('total')}.`));
}
function selectRow(key, restore = false) {
  state.selected = key; state.primary = null; state.returnKey = key;
  $('primary').value = ''; $('fit-selection').disabled = false;
  renderList(); renderMaps(); renderEvidence(); renderGeometry();
  $('live').textContent = `${t('selected')}: ${state.bundle.rows.get(key).dependent_id}`;
  if (restore) [...document.querySelectorAll('[data-row-key]')].find(node => node.dataset.rowKey === key)?.focus({preventScroll:true});
  onboarding.update();
}
function renderEvidence() {
  const body = $('evidence-body'), key = state.selected;
  $('clear-selection').disabled = !key && !state.primary;
  $('fit-selection').disabled = !key && !state.primary;
  $('selection-summary').hidden = !key;
  if (key) $('selection-summary').replaceChildren(el('a',{href:'#evidence'},`${t('selected')}: ${state.bundle.rows.get(key).dependent_id} · ${t('evidence')} ↓`));
  if (!key) { body.replaceChildren(el('p',{class:'selection-empty'},el('span',{class:'selection-glyph','aria-hidden':'true'},'◎'),t('selectHint'))); return; }
  const b = state.bundle,row = b.rows.get(key),reg = b.regressionByRow.get(key),boundary = b.boundaries.get(key);
  body.replaceChildren(el('h3',{class:'selected-id'},row.dependent_id),el('p',{class:'selected-dataset'},row.dependent_dataset),el('span',{class:`state-pill ${row.change_type}`},t(row.change_type)),
    el('div',{class:'assignment'},el('span',{},t('before')),el('code',{},JSON.stringify(row.before)),row.before.length ? null : el('small',{},t('noWithin'))),
    el('div',{class:'assignment after'},el('span',{},t('after')),el('code',{},JSON.stringify(row.after)),row.after.length ? null : el('small',{},t('noWithin'))),
    el('dl',{class:'field-list'},field('predicate',row.predicate),field('change_type',row.change_type),field('evidence_id',reg?.evidence_id || t('noEvidence'),true),field('boundary_ambiguities',boundary ? JSON.stringify(boundary) : t('boundaryNone'),true),field('JSON pointer',`/relationships/${b.rowIndices.get(key)}`,true)),
    download('report.json',t('openRecord')));
  body.lastElementChild.classList.add('record-link');
}
function renderGeometry() {
  const pc = state.bundle.report.primary_change, body = $('geometry-body');
  const selected = state.primary ? [[state.primary,pc.feature_geometry_status[state.primary]]] : state.selected ? [...new Set([...state.bundle.rows.get(state.selected).before,...state.bundle.rows.get(state.selected).after])].map(id=>[id,pc.feature_geometry_status[id]]) : Object.entries(pc.feature_geometry_status);
  body.replaceChildren(el('p',{},t('unchangedGeometry')),el('div',{class:'geometry-statuses'},selected.map(([id,status])=>el('span',{},`${id} · ${t(status)}`))),
    el('dl',{class:'field-list'},field('changed_footprint_area_m2',`${pc.changed_footprint_area_m2} m²`,true),field('max_boundary_displacement_m',`${pc.max_boundary_displacement_m} m · modified shared IDs only`,true)),el('p',{},t('footprint')));
}
function renderProvenance() {
  const b = state.bundle;
  $('versions').replaceChildren(...Object.entries(b.report.provenance.engine).map(([name,version])=>el('div',{class:'version'},el('small',{},name),version)));
  $('input-files').replaceChildren(...Object.entries(b.manifest.files).map(([role,entry])=>el('div',{class:'file-row','data-source-file':role,...(role === 'report.json' ? {'data-tour-target':'report-file'} : {})},el('strong',{},role),el('div',{},el('code',{},entry.sha256),el('small',{},`${entry.size_bytes} ${t('bytes')} · SHA-256 · ${t('verified')}`)),download(role))));
  $('config-raw').textContent = new TextDecoder().decode(b.bytes.get('config'));
  $('sources').replaceChildren(el('p',{class:'credit'},b.manifest.attribution),el('ul',{},b.manifest.sources.map(source=>
    el('li',{},el('span',{},source.title),el('small',{},source.terms))
  )));
  $('limitations').textContent = b.manifest.limitations[state.lang];
}
function allCoordinates(geometry) {
  if (geometry.type === 'Point') return [geometry.coordinates];
  return geometry.type === 'Polygon' ? geometry.coordinates.flat() : geometry.coordinates.flat(2);
}
// View framing only: affine CRS84 lon/lat coordinates, y inverted for SVG.
// No projected report geometry, distances, areas or point-in-polygon operations.
function extent(coordinates) {
  const xs=coordinates.map(p=>p[0]),ys=coordinates.map(p=>-p[1]);
  const x=Math.min(...xs),y=Math.min(...ys),w=Math.max(...xs)-x,h=Math.max(...ys)-y;
  const span=Math.max(w,h,0.00001),pad=span*.18;
  return {x:x-pad,y:y-pad,w:w+pad*2,h:h+pad*2};
}
function fullExtent() {
  const b=state.bundle;
  return extent([...b.base.values(),...b.candidate.values(),...b.allPoints.values()].flatMap(f=>allCoordinates(f.geometry)));
}
function pathFor(g) {
  const polygons=g.type==='Polygon'?[g.coordinates]:g.coordinates;
  return polygons.map(p=>p.map(r=>r.map((c,i)=>`${i?'L':'M'}${c[0]},${-c[1]}`).join(' ')+'Z').join(' ')).join(' ');
}
function renderMaps() {
  for (const snapshot of ['base','candidate']) {
    const map=$(snapshot+'-map'),b=state.bundle,v=state.view;
    map.replaceChildren();map.classList.toggle('candidate',snapshot==='candidate');map.setAttribute('viewBox',`${v.x} ${v.y} ${v.w} ${v.h}`);
    map.setAttribute('aria-label',`${snapshot.toUpperCase()} · ${t('originalGeometry')} · ${b.allPoints.size} ${t('points')}`);
    const row=b.rows.get(state.selected),chosen=new Set(state.primary?[state.primary]:row?(snapshot==='base'?row.before:row.after):[]);
    if ($('polygons-toggle').checked) for (const [id,f] of b[snapshot]) {
      const path=svg('path',{d:pathFor(f.geometry),class:`${b.report.primary_change.feature_geometry_status[id]} ${chosen.has(id)?'selected':''}`,'data-primary-id':id});
      const title=svg('title');title.textContent=`${id} · ${b.report.primary_change.feature_geometry_status[id]}`;path.append(title);
      path.addEventListener('click',()=>{state.primary=id;state.selected=null;$('primary').value=id;renderMaps();renderEvidence();renderGeometry();renderList();});map.append(path);
    }
    const radius=Math.max(v.w,v.h)/105;
    if ($('points-toggle').checked) for (const [key,f] of b.allPoints) {
      const row=b.rows.get(key),reg=b.regressionByRow.has(key),boundary=b.boundaries.has(key),[x,lat]=f.geometry.coordinates,y=-lat;
      const attrs={class:`point ${reg?'changed':''} ${boundary?'boundary':''} ${state.selected===key?'selected':''}`,'data-point-key':key};
      const point=reg?svg('path',{...attrs,d:`M${x},${y-radius*1.4}l${radius*1.4},${radius*1.4}l${-radius*1.4},${radius*1.4}l${-radius*1.4},${-radius*1.4}Z`}):boundary?svg('rect',{...attrs,x:x-radius,y:y-radius,width:radius*2,height:radius*2}):svg('circle',{...attrs,cx:x,cy:y,r:state.selected===key?radius*1.3:radius});
      const title=svg('title');title.textContent=`${row.dependent_id} · ${row.change_type}`;point.append(title);point.addEventListener('click',e=>{e.stopPropagation();selectRow(key);});map.append(point);
    }
    $(snapshot+'-frame').classList.toggle('mobile-hidden',state.snapshot!==snapshot);
  }
}
function zoom(factor) {
  if (!state.bundle?.report) return;
  const v=state.view;state.view={x:v.x+(v.w-v.w*factor)/2,y:v.y+(v.h-v.h*factor)/2,w:v.w*factor,h:v.h*factor};renderMaps();
}
function pan(dx,dy) { if (!state.bundle?.report) return;state.view={...state.view,x:state.view.x+state.view.w*dx,y:state.view.y+state.view.h*dy};renderMaps(); }
function fitSelection() {
  const b=state.bundle;
  if (state.primary) state.view=extent([b.base.get(state.primary),b.candidate.get(state.primary)].filter(Boolean).flatMap(f=>allCoordinates(f.geometry)));
  else if (state.selected) { const p=b.allPoints.get(state.selected).geometry.coordinates,full=fullExtent();state.view={x:p[0]-full.w/7,y:-p[1]-full.h/7,w:full.w/3.5,h:full.h/3.5}; }
  renderMaps();
}
$('language').addEventListener('change',()=>{state.lang=$('language').value;localize();});
$('case').addEventListener('change',changeCase);
for (const id of ['search','filter','transition']) $(id).addEventListener(id==='search'?'input':'change',()=>{state.page=0;renderList();});
$('previous').addEventListener('click',()=>{state.page--;renderList();});$('next').addEventListener('click',()=>{state.page++;renderList();});
$('zoom-in').addEventListener('click',()=>zoom(.75));$('zoom-out').addEventListener('click',()=>zoom(1.333333));
$('fit-all').addEventListener('click',()=>{state.view=fullExtent();renderMaps();});$('fit-selection').addEventListener('click',fitSelection);
for (const [label,dx,dy,icon] of [['panLeft',-.15,0,'←'],['panRight',.15,0,'→'],['panUp',0,-.15,'↑'],['panDown',0,.15,'↓']]) document.querySelector('.button-group').append(el('button',{type:'button','data-i18n-aria':label,'aria-label':t(label),onclick:()=>pan(dx,dy)},icon));
for (const id of ['points-toggle','polygons-toggle']) $(id).addEventListener('change',renderMaps);
$('primary').addEventListener('change',()=>{state.primary=$('primary').value||null;state.selected=null;renderList();renderMaps();renderEvidence();renderGeometry();});
for (const snapshot of ['base','candidate']) {
  $(snapshot+'-tab').addEventListener('click',()=>{state.snapshot=snapshot;for(const s of ['base','candidate']) $(s+'-tab').setAttribute('aria-pressed',String(s===snapshot));renderMaps();});
  const map=$(snapshot+'-map');let pointer=null;
  map.addEventListener('keydown',event=>{
    const keys={ArrowLeft:[-.1,0],ArrowRight:[.1,0],ArrowUp:[0,-.1],ArrowDown:[0,.1]};
    if(keys[event.key]){event.preventDefault();pan(...keys[event.key]);}
    else if(['+','=','-'].includes(event.key)){event.preventDefault();zoom(event.key==='-'?1.333333:.75);}
  });
  map.addEventListener('pointerdown',e=>{if(e.target===map&&e.pointerType==='mouse'&&e.button===0){pointer={x:e.clientX,y:e.clientY,view:{...state.view}};map.setPointerCapture(e.pointerId);}});
  map.addEventListener('pointermove',e=>{if(!pointer)return;const rect=map.getBoundingClientRect(),scale=Math.min(rect.width/pointer.view.w,rect.height/pointer.view.h);state.view={...pointer.view,x:pointer.view.x-(e.clientX-pointer.x)/scale,y:pointer.view.y-(e.clientY-pointer.y)/scale};renderMaps();});
  map.addEventListener('pointerup',()=>{pointer=null;});map.addEventListener('pointercancel',()=>{pointer=null;});
}
function clearSelection(restore=false) {
  state.selected=null;state.primary=null;$('primary').value='';renderList();renderMaps();renderEvidence();renderGeometry();
  if(restore) ([...document.querySelectorAll('[data-row-key]')].find(n=>n.dataset.rowKey===state.returnKey)||$('search')).focus({preventScroll:true});
}
$('clear-selection').addEventListener('click',()=>clearSelection(true));
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&state.bundle?.report&&(state.selected||state.primary)){e.preventDefault();clearSelection(true);}});
localize();
try {
  state.catalog=await loadCatalog(catalogHash);
  $('case').replaceChildren(...state.catalog.cases.map(c=>el('option',{value:c.id},c.title[state.lang])));$('case').disabled=false;
  await changeCase();
} catch(error) { state.error=error;showProblem(error); }
