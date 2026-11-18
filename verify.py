"""생성 HTML의 고정 키, 내부 링크, 에셋, 금지 배포 파일을 확인한다."""
from pathlib import Path
from html.parser import HTMLParser
import json
from src.content import CHAPTERS, SOURCES, META
ROOT = Path(__file__).resolve().parent

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.assets, self.checks = [], [], [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a':
            self.links.append(a.get('href',''))
            assert 'download' not in a, '다운로드 링크 발견'
        if tag in ('link','script') and ('href' in a or 'src' in a): self.assets.append(a.get('src',a.get('href')))
        if a.get('type') == 'checkbox': self.checks.append(a['data-key'])

html = (ROOT/'dist/index.html').read_text(encoding='utf-8')
p=Page(); p.feed(html)
assert len(p.ids) == len(set(p.ids)), '중복 HTML ID'
assert len(p.checks) == len(set(p.checks)), '중복 저장 키'
for link in p.links:
    if link.startswith('#'): assert link[1:] in p.ids, f'없는 앵커: {link}'
for asset in p.assets: assert (ROOT/'dist'/asset).is_file(), f'없는 에셋: {asset}'
for ch in CHAPTERS:
    assert ch['steps'] and ch['checked'] == META['date']
    assert ch['edition'].startswith('Switch 2')
    for key in ch['sources']: assert key in SOURCES
    for step in ch['steps']: assert step['id'] in p.ids
assert set(p.checks) == {s['id'] for ch in CHAPTERS for s in ch['steps']}
assert all('offline' not in f.name.lower() and 'download' not in f.name.lower() for f in (ROOT/'dist').rglob('*'))
assert not list((ROOT/'dist').glob('*service*worker*'))
assert 'lang="ko"' in html and META['version'] in html and META['date'] in html
audit=json.loads((ROOT/'docs/sources.json').read_text(encoding='utf-8'))
assert audit['chapters'] == CHAPTERS
print(json.dumps(dict(result='PASS', chapters=len(CHAPTERS), steps=len(p.checks), ids=len(p.ids), internal_links=sum(l.startswith('#') for l in p.links), assets=len(p.assets)),ensure_ascii=False))
