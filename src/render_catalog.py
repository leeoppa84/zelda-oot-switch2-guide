from html import escape as e
import json
from src.collection import ENTRIES, MASKS
from src.illustrations import PHOTOS

PANELS=[('equipment','장비','장비·도구','입수처와 활용 조건을 확인하고, 얻은 장비를 체크하세요.'),('quests','서브 퀘스트','서브 퀘스트','가면·교환·이동·강화 이벤트를 순서대로 정리했습니다.'),('collectibles',None,'지역별 하트·보물상자','하트 조각 36개 항목과 핵심 보물상자 목록입니다. 모든 루피·열쇠 상자의 전수 목록은 아닙니다.'),('secrets','숨겨진 요소','숨겨진 요소','시대 연계·숨은 구멍·부가 상호작용을 모았습니다.')]

def figure(path,title,kind='설명용 그림'):
    return f'<figure class="guide-figure"><a href="./{e(path)}" target="_blank" rel="noopener" aria-label="{e(title)} 크게 보기"><img src="./{e(path)}" alt="{e(title)}" loading="lazy"></a><figcaption>{kind} · {e(title)} · 눌러서 크게 보기</figcaption></figure>'

def card(item,number=None):
    prefix=f'{number:02} · ' if number else ''
    related=f'<a class="related-link" href="#{e(item["related"])}">관련 공략 보기 →</a>' if item.get('related') else ''
    notes=f'<p>{e(item["note"])}</p>' if item.get('note') else ''
    masks='<div class="mask-grid">'+''.join(f'<div><strong>{e(name)}</strong><span>{e(effect)}</span></div>' for name,effect in MASKS)+'</div>' if item['id']=='quest-masks' else ''
    photo_id={'quest-epona':'photo-epona','secret-cow':'photo-ocarina'}.get(item['id'])
    photo=next((p for p in PHOTOS if p['id']==photo_id),None)
    media=figure(photo['path'],photo['title'],'공식 소개 화면 · © Nintendo / 위치 참고용 아님') if photo else ''
    return f'''<details class="catalog-card reference-entry" id="{item['id']}" data-entry="{item['id']}"><summary><span class="entry-kind">{e(item['category'])}</span><strong>{prefix}{e(item['title'])}</strong><span class="entry-mark" aria-hidden="true"></span></summary><div class="catalog-body"><p class="entry-location">{e(item['region'])} · {e(item['era'])}</p><p class="entry-need">조건 · {e(item['need'])}</p>{media}<ol>{''.join(f'<li>{e(step)}</li>' for step in item['steps'])}</ol>{masks}{notes}<p class="entry-reward">보상·활용 · {e(item['reward'])}</p><div class="entry-actions"><label><input type="checkbox" class="collection-check" data-collection="{item['id']}"> 획득·완료 체크</label>{related}</div></div></details>'''

def panels(media):
    out=''
    for id,category,title,description in PANELS:
        items=[x for x in ENTRIES if x['category'] in ('하트 조각','보물상자')] if id=='collectibles' else [x for x in ENTRIES if x['category']==category]
        content=''
        if id=='collectibles':
            regions=list(dict.fromkeys(x['region'] for x in items))
            for i,region in enumerate(regions):
                hearts=[x for x in items if x['region']==region and x['category']=='하트 조각']
                chests=[x for x in items if x['region']==region and x['category']=='보물상자']
                heart_chests=[x for x in hearts if x.get('container')=='보물상자']
                chest_links=''.join(f'<a class="heart-chest-link" href="#{x["id"]}">하트 상자 · {e(x["title"])} →</a>' for x in heart_chests)
                diagram=next((m for m in media if m['id']=='hearts-'+region),None)
                image=figure(diagram['path'],diagram['title'],'탐색 기준점 · 실제 지도 아님') if diagram else ''
                content+=f'<details class="region-block" data-region="{e(region)}" {"open" if i==0 else ""}><summary><strong>{e(region)}</strong><span>하트 {len(hearts)} · 상자 {len(chests)+len(heart_chests)}</span></summary><div class="region-body">{image}{"<h3>하트 조각</h3>" if hearts else ""}{"".join(card(x,n) for n,x in enumerate(hearts,1))}{"<h3>보물상자</h3>" if chests or heart_chests else ""}{chest_links}{"".join(card(x) for x in chests)}</div></details>'
        else:
            content=''.join(card(x) for x in items)
        out+=f'''<section id="{id}-panel" class="catalog-panel" role="tabpanel" aria-labelledby="tab-{id}" hidden><h2>{title}</h2><p class="sub">{description}</p><p class="catalog-status" data-panel-status="{id}"></p><p class="catalog-empty" hidden>해당 조건의 항목이 없습니다. 검색어나 지역·시대 필터를 바꿔 보세요.</p>{content}</section>'''
    return out

def data_script():
    return '<script type="application/json" id="collection-data">'+json.dumps(ENTRIES,ensure_ascii=False).replace('</','<\\/')+'</script>'
