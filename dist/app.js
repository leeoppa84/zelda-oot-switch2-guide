'use strict';
(() => {
  const DATA = JSON.parse(document.querySelector('#guide-data').textContent);
  const chapters = [...document.querySelectorAll('.chapter')];
  const steps = [...document.querySelectorAll('.step input')];
  const ids = new Set(steps.map(input => input.dataset.key));
  const key = 'zelda-oot-switch2:progress:v1';
  let checked = new Set();
  const storage = document.querySelector('#storage-status');
  try {
    const saved = JSON.parse(localStorage.getItem(key) || '[]');
    if (Array.isArray(saved)) checked = new Set(saved.filter(id => typeof id === 'string' && ids.has(id)));
  } catch { storage.textContent = '저장 기록을 읽지 못했습니다. 이번 화면의 체크만 사용합니다.'; storage.className = 'storage-error'; }
  steps.forEach(input => { input.checked = checked.has(input.dataset.key); });
  function updateProgress() {
    steps.forEach(input => input.closest('.step').classList.toggle('checked', input.checked));
    chapters.forEach(ch => {
      const list = [...ch.querySelectorAll('input')];
      const done = list.filter(input => input.checked).length;
      ch.querySelector('.summary-progress').textContent = `${done}/${list.length}`;
      document.querySelectorAll(`[data-progress="${ch.id}"]`).forEach(el => { el.textContent = `${done}/${list.length}`; });
    });
    document.querySelector('#total-progress').textContent = `${checked.size} / ${steps.length}단계 완료`;
    document.querySelector('#progress-fill').style.width = `${checked.size / steps.length * 100}%`;
    const next = steps.find(input => !input.checked);
    const resume = document.querySelector('#resume');
    resume.href = next ? `#${next.dataset.key}` : '#walkthrough';
    resume.textContent = next ? '이어서 공략 보기 →' : '전체 진행 다시 보기 →';
  }
  steps.forEach(input => input.addEventListener('change', () => {
    if (input.checked) checked.add(input.dataset.key); else checked.delete(input.dataset.key);
    try { localStorage.setItem(key, JSON.stringify([...checked])); storage.textContent = '진행 체크는 이 브라우저에 저장됩니다.'; storage.className = ''; }
    catch { storage.textContent = '저장할 수 없습니다. 창을 닫으면 체크가 사라질 수 있습니다.'; storage.className = 'storage-error'; }
    updateProgress();
  }));
  const search = document.querySelector('#search');
  const era = document.querySelector('#era');
  let openBeforeSearch = null;
  function filter() {
    const q = search.value.normalize('NFKC').toLocaleLowerCase().trim();
    let count = 0;
    if (q && openBeforeSearch === null) openBeforeSearch = new Set(chapters.filter(ch => ch.open).map(ch => ch.id));
    chapters.forEach((ch, i) => {
      const item = DATA[i];
      const match = (!q || JSON.stringify(item).normalize('NFKC').toLocaleLowerCase().includes(q)) && (!era.value || item.era === era.value || item.era === '두 시대');
      ch.hidden = !match;
      if (match) { count++; if (q) ch.open = true; }
      if (!q && openBeforeSearch !== null) ch.open = openBeforeSearch.has(ch.id);
    });
    if (!q) openBeforeSearch = null;
    document.querySelector('#result-count').textContent = `${count}개 장 표시`;
    document.querySelector('#empty').hidden = count !== 0;
    document.querySelector('#clear-search').hidden = !q && !era.value;
  }
  search.addEventListener('input', filter);
  era.addEventListener('change', filter);
  document.querySelector('#clear-search').addEventListener('click', () => { search.value = ''; era.value = ''; filter(); search.focus(); });
  document.querySelector('#expand').addEventListener('click', () => chapters.filter(ch => !ch.hidden).forEach(ch => { ch.open = true; }));
  document.querySelector('#collapse').addEventListener('click', () => chapters.forEach(ch => { ch.open = false; }));
  const guidePanel = document.querySelector('#guide-panel');
  const sourcePanel = document.querySelector('#sources');
  function setView(isSources) {
    guidePanel.hidden = isSources;
    sourcePanel.hidden = !isSources;
    document.querySelector('#guide-tools').hidden = isSources;
    document.querySelector('.layout').classList.toggle('sources-view', isSources);
    document.querySelector('#tab-guide').setAttribute('aria-selected', String(!isSources));
    document.querySelector('#tab-sources').setAttribute('aria-selected', String(isSources));
  }
  document.querySelectorAll('.view-tabs a').forEach(link => link.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      const other = document.querySelector(link.id === 'tab-guide' ? '#tab-sources' : '#tab-guide');
      other.focus(); other.click();
    }
  }));
  function revealHash() {
    let hash;
    try { hash = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(hash);
    if (!target) return;
    if (sourcePanel.contains(target)) {
      setView(true);
      const group = target.closest('.source-group');
      if (group) group.open = true;
    } else if (hash !== 'top') setView(false);
    const parent = target.closest('.chapter');
    if (parent) { search.value = ''; era.value = ''; filter(); parent.open = true; parent.hidden = false; }
    document.querySelector('#mobile-menu').open = false;
    requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
  }
  addEventListener('hashchange', revealHash);
  document.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener('click', () => { if (link.hash === location.hash) revealHash(); }));
  setView(false); updateProgress(); filter(); if (location.hash) revealHash();
})();
