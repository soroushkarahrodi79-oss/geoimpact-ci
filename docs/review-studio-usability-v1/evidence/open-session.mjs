/* Facilitator utility, not product code. No participant recording or telemetry.
   Close the Chromium window to end a normal launch. --self-check is engineering QA. */
import { chromium } from '../../../experiments/review-studio-local/node_modules/playwright/index.mjs';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';

const args=process.argv.slice(2),value=(name,fallback)=>args.includes(name)?args[args.indexOf(name)+1]:fallback;
const scenario=value('--scenario','normal'),language=value('--lang','es');
const width=Number(value('--width','1440')),height=Number(value('--height','900'));
assert(['normal','load-error'].includes(scenario));assert(['es','en'].includes(language));
assert(Number.isFinite(width)&&width>=320&&Number.isFinite(height)&&height>=600);
const base=new URL(process.env.STUDIO_URL || 'http://127.0.0.1:8765');
assert(['127.0.0.1','localhost'].includes(base.hostname));
// Default preserves the historical audit; future sessions must pin their version.
const reference=value('--reference','32f3ab50bb8a91d21118610bfc135b33e3fb2f3c');
assert(/^[0-9a-f]{40}$/.test(reference),'Use a complete, exact study commit');
const root=fileURLToPath(new URL('../../../',import.meta.url));
const hash=b=>createHash('sha256').update(b).digest('hex');
for(const name of ['index.html','app.js','reader.js','style.css','onboarding.js','onboarding-copy.js','onboarding.css']) {
  const expected=execFileSync('git',['show',`${reference}:experiments/review-studio-local/web/${name}`],{cwd:root});
  const served=Buffer.from(await (await fetch(new URL(name,base))).arrayBuffer());
  assert.equal(hash(served),hash(expected),'Stop: the server no longer serves the study reference');
}
const catalog=await (await fetch(new URL('catalog.json',base))).json();
assert(catalog.cases.every(c=>['synthetic-block','synthetic-pass','synthetic-error','sierra-local'].includes(c.id)),'Unapproved study case');
assert(!catalog.cases.some(c=>c.id==='sierra-local')||args.includes('--allow-local-sierra'),'Use synthetic-only preparation, or explicitly approve the retained local Sierra variant');
const browser=await chromium.launch({headless:args.includes('--self-check'),...(process.env.STUDIO_CHROMIUM_EXECUTABLE?{executablePath:process.env.STUDIO_CHROMIUM_EXECUTABLE}:{})});
const context=await browser.newContext({viewport:{width,height}});
await context.route('**/*',async route=>{
  const u=new URL(route.request().url());
  if(u.origin!==base.origin){await route.abort();return;}
  if(scenario==='load-error'&&u.pathname.endsWith('/data/synthetic-block/report.json')) {
    await route.fulfill({status:404,body:''});return;
  }
  await route.continue();
});
const page=await context.newPage();await page.goto(base.href);
if(scenario==='normal')await page.locator('#onboarding-dialog[open][data-page=welcome]').waitFor();
else {await page.locator('#problem:not([hidden])').waitFor();assert.equal(await page.locator('#completed').isVisible(),false);}
if(language==='en')await page.locator(scenario==='normal'?'#onboarding-language':'#language').selectOption('en');
console.log(JSON.stringify({reference,scenario,language,viewport:{width,height},recording:false,storage:'Fresh ephemeral context; no participant files saved',self_check:args.includes('--self-check')}));
if(args.includes('--self-check'))await browser.close();
else await new Promise(resolve=>browser.on('disconnected',resolve));
