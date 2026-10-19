/* End-to-end acceptance through a real Chromium process. No physical devices.
   Faults are intercepted test copies; no canonical file or report is edited. */
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { request } from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root=fileURLToPath(new URL('../',import.meta.url)),web=path.join(root,'web');
const base=process.env.STUDIO_URL || 'http://127.0.0.1:8765';
assert(['127.0.0.1','localhost'].includes(new URL(base).hostname),'Only loopback testing is allowed');
const screenshots=path.join(root,'qa/screenshots'),local=path.join(root,'qa/local');
await mkdir(screenshots,{recursive:true});await mkdir(local,{recursive:true});
const browser=await chromium.launch({headless:true,...(process.env.STUDIO_CHROMIUM_EXECUTABLE?{executablePath:process.env.STUDIO_CHROMIUM_EXECUTABLE}:{})});
const records=[], external=[], unexpected=[], consoleErrors=[], expectedFaultConsoleErrors=[];
const catalog=JSON.parse(await readFile(path.join(web,'catalog.json'),'utf8'));
const hasSierra=catalog.cases.some(c=>c.id==='sierra-local');
async function open(viewport={width:1440,height:1000},overrides=new Map()) {
  const context=await browser.newContext({viewport,reducedMotion:'reduce'});
  // These regression checks exercise the normal review workspace, not first visit.
  // Dedicated onboarding acceptance starts with genuinely empty storage instead.
  await context.addInitScript(() => localStorage.setItem('geoimpact:review-studio:onboarding:v1', JSON.stringify({status:'dismissed'})));
  await context.route('**/*',async route=>{
    const url=new URL(route.request().url());
    if(url.origin!==new URL(base).origin){external.push(url.origin);await route.abort();return;}
    const key=decodeURIComponent(url.pathname.slice(1));
    if(overrides.has(key)){const value=overrides.get(key);if(value===null){await route.fulfill({status:404,body:''});return;}
      await route.fulfill({status:200,body:value,contentType:key.endsWith('.js')?'text/javascript':'application/json'});return;}
    await route.continue();
  });
  const page=await context.newPage();
  page.on('pageerror',error=>unexpected.push(error.message));
  page.on('console',message=>{if(message.type()==='error')(overrides.size?expectedFaultConsoleErrors:consoleErrors).push(message.text());});
  const start=performance.now();await page.goto(base);await page.waitForSelector('#completed:not([hidden]),#problem:not([hidden])');
  return {page,context,coldLoadMs:performance.now()-start};
}
async function completed(page){await page.waitForSelector('#completed:not([hidden])');}
async function selectCase(page,id){await page.locator('#case').selectOption(id);await page.waitForSelector('#completed:not([hidden]),#problem:not([hidden])');}
async function noOverflow(page){assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1),'Unexpected horizontal page overflow');}
const check=async(name,fn)=>{const start=performance.now();try{const detail=await fn();records.push({name,status:'PASS',duration_ms:Math.round(performance.now()-start),...detail});console.log('PASS',name);}catch(error){records.push({name,status:'FAIL',message:error.message});throw error;}};
try {
  for(const [width,height] of [[1440,900],[1440,1000],[834,1112],[375,812],[390,844],[320,812]]) {
    await check(`J1–J4 / ${width}x${height} viewport emulation`,async()=>{
      const {page,context,coldLoadMs}=await open({width,height});await completed(page);
      assert.equal(await page.locator('#verdict').textContent(),'BLOCK');
      assert.equal(await page.locator('#stats .stat strong').allTextContents().then(x=>x.join(',')),'2,1,3,2');
      assert.equal(await page.locator('#base-map [data-primary-id]').count(),2);
      assert.equal(await page.locator('#candidate-map [data-point-key]').count(),3);
      await page.locator('#search').fill('hotel_813');assert.equal(await page.locator('.row').count(),1);
      const row=page.locator('.row').first();await row.focus();await page.keyboard.press('Space');
      assert.equal(await page.locator('.row').first().getAttribute('aria-pressed'),'true');
      assert((await page.locator('#evidence-body').innerText()).includes('relationship-regression-526712f2a3cfcdb0b86e03e9b060807c34ec8909095e5bb87cd57ab47e3cde49'));
      assert((await page.locator('#evidence-body').innerText()).includes('["chamberi"]'));
      assert.equal(await page.locator('#base-map .point.selected').count(),1);
      assert.equal(await page.locator('#candidate-map .point.selected').count(),1);
      await page.locator('#fit-selection').click();
      const selectedView=await page.locator('#base-map').getAttribute('viewBox');
      assert.equal(selectedView,await page.locator('#candidate-map').getAttribute('viewBox'));
      await page.locator('#base-map').focus();await page.keyboard.press('ArrowRight');
      assert.notEqual(selectedView,await page.locator('#base-map').getAttribute('viewBox'));
      await page.keyboard.press('Escape');assert.equal(await page.locator('#base-map .point.selected').count(),0);
      assert.equal(await page.locator('.row').first().evaluate(n=>n===document.activeElement),true);
      await page.keyboard.press('Enter');
      await page.locator('#fit-all').click();
      const pair=await page.locator('#transition option').nth(1).getAttribute('value');
      await page.locator('#transition').selectOption(pair);assert.equal(await page.locator('.row').count(),1);
      assert((await page.locator('#row-count').textContent()).includes('3 total'));
      if(width<=700){
        assert.equal(await page.locator('#base-frame').isVisible(),true);assert.equal(await page.locator('#candidate-frame').isVisible(),false);
        await page.locator('#candidate-tab').click();assert.equal(await page.locator('#candidate-frame').isVisible(),true);
        assert.equal(await page.locator('#candidate-map .point.selected').count(),1);
        await page.locator('#base-tab').click();
      }
      assert.equal(await page.locator('#input-files .file-row').count(),8);
      await page.locator('summary').click();assert((await page.locator('#config-raw').textContent()).includes('threshold: 1'));
      const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#input-files .file-row').filter({hasText:'report.json'}).getByRole('link').click()]);
      const bytes=await readFile(await download.path());assert.equal(createHash('sha256').update(bytes).digest('hex'),'d09f70d2f7fa07cef3fa87f5b1fe73d932c8f9c4619487c4a0fe8c4cc1d7b8dd');
      await page.locator('#language').selectOption('en');assert.equal(await page.locator('html').getAttribute('lang'),'en');
      assert((await page.locator('#verdict-meaning').textContent()).startsWith('BLOCK:'));
      assert((await page.locator('#evidence-body').textContent()).includes('hotel_813'));
      await page.locator('#language').selectOption('es');await noOverflow(page);
      await page.evaluate(()=>window.scrollTo(0,0));
      await page.screenshot({path:path.join(screenshots,`synthetic-${width}x${height}.png`),fullPage:false});
      if(width===390)await page.screenshot({path:path.join(screenshots,'synthetic-mobile-full.png'),fullPage:true});
      await context.close();return {viewport:{width,height},cold_load_ms:Math.round(coldLoadMs),device:'CSS viewport emulation; no physical device'};
    });
  }
  await check('PASS can contain regressions / recorded ERROR clears previous evidence',async()=>{
    const {page,context}=await open();await selectCase(page,'synthetic-pass');await completed(page);
    assert.equal(await page.locator('#verdict').textContent(),'PASS');assert.equal(await page.locator('#stats .stat strong').allTextContents().then(x=>x.join(',')),'2,2,3,2');
    await selectCase(page,'synthetic-error');assert.equal(await page.locator('#completed').isVisible(),false);
    assert.equal(await page.locator('#verdict').textContent(),'');assert.equal(await page.locator('#base-map').innerHTML(),'');
    assert((await page.locator('#problem').innerText()).includes('exit 2'));
    await page.screenshot({path:path.join(screenshots,'analysis-error.png'),fullPage:false});
    await selectCase(page,'synthetic-block');await completed(page);assert.equal(await page.locator('#verdict').textContent(),'BLOCK');await context.close();
  });
  await check('Point selection, primary selection, layers, zoom and keyboard exit',async()=>{
    const {page,context}=await open();await completed(page);
    await page.locator('#base-map .point').first().click();assert.equal(await page.locator('#base-map .point.selected').count(),1);
    await page.locator('#primary').selectOption('chamberi');assert.equal(await page.locator('#base-map path.selected[data-primary-id]').count(),1);
    assert.equal(await page.locator('#base-map .point.selected').count(),0);
    await page.locator('#points-toggle').uncheck();assert.equal(await page.locator('#base-map .point').count(),0);await page.locator('#points-toggle').check();
    await page.locator('#polygons-toggle').uncheck();assert.equal(await page.locator('#base-map [data-primary-id]').count(),0);await page.locator('#polygons-toggle').check();
    const v=await page.locator('#base-map').getAttribute('viewBox');await page.locator('#base-map').focus();await page.keyboard.press('+');assert.notEqual(v,await page.locator('#base-map').getAttribute('viewBox'));
    await page.keyboard.press('Tab');assert.equal(await page.locator('#base-map').evaluate(n=>n===document.activeElement),false);
    await context.close();
  });
  await check('J5 / missing, whitespace-tampered report and unsupported V4 fail closed',async()=>{
    for(const [scenario,expected] of [['missing','MISSING'],['tampered','HASH_MISMATCH'],['v4','UNSUPPORTED_REPORT']]){
      const overrides=new Map();
      const file='data/synthetic-block/report.json';
      if(scenario==='missing')overrides.set(file,null);
      if(scenario==='tampered')overrides.set(file,(await readFile(path.join(web,file),'utf8'))+' ');
      if(scenario==='v4'){
        const report=JSON.parse(await readFile(path.join(web,file),'utf8'));report.report_version='4';const raw=JSON.stringify(report);overrides.set(file,raw);
        const manifestPath='data/synthetic-block/manifest.json',manifest=JSON.parse(await readFile(path.join(web,manifestPath),'utf8'));
        const identity=value=>({sha256:createHash('sha256').update(value).digest('hex'),size_bytes:Buffer.byteLength(value)});
        manifest.files['report.json']={...manifest.files['report.json'],...identity(raw)};
        const mf=JSON.stringify(manifest);overrides.set(manifestPath,mf);
        const c=structuredClone(catalog);Object.assign(c.cases.find(x=>x.id==='synthetic-block'),identity(mf));
        const cat=JSON.stringify(c);overrides.set('catalog.json',cat);overrides.set('trust.js',`export const catalogHash="${identity(cat).sha256}";`);
      }
      const {page,context}=await open(undefined,overrides);
      assert((await page.locator('#problem').textContent()).includes(expected));assert.equal(await page.locator('#completed').isVisible(),false);assert.equal(await page.locator('#verdict').textContent(),'');
      if(scenario==='tampered')await page.screenshot({path:path.join(screenshots,'integrity-error.png'),fullPage:false});
      await context.close();
    }
  });
  if(hasSierra)await check('Sierra local / J1–J5 meaningful zero and complete inventory',async()=>{
    const {page,context}=await open();await selectCase(page,'sierra-local');await completed(page);
    assert.equal(await page.locator('#verdict').textContent(),'PASS');
    assert.equal(await page.locator('#base-map .point').count(),52);assert.equal(await page.locator('#candidate-map .point').count(),52);
    assert.equal(await page.locator('#base-map .point.changed').count(),0);
    assert((await page.locator('#geometry-body').textContent()).includes('69 · modificada'));
    assert((await page.locator('#map-credit').textContent()).includes('REDIAM'));
    await page.locator('#filter').selectOption('regressions');assert.equal(await page.locator('.row').count(),0);
    assert((await page.locator('#empty').textContent()).includes('52 relaciones evaluadas'));
    assert.equal(await page.locator('#base-map .point').count(),52);
    await page.screenshot({path:path.join(local,'sierra-zero-desktop.png'),fullPage:true});
    await page.locator('#filter').selectOption('all');
    const sierraEntry=catalog.cases.find(c=>c.id==='sierra-local'),manifest=JSON.parse(await readFile(path.join(web,sierraEntry.path),'utf8'));
    const report=JSON.parse(await readFile(path.join(web,manifest.files['report.json'].path),'utf8'));
    for(const assigned of [true,false]){
      const row=report.relationships.find(r=>(r.before.length>0)===assigned);await page.locator('#search').fill(row.dependent_id);await page.locator('.row').first().click();
      assert((await page.locator('#evidence-body').innerText()).includes(assigned?'["69"]':'[]'));
      assert((await page.locator('#evidence-body').innerText()).includes('Sin ID de evidencia de regresión'));
    }
    await page.locator('#search').fill('');await page.locator('#next').click();assert((await page.locator('#page-label').textContent()).includes('2 de 7'));
    await page.setViewportSize({width:390,height:844});await noOverflow(page);await page.locator('#primary').selectOption('69');await page.locator('#fit-selection').click();
    await page.locator('#review').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(local,'sierra-mobile.png'),fullPage:false});
    await context.close();
  });
  await check('200% CSS zoom reflow emulation / 320px reflow / contrast / skip link',async()=>{
    const {page,context}=await open();await completed(page);
    await page.keyboard.press('Tab');assert.equal(await page.locator('.skip').evaluate(n=>n===document.activeElement),true);
    await page.keyboard.press('Enter');assert.equal(await page.locator('#review').evaluate(n=>n===document.activeElement),true);
    // CSS zoom is explicitly reported as emulation, not physical hardware or a full WCAG assessment.
    await page.evaluate(()=>document.documentElement.style.zoom='2');await noOverflow(page);
    await page.screenshot({path:path.join(screenshots,'synthetic-zoom-200.png'),fullPage:false});
    await page.evaluate(()=>document.documentElement.style.zoom='1');
    const colors=await page.locator('body').evaluate(n=>({fg:getComputedStyle(n).color,bg:getComputedStyle(n).backgroundColor}));
    const luminance=rgb=>rgb.match(/[\d.]+/g).slice(0,3).map(v=>Number(v)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
    const a=luminance(colors.fg),b=luminance(colors.bg),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);assert(ratio>=4.5);
    await context.close();return {zoom:'200% CSS zoom emulation',body_text_contrast:Number(ratio.toFixed(2)),screen_reader:'not tested'};
  });
  await check('Static serving boundary and zero external runtime requests',async()=>{
    const response=await fetch(base+'/../research/sierra-de-baza-2015-2025/base.geojson');assert.equal(response.status,404);
    assert.equal((await fetch(base+'/data/')).status,403);
    const hostStatus=await new Promise((resolve,reject)=>{const r=request(base,{headers:{Host:'example.com'}},response=>{response.resume();resolve(response.statusCode);});r.on('error',reject);r.end();});
    assert.equal(hostStatus,403);
    assert.equal(external.length,0);assert.equal(unexpected.length,0);assert.equal(consoleErrors.length,0);
  });
} catch(error) { console.error(error);process.exitCode=1; }
finally {
  let git;try{git=execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim();}catch{}
  const report={tested_at_utc:new Date().toISOString(),browser:await browser.version(),playwright:'1.56.1',platform:process.platform,node:process.version,source_base_commit:git,working_tree:'UI files under test may be uncommitted; final validation records the source tree digest',physical_devices:false,screen_reader_tested:false,Sierra:hasSierra?'local only':'not included',records,external_requests:external,uncaught_errors:unexpected,console_errors:consoleErrors,expected_injected_fault_console_errors:expectedFaultConsoleErrors};
  await writeFile(path.join(local,'browser-results.json'),JSON.stringify(report,null,2)+'\n');
  await browser.close();
}
