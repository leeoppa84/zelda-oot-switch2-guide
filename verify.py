"""생성 HTML의 고정 키, 내부 링크, 에셋, 금지 배포 파일을 확인한다."""
from pathlib import Path
from html.parser import HTMLParser
import json
from src.content import CHAPTERS, SOURCES, META
from src.collection import ENTRIES, NEW_SOURCES
import xml.etree.ElementTree as ET
SOURCES.update(NEW_SOURCES)
ROOT = Path(__file__).resolve().parent

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.assets, self.checks, self.collections = [], [], [], [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a':
            self.links.append(a.get('href',''))
            assert 'download' not in a, '다운로드 링크 발견'
        if tag in ('link','script') and ('href' in a or 'src' in a): self.assets.append(a.get('src',a.get('href')))
        if tag == 'img':
            assert a.get('alt'), '대체 텍스트 없는 이미지'
            self.assets.append(a['src'])
        if a.get('type') == 'checkbox':
            if 'data-key' in a: self.checks.append(a['data-key'])
            else: self.collections.append(a['data-collection'])

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
assert audit['entries'] == ENTRIES
assert len(p.collections)==len(set(p.collections))==len(ENTRIES)
assert {x['id'] for x in ENTRIES}==set(p.collections)
assert sum(x['category']=='하트 조각' for x in ENTRIES)==36
for item in ENTRIES:
    assert item['edition'].startswith('Switch 2') and item['sources'] and item['steps']
    for key in item['sources']: assert key in SOURCES
    if item.get('related'): assert item['related'] in p.ids
for svg in (ROOT/'dist/assets/diagrams').glob('*.svg'):
    tree=ET.parse(svg)
    assert tree.getroot().find('{http://www.w3.org/2000/svg}title') is not None
for media in audit['media']:
    assert (ROOT/'dist'/media['path']).is_file()
assert len([m for m in audit['media'] if m['kind']=='공식 소개 화면'])==4
print(json.dumps(dict(result='PASS', chapters=len(CHAPTERS), steps=len(p.checks), collection_entries=len(p.collections), hearts=36, ids=len(p.ids), internal_links=sum(l.startswith('#') for l in p.links), image_uses=len(p.assets)-2, unique_media=len(audit['media'])),ensure_ascii=False))
