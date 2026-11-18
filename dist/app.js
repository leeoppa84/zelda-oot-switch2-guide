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
  const entries = JSON.parse(document.querySelector('#collection-data').textContent);
  const entryById = new Map(entries.map(item => [item.id,item]));
  const entryCards = [...document.querySelectorAll('.reference-entry')];
  const catalogKey = 'zelda-oot-switch2:collection:v1';
  const validCatalogIds = new Set(entries.map(item => item.id));
  let acquired = new Set();
  try {
    const saved = JSON.parse(localStorage.getItem(catalogKey) || '[]');
    if (Array.isArray(saved)) acquired = new Set(saved.filter(id => validCatalogIds.has(id)));
  } catch { storage.textContent = '수집 기록을 읽지 못했습니다. 이번 화면에서만 체크할 수 있습니다.'; }
  function collectionProgress() {
    document.querySelectorAll('.collection-check').forEach(input => {
      input.checked = acquired.has(input.dataset.collection);
      input.closest('.catalog-card').classList.toggle('acquired',input.checked);
    });
    document.querySelector('#collection-progress').textContent = `수집·이벤트 ${acquired.size}개 체크`;
  }
  document.querySelectorAll('.collection-check').forEach(input => input.addEventListener('change',()=>{
    if (input.checked) acquired.add(input.dataset.collection); else acquired.delete(input.dataset.collection);
    try { localStorage.setItem(catalogKey,JSON.stringify([...acquired])); }
    catch { storage.textContent='수집 기록을 저장하지 못했습니다. 창을 닫으면 사라질 수 있습니다.'; }
    collectionProgress(); filter();
  }));
  const search = document.querySelector('#search');
  const era = document.querySelector('#era');
  const region = document.querySelector('#region');
  const panelIds = ['guide','equipment','quests','collectibles','secrets','sources'];
  const panel = id => document.querySelector(id==='sources'?'#sources':`#${id}-panel`);
  let active = 'guide';
  let openBeforeSearch = null;
  const matchesEra = value => !era.value || value===era.value || value==='두 시대' || (value==='소년→청년' && ['소년','청년','전환','두 시대'].includes(era.value));
  function filter() {
    const q = search.value.normalize('NFKC').toLocaleLowerCase().trim();
    let count = 0;
    if (q && openBeforeSearch === null) openBeforeSearch = new Set(chapters.filter(ch => ch.open).map(ch => ch.id));
    chapters.forEach((ch,i)=>{
      const item=DATA[i];
      const match=(!q || JSON.stringify(item).normalize('NFKC').toLocaleLowerCase().includes(q)) && matchesEra(item.era);
      ch.hidden=!match;
      if (match && q) ch.open=true;
      if (!q && openBeforeSearch!==null) ch.open=openBeforeSearch.has(ch.id);
      if (match && active==='guide') count++;
    });
    if (!q) openBeforeSearch=null;
    entryCards.forEach(card=>{
      const item=entryById.get(card.dataset.entry);
      const match=(!q || JSON.stringify(item).normalize('NFKC').toLocaleLowerCase().includes(q)) && matchesEra(item.era) && (!region.value || region.value===item.region);
      card.hidden=!match;
      if(match && q) card.open=true;
      if(match && card.closest('[role=tabpanel]')===panel(active)) count++;
    });
    document.querySelectorAll('.region-block').forEach(block=>{
      const visible=[...block.querySelectorAll('.reference-entry')].some(card=>!card.hidden);
      block.hidden=!visible;
      if(visible && (q || region.value || era.value)) block.open=true;
    });
    document.querySelector('#result-count').textContent=active==='guide'?`${count}개 장 표시`:`${count}개 항목 표시`;
    document.querySelector('#empty').hidden=count!==0 || active!=='guide';
    document.querySelector('#clear-search').hidden=!q && !era.value;
    document.querySelectorAll('.catalog-panel').forEach(p=>{
      const cards=[...p.querySelectorAll('.reference-entry')];
      const visible=cards.filter(card=>!card.hidden);
      p.querySelector('.catalog-empty').hidden=visible.length!==0;
      p.querySelector('.catalog-status').textContent=`전체 ${cards.length}개 · 현재 ${visible.length}개 · 체크 ${cards.filter(card=>acquired.has(card.id)).length}개`;
    });
  }
  search.addEventListener('input',filter);era.addEventListener('change',filter);region.addEventListener('change',filter);
  document.querySelector('#clear-search').addEventListener('click',()=>{search.value='';era.value='';region.value='';filter();search.focus();});
  document.querySelector('#expand').addEventListener('click',()=>chapters.filter(ch=>!ch.hidden).forEach(ch=>{ch.open=true;}));
  document.querySelector('#collapse').addEventListener('click',()=>chapters.forEach(ch=>{ch.open=false;}));
  function setView(id) {
    active=id;
    panelIds.forEach(name=>{
      panel(name).hidden=name!==id;
      document.querySelector(`#tab-${name}`).setAttribute('aria-selected',String(name===id));
    });
    document.querySelector('#guide-tools').hidden=id==='sources';
    document.querySelector('.layout').classList.toggle('sources-view',id!=='guide');
    region.hidden=['guide','sources'].includes(id);
    filter();
  }
  const tabs=[...document.querySelectorAll('.view-tabs a')];
  tabs.forEach((link,index)=>link.addEventListener('keydown',event=>{
    if(['ArrowLeft','ArrowRight','Home','End'].includes(event.key)){
      event.preventDefault();
      let next=event.key==='Home'?0:event.key==='End'?tabs.length-1:(index+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;
      tabs[next].focus();tabs[next].click();
    }
  }));
  function revealHash() {
    let hash;try{hash=decodeURIComponent(location.hash.slice(1));}catch{return;}
    const target=document.getElementById(hash);if(!target)return;
    if(hash!=='top'){
      const owner=target.closest('[role=tabpanel]');
      const id=owner?(owner.id==='sources'?'sources':owner.id.replace('-panel','')):'guide';
      if(target.classList.contains('reference-entry') || target.closest('.chapter')){search.value='';era.value='';region.value='';}
      setView(id);
      let details=target.closest('details');
      while(details){details.open=true;details=details.parentElement.closest('details');}
    }
    document.querySelector('#mobile-menu').open=false;
    requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
  }
  addEventListener('hashchange',revealHash);
  document.querySelectorAll('a[href^="#"]').forEach(link=>link.addEventListener('click',()=>{if(link.hash===location.hash)revealHash();}));
  collectionProgress();updateProgress();setView('guide');if(location.hash)revealHash();
})();
