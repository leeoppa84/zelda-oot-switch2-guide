"""공략 설명용 SVG 생성. 실제 게임 지도·스크린샷으로 표시하지 않는다."""
from html import escape
from pathlib import Path
import textwrap

def text(x,y,value,size=19,color='#253f34',bold=False):
    lines=textwrap.wrap(value,9) or ['']
    return ''.join(f'<text x="{x}" y="{y+i*25}" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}">{escape(line)}</text>' for i,line in enumerate(lines))

def diagram(path,title,nodes,subtitle):
    rows=(len(nodes)+1)//2
    height=110+rows*115
    body=f'<rect width="480" height="{height}" rx="15" fill="#e8eddf"/>'+f'<text x="22" y="35" font-size="20" font-weight="700" fill="#253f34">{escape(title)}</text>'
    body+=f'<text x="22" y="68" font-size="13" fill="#526654">{escape(subtitle)}</text>'
    for i,node in enumerate(nodes):
        x=16+(i%2)*234; y=90+(i//2)*115
        body+=f'<rect x="{x}" y="{y}" width="222" height="99" rx="9" fill="#fffdf5" stroke="#bac9b1"/><circle cx="{x+24}" cy="{y+26}" r="15" fill="#315b43"/>'
        body+=f'<text x="{x+24}" y="{y+32}" text-anchor="middle" font-size="17" fill="white">{i+1}</text>'+text(x+48,y+30,node,18)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="{height}" viewBox="0 0 480 {height}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><g font-family="Malgun Gothic,Apple SD Gothic Neo,sans-serif">{body}</g></svg>'
    path.write_text(svg,encoding='utf-8')

SPECIAL={
 'deku':('거미줄을 뚫는 순서',['상층에서 나침반','중앙 거미줄로 낙하','지하에서 불 옮기기','데크너츠 2→3→1']),
 'dodongo':('해골의 눈을 여는 순서',['상층 폭탄 주머니','해골 위 다리로 이동','양쪽 눈구멍에 폭탄','열린 입 안으로 진입']),
 'water':('수위별로 확인할 장소',['낮음: 루토 쪽 문양','중간: 중앙 탑 아래','높음: 상층 경로','다크 링크→롱샷','수위 재조절→열쇠','높음: 보스 방']),
 'spirit':('두 시대의 역할 분담',['소년: 왼쪽 구멍','소년: 은 장갑 획득','시간의 신전으로 귀환','청년: 큰 블록 밀기','청년: 거울 방패','빛 반사→보스']),
 'ganon':('리메이크 최종전의 약점',['전반: 꼬리의 약점','마스터 소드 회수','후반: 팔의 붉은 부분','젤다가 힘을 제압','이마 눈에 빛의 화살','마스터 소드 마무리'])
}

def puzzle_diagram(path,key,title):
    """반복 목록 대신 낙하·폭탄·수위·시대의 관계를 도식화한다."""
    start=f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="420" viewBox="0 0 640 420"><title>{escape(title)}</title><defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10" fill="#ad692d"/></marker></defs><rect width="640" height="420" rx="14" fill="#e8eddf"/><g font-family="Malgun Gothic,Apple SD Gothic Neo,sans-serif" fill="#243e32"><text x="25" y="37" font-size="25" font-weight="bold">{escape(title)}</text><text x="25" y="64" font-size="14">원리를 단순화한 설명 그림 · 실제 화면·방 배치 아님</text>'
    if key=='deku':
        body='<path d="M55 120H295M55 220H295M55 290H295" stroke="#7b8b6f" stroke-width="8"/><path d="M165 100V337" stroke="#ad692d" stroke-width="7" marker-end="url(#arrow)"/><ellipse cx="165" cy="287" rx="82" ry="17" fill="#fffdf5" stroke="#9a9c89" stroke-width="3"/><path d="M83 287H247M107 275L226 300M107 300L226 275" stroke="#9a9c89"/><circle cx="165" cy="90" r="16" fill="#315b43"/><text x="340" y="117" font-size="23">① 높은 통로로 이동</text><text x="340" y="225" font-size="23">② 중앙을 향해 낙하</text><text x="340" y="297" font-size="23">③ 거미줄 관통</text><text x="340" y="350" font-size="23">④ 지하 탐색 시작</text><text x="25" y="395" font-size="18">낮은 곳에서 밟거나 검으로 베는 방식이 아닙니다.</text>'
    elif key=='dodongo':
        body='<rect x="95" y="150" width="450" height="190" rx="85" fill="#b7bca8" stroke="#7a866c" stroke-width="4"/><circle cx="225" cy="224" r="39" fill="#e8a351" stroke="#885a2a" stroke-width="4"/><circle cx="415" cy="224" r="39" fill="#e8a351" stroke="#885a2a" stroke-width="4"/><circle cx="320" cy="108" r="20" fill="#343b31"/><path d="M310 119L229 178M330 119L410 178" stroke="#ad692d" stroke-width="5" marker-end="url(#arrow)"/><rect x="268" y="284" width="104" height="56" rx="14" fill="#203a30"/><text x="25" y="114" font-size="19">상층 다리에서</text><text x="25" y="140" font-size="19">폭탄을 떨어뜨림</text><text x="195" y="232" font-size="19">왼쪽</text><text x="386" y="232" font-size="19">오른쪽</text><path d="M320 343V369" stroke="#ad692d" stroke-width="4" marker-end="url(#arrow)"/><text x="170" y="402" font-size="22">두 눈을 켜면 입 안으로 진입</text>'
    elif key=='water':
        body='<rect x="38" y="92" width="255" height="260" rx="10" fill="#f8fcfa" stroke="#587e76" stroke-width="4"/><rect x="40" y="192" width="251" height="158" fill="#9dc9c5"/><path d="M40 115H291M40 192H291M40 282H291" stroke="#3d8079" stroke-width="3" stroke-dasharray="9 7"/><rect x="130" y="174" width="68" height="38" fill="#8c9077"/><path d="M165 223V310" stroke="#ad692d" stroke-width="5" marker-end="url(#arrow)"/><text x="320" y="125" font-size="22">높음 → 상층·롱샷 경로</text><text x="320" y="204" font-size="22">중간 → 중앙 탑</text><text x="320" y="237" font-size="18">뜬 블록 아래로 잠수</text><text x="320" y="293" font-size="22">낮음 → 하층 열쇠 탐색</text><text x="26" y="392" font-size="20">수위·현재 층·열쇠를 함께 확인합니다.</text>'
    elif key=='spirit':
        body='<rect x="30" y="100" width="270" height="230" rx="13" fill="#fffdf5" stroke="#abb99d"/><rect x="340" y="100" width="270" height="230" rx="13" fill="#d4e3df" stroke="#90b4a9"/><text x="110" y="140" font-size="25" font-weight="bold">소년 시대</text><text x="420" y="140" font-size="25" font-weight="bold">청년 시대</text><text x="65" y="195" font-size="23">왼쪽 작은 구멍</text><text x="65" y="250" font-size="23">은 장갑 획득</text><text x="375" y="195" font-size="23">오른쪽 큰 블록</text><text x="375" y="250" font-size="23">거울 방패 획득</text><path d="M280 270H355" stroke="#ad692d" stroke-width="5" marker-end="url(#arrow)"/><text x="78" y="379" font-size="21">시간의 신전에서 전환 → 레퀴엠으로 재방문</text>'
    else:
        return
    path.write_text(start+body+'</g></svg>',encoding='utf-8')

def build_diagrams(root,chapters,entries):
    out=Path(root)/'diagrams';out.mkdir(parents=True,exist_ok=True)
    media=[]
    for ch in chapters:
        title,nodes=SPECIAL.get(ch['id'],(ch['title']+' 진행',ch['route']))
        name='route-'+ch['id']+'.svg'
        diagram(out/name,title,nodes,'설명용 진행도 · 번호 순서 / 실제 방 배치·축척 아님')
        if ch['id'] in ('deku','dodongo','water','spirit'): puzzle_diagram(out/name,ch['id'],title)
        media.append(dict(id='route-'+ch['id'],path='assets/diagrams/'+name,kind='자체 제작 SVG',title=title,sources=ch['sources'],scope='진행 순서 설명 · 실제 지도 아님'))
    regions=list(dict.fromkeys(x['region'] for x in entries if x['category']=='하트 조각'))
    for index,region in enumerate(regions,1):
        nodes=[x['title'] for x in entries if x['region']==region and x['category']=='하트 조각']
        name=f'hearts-{index:02}.svg'
        diagram(out/name,region+' 탐색 지점',nodes,'번호는 아래 목록과 대응 · 위치·방향·거리 미표현')
        media.append(dict(id='hearts-'+region,path='assets/diagrams/'+name,kind='자체 제작 SVG',title=region+' 탐색 지점',sources=list(dict.fromkeys(k for x in entries if x['region']==region and x['category']=='하트 조각' for k in x['sources'])),scope='랜드마크 목록도 · 실제 지도 아님'))
    return media

PHOTOS=[
 dict(id='photo-saria',path='assets/screens/intro_scene_thumb_01.webp',chapter='goron',title='사리아와 소년 링크의 연주 장면',source='official',url='https://www.nintendo.com/kr/games/switch2/aa9ja/assets/img/top/intro_scene_thumb_01.webp'),
 dict(id='photo-master',path='assets/screens/intro_scene_thumb_02.webp',chapter='time',title='마스터 소드를 든 청년 링크',source='official',url='https://www.nintendo.com/kr/games/switch2/aa9ja/assets/img/top/intro_scene_thumb_02.webp'),
 dict(id='photo-ocarina',path='assets/screens/age_scene_thumb_01.webp',chapter=None,title='오카리나를 연주하는 청년 링크',source='official',url='https://www.nintendo.com/kr/games/switch2/aa9ja/assets/img/top/age_scene_thumb_01.webp'),
 dict(id='photo-epona',path='assets/screens/age_scene_thumb_02.webp',chapter=None,title='목장의 에포나와 소년 링크',source='official',url='https://www.nintendo.com/kr/games/switch2/aa9ja/assets/img/top/age_scene_thumb_02.webp')]
for photo in PHOTOS:
    photo.update(kind='공식 소개 화면',rights_holder='Nintendo',checked='2026-11-18',scope='상황 참고 장면 · 세부 위치를 표시한 화면 아님')
