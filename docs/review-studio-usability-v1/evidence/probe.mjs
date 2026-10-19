/* Engineering inspection of the pinned UI. This does not simulate participants.
   Only browser-local fault responses/CSS are changed, never retained files. */
import { chromium } from '../../../experiments/review-studio-local/node_modules/playwright/index.mjs';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const reference='32f3ab50bb8a91d21118610bfc135b33e3fb2f3c';
const root=fileURLToPath(new URL('../../../',import.meta.url));
const out=fileURLToPath(new URL('./',import.meta.url)), shots=path.join(out,'screenshots');
const base=new URL(process.env.STUDIO_URL || 'http://127.0.0.1:8765');
assert(['localhost','127.0.0.1'].includes(base.hostname),'Only a local server is allowed');
const key='geoimpact:review-studio:onboarding:v1', observations=[], external=[], uncaught=[], ordinaryConsole=[];
const digest=bytes=>createHash('sha256').update(bytes).digest('hex');
const sourceNames=['index.html','app.js','reader.js','style.css','onboarding.js','onboarding-copy.js','onboarding.css'];
await mkdir(shots,{recursive:true});
const sources={};
for(const name of sourceNames) {
  const pinned=execFileSync('git',['show',`${reference}:experiments/review-studio-local/web/${name}`],{cwd:root});
  const served=Buffer.from(await (await fetch(new URL(name,base))).arrayBuffer());
  assert.equal(digest(served),digest(pinned),`Server differs from reference: ${name}`); sources[name]=digest(served);
}
const catalog=await (await fetch(new URL('catalog.json',base))).json();
assert(catalog.cases.every(c=>['synthetic-block','synthetic-pass','synthetic-error','sierra-local'].includes(c.id)));
const manifests=new Map();
async function inventory() {
  const hashes={};
  for(const c of catalog.cases) {
    const raw=Buffer.from(await (await fetch(new URL(c.path,base))).arrayBuffer());
    assert.equal(digest(raw),c.sha256);hashes[c.path]=digest(raw);
    const m=JSON.parse(raw); manifests.set(c.id,m);
    for(const f of Object.values(m.files || {})) {
      const bytes=Buffer.from(await (await fetch(new URL(f.path,base))).arrayBuffer());
      assert.equal(digest(bytes),f.sha256);hashes[f.path]=digest(bytes);
    }
  }
  return hashes;
}
const before=await inventory();
const browser=await chromium.launch({headless:true,...(process.env.STUDIO_CHROMIUM_EXECUTABLE?{executablePath:process.env.STUDIO_CHROMIUM_EXECUTABLE}:{})});
const record=(id,result,detail)=>{observations.push({id,result,...detail});console.log(id,result);};
async function open(viewport,{fresh=false,fault=null}={}) {
  const context=await browser.newContext({viewport,reducedMotion:'reduce'});
  if(!fresh)await context.addInitScript(k=>localStorage.setItem(k,'{"status":"dismissed"}'),key);
  await context.route('**/*',async route=>{
    const u=new URL(route.request().url());
    if(u.origin!==base.origin){external.push(u.origin);await route.abort();return;}
    if(fault && u.pathname.endsWith('/data/synthetic-block/report.json')) {
      if(fault==='missing')await route.fulfill({status:404,body:''});
      else {const response=await route.fetch();await route.fulfill({response,body:(await response.text())+' '});}
      return;
    }
    await route.continue();
  });
  const page=await context.newPage();page.on('pageerror',e=>uncaught.push(e.message));
  page.on('console',m=>{if(m.type()==='error'&&!fault)ordinaryConsole.push(m.text());});
  await page.goto(base.href);await page.locator('#completed:not([hidden]),#problem:not([hidden])').waitFor();
  return {page,context};
}
const ready=page=>page.locator('#completed:not([hidden])').waitFor();
async function choose(page,id){await page.locator('#case').selectOption(id);await page.locator('#completed:not([hidden]),#problem:not([hidden])').waitFor();}
async function help(page){await page.locator('#help-button').click();await page.locator('#onboarding-dialog[open][data-page=help]').waitFor();}
const action=(page,name)=>page.locator(`[data-guide-action="${name}"]`).click();
async function shot(page,name) {
  assert((await page.locator('#case').inputValue()).startsWith('synthetic-'),'Only synthetic captures may be retained');
  await page.screenshot({path:path.join(shots,name)});
}
const overflow=page=>page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,overflow:document.documentElement.scrollWidth>innerWidth+1}));
async function focusState(page) {
  return page.evaluate(()=>{
    const n=document.activeElement,r=n.getBoundingClientRect(),dock=document.getElementById('guide-panel'),d=dock.getBoundingClientRect();
    const inside=Boolean(n.closest('#guide-panel'));
    const fullyCovered=!dock.hidden&&!inside&&r.width>0&&r.height>0&&r.left>=d.left&&r.right<=d.right&&r.top>=d.top&&r.bottom<=d.bottom;
    const hit=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
    return {id:n.id||n.dataset.i18nAria||n.tagName,text:n.textContent.trim().slice(0,70),rect:{x:r.x,y:r.y,width:r.width,height:r.height},dock:{x:d.x,y:d.y,width:d.width,height:d.height},fullyCovered,hitGuide:Boolean(hit?.closest('#guide-panel')),focusVisible:n.matches(':focus-visible'),outline:getComputedStyle(n).outline};
  });
}
async function colors(page) {
  return page.evaluate(()=>{
    const rgb=s=>s.match(/[\d.]+/g).map(Number),lum=values=>values.slice(0,3).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((sum,v,i)=>sum+v*[.2126,.7152,.0722][i],0);
    const background=n=>{for(let a=n;a;a=a.parentElement){const c=getComputedStyle(a).backgroundColor;if(rgb(c)[3]!==0)return c;}return 'rgb(255, 255, 255)';};
    return ['body','.intro-copy','.scope-note','#verdict-meaning','.stat small','.row small','.row .transition-code','.assignment span','.field dd','.provenance-note','.file-row code','#help-button','.guide-panel-body p','.onboarding-primary','.onboarding-notice'].flatMap(selector=>{
      const n=document.querySelector(selector);if(!n||!n.getClientRects().length||n.closest('[hidden]'))return [];
      const s=getComputedStyle(n),bg=background(n),a=lum(rgb(s.color)),b=lum(rgb(bg));
      return [{selector,foreground:s.color,background:bg,fontSize:s.fontSize,fontWeight:s.fontWeight,ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05),note:'Opaque CSS token pair only; not every state, pixel or SVG boundary.'}];
    });
  });
}
try {
  for(const [width,height] of [[1440,900],[1440,1000],[834,1112],[390,844],[375,812],[320,812]]) {
    const {page,context}=await open({width,height},{fresh:true});
    await page.locator('#onboarding-dialog[open][data-page=welcome]').waitFor();
    const modalFocus=[];for(let i=0;i<16;i++){await page.keyboard.press(i<8?'Tab':'Shift+Tab');modalFocus.push(await page.evaluate(()=>Boolean(document.activeElement.closest('#onboarding-dialog'))));}
    assert(modalFocus.every(Boolean));assert(!(await overflow(page)).overflow);
    if(width===1440&&height===900)await shot(page,'welcome-desktop.png');
    await page.keyboard.press('Escape');assert.equal(await page.locator('#help-button').evaluate(n=>n===document.activeElement),true);
    await page.locator('#search').fill('hotel_813');await page.locator('.row').focus();await page.keyboard.press('Enter');
    const evidence=await page.locator('#evidence-body').innerText();assert(evidence.includes('["chamberi"]')&&evidence.includes('["tetuan"]'));
    const selectionLink=await page.locator('#selection-summary a').textContent();
    if(width===390){await page.locator('#evidence').scrollIntoViewIfNeeded();await shot(page,'evidence-mobile.png');}
    await page.locator('#filter').selectOption('unchanged');
    const retained={visibleRows:await page.locator('.row').count(),selectedId:await page.locator('#evidence-body h3').textContent(),selectedSummary:await page.locator('#selection-summary').textContent(),rowCount:await page.locator('#row-count').textContent()};
    assert.equal(retained.visibleRows,0);assert.equal(retained.selectedId,'hotel_813');
    if(width===1440&&height===900){await page.locator('#relationships').scrollIntoViewIfNeeded();await shot(page,'selection-outside-filter.png');}
    await page.locator('#filter').selectOption('all');await page.locator('#search').fill('');
    const initial=await page.locator('#base-map').getAttribute('viewBox');
    await page.locator('#zoom-in').click();assert.notEqual(await page.locator('#base-map').getAttribute('viewBox'),initial);
    await page.locator('#fit-all').click();assert.equal(await page.locator('#base-map').getAttribute('viewBox'),initial);
    await page.locator('#base-map').focus();await page.keyboard.press('ArrowRight');
    const panned=await page.locator('#base-map').getAttribute('viewBox');assert.notEqual(panned,initial);assert.equal(panned,await page.locator('#candidate-map').getAttribute('viewBox'));
    await page.keyboard.press('Tab');assert.equal(await page.locator('#base-map').evaluate(n=>n===document.activeElement),false);
    if(width<=700){await page.locator('#candidate-tab').click();assert.equal(await page.locator('#candidate-tab').getAttribute('aria-pressed'),'true');assert.equal(await page.locator('#base-frame').isVisible(),false);await page.locator('#base-tab').click();}
    await page.keyboard.press('Escape');await page.locator('#fit-all').click();
    const tokenColors=await colors(page);
    const semantics={maps:await page.locator('#review').ariaSnapshot(),relationships:await page.locator('#relationships').ariaSnapshot(),landmarks:await page.evaluate(()=>({main:document.querySelectorAll('main').length,h1:document.querySelectorAll('h1').length,lang:document.documentElement.lang}))};
    await help(page);const helpAX=await page.locator('#onboarding-dialog').ariaSnapshot();assert(helpAX.includes('Ayuda y aprendizaje'));
    if(width===390)await shot(page,'help-mobile.png');
    await page.locator('[data-help-action=tour]').click();
    const focusTrace=[];let captured=false;
    for(let i=0;i<50;i++){
      await page.keyboard.press('Tab');const f=await focusState(page);focusTrace.push(f);
      if(f.fullyCovered&&f.hitGuide&&!captured&&[1440,834,390].includes(width)){
        await shot(page,`covered-focus-${width}.png`);captured=true;
      }
    }
    const coveredFocus=focusTrace.some(f=>f.fullyCovered&&f.hitGuide);
    await page.keyboard.press('Escape');await help(page);await page.locator('[data-help-action=tour]').click();
    for(let step=1;step<=8;step++) {
      assert.equal(await page.locator('#guide-panel').getAttribute('data-step'),String(step));
      await page.locator('#guide-language').selectOption('en');assert.equal(await page.locator('#guide-panel').getAttribute('data-step'),String(step));
      await page.locator('#guide-language').selectOption('es');
      if(step===4&&[1440,834,390].includes(width)){await shot(page,`tour-maps-${width}.png`);tokenColors.push(...await colors(page));}
      assert(!(await overflow(page)).overflow);await action(page,'next');
    }
    assert.equal(await page.locator('#guide-panel').isVisible(),false);
    record(`viewport-${width}x${height}`,coveredFocus?'VERIFIED_WITH_FINDING':'VERIFIED',{viewport:{width,height},modalFocusContained:true,modalEscapeRestoredHelp:true,mapKeyboardAndCamera:true,mapZoomAndFit:true,semantics,selectionLink,retainedSelectionOutsideFilter:retained,overflow:await overflow(page),focusTrace,contrastSamples:tokenColors,helpAccessibleSnapshot:helpAX});
    await context.close();
  }
  {
    const {page,context}=await open({width:1440,height:900});await help(page);await page.locator('[data-help-action=practice]').click();await page.locator('[data-onboarding-action=practice-start]').click();
    await action(page,'next');await page.locator('#search').fill('hotel_813');await action(page,'next');await page.locator('.row').click();await action(page,'next');
    await page.locator('#policy-summary').scrollIntoViewIfNeeded();await page.locator('input[value=policy]').check();await action(page,'next');
    assert.equal(await page.locator('#guide-panel').getAttribute('data-step'),'4');assert((await page.locator('[data-guide-feedback]').textContent()).includes('aún no'));
    await shot(page,'practice-explicit-action-gate.png');
    await action(page,'target');await action(page,'next');assert.equal(await page.locator('#guide-panel').getAttribute('data-step'),'5');
    await action(page,'target');await action(page,'next');await page.locator('#onboarding-dialog[data-page=practice-done][open]').waitFor();
    record('practice-action-gate','VERIFIED_WITH_FINDING',{correctAnswerAndScrollAloneAdvance:false,helperVisitThenAdvance:true,realEvidenceAndSourceComplete:true,interpretation:'A specific instrumented visit is required; no human comprehension conclusion follows.'});await context.close();
  }
  {
    const {page,context}=await open({width:1440,height:900});
    await page.locator('#provenance details summary').click();
    const manifest=manifests.get('synthetic-block');
    assert.equal(await page.locator('#versions .version').count(),5);
    assert.equal(await page.locator('#input-files .file-row').count(),Object.keys(manifest.files).length);
    assert.equal(digest(await page.locator('#config-raw').textContent()),manifest.files.config.sha256);
    const [download]=await Promise.all([page.waitForEvent('download'),page.locator('[data-source-file="report.json"] a').click()]);
    const reportHash=digest(await readFile(await download.path()));assert.equal(reportHash,manifest.files['report.json'].sha256);
    assert((await page.locator('#interpretation-limits').innerText()).includes('no acredita efectos reales'));
    await page.locator('#provenance').scrollIntoViewIfNeeded();await shot(page,'provenance-desktop.png');
    record('provenance-source-download','VERIFIED',{versions:5,originalFileRows:Object.keys(manifest.files).length,originalConfigHashMatches:true,downloadedReportSha256:reportHash,limitsPresent:true});await context.close();
  }
  {
    const {page,context}=await open({width:1440,height:900});await choose(page,'synthetic-pass');await ready(page);
    assert.equal(await page.locator('#verdict').textContent(),'PASS');assert.deepEqual(await page.locator('#stats .stat strong').allTextContents(),['2','2','3','2']);
    await choose(page,'synthetic-error');assert.equal(await page.locator('#completed').isVisible(),false);assert.equal(await page.locator('#verdict').textContent(),'');assert.equal(await page.locator('#base-map .point').count(),0);
    await shot(page,'analysis-error.png');await help(page);assert(await page.locator('[data-help-action=tour]').isDisabled());await page.locator('[data-help-action=glossary]').click();
    record('pass-and-analysis-error','VERIFIED',{passHasTwoRegressions:true,analysisErrorClearsScientificView:true,safeHelp:true});await context.close();
  }
  for(const fault of ['missing','byte-change']) {
    const {page,context}=await open({width:390,height:844},{fresh:true,fault});
    assert.equal(await page.locator('#completed').isVisible(),false);assert.equal(await page.locator('#verdict').textContent(),'');assert.equal(await page.locator('#onboarding-dialog[open]').count(),0);
    const problem=await page.locator('#problem').innerText();assert(problem.includes(fault==='missing'?'MISSING':'HASH_MISMATCH'));
    if(fault==='byte-change')await shot(page,'integrity-error-mobile.png');await help(page);assert(await page.locator('[data-help-action=practice]').isDisabled());
    record(`load-${fault}`,'VERIFIED',{normalViewHidden:true,noScientificVerdict:true,noWelcomeInterruption:true,safeHelp:true,problem});await context.close();
  }
  {
    const {page,context}=await open({width:1440,height:1000});
    await page.evaluate(()=>{document.documentElement.style.zoom='2';dispatchEvent(new Event('resize'));});
    const zoomed=await overflow(page);assert(!zoomed.overflow);await help(page);await page.locator('[data-help-action=tour]').click();await action(page,'next');assert(!(await overflow(page)).overflow);
    record('reflow-zoom','VERIFIED',{method:'200% CSS zoom at 1440x1000 plus 320px viewport; not browser-chrome zoom',normal:zoomed,reducedMotion:await page.evaluate(()=>matchMedia('(prefers-reduced-motion: reduce)').matches)});await context.close();
  }
  if(process.env.STUDIO_AUDIT_SIERRA==='1'&&catalog.cases.some(c=>c.id==='sierra-local')) {
    const {page,context}=await open({width:1440,height:900});await choose(page,'sierra-local');await ready(page);
    assert.equal(await page.locator('#verdict').textContent(),'PASS');assert.equal(await page.locator('#base-map .point').count(),52);
    await page.locator('#filter').selectOption('regressions');assert.equal(await page.locator('.row').count(),0);assert.equal(await page.locator('#base-map .point').count(),52);
    await page.locator('#filter').selectOption('all');await page.locator('.row').first().click();assert((await page.locator('#evidence-body').innerText()).includes('Sin ID de evidencia de regresión'));
    record('sierra-local-zero','VERIFIED',{relationships:52,regressions:0,originalPointsRemain:true,noInventedRegressionId:true,screenshotsRetained:false,rights:'Retained local preparation/attribution only; no new legal clearance.'});await context.close();
  } else record('sierra-local-zero','NOT_EVALUATED',{reason:'Optional local case not requested/prepared'});
  assert.deepEqual(await inventory(),before);assert.equal(external.length,0);assert.equal(uncaught.length,0);assert.equal(ordinaryConsole.length,0);
} catch(error) {
  record('probe-execution','FAILED',{message:error.message});process.exitCode=1;
} finally {
  const report={reference_commit:reference,executed_at_utc:new Date().toISOString(),command:'node docs/review-studio-usability-v1/evidence/probe.mjs',browser:browser.version(),playwright:'1.56.1',node:process.version,platform:process.platform,source_sha256:sources,script_sha256:digest(await readFile(fileURLToPath(import.meta.url))),independence:'Separate engineering audit by the same assistant that implemented onboarding; not an external human review.',participants_recruited:0,human_sessions:0,physical_device_testing:false,screen_reader_testing:false,observations,external_requests:external,uncaught_errors:uncaught,ordinary_console_errors:ordinaryConsole,scientific_bytes_unchanged:JSON.stringify(await inventory())===JSON.stringify(before),retained_bytes_sha256:before};
  await writeFile(path.join(out,'technical.json'),JSON.stringify(report,null,2)+'\n');await browser.close();
}
