import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { ONBOARDING_KEY, readPreference, storePreference, practiceReady, tourTargets } from '../web/onboarding.js';
import { copy } from '../web/onboarding-copy.js';
import { loadCase } from '../web/reader.js';

test('persistence contains only a versioned completion/dismissal enum', () => {
  const values = new Map(), storage = {getItem:k=>values.get(k),setItem:(k,v)=>values.set(k,v)};
  assert.equal(readPreference(storage),null);
  for(const status of ['completed','dismissed']) {
    storePreference(storage,status);
    assert.deepEqual(JSON.parse(values.get(ONBOARDING_KEY)),{status});
    assert.equal(readPreference(storage),status);
  }
  storePreference(storage,'hotel_813'); assert.equal(readPreference(storage),'dismissed');
  assert.equal(values.size,1);
});
test('disabled, malformed and unknown storage cannot block help or treat a visit as complete',()=>{
  const blocked={getItem:()=>{throw Error('blocked');},setItem:()=>{throw Error('blocked');}};
  assert.equal(readPreference(blocked),null);assert.doesNotThrow(()=>storePreference(blocked,'completed'));
  for(const value of ['not JSON','{"status":"other"}','null'])assert.equal(readPreference({getItem:()=>value}),null);
});
test('copy is complete in both languages, with eight semantic targets and eleven glossary meanings',()=>{
  assert.deepEqual(Object.keys(copy.es).sort(),Object.keys(copy.en).sort());
  assert.equal(tourTargets.length,8);
  for(const lang of ['es','en']) {
    assert.equal(copy[lang].tour.length,8);assert.equal(copy[lang].practice.length,5);assert.equal(copy[lang].glossary.length,11);
    assert(copy[lang].welcomeBody[2].includes(lang==='es'?'ni calcula nuevos impactos':'calculate new impacts'));
    assert(copy[lang].tour[6][1].includes('SHA-256'));
  }
});
test('practice gates use an actual released V5 report and observable actions; they cannot issue a new verdict',async()=>{
  const web=new URL('../web/',import.meta.url), catalog=JSON.parse(await readFile(new URL('catalog.json',web)));
  const b=await loadCase(catalog.cases.find(c=>c.id==='synthetic-block'),async p=>new Response(await readFile(new URL(p,web))));
  const key='["hotels","hotel_813"]', view={valid:true,caseId:b.manifest.id,reportVersion:b.report.report_version,verdict:b.report.verdict,observed:b.report.policy.observed_value,threshold:b.report.policy.threshold,search:'hotel_813',visibleKeys:[key],selected:b.rows.get(key),evidenceId:b.regressionByRow.get(key).evidence_id,sourceIdentityVisible:true,versionCount:5};
  assert(practiceReady(0,view,{}));assert(practiceReady(1,view,{}));assert(practiceReady(2,view,{}));
  assert.equal(practiceReady(3,view,{}),false);assert.equal(practiceReady(3,view,{result:true,answer:'harm'}),false);
  assert(practiceReady(3,view,{result:true,answer:'policy'}));
  assert.equal(practiceReady(4,view,{}),false);assert(practiceReady(4,view,{provenance:true}));
  for(const patch of [{valid:false},{caseId:'sierra-local'},{verdict:'PASS'},{threshold:2},{reportVersion:'4'}])for(let step=0;step<5;step++)assert.equal(practiceReady(step,{...view,...patch},{result:true,answer:'policy',provenance:true}),false);
  assert.equal(practiceReady(1,{...view,search:''},{}),false);
  assert.equal(practiceReady(2,{...view,evidenceId:null},{}),false);
  assert.equal(practiceReady(4,{...view,sourceIdentityVisible:false},{provenance:true}),false);
  assert.equal(b.report.policy.status,'BLOCK');assert.equal(b.report.policy.threshold,1);
});
