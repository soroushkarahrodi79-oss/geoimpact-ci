import { copy } from './onboarding-copy.js';

export const ONBOARDING_KEY = 'geoimpact:review-studio:onboarding:v1';
export const tourTargets = [
  ['purpose', null], ['case', null], ['verdict', '[data-tour-target="verdict-strip"]'],
  ['maps', '[data-tour-target="map-controls"]'], ['relationships', '#search'],
  ['evidence', '#evidence-title'], ['provenance', '#provenance-title'], ['limitations', null]
];
const practiceTargets = ['case', 'search', 'relationship-list', 'verdict', 'report-file'];

// Only completion/dismissal is retained. Failure/disabled storage is harmless.
export function readPreference(storage) {
  try {
    const value = JSON.parse(storage.getItem(ONBOARDING_KEY));
    return ['completed', 'dismissed'].includes(value?.status) ? value.status : null;
  } catch { return null; }
}
export function storePreference(storage, status) {
  if (!['completed', 'dismissed'].includes(status)) return;
  try { storage.setItem(ONBOARDING_KEY, JSON.stringify({ status })); } catch { /* page-local fallback */ }
}

// This checks the released exercise fixture and UI actions, not a spatial
// predicate or a new verdict. The verified V5 report remains authoritative.
export function practiceReady(step, view, actions) {
  if (!view.valid || view.caseId !== 'synthetic-block' || view.reportVersion !== '5' ||
      view.verdict !== 'BLOCK' || view.observed !== 2 || view.threshold !== 1) return false;
  if (step === 0) return true; // Already-selected, verified BLOCK is a valid starting state.
  if (step === 1) return view.search.trim() === 'hotel_813' && view.visibleKeys.includes('["hotels","hotel_813"]');
  if (step === 2) return view.selected?.dependent_dataset === 'hotels' && view.selected?.dependent_id === 'hotel_813' &&
    JSON.stringify(view.selected.before) === '["chamberi"]' && JSON.stringify(view.selected.after) === '["tetuan"]' && Boolean(view.evidenceId);
  if (step === 3) return actions.result === true && actions.answer === 'policy';
  if (step === 4) return actions.provenance === true && view.sourceIdentityVisible && view.versionCount === 5;
  return false;
}

function node(tag, attrs = {}, ...children) {
  const element = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key.startsWith('on')) element.addEventListener(key.slice(2), value);
    else if (value !== undefined && value !== null) element.setAttribute(key, String(value));
  }
  for (const child of children.flat()) if (child !== undefined && child !== null) element.append(child instanceof Node ? child : document.createTextNode(String(child)));
  return element;
}
const visible = element => Boolean(element?.isConnected && element.getClientRects().length && getComputedStyle(element).visibility !== 'hidden' && !element.closest('[hidden]'));

export function installOnboarding(api) {
  const help = document.getElementById('help-button');
  const dialog = node('dialog', { id:'onboarding-dialog', class:'onboarding-dialog', 'aria-labelledby':'onboarding-title' });
  const panel = node('aside', { id:'guide-panel', class:'guide-panel', role:'region', 'aria-labelledby':'guide-title', hidden:'' });
  const announcement = node('div', { class:'sr-only', role:'status', 'aria-live':'polite', 'aria-atomic':'true', id:'onboarding-announcement' });
  document.body.append(dialog, panel, announcement);
  const state = { mode:null, page:null, step:0, opener:help, previousCase:null, actions:{}, feedback:false, offered:false, currentTarget:null, unavailable:null, scheduled:false };
  const text = () => copy[api.language()]; // One language owner: app.js.
  const markSession = () => { state.offered = true; try { sessionStorage.setItem(ONBOARDING_KEY, 'seen'); } catch {} };
  const mark = status => { markSession(); try { storePreference(localStorage, status); } catch {} };
  const focus = element => {
    const target = visible(element) ? element : help;
    target.focus({ preventScroll:true });
    const rect = target.getBoundingClientRect();
    if (rect.top < 0 || rect.bottom > innerHeight) target.scrollIntoView({ block:'nearest', behavior:'instant' });
  };
  const button = (label, action, attrs = {}) => node('button', { type:'button', onclick:action, ...attrs }, label);
  function languageControl(id) {
    return node('label', { class:'onboarding-language', for:id }, node('span', { class:'sr-only' }, text().language),
      node('select', { id, 'data-guide-control':'language', onchange:event => api.setLanguage(event.target.value) },
        ...['es','en'].map(lang => node('option', { value:lang, ...(api.language() === lang ? { selected:'' } : {}) }, lang.toUpperCase()))));
  }
  function clearHighlight() {
    document.querySelectorAll('.guide-highlight').forEach(element => { element.classList.remove('guide-highlight'); delete element.dataset.guideConnection; });
    delete panel.dataset.connectedTarget;
    state.currentTarget = null;
  }
  function hidePanel() {
    panel.hidden = true; document.body.classList.remove('guide-open'); clearHighlight();
  }
  function restoreFocus() {
    focus(state.opener); state.opener = help;
  }
  function closeDialog({ resume = true, restore = true } = {}) {
    state.page = null; if (dialog.open) dialog.close();
    if (resume && state.mode) renderPanel({ scroll:true });
    if (restore) restoreFocus();
  }
  function showDialog(page, opener = document.activeElement) {
    if (!dialog.open) state.opener = visible(opener) ? opener : help;
    state.page = page; hidePanel(); renderDialog();
    if (!dialog.open) dialog.showModal();
    fitDialog();
    document.getElementById('onboarding-title').focus();
  }
  function startTour() {
    if (!api.snapshot().valid) return;
    markSession(); closeDialog({ resume:false, restore:false });
    state.mode = 'tour'; state.step = 0; state.opener = help; renderPanel({ scroll:true, announce:true });
  }
  function introPractice() {
    const view = api.snapshot();
    if (!view.valid || !view.caseIds.includes('synthetic-block')) return;
    state.mode = null; state.previousCase = view.caseId; state.step = 0; state.actions = {}; state.feedback = false;
    showDialog('practice-intro');
  }
  function startPractice() {
    if (!api.snapshot().valid) return;
    markSession(); closeDialog({ resume:false, restore:false });
    state.mode = 'practice'; state.step = 0; state.opener = help; renderPanel({ scroll:true, announce:true });
  }
  function finishOrSkipPractice(done = false) {
    if (done) mark('completed');
    state.mode = null; hidePanel();
    showDialog(done ? 'practice-done' : 'practice-exit', help);
  }
  function finishTour() {
    if (state.step !== 7 || !availableTarget()) return;
    mark('completed'); state.mode = null; hidePanel(); restoreFocus();
  }
  function stopTour(persistent = false) {
    if (persistent) mark('dismissed'); else markSession();
    state.mode = null; hidePanel(); restoreFocus();
  }
  function returnToCase() {
    const previous = state.previousCase;
    closeDialog({ resume:false, restore:false }); state.mode = null; hidePanel();
    // Explicit user action, through the application's ordinary case control.
    api.returnToCase(previous); focus(document.getElementById('case'));
  }
  function menuBody() {
    const c = text(), view = api.snapshot();
    const actions = [() => showDialog('about'), startTour, introPractice, () => showDialog('status'), () => showDialog('glossary'), () => {
      closeDialog({ resume:false, restore:false }); state.mode = null; hidePanel(); scrollAndFocus(document.querySelector('[data-tour-target="limitations"]'));
    }];
    return [node('nav', { class:'onboarding-menu', 'aria-label':c.helpTitle }, c.menu.map((label, i) => button(label, actions[i], {
      'data-help-action':['about','tour','practice','status','glossary','limits'][i],
      ...((i === 1 || i === 2 || i === 5) && !view.valid || i === 2 && !view.caseIds.includes('synthetic-block') ? { disabled:'' } : {})
    }))), !view.valid ? node('p', { class:'onboarding-notice', role:'status' }, c.unsafe) : null,
    node('a', { href:'https://github.com/soroushkarahrodi79-oss/geoimpact-ci/issues', target:'_blank', rel:'noopener noreferrer' }, c.support),
    button(c.welcomeLink, () => showDialog('welcome'), { 'data-help-action':'welcome', ...(!view.valid ? { disabled:'' } : {}) })];
  }
  function renderDialog() {
    const c = text(), view = api.snapshot(), page = state.page;
    const activeLanguage = document.activeElement?.dataset.guideControl === 'language';
    let title = c.helpTitle, content = [], actions = [];
    if (page === 'welcome') {
      title = c.welcomeTitle; content = [...c.welcomeBody.map(p => node('p', {}, p)), node('p', { class:'onboarding-notice' }, c.caution)];
      actions = [button(c.start, startTour, { class:'onboarding-primary', 'data-onboarding-action':'start', ...(!view.valid ? {disabled:''} : {}) }),
        button(c.explore, () => { mark('dismissed'); closeDialog(); }, { 'data-onboarding-action':'explore' }),
        button(c.later, () => { markSession(); closeDialog(); }, { 'data-onboarding-action':'later' })];
    } else if (page === 'help') content = menuBody();
    else if (page === 'about') {
      title = c.menu[0]; content = [...c.welcomeBody.map(p => node('p', {}, p)), node('p', { class:'onboarding-notice' }, c.caution)];
    } else if (page === 'glossary') {
      title = c.glossaryTitle;
      content = [node('dl', { class:'onboarding-glossary' }, c.glossary.map(([term, definition]) => node('div', {}, node('dt', {}, term), node('dd', {}, definition))))];
    } else if (page === 'status') {
      title = c.menu[3]; content = [node('p', {}, c.tour[2][1]), node('p', { class:'onboarding-notice' }, c.caution), node('p', {}, c.statusHelp)];
    } else if (page === 'practice-intro') {
      title = c.practiceTitle; content = [node('p', {}, c.practiceIntro), node('p', { class:'onboarding-notice' }, c.previousCase)];
      actions = [button(c.practiceStart, startPractice, { class:'onboarding-primary', 'data-onboarding-action':'practice-start', ...(!view.valid ? { disabled:'' } : {}) }), button(c.practiceSkip, () => closeDialog())];
    } else if (page === 'practice-done' || page === 'practice-exit') {
      title = page === 'practice-done' ? c.practiceDoneTitle : c.helpTitle;
      content = [node('p', {}, page === 'practice-done' ? c.practiceDone : c.exited)];
      actions = [button(page === 'practice-done' ? c.practiceFinish : c.continueHere, () => closeDialog())];
      if (state.previousCase && state.previousCase !== view.caseId && view.caseIds.includes(state.previousCase)) actions.unshift(button(c.returnCase, returnToCase, { 'data-onboarding-action':'return-case' }));
    }
    if (['about','glossary','status'].includes(page)) actions.push(button(c.menuBack, () => showDialog('help')));
    dialog.replaceChildren(node('div', { class:'onboarding-modal-top' }, node('span', { class:'eyebrow' }, c.learn), languageControl('onboarding-language'),
      button('×', () => dismissModal(), { class:'onboarding-close', 'aria-label':c.close, 'data-onboarding-action':'close' })),
      node('div', { class:'onboarding-modal-body' }, node('h2', { id:'onboarding-title', tabindex:'-1' }, title), ...content),
      ...(actions.length ? [node('div', { class:'onboarding-modal-actions' }, actions)] : []));
    dialog.dataset.page = page;
    if (activeLanguage) document.getElementById('onboarding-language').focus();
  }
  function dismissModal() {
    if (state.page === 'welcome') markSession();
    closeDialog();
  }
  function requestedTarget() {
    if (state.mode === 'practice' && state.step === 2 && practiceReady(2, api.snapshot(), state.actions)) return document.querySelector('[data-tour-target="evidence"]');
    const name = state.mode === 'tour' ? tourTargets[state.step][0] : practiceTargets[state.step];
    return document.querySelector(`[data-tour-target="${name}"]`);
  }
  function availableTarget() {
    const view = api.snapshot();
    if (!view.valid) return null;
    if (state.mode === 'practice' && state.step > 0 && view.caseId !== 'synthetic-block') return null;
    const target = requestedTarget(); return visible(target) ? target : null;
  }
  function resizeSpace() {
    const zoom = Number(getComputedStyle(document.documentElement).zoom) || 1;
    const height = (window.visualViewport?.height || innerHeight) / zoom;
    document.documentElement.style.setProperty('--guide-max-height', `${Math.min(350, height * .43)}px`);
    const space = panel.getBoundingClientRect().height / zoom + 40;
    document.documentElement.style.setProperty('--guide-space', `${space}px`);
  }
  function fitDialog() {
    const zoom = Number(getComputedStyle(document.documentElement).zoom) || 1;
    document.documentElement.style.setProperty('--onboarding-dialog-height', `${(window.visualViewport?.height || innerHeight) / zoom - 32}px`);
    document.documentElement.style.setProperty('--onboarding-dialog-width', `${(window.visualViewport?.width || innerWidth) / zoom - 32}px`);
  }
  function revealFocusedControl() {
    if (!state.mode || panel.hidden || dialog.open) return;
    const target = document.activeElement;
    if (!visible(target) || panel.contains(target) || !target.matches('button,input,select,a[href],summary,[tabindex]')) return;
    const rect = target.getBoundingClientRect(), top = 8;
    const bottom = Math.min(panel.getBoundingClientRect().top, innerHeight) - 8;
    // Native focus scrolling uses the viewport, which includes our fixed dock.
    // Reveal the actual focus above it, without moving focus or handling Tab.
    // A map taller than the available space keeps its top/keyboard focus visible.
    const delta = rect.height > bottom - top || rect.top < top ? rect.top - top : Math.max(0, rect.bottom - bottom);
    if (delta) window.scrollBy({ top:delta, behavior:'instant' });
  }
  function chooseFocus(target) {
    const available = panel.getBoundingClientRect().top - 34;
    if (target.getBoundingClientRect().height <= available) return target;
    const fallback = state.mode === 'tour' ? tourTargets[state.step][1] : state.step === 2 ? target.dataset.tourTarget === 'evidence' ? '#evidence-title' : '#relation-list .row' : state.step === 3 ? '[data-tour-target="verdict-strip"]' : null;
    const element = fallback ? document.querySelector(fallback) : target;
    return visible(element) ? element : target;
  }
  function scrollAndFocus(target, setFocus = true) {
    if (!visible(target)) return;
    target.scrollIntoView({ block:'start', behavior:'instant' });
    window.scrollBy({ top:target.getBoundingClientRect().top - 16, behavior:'instant' });
    if (setFocus) {
      const control = target.matches('button,input,select,a,[tabindex]') ? target : target.querySelector('input,select,button,a') || target;
      if (!control.hasAttribute('tabindex') && !control.matches('button,input,select,a')) control.setAttribute('tabindex', '-1');
      focus(control);
    }
  }
  function connect({ scroll = false } = {}) {
    clearHighlight();
    const target = availableTarget();
    if (!target || panel.hidden) return;
    const connected = chooseFocus(target); connected.classList.add('guide-highlight'); state.currentTarget = connected;
    panel.dataset.connectedTarget = target.dataset.tourTarget;
    connected.dataset.guideConnection = target.dataset.tourTarget;
    if (scroll) scrollAndFocus(connected, false);
  }
  function goToTarget() {
    if (!availableTarget()) { renderPanel({ announce:true }); return; }
    let target = state.currentTarget;
    if (state.mode === 'practice') {
      if (state.step === 2 && !practiceReady(2, api.snapshot(), state.actions)) target = document.querySelector('[data-dependent-dataset="hotels"][data-dependent-id="hotel_813"]') || target;
      if (state.step === 3) state.actions.result = true;
      if (state.step === 4) state.actions.provenance = true;
    }
    scrollAndFocus(target);
  }
  function checkPractice() {
    if (!availableTarget()) { renderPanel({ announce:true }); return; }
    if (!practiceReady(state.step, api.snapshot(), state.actions)) {
      state.feedback = true;
      const feedback = panel.querySelector('[data-guide-feedback]'); feedback.textContent = text().notYet; resizeSpace(); connect({ scroll:true }); return;
    }
    state.feedback = false;
    if (state.step === 4) finishOrSkipPractice(true);
    else { state.step++; renderPanel({ scroll:true, announce:true }); }
  }
  function renderPanel({ scroll = false, announce = false } = {}) {
    if (!state.mode || dialog.open) return;
    const c = text(), touring = state.mode === 'tour', activeLanguage = document.activeElement?.dataset.guideControl === 'language';
    const available = Boolean(availableTarget()); state.unavailable = !available;
    const entry = touring ? c.tour[state.step] : [c.practiceNames[state.step], c.practice[state.step]];
    const progress = (touring ? c.step : c.practiceProgress).replace('{current}', state.step + 1);
    const body = [node('h2', { id:'guide-title', tabindex:'-1' }, entry[0]), node('p', {}, entry[1])];
    if (entry[2]) body.push(node('p', { class:'onboarding-notice' }, entry[2]));
    if (!available) body.push(node('p', { class:'onboarding-notice', role:'status', 'data-guide-unavailable':'' }, api.snapshot().valid && !touring && state.step > 0 && api.snapshot().caseId !== 'synthetic-block' ? c.wrongCase : c.unavailable));
    if (touring && state.step === 5 && !api.snapshot().selected) body.push(node('p', { class:'onboarding-note' }, c.noSelection));
    if (!touring) {
      body.push(node('details', {}, node('summary', {}, c.hint), node('p', {}, c.hints[state.step])));
      if (state.step === 3) body.push(node('fieldset', { class:'onboarding-question' }, node('legend', {}, c.question), c.answers.map((answer, i) => node('label', {},
        node('input', { type:'radio', name:'onboarding-block-answer', value:['policy','harm','movement'][i], ...(state.actions.answer === ['policy','harm','movement'][i] ? { checked:'' } : {}), onchange:event => { state.actions.answer = event.target.value; } }), answer))));
    }
    body.push(node('p', { 'data-guide-feedback':'', role:'status', class:'onboarding-note' }, state.feedback ? c.notYet : ''));
    const navigation = [button(touring ? c.back : c.practiceBack, () => { state.step--; state.feedback = false; renderPanel({ scroll:true, announce:true }); }, { disabled:state.step === 0 ? '' : null, 'data-guide-action':'back' }),
      button(touring ? c.go : state.step === 2 && practiceReady(2, api.snapshot(), state.actions) ? c.goEvidence : [c.goCase,c.goSearch,c.goRow,c.goVerdict,c.goSource][state.step], goToTarget, { disabled:available ? null : '', 'data-guide-action':'target' })];
    navigation.push(button(touring ? state.step === 7 ? c.finish : c.next : c.check, touring ? () => { if (!availableTarget()) { renderPanel({ announce:true }); return; } if (state.step === 7) finishTour(); else { state.step++; renderPanel({ scroll:true, announce:true }); } } : checkPractice,
      { class:'onboarding-primary', disabled:available ? null : '', 'data-guide-action':'next' }));
    if (touring && state.step === 7) navigation.push(button(c.example, () => { if (availableTarget()) { mark('completed'); introPractice(); } }, { disabled:available ? null : '', 'data-guide-action':'example' }));
    navigation.push(button(touring ? c.skip : c.practiceSkip, touring ? () => stopTour(true) : () => finishOrSkipPractice(), { 'data-guide-action':'skip' }));
    panel.replaceChildren(node('div', { class:'guide-panel-top' }, node('p', { id:'guide-progress', role:'status', 'aria-live':'polite', 'aria-atomic':'true' }, progress),
      languageControl('guide-language'), button('×', touring ? () => stopTour() : () => finishOrSkipPractice(), { class:'onboarding-close', 'aria-label':c.close, 'data-guide-action':'close' })),
      node('div', { class:'guide-panel-body', tabindex:'0', 'aria-label':c.resume }, body),
      node('nav', { class:'guide-panel-actions', 'aria-label':progress }, navigation));
    panel.hidden = false; panel.dataset.mode = state.mode; panel.dataset.step = String(state.step + 1);
    document.body.classList.add('guide-open'); resizeSpace(); connect({ scroll });
    if (!available) panel.querySelector('.guide-panel-actions').append(button(c.retry, () => renderPanel({ scroll:true }), { 'data-guide-action':'retry' }));
    if (activeLanguage) document.getElementById('guide-language').focus();
    else if (announce) document.getElementById('guide-title').focus({ preventScroll:true });
    announcement.textContent = `${progress}. ${entry[0]}.${available ? '' : ' ' + c.unavailable}`;
  }
  function maybeWelcome() {
    if (state.offered || state.mode || dialog.open || !api.snapshot().valid) return;
    try { if (readPreference(localStorage) || sessionStorage.getItem(ONBOARDING_KEY)) return; } catch {}
    state.offered = true; showDialog('welcome', help);
  }
  function refresh() {
    help.textContent = text().help;
    if (dialog.open) {
      if (state.page === 'welcome' && !api.snapshot().valid) { markSession(); closeDialog({ resume:false }); }
      else { renderDialog(); fitDialog(); }
    } else if (state.mode) {
      const evidenceAppeared = state.mode === 'practice' && state.step === 2 && practiceReady(2, api.snapshot(), state.actions) && panel.dataset.connectedTarget !== 'evidence';
      if (state.mode === 'practice' && practiceReady(state.step, api.snapshot(), state.actions)) state.feedback = false;
      renderPanel({ scroll:evidenceAppeared, announce:evidenceAppeared });
    }
    else maybeWelcome();
  }
  function scheduleRefresh() {
    if (!state.mode || state.scheduled || dialog.open) return;
    state.scheduled = true;
    requestAnimationFrame(() => {
      state.scheduled = false;
      const unavailable = !availableTarget();
      if (unavailable !== state.unavailable) renderPanel();
      else connect();
    });
  }
  help.addEventListener('click', () => { markSession(); showDialog('help', help); });
  dialog.addEventListener('cancel', event => { event.preventDefault(); dismissModal(); });
  dialog.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const controls = [...dialog.querySelectorAll('button:not([disabled]),select:not([disabled]),a[href],input:not([disabled]),[tabindex="0"]')].filter(visible);
    const first = controls[0], last = controls.at(-1), active = document.activeElement;
    if (!first) return;
    if (!controls.includes(active) || (!event.shiftKey && active === last) || (event.shiftKey && active === first)) {
      event.preventDefault(); focus(event.shiftKey ? last : first);
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape' || (!dialog.open && !state.mode)) return;
    event.preventDefault(); event.stopImmediatePropagation();
    if (dialog.open) dismissModal();
    else if (state.mode === 'practice') finishOrSkipPractice();
    else stopTour();
  }, true);
  document.addEventListener('click', event => {
    if (state.mode !== 'practice') return;
    if (state.step === 3 && event.target.closest('[data-provenance-link]')) state.actions.result = true;
    if (state.step === 4 && event.target.closest('[data-source-file="report.json"], [data-provenance-link]')) state.actions.provenance = true;
  });
  new MutationObserver(scheduleRefresh).observe(document.querySelector('main'), { subtree:true, childList:true, attributes:true, attributeFilter:['hidden','style','data-tour-target'] });
  document.addEventListener('focusin', () => requestAnimationFrame(revealFocusedControl));
  const resize = () => { fitDialog(); if (state.mode && !dialog.open) { resizeSpace(); connect({ scroll:true }); revealFocusedControl(); } };
  window.addEventListener('resize', resize);
  window.visualViewport?.addEventListener('resize', resize);
  help.textContent = text().help;
  return { update:refresh, languageChanged:refresh, get active() { return Boolean(dialog.open || state.mode); } };
}
