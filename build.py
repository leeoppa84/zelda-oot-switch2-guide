"""의존성 없는 GitHub Pages 빌드. 원본은 src/, 공개 파일은 dist/."""
from pathlib import Path
import json
import shutil
from urllib.parse import urlparse
from html import escape as e
from src.content import META, SOURCES, CHAPTERS, EXTRAS

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
OUT.mkdir(exist_ok=True)

def nav():
    out = ''
    era = None
    for i, ch in enumerate(CHAPTERS, 1):
        if ch['era'] != era:
            era = ch['era']
            out += f'<p class="navtitle">{e(era)} 링크</p>'
        out += f'<a href="#{ch["id"]}"><span class="num">{i:02}</span><span>{e(ch["title"])}</span><span class="done" data-progress="{ch["id"]}">0/{len(ch["steps"])}</span></a>'
    return out + '<a href="#notes">기본 정보·수집 안내</a><a href="#sources">출처·적용 범위</a>'

cards = []
md = [f'# {META["title"]} 한국어 공략', f'\nNintendo Switch 2 리메이크 · v{META["version"]} · {META["date"]}\n', '> 메인 스토리 진행 요약. 후반 스포일러 포함. 실기 전체 검증·수집품 전수 공략 아님.\n']
for i, ch in enumerate(CHAPTERS, 1):
    steps = ''.join(f'<li class="step" id="{s["id"]}"><label><input type="checkbox" data-key="{s["id"]}"><span>{e(s["title"])}</span></label><p>{e(s["body"])}</p></li>' for s in ch['steps'])
    boss = f'<div class="boss"><h4>보스 · {e(ch["boss"]["name"])}</h4><p>{e(ch["boss"]["strategy"])}</p></div>' if ch['boss'] else ''
    cards.append(f'''<details class="chapter" id="{ch['id']}" {'open' if i == 1 else ''}>
    <summary><span class="chapter-no">{i:02}</span><div><span class="tag">{e(ch['era'])}</span><h3>{e(ch['title'])}</h3></div><span class="summary-progress">0/{len(ch['steps'])}</span></summary>
    <div class="chapter-inner"><p class="goal">{e(ch['goal'])}</p><p class="need">준비 · {e(' / '.join(ch['need']))}</p>
    <div class="route" aria-label="진행 순서">{''.join(f'<span>{e(x)}</span>' for x in ch['route'])}</div><ol class="steps">{steps}</ol>
    <aside class="tip"><strong>막힐 때 확인</strong>{e(ch['tip'])}</aside>{boss}<p class="reward"><strong>완료 후</strong> · {e(ch['reward'])}</p>
    </div></details>''')
    md += [f'\n## {i:02}. {ch["title"]} — {ch["era"]}\n',f'목표: {ch["goal"]}\n\n준비: {" / ".join(ch["need"])}\n',f'진행: {" → ".join(ch["route"])}\n']
    for s in ch['steps']:
        md += [f'- [ ] **{s["title"]}**: {s["body"]}']
    md += [f'\n막힐 때: {ch["tip"]}\n']
    if ch['boss']:
        md += [f'보스 — {ch["boss"]["name"]}: {ch["boss"]["strategy"]}\n']
    md += [f'완료 후: {ch["reward"]}\n',f'확인 상태: {ch["status"]}\n', '참고: ' + ' · '.join(f'[{SOURCES[k][0]}]({SOURCES[k][1]})' for k in ch['sources']) + '\n']

extra_html = ''.join(f'<article class="extra" id="note-{x["id"]}"><h3>{e(x["title"])}</h3><p>{e(x["text"])}</p></article>' for x in EXTRAS)
used = list(dict.fromkeys(['official','dev','interview'] + [k for ch in CHAPTERS for k in ch['sources']] + [k for x in EXTRAS for k in x['sources']]))
groups = [
    ('i-njoy.net', 'nJOY', '일본어 리메이크 전용 공략 · 핵심 진행·던전'),
    ('gamewith.jp', 'GameWith', '일본어 리메이크 전용 공략 · 후반 신전·보스'),
    ('ootguide.com', 'OoT Guide', '한국어 제공 공략 · GameWith 재가공 부분은 독립 검증에서 제외'),
    ('www.nintendo.com', '한국닌텐도', '한국어 공식 · 판본·개발·변경점'),
    ('gamereviewkr.tistory.com', '정직한 게임 리뷰어', '한국어 개인 공략 · 초반 내용 대조'),
]
source_counts = [(name, sum(urlparse(SOURCES[k][1]).netloc == domain for k in used)) for domain, name, _ in groups]
largest_name, largest_count = max(source_counts, key=lambda item: item[1])
source_html = ''
for domain, name, note in groups:
    keys = [k for k in used if urlparse(SOURCES[k][1]).netloc == domain]
    links = ''.join(f'<li id="source-{k}"><a href="{e(SOURCES[k][1])}" target="_blank" rel="noopener noreferrer">{e(SOURCES[k][0].split(" · ",1)[-1])} ↗</a></li>' for k in keys)
    source_html += f'<details class="source-group"><summary><strong>{name}</strong><span>{len(keys)}개 문서</span></summary><p>{note}</p><ul>{links}</ul></details>'

total = sum(len(ch['steps']) for ch in CHAPTERS)
data = json.dumps(CHAPTERS, ensure_ascii=False).replace('</','<\\/')
html = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="시간의 오카리나 Switch 2 리메이크 한국어 메인 스토리 공략. 준비물, 던전, 보스와 진행 체크."><meta name="theme-color" content="#133e32"><title>시간의 오카리나 · Switch 2 한국어 공략</title><link rel="stylesheet" href="./style.css"><script src="./app.js" defer></script></head><body id="top">
<a class="skip" href="#walkthrough">본문으로 건너뛰기</a><header class="mast"><div class="topline"><span>게임 공략 노트 / 01</span><span class="platform">Nintendo Switch 2 · 2026 리메이크</span></div><div class="seal" aria-hidden="true"></div><div class="hero"><div class="eyebrow">두 시대를 잇는 모험</div><h1><small>젤다의 전설</small>시간의 오카리나</h1><p>다음에 어디로 가야 할지 막막할 때.<br>소년의 숲에서 마지막 전투까지, 진행 순서와 해법을 한국어로 따라갑니다.</p><a class="primary" href="#kokiri" id="resume">처음부터 공략 보기 →</a><div class="metrics"><span><strong>{len(CHAPTERS):02}</strong>개 장</span><span><strong>{total}</strong>개 진행 체크</span><span>메인 스토리 · 보스</span></div></div></header>
<noscript><p class="nojs">본문은 읽을 수 있습니다. 검색과 진행 저장은 자바스크립트를 켜야 사용할 수 있습니다.</p></noscript>
<nav class="view-tabs" aria-label="공략집 탭" role="tablist"><a id="tab-guide" href="#guide-panel" role="tab" aria-controls="guide-panel" aria-selected="true">공략</a><a id="tab-sources" href="#sources" role="tab" aria-controls="sources" aria-selected="false">출처</a></nav>
<div class="toolbar" id="guide-tools"><div class="tools"><label class="searchbox"><span>검색</span><input type="search" id="search" placeholder="장소, 장비, 보스 이름" aria-label="장소, 장비, 보스 검색"></label><select id="era" aria-label="시대 선택"><option value="">모든 시대</option><option>소년</option><option>청년</option><option>전환</option><option>두 시대</option></select></div><div class="tool-meta"><span id="result-count" aria-live="polite">{len(CHAPTERS)}개 장 표시</span><span id="storage-status" role="status">진행 체크는 이 브라우저에 저장됩니다.</span></div></div>
<div class="layout"><aside class="sidebar"><div class="navheading">모험의 순서</div><nav class="nav" aria-label="공략 목차">{nav()}</nav><div class="sidebar-bottom">v{META['version']} · {META['date']}<br>한국어 자료 + 일본어 자료 대조</div></aside><main><div id="guide-panel" role="tabpanel" aria-labelledby="tab-guide"><details class="mobile-nav" id="mobile-menu"><summary>목차 열기 · {len(CHAPTERS)}개 장</summary><nav class="nav" aria-label="모바일 공략 목차">{nav()}</nav></details>
<div class="notice"><strong>읽기 전에</strong> · Switch 2판 메인 스토리 요약 공략입니다. 후반 지역과 보스의 스포일러가 포함됩니다. 한국판 실기 검증과 세부 명칭 대조는 진행 전이며, 100% 수집 공략은 포함하지 않습니다.</div>
<section id="walkthrough"><h2 class="intro-title">모험을 계속할 차례</h2><p class="sub">장을 펼쳐 다음 행동을 확인하고, 끝낸 단계만 체크하세요.</p><div class="controls"><span id="total-progress" aria-live="polite">0 / {total}단계 완료</span><div><button id="expand" type="button">모두 펼치기</button> <button id="collapse" type="button">모두 접기</button></div></div><div class="progressline" aria-hidden="true"><div id="progress-fill"></div></div><div id="empty" class="empty" hidden><strong>검색 결과가 없습니다.</strong><p>다른 장소 이름이나 장비 이름으로 찾아보세요.</p></div><button id="clear-search" type="button" hidden>검색·필터 초기화</button>{''.join(cards)}</section>
<section class="extras" id="notes"><h2>모험을 돕는 메모</h2>{extra_html}</section></div><section class="sources" id="sources" role="tabpanel" aria-labelledby="tab-sources"><h2>참고한 자료</h2><p class="sub">5개 사이트 · {len(used)}개 문서 · 확인 {META["date"]}<br>일본어 자료는 한국어로 요약했습니다. 한국판 실기·세부 명칭은 전체 대조 전입니다.</p><p class="source-overview">문서 수 기준 <strong>{e(largest_name)} {largest_count}개</strong>가 가장 많습니다. OoT Guide는 GameWith를 인용한 부분이 있어 독립 근거로 중복 계산하지 않습니다.</p>{source_html}</section></main></div>
<footer><span>제작·정리 {e(META['author'])}{(' · <a href="' + e(META['blog_url']) + '" target="_blank" rel="noopener">네이버 블로그</a>') if META.get('blog_url') else ''} · v{META['version']} · {META['date']}</span><span>비공식 팬 공략 · 게임의 권리는 Nintendo 등 해당 권리자에게 있습니다.</span></footer><a class="backtop" href="#top" aria-label="페이지 맨 위로">위로 ↑</a><script type="application/json" id="guide-data">{data}</script></body></html>'''
(OUT / 'index.html').write_text(html, encoding='utf-8')
for name in ['style.css','app.js']:
    shutil.copy2(ROOT / 'src' / name, OUT / name)
(OUT / '.nojekyll').write_text('', encoding='utf-8')
for x in EXTRAS:
    md += [f'\n## {x["title"]}\n\n{x["text"]}\n']
(ROOT / 'docs' / '한국어_공략_v0.1.md').write_text('\n'.join(md),encoding='utf-8')
(ROOT / 'docs' / 'sources.json').write_text(json.dumps(dict(meta=META,sources={k:dict(title=v[0],url=v[1],language=v[2],scope=v[3],checked=META['date']) for k,v in SOURCES.items()},chapters=CHAPTERS), ensure_ascii=False,indent=2),encoding='utf-8')
print(f'빌드 완료: {len(CHAPTERS)}개 장, {total}개 단계 / {OUT}')
