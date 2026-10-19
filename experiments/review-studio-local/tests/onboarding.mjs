/* Actual Chromium onboarding acceptance. Synthetic screenshots only.
   Viewport/CSS-zoom emulation is not physical-device or comprehension evidence. */
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { readFile, writeFile, mkdir, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { ONBOARDING_KEY as KEY } from '../web/onboarding.js';
import { copy } from '../web/onboarding-copy.js';

const root=fileURLToPath(new URL('../',import.meta.url)), web=path.join(root,'web');
const url=process.env.STUDIO_URL || 'http://127.0.0.1:8765';
assert(['127.0.0.1','localhost'].includes(new URL(url).hostname));
const local=path.join(root,'qa/local'),shots=path.join(root,'qa/screenshots/onboarding');
await mkdir(local,{recursive:true});await mkdir(shots,{recursive:true});
const browser=await chromium.launch({headless:true,...(process.env.STUDIO_CHROMIUM_EXECUTABLE?{executablePath:process.env.STUDIO_CHROMIUM_EXECUTABLE}:{})});
const records=[],external=[],errors=[],consoleErrors=[];
const originalCatalog=JSON.parse(await readFile(path.join(web,'catalog.json'),'utf8'));
const hasSierra=originalCatalog.cases.some(c=>c.id==='sierra-local');
const hash=raw=>createHash('sha256').update(raw).digest('hex');
async function scientificBytes() {
  const result={};
  for(const c of originalCatalog.cases) {
    const manifest=JSON.parse(await readFile(path.join(web,c.path),'utf8'));
    for(const [role,file] of Object.entries(manifest.files || {}))result[`${c.id}/${role}`]=hash(await readFile(path.join(web,file.path)));
  }
  return result;
}
const before=await scientificBytes();
async function open({viewport={width:1440,height:1000},dismissed=false,storageState,route:override,blockedStorage=false}={}) {
  const context=await browser.newContext({viewport,reducedMotion:'reduce',...(storageState?{storageState}:{})});
  if(dismissed)await context.addInitScript(key=>localStorage.setItem(key,JSON.stringify({status:'dismissed'})),KEY);
  if(blockedStorage)await context.addInitScript(()=>{Storage.prototype.getItem=()=>{throw new Error('storage disabled');};Storage.prototype.setItem=()=>{throw new Error('storage disabled');};});
  await context.route('**/*',async route=>{
    if(new URL(route.request().url()).origin!==new URL(url).origin){external.push(route.request().url());await route.abort();return;}
    if(override && await override(route))return;
    await route.continue();
  });
  const page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  page.on('console',m=>{if(m.type()==='error'&&!override)consoleErrors.push(m.text());});
  await page.goto(url,{waitUntil:'commit'});
  return {page,context};
}
const check=async(name,fn)=>{try{const detail=await fn();records.push({name,status:'PASS',...detail});console.log('PASS',name);}catch(e){records.push({name,status:'FAIL',message:e.message});throw e;}};
async function ready(page) {
  try { await page.waitForSelector('#completed:not([hidden])'); }
  catch(error) {
    const observed=await page.evaluate(()=>({loading:!document.getElementById('loading').hidden,problem:document.getElementById('problem').innerText}));
    throw new Error(`Case did not become ready: ${JSON.stringify(observed)}`,{cause:error});
  }
}
const welcome=page=>page.waitForSelector('#onboarding-dialog[open][data-page=welcome]');
const panel=page=>page.locator('#guide-panel');
async function step(page,n){await page.waitForSelector(`#guide-panel:not([hidden])[data-step="${n}"]`);}
async function help(page){await page.locator('#help-button').click();await page.waitForSelector('#onboarding-dialog[open][data-page=help]');}
async function action(page,name){await page.locator(`[data-guide-action="${name}"]`).click();}
async function selectCase(page,id){await page.locator('#case').selectOption(id);await page.waitForSelector('#completed:not([hidden]),#problem:not([hidden])');}
async function bounded(page,selector) {
  const rect=await page.locator(selector).boundingBox();assert(rect,`Missing visible ${selector}`);
  const size=page.viewportSize();assert(rect.x>=-1&&rect.y>=-1&&rect.x+rect.width<=size.width+1&&rect.y+rect.height<=size.height+1,`Offscreen ${selector}: ${JSON.stringify(rect)}`);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Horizontal page overflow');
}
async function connected(page,expected) {
  assert.equal(await panel(page).getAttribute('data-connected-target'),expected);
  await bounded(page,'#guide-panel');
  const target=await page.locator('.guide-highlight').boundingBox(),dock=await panel(page).boundingBox();
  assert(target&&target.y>=-1&&target.y+target.height<=dock.y-5,`Target obscured: ${expected} ${JSON.stringify({target,dock})}`);
}
async function persisted(page){return page.evaluate(key=>localStorage.getItem(key),KEY);}
try {
  await check('Welcome waits for verified ready, is opt-in, and Not now postpones only this session',async()=>{
    let release;const hold=new Promise(resolve=>{release=resolve;});
    const {page,context}=await open({route:async route=>{if(route.request().url().endsWith('/data/synthetic-block/report.json')){await hold;return false;}return false;}});
    await page.waitForSelector('#loading:not([hidden])');assert.equal(await page.locator('#onboarding-dialog[open]').count(),0);
    release();await welcome(page);await ready(page);
    assert.equal(await panel(page).isVisible(),false);
    assert((await page.locator('#onboarding-dialog').innerText()).includes(copy.es.caution));
    assert.equal(await page.locator('#onboarding-title').evaluate(n=>n===document.activeElement),true);
    await page.locator('[data-onboarding-action=later]').click();assert.equal(await persisted(page),null);
    await page.reload();await ready(page);assert.equal(await page.locator('#onboarding-dialog[open]').count(),0);
    const stored=await context.storageState();await context.close();
    const next=await open({storageState:stored});await welcome(next.page);await next.context.close();
  });
  await check('Explore and Skip persist dismissal; Help restarts after dismissal; Escape never marks completion',async()=>{
    const {page,context}=await open();await welcome(page);await page.locator('[data-onboarding-action=explore]').click();
    assert.equal(JSON.parse(await persisted(page)).status,'dismissed');
    await page.reload();await ready(page);assert.equal(await page.locator('#onboarding-dialog[open]').count(),0);
    await help(page);await page.locator('[data-help-action=tour]').click();await step(page,1);await action(page,'skip');
    assert.equal(JSON.parse(await persisted(page)).status,'dismissed');
    await help(page);await page.locator('[data-help-action=tour]').click();await action(page,'next');await page.keyboard.press('Escape');
    assert.equal(await panel(page).isVisible(),false);assert.equal(JSON.parse(await persisted(page)).status,'dismissed');
    assert.equal(await page.locator('#help-button').evaluate(n=>n===document.activeElement),true);
    await context.close();
  });
  for(const [width,height] of [[1440,900],[1440,1000],[834,1112],[375,812],[390,844],[320,812]]) {
    await check(`Eight-step tour / bilingual / focus / targets / Help at ${width}x${height}`,async()=>{
      const {page,context}=await open({viewport:{width,height}});await welcome(page);await bounded(page,'#onboarding-dialog');
      for(let i=0;i<9;i++) {await page.keyboard.press('Tab');assert(await page.evaluate(()=>Boolean(document.activeElement.closest('#onboarding-dialog'))),'Native modal focus escaped');}
      await page.locator('#onboarding-language').selectOption('en');assert((await page.locator('#onboarding-title').textContent()).includes('Welcome'));
      await page.locator('#onboarding-language').selectOption('es');
      if(width===1440&&height===1000)await page.screenshot({path:path.join(shots,'welcome-desktop.png')});
      if(width===390)await page.screenshot({path:path.join(shots,'welcome-mobile.png')});
      await page.locator('[data-onboarding-action=start]').click();
      const targets=['purpose','case','verdict','maps','relationships','evidence','provenance','limitations'];
      for(let i=0;i<8;i++) {
        await step(page,i+1);await connected(page,targets[i]);
        assert.equal(await page.locator('#guide-title').textContent(),copy.es.tour[i][0]);
        await page.locator('#guide-language').selectOption('en');
        assert.equal(await page.locator('html').getAttribute('lang'),'en');assert.equal(await panel(page).getAttribute('data-step'),String(i+1));
        assert.equal(await page.locator('#guide-title').textContent(),copy.en.tour[i][0]);
        await page.locator('#guide-language').selectOption('es');await connected(page,targets[i]);
        if(i===1){await action(page,'back');await step(page,1);await action(page,'next');await step(page,2);}
        if(i===3&&width===1440&&height===1000)await page.screenshot({path:path.join(shots,'tour-maps-desktop.png')});
        if(i===3&&width===390)await page.screenshot({path:path.join(shots,'tour-maps-mobile.png')});
        if(i===7&&width===1440&&height===1000)await page.screenshot({path:path.join(shots,'tour-limitations-desktop.png')});
        await action(page,'next');
      }
      assert.equal(await panel(page).isVisible(),false);assert.equal(JSON.parse(await persisted(page)).status,'completed');
      assert.equal(await page.locator('#case').inputValue(),'synthetic-block');assert.equal(await page.locator('#search').inputValue(),'');
      assert.equal(await page.locator('#help-button').evaluate(n=>n===document.activeElement),true);
      await page.reload();await ready(page);assert.equal(await page.locator('#onboarding-dialog[open]').count(),0);
      await help(page);await bounded(page,'#onboarding-dialog');
      assert.equal(await page.locator('#onboarding-dialog').evaluate(n=>[...n.childNodes].some(c=>c.nodeType===Node.TEXT_NODE&&c.textContent.trim()==='null')),false);
      assert.equal(await page.locator('[data-help-action]').count(),7);
      if(width===390)await page.screenshot({path:path.join(shots,'help-mobile.png')});
      await page.locator('[data-help-action=glossary]').click();assert.equal(await page.locator('.onboarding-glossary dt').count(),11);
      await page.keyboard.press('Escape');assert.equal(await page.locator('#onboarding-dialog[open]').count(),0);
      await help(page);await page.locator('[data-help-action=tour]').click();await step(page,1);await action(page,'skip');
      await context.close();return {viewport:{width,height},physical_device:false};
    });
  }
  await check('Hidden/missing targets pause without crashes or false completion; valid recovery retains the step',async()=>{
    const {page,context}=await open({dismissed:true});await ready(page);await help(page);await page.locator('[data-help-action=tour]').click();await action(page,'next');
    await page.locator('#case').evaluate(n=>n.style.display='none');await page.waitForSelector('[data-guide-unavailable]');
    assert(await page.locator('[data-guide-action=next]').isDisabled());assert.equal(await page.locator('.guide-highlight').count(),0);await action(page,'retry');await step(page,2);
    await page.locator('#case').evaluate(n=>n.style.display='');await page.waitForSelector('#guide-panel[data-connected-target=case]');
    await action(page,'next');await step(page,3);
    await page.evaluate(()=>document.getElementById('policy-summary').setAttribute('data-tour-target','temporarily-unavailable'));
    await page.waitForSelector('[data-guide-unavailable]');assert(await page.locator('[data-guide-action=next]').isDisabled());
    await step(page,3);assert.notEqual(JSON.parse(await persisted(page)).status,'completed');
    await page.evaluate(()=>document.getElementById('policy-summary').setAttribute('data-tour-target','verdict'));
    await page.keyboard.press('Escape');await context.close();
  });
  await check('ERROR never launches welcome; Help stays safe; active tours pause on analysis ERROR',async()=>{
    const faulty=await open({route:async route=>{if(route.request().url().endsWith('/data/synthetic-block/report.json')){await route.fulfill({status:200,body:'tampered',contentType:'application/json'});return true;}return false;}});
    await faulty.page.waitForSelector('#problem:not([hidden])');assert.equal(await faulty.page.locator('#onboarding-dialog[open]').count(),0);
    assert.equal(await faulty.page.locator('#verdict').textContent(),'');await help(faulty.page);
    assert(await faulty.page.locator('[data-help-action=tour]').isDisabled());assert(await faulty.page.locator('[data-help-action=practice]').isDisabled());
    await faulty.page.locator('[data-help-action=glossary]').click();assert.equal(await faulty.page.locator('.onboarding-glossary dt').count(),11);await faulty.context.close();
    const {page,context}=await open({dismissed:true});await ready(page);await help(page);await page.locator('[data-help-action=tour]').click();
    await selectCase(page,'synthetic-error');assert.equal(await page.locator('#completed').isVisible(),false);await page.waitForSelector('[data-guide-unavailable]');
    assert.equal(await page.locator('#verdict').textContent(),'');assert.equal(await page.locator('#base-map .point').count(),0);assert(await page.locator('[data-guide-action=next]').isDisabled());
    await help(page);assert(await page.locator('[data-help-action=tour]').isDisabled());await page.keyboard.press('Escape');
    await selectCase(page,'synthetic-block');await ready(page);await page.waitForSelector('#guide-panel[data-connected-target=purpose]');
    await action(page,'skip');await context.close();
  });
  await check('Real hotel_813 practice gates search, selection, interpretation and provenance; restores previous case',async()=>{
    const {page,context}=await open({dismissed:true});await ready(page);await selectCase(page,'synthetic-pass');await ready(page);
    await help(page);await page.locator('[data-help-action=practice]').click();
    assert.equal(await page.locator('#case').inputValue(),'synthetic-pass');await page.screenshot({path:path.join(shots,'practice-intro-desktop.png')});
    await page.locator('[data-onboarding-action=practice-start]').click();await action(page,'next');await step(page,1);assert((await page.locator('[data-guide-feedback]').textContent()).includes(copy.es.notYet));
    await selectCase(page,'synthetic-block');await ready(page);await action(page,'next');await step(page,2);
    await action(page,'next');await step(page,2);await page.locator('#search').fill('hotel_unchanged');await action(page,'next');await step(page,2);
    await page.locator('#search').fill('hotel_813');await action(page,'next');await step(page,3);
    await action(page,'target');await action(page,'next');await step(page,3); // Focus is not selection.
    await page.locator('[data-dependent-dataset=hotels][data-dependent-id=hotel_813]').focus();await page.keyboard.press('Enter');
    assert((await page.locator('#evidence-body').innerText()).includes('["chamberi"]'));assert((await page.locator('#evidence-body').innerText()).includes('["tetuan"]'));
    assert((await page.locator('#evidence-body').textContent()).includes('relationship-regression-526712f2a3cfcdb0b86e03e9b060807c34ec8909095e5bb87cd57ab47e3cde49'));
    await connected(page,'evidence');assert.equal(await page.locator('[data-guide-feedback]').textContent(),'');
    await page.screenshot({path:path.join(shots,'practice-selection-desktop.png')});
    await action(page,'next');await step(page,4);await action(page,'next');await step(page,4);
    await action(page,'target');await page.locator('input[name=onboarding-block-answer][value=harm]').check();await action(page,'next');await step(page,4);
    await page.locator('input[name=onboarding-block-answer][value=policy]').check();await action(page,'next');await step(page,5);
    await action(page,'next');await step(page,5);await action(page,'target');await action(page,'next');
    await page.waitForSelector('#onboarding-dialog[open][data-page=practice-done]');assert.equal(await page.locator('#onboarding-title').textContent(),copy.es.practiceDoneTitle);
    await page.screenshot({path:path.join(shots,'practice-complete-desktop.png')});
    await page.locator('[data-onboarding-action=return-case]').click();await ready(page);assert.equal(await page.locator('#case').inputValue(),'synthetic-pass');assert.equal(await page.locator('#verdict').textContent(),'PASS');
    assert.equal(JSON.parse(await persisted(page)).status,'completed');await context.close();
  });
  for(const width of [390,320])await check(`Actual practice, language, evidence and source navigation at ${width}px`,async()=>{
    const {page,context}=await open({viewport:{width,height:844},dismissed:true});await ready(page);await help(page);
    await page.locator('[data-help-action=tour]').click();for(let i=1;i<8;i++)await action(page,'next');
    await action(page,'example');await page.waitForSelector('#onboarding-dialog[open][data-page=practice-intro]');
    assert.equal(JSON.parse(await persisted(page)).status,'completed');
    await page.locator('[data-onboarding-action=practice-start]').click();await action(page,'next');await step(page,2);
    await action(page,'target');assert.equal(await page.locator('#search').evaluate(n=>n===document.activeElement),true);
    await page.keyboard.type('hotel_813');await action(page,'next');await step(page,3);await action(page,'target');await page.keyboard.press('Enter');
    await connected(page,'evidence');await page.locator('#guide-language').selectOption('en');await step(page,3);await connected(page,'evidence');
    assert((await page.locator('#evidence-body').innerText()).includes('tetuan'));
    if(width===390)await page.screenshot({path:path.join(shots,'practice-evidence-mobile.png')});
    await action(page,'next');await action(page,'target');await page.locator('input[name=onboarding-block-answer][value=policy]').check();
    if(width===390)await page.screenshot({path:path.join(shots,'practice-block-mobile.png')});
    await bounded(page,'#guide-panel');await action(page,'next');await step(page,5);await action(page,'target');
    await connected(page,'report-file');await action(page,'next');await page.waitForSelector('#onboarding-dialog[open][data-page=practice-done]');
    assert.equal(await page.locator('#onboarding-title').textContent(),copy.en.practiceDoneTitle);await context.close();
  });
  await check('Welcome Escape postpones; Help information, limits and resume are reachable by keyboard',async()=>{
    const {page,context}=await open();await welcome(page);await page.keyboard.press('Escape');assert.equal(await persisted(page),null);
    await page.reload();await ready(page);assert.equal(await page.locator('#onboarding-dialog[open]').count(),0);
    await page.locator('#help-button').focus();await page.keyboard.press('Enter');await page.locator('[data-help-action=about]').click();
    assert((await page.locator('#onboarding-dialog').innerText()).includes(copy.es.welcomeBody[0]));await page.keyboard.press('Escape');
    await help(page);await page.locator('[data-help-action=status]').click();assert((await page.locator('#onboarding-dialog').innerText()).includes(copy.es.tour[2][1]));await page.keyboard.press('Escape');
    await help(page);await page.locator('[data-help-action=limits]').click();assert.equal(await page.locator('#onboarding-dialog[open]').count(),0);
    assert.equal(await page.locator('[data-tour-target=limitations]').evaluate(n=>n.contains(document.activeElement)),true);
    await help(page);await page.locator('[data-help-action=practice]').click();await page.locator('[data-onboarding-action=practice-start]').click();
    await action(page,'next');await step(page,2);await help(page);await page.locator('[data-help-action=glossary]').click();await page.keyboard.press('Escape');
    await step(page,2);assert.equal(await page.locator('#help-button').evaluate(n=>n===document.activeElement),true);
    await action(page,'target');await connected(page,'search');await page.keyboard.press('Escape');await context.close();
  });
  await check('Practice skip/escape and Help close restore focus without completing the exercise',async()=>{
    const {page,context}=await open({dismissed:true});await ready(page);await help(page);await page.locator('[data-help-action=practice]').click();await page.locator('[data-onboarding-action=practice-start]').click();
    await action(page,'skip');await page.waitForSelector('#onboarding-dialog[open][data-page=practice-exit]');assert(!(await page.locator('#onboarding-title').textContent()).includes(copy.es.practiceDoneTitle));
    await page.keyboard.press('Escape');assert.equal(await page.locator('#help-button').evaluate(n=>n===document.activeElement),true);
    await help(page);await page.keyboard.press('Escape');assert.equal(await page.locator('#help-button').evaluate(n=>n===document.activeElement),true);await context.close();
  });
  if(hasSierra)await check('Sierra tour preserves meaningful zero, original 52 points, selection and absence of regression IDs',async()=>{
    const {page,context}=await open({dismissed:true});await ready(page);await selectCase(page,'sierra-local');await ready(page);
    await page.locator('.row').first().click();assert((await page.locator('#evidence-body').textContent()).includes('Sin ID de evidencia de regresión'));
    await help(page);await page.locator('[data-help-action=tour]').click();
    for(let i=1;i<6;i++)await action(page,'next');await step(page,6);
    assert.equal(await page.locator('#base-map .point').count(),52);assert.equal(await page.locator('#base-map .point.changed').count(),0);
    assert((await page.locator('#evidence-body').textContent()).includes('Sin ID de evidencia de regresión'));
    assert.equal(await page.locator('#case').inputValue(),'sierra-local');await action(page,'skip');await context.close();
  });
  await check('200% CSS zoom, resize mid-tour, reduced motion and blocked storage',async()=>{
    const {page,context}=await open();await welcome(page);
    await page.evaluate(()=>{document.documentElement.style.zoom='2';dispatchEvent(new Event('resize'));});await bounded(page,'#onboarding-dialog');
    await page.locator('[data-onboarding-action=start]').click();await connected(page,'purpose');await action(page,'next');await connected(page,'case');
    await page.evaluate(()=>{document.documentElement.style.zoom='1';dispatchEvent(new Event('resize'));});
    await page.setViewportSize({width:320,height:812});await connected(page,'case');assert(await page.evaluate(()=>matchMedia('(prefers-reduced-motion: reduce)').matches));
    await action(page,'next');await connected(page,'verdict');await action(page,'skip');await context.close();
    const blocked=await open({blockedStorage:true});await welcome(blocked.page);await blocked.page.locator('[data-onboarding-action=later]').click();await help(blocked.page);await blocked.page.locator('[data-help-action=glossary]').click();await blocked.context.close();
  });
  await check('No external runtime requests, uncaught errors, data mutations or non-state persistence',async()=>{
    assert.deepEqual(await scientificBytes(),before);assert.equal(external.length,0);assert.equal(errors.length,0);assert.equal(consoleErrors.length,0);
    const {page,context}=await open();await welcome(page);await page.locator('[data-onboarding-action=explore]').click();
    const storage=await page.evaluate(()=>({local:Object.entries(localStorage),session:Object.entries(sessionStorage)}));
    assert.deepEqual(storage.local,[[KEY,'{"status":"dismissed"}']]);assert.deepEqual(storage.session,[[KEY,'seen']]);await context.close();
  });
} catch(error) { console.error(error);process.exitCode=1; }
finally {
  const report={tested_at_utc:new Date().toISOString(),browser:browser.version(),playwright:'1.56.1',platform:process.platform,node:process.version,physical_devices:false,screen_reader_tested:false,human_comprehension_tested:false,records,external_requests:external,uncaught_errors:errors,ordinary_console_errors:consoleErrors,scientific_bytes_unchanged:JSON.stringify(before)===JSON.stringify(await scientificBytes()),screenshots:await readdir(shots)};
  await writeFile(path.join(local,'onboarding-results.json'),JSON.stringify(report,null,2)+'\n');await browser.close();
}
