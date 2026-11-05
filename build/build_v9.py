# 클로드 디자인 v2(design/v9/app.dc.html)를 기존 데이터·기능에 연결해 내보냄.
#  - 화면(마크업)은 디자인 파일 그대로. 시안용 요소(가짜 상태바·가짜 지도·예시 숫자)만 실제 것으로 교체.
#  - 데이터·기능은 기존 앱(index.html)의 로직을 그대로 가져와 씀.
#  - 사용: python3 build/build_v9.py [출력폴더(기본 new)]
import os, sys, re, shutil, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'design', 'v9', 'app.dc.html')
OUT = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else '.')
dc = open(SRC, encoding='utf-8').read()
old = open(os.path.join(ROOT, 'old', 'index.html'), encoding='utf-8').read()
v8src = open(os.path.join(HERE, 'build_v8.py'), encoding='utf-8').read()


def rep(a, b, cnt=1, src=None):
    global dc
    s = dc if src is None else src
    assert s.count(a) == cnt, (s.count(a), a[:140])
    s = s.replace(a, b)
    if src is None:
        dc = s
    return s


def tx(a, b, cnt=1):
    rep('>' + a + '<', '>' + b + '<', cnt)


WIDE = "(typeof window !== 'undefined' && window.innerWidth >= 640)"
# ───────────────────────── 1. 화면 틀 ─────────────────────────
rep("box-shadow:0 30px 60px rgba(40,40,90,.18);", "")
# 시안용 가짜 상태바 제거
i = dc.index('<b style="font-size:14px">14:20</b>')
a0 = dc.rindex('<div style="position:absolute;left:0;right:0;top:0;height:44px;', 0, i)
a1 = dc.index('</div>', i) + 6
dc = dc[:a0] + dc[a1:]
SAT, SAB = 'env(safe-area-inset-top)', 'env(safe-area-inset-bottom)'
rep('padding:52px 0 200px', 'padding:calc(%s + 12px) 0 calc(%s + 168px)' % (SAT, SAB))
rep('padding:52px 0 110px', 'padding:calc(%s + 12px) 0 calc(%s + 110px)' % (SAT, SAB))
rep('padding:52px 20px 26px', 'padding:calc(%s + 12px) 20px calc(%s + 26px)' % (SAT, SAB))
rep('padding:52px 16px 14px', 'padding:calc(%s + 12px) 16px 14px' % SAT)
rep('left:16px;top:52px;width:48px', 'left:16px;top:calc(%s + 12px);width:48px' % SAT)
rep('left:74px;top:60px;', 'left:74px;top:calc(%s + 20px);' % SAT)
rep('left:12px;right:12px;top:50px;z-index:20', 'left:12px;right:12px;top:calc(%s + 10px);z-index:20' % SAT)
rep('right:0;top:54px;z-index:2;', 'right:0;top:calc(%s + 14px);z-index:2;' % SAT)
rep('left:12px;right:12px;bottom:16px;z-index:5', 'left:12px;right:12px;bottom:calc(%s + 14px);z-index:5' % SAB)
rep('left:12px;right:12px;bottom:98px;z-index:5', 'left:12px;right:12px;bottom:calc(%s + 96px);z-index:5' % SAB)
rep('right:16px;bottom:200px;', 'right:16px;bottom:calc(%s + 200px);' % SAB)
rep('right:16px;bottom:22px;', 'right:16px;bottom:calc(%s + 22px);' % SAB, cnt=2)

# 아이콘 글꼴: 새로 쓰는 아이콘 추가 (이름 순서대로)
m = re.search(r'icon_names=([a-z_,0-9]+)', dc)
names = set(m.group(1).split(',')) | {'south', 'north', 'savings', 'calendar_month', 'today', 'favorite', 'straighten', 'schedule', 'my_location', 'footprint', 'route', 'directions_walk', 'grid_view', 'edit_calendar', 'open_in_new', 'timer', 'flag', 'local_fire_department', 'thermostat', 'partly_cloudy_day', 'foggy', 'thunderstorm', 'umbrella', 'wb_twilight', 'delete', 'edit', 'close', 'expand_less', 'refresh', 'restart_alt', 'swap_vert', 'translate', 'watch', 'train', 'today', 'info', 'warning', 'add', 'remove', 'search', 'water_drop', 'air', 'undo', 'arrow_forward', 'visibility', 'keyboard_arrow_up', 'keyboard_arrow_down'}
dc = dc.replace(m.group(0), 'icon_names=' + ','.join(sorted(names)))

# ───────────────────────── 2. 문서 머리 (v8 빌드의 것을 그대로) ─────────────────────────
DEMO = v8src[v8src.index("DEMO = r'''") + len("DEMO = r'''"):]
DEMO = DEMO[:DEMO.index("'''\n")]
DEMO = DEMO.replace("JSON.stringify({ stage: 3, bodyLog: { '2026-12-15': { 'foot': 2, 'back': 1, 'tired': 2 } },",
  "JSON.stringify({ stage: 3, stageDate: '2026-12-15', walk: 'walking', wsrc: 'watch', wDay: '2026-12-15', wStart: 1797295680000, bodyLog: { '2026-12-15': { '발바닥': 2, '무릎': 1, '종아리': 3, '어깨': 0, '피로': 2 }, '2026-12-14': { '발바닥': 3, '무릎': 1, '종아리': 2, '어깨': 1, '피로': 3 }, '2026-12-13': { '발바닥': 1, '무릎': 1, '종아리': 1, '어깨': 0, '피로': 2 } },")
assert "wStart: 1797295680000" in DEMO
head_shim = old[old.index('<script>(function(){var F=\'.image-slots.state.json\''):]
head_shim = head_shim[:head_shim.index('</script>') + 9]
rep('<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">' + DEMO + '<title>도카이도 53의 쉼표</title>'
    '<meta name="theme-color" content="#DCE2FF"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes">'
    '<meta name="apple-mobile-web-app-status-bar-style" content="default">'
    '<link rel="manifest" href="/manifest.json"><link rel="icon" href="/icon-192.png"><link rel="apple-touch-icon" href="/icon-180.png">'
    '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'
    '<script src="./image-slot.js"></script><style>image-slot.ro{display:none}image-slot.ro::part(empty){display:none!important}html,body{overscroll-behavior:none;-webkit-text-size-adjust:100%;overflow-x:hidden;touch-action:pan-y;background:#DCE2FF}[data-v8map] .leaflet-control-attribution{display:none}[data-v8map]{isolation:isolate;z-index:0}textarea{font-family:inherit}</style>'
    + head_shim)

# ───────────────────────── 3. 마크업: 시안 숫자 → 실제 값 ─────────────────────────
# 히어로
rep("background:#5B6FD4 url('assets/tk-fuji-sea.avif') center 30%/cover", "background:#5B6FD4 url('{{ hr.photo }}') center 40%/cover")
rep('>DAY 12<span', '>DAY {{ hr.day }}<span')
rep('>sunny</span>18°<span style="font-weight:600;opacity:.8;margin-left:2px">/ 최저 9°</span>', '>{{ hr.wx.icon }}</span>{{ hr.wx.t }}<span style="font-weight:600;opacity:.8;margin-left:2px">/ 최저 {{ hr.wx.lo }}</span>')
tx('기록 저장', '닫기')
tx('오늘 · 11월 3일 화요일', '{{ hr.when }}')
tx('마리코 → 후지에다', '{{ hr.title }}', cnt=2) if False else None
rep('line-height:1.12">마리코 → 후지에다</b>', 'line-height:1.12">{{ hr.title }}</b>')
tx('丸子宿 → 藤枝宿 · 경유지 3곳', '{{ hr.jpl }}')
tx('마리코 宿', '{{ pg.a }}'); tx('후지에다 宿', '{{ pg.b }}')
# 숙소 카드
rep("filter:{{ dkImg }};background:url('assets/tk-onsen.jpg') center/cover no-repeat", "filter:{{ dkImg }};background:url('{{ hr.photo }}') center/cover no-repeat")
rep('>TONIGHT · 오늘 밤 숙소<', '>{{ lodge.when }}<')
tx('후지에다 역 앞 비즈니스호텔', '{{ lodge.name }}')
tx('藤枝駅前 · 체크인 15:00 · 1박 ¥7,800', '{{ lodge.sub }}')
rep('padding:4px 9px;border-radius:99px;background:#E4F8EC;color:#16804A">예약 확정</span><a href="https://www.google.com/maps/dir/?api=1&amp;travelmode=walking&amp;destination=%E8%97%A4%E6%9E%9D%E9%A7%85"',
    'padding:4px 9px;border-radius:99px;background:{{ lodge.cb }};color:{{ lodge.cf }}">{{ lodge.chip }}</span><a href="{{ lodge.dir }}"')
# 지도 범례의 '예시'
rep('<span style="color:#8C96B0">예시</span>', '', cnt=2)
# 여정
rep('역참 · 남은 19일<', '역참 · 남은 {{ tt.left }}<')
# 기록
rep('{{ lgd.n }}일차 · {{ lgd.date }}', '{{ lgd.nl }} · {{ lgd.date }}')
rep('>Galaxy Watch9 연결됨<', '>{{ lg2.sync.t }}<')
rep('>마지막 동기화 14:18 · 심박 실시간 수신<', '>{{ lg2.sync.s }}<')
rep('>정상</span></div>\n<div', '>{{ lg2.sync.chip }}</span></div>\n<div')
rep('>17,820<span', '>{{ lg2.steps }}<span')
rep('>2,180걸음 남음<', '>{{ lg2.goalLeft }}<')
rep('>가장 많이 11시 · 옆으로 밀기<', '>{{ lg2.hourNote }}<')
rep('>평균 108 bpm<', '>{{ lg2.hrAvgT }}<')
rep('<span>09:10</span><span>11:40</span><span>지금</span>', '<span>{{ lg2.hx0 }}</span><span>{{ lg2.hx1 }}</span><span>{{ lg2.hx2 }}</span>')
rep('>예시 데이터<', '>{{ lg2.cumTitle }}<')
rep('>계획보다 25.3km 덜 걸음<', '>{{ lg2.cumNote }}<')
rep('>12일차까지 누적 · 하루 평균 ₩92,000<', '>{{ lg2.cumNoteE }}<')
# 걷기 모드
rep('>17,820걸음 · 89%<', '>{{ wm.steps }}<')
rep('>3:12:40<', '>{{ wm.time }}<')
rep('>118<span', '>{{ wm.hr }}<span')
# 도착 알림
tx('오카베 宿에 도착했습니다', '{{ toastT.a }}'); tx('오늘의 네 번째 경유지입니다', '{{ toastT.b }}')
# 하루 완료 카드
rep('>DAY 12 완료 · 11월 3일<', '>{{ dnC.head }}<')
rep('>마리코 → 후지에다</b><span', '>{{ dnC.path }}</b><span')
tx('53역참 중 22번째까지 · 전체 41%', '{{ dnC.sub }}')
tx('방문한 경유지 5 / 5', '{{ dnC.wpHead }}')
rep('>“우쓰노야 고개 옛길이 생각보다 가팔랐다. 초지야 도로로지루는 다시 먹고 싶다.”<', '>{{ dnC.note }}<')
# 날씨 · 환율
rep('>WEATHER · 지금 · 오카베<', '>{{ wxCard.place }}<')
rep('>sunny</span></span><b', '>{{ wxCard.icon }}</span></span><b')
rep('>18°</b><span', '>{{ wxCard.t }}</b><span')
tx('맑음 · 체감 17° · 바람 2m/s · 습도 52%', '{{ wxCard.desc }}')
tx('100엔 = 905원 · 예시', '{{ fxLabel }}')

# ───────────────────────── 4. 지도: 가짜 지도(SVG) → 실제 지도(Leaflet) ─────────────────────────
svgs = [x for x in re.finditer(r'<svg viewBox="0 0 360 (?:300|200)"[^>]*>.*?</svg>', dc, re.S)]
assert len(svgs) == 3, len(svgs)
kinds = ['<div data-v8map="home" data-k="home" style="position:absolute;inset:0;pointer-events:none"></div>',
         '<iframe src="{{ gmSrc }}" title="구글 지도" style="position:absolute;left:0;top:-130px;width:100%;height:calc(100% + 130px);border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>',
         '<div data-v8map="log" data-k="log" style="position:absolute;inset:0"></div>']
for x, k in reversed(list(zip(svgs, kinds))):
    dc = dc[:x.start()] + k + dc[x.end():]
# 사진 일기 카드/하루 사진: 기기에 저장되는 사진 칸(image-slot)
SLOT = '<image-slot class="{{ %s.slotCls }}" id="{{ %s.slot }}" shape="rect" placeholder="사진 추가" style="position:absolute;inset:0;width:100%%;height:100%%"></image-slot>'
g = dc.index('{{ d.icon }}</span>', dc.index('{{ d.grad }}'))  # 사진 일기 카드
g += len('{{ d.icon }}</span>')
dc = dc[:g] + '<span onClick="{{ d.stopIf }}" style="position:absolute;inset:0;display:block">' + SLOT % ('d', 'd') + '</span>' + dc[g:]
# 하루 자세히: 사진 3칸
p = dc.index('{{ p.icon }}</span></span></sc-for>', dc.index('{{ dd2.photos }}'))
dc = dc[:p] + '{{ p.icon }}</span>' + SLOT % ('p', 'p') + '</span></sc-for>' + dc[p + len('{{ p.icon }}</span></span></sc-for>'):]
# 하루 자세히: 한 줄 쓰기
rep('<p style=', '<textarea rows="3" placeholder="걷고 난 뒤 한 줄을 남겨 보세요" onChange="{{ dd2.onNote }}" style=', cnt=dc.count('<p style=')) if False else None
E_NOTE = re.search(r'<p style="([^"]*)">\{\{ dd2\.note \}\}</p>', dc)
assert E_NOTE
dc = dc.replace(E_NOTE.group(0), '<p style="' + E_NOTE.group(1) + '">{{ dd2.note }}</p><sc-if value="{{ dd2.canNote }}" hint-placeholder-val="{{ false }}"><textarea rows="2" placeholder="오늘의 한 줄" onChange="{{ dd2.onNote }}" style="width:100%;box-sizing:border-box;border:1px solid #DCE0F7;border-radius:14px;padding:10px 12px;font:600 15px Pretendard Variable,Pretendard,sans-serif;color:#18324F;background:#fff;resize:none;outline:none">{{ dd2.noteV }}</textarea></sc-if>')
# 다음 장소 시트: 도착 체크 버튼
cta = re.search(r'<sc-if value="\{\{ sh\.hasCta \}\}"[^>]*><a href="\{\{ sh\.href \}\}"[^>]*>.*?</a></sc-if>', dc, re.S)
assert cta
a_open = re.search(r'<a href="\{\{ sh\.href \}\}" target="_blank" style="([^"]*)"', cta.group(0)).group(1)
dc = dc.replace(cta.group(0), cta.group(0) + '<sc-if value="{{ sh.hasCheck }}" hint-placeholder-val="{{ false }}"><button onClick="{{ sh.check }}" style="' + a_open.replace('background:', 'background:').rstrip(';') + ';border:0;cursor:pointer;font-family:inherit">도착 체크 ✓</button></sc-if>')
# 날짜 칩(오늘/어제…): 누르면 오늘로

# 하단 시작 영역: 평소엔 한 줄(작게), 와치 칸을 누르면 안내 카드가 펼쳐졌다가 6초 뒤 자동으로 접힘
_m = re.search(r'<sc-if value="\{\{ ctl\.ready \}\}" hint-placeholder-val="\{\{ false \}\}">(.*?)</sc-if>', dc, re.S)
assert _m
_inner = _m.group(1)
_ico = "font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:'liga';font-variation-settings:'FILL' 1,'wght' 500;"
_compact = ('<div style="display:flex;justify-content:flex-end"><button onClick="{{ start }}" aria-label="폰에서 걷기 시작" style="height:52px;padding:0 20px 0 14px;border:0;border-radius:26px;background:linear-gradient(135deg,#3B5BDB,#6C7FE8);color:#fff;display:flex;align-items:center;gap:6px;box-shadow:0 10px 22px rgba(59,91,219,.36);cursor:pointer;font-family:inherit"><span style="'+_ico+'font-size:26px;color:#fff">directions_walk</span><b style="font-size:17px;font-weight:800">시작</b></button></div>')
dc = dc.replace(_m.group(0), '<sc-if value="{{ ctl.ready }}" hint-placeholder-val="{{ false }}">' + _compact + '</sc-if>')
# 일정 변경 시트의 4개 항목에 클릭 동작 연결(원래 마크업에 onClick이 빠져 있었음)
rep('<sc-for list="{{ planOpts }}" as="p" hint-placeholder-count="4"><button style="display:grid;', '<sc-for list="{{ planOpts }}" as="p" hint-placeholder-count="4"><button onClick="{{ p.run }}" style="display:grid;')
# 더보기: 설정 행을 비상 연락처 행과 같은 모양·높이로
rep('<button onClick="{{ r.pick }}" style="display:flex;align-items:center;gap:12px;padding:8px 0;border:0;border-top:{{ r.top }};background:transparent;cursor:pointer;text-align:left;font-family:inherit;color:#18324F;width:100%"><span style="flex:none;width:38px;height:38px;border-radius:12px;background:#EDF0FF;',
    '<button onClick="{{ r.pick }}" style="display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:18px;background:#F6F7FF;border:1px solid #E2E5FA;cursor:pointer;text-align:left;font-family:inherit;color:#18324F;width:100%;box-sizing:border-box"><span style="flex:none;width:40px;height:40px;border-radius:13px;background:#EDF0FF;')
rep('<span style="display:flex;align-items:baseline;justify-content:space-between;gap:8px"><b style="font-size:18px;font-weight:800;letter-spacing:-.03em">설정</b></span>',
    '<span style="display:flex;align-items:center;justify-content:space-between;gap:8px;min-height:30px"><b style="font-size:18px;font-weight:800;letter-spacing:-.03em">설정</b></span>')
rep('<span style="display:flex;align-items:baseline;justify-content:space-between;gap:8px"><b style="font-size:18px;font-weight:800;letter-spacing:-.03em">비상 연락처</b>',
    '<span style="display:flex;align-items:center;justify-content:space-between;gap:8px;min-height:30px"><b style="font-size:18px;font-weight:800;letter-spacing:-.03em">비상 연락처</b>', cnt=2)
# 홈 날짜 카드: 일정 변경 버튼을 아이콘만(제목 가림 방지)
rep('aria-label="일정 변경" style="flex:none;white-space:nowrap;height:44px;padding:0 12px;border-radius:22px;', 'aria-label="일정 변경" style="flex:none;white-space:nowrap;height:44px;padding:0 12px 0 8px;border-radius:22px;border:1.5px solid #C9D3FF;')
rep('edit_calendar</span>일정 변경</button>', 'edit_calendar</span>목적지</button>')
# 일본어 상단 카드 글자 키움 / 하단 걷기 바 높이 축소
rep('<b style="font-size:{{ fr.jpFs }};font-weight:800;line-height:1.3;', '<b style="word-break:auto-phrase;overflow-wrap:anywhere;max-width:100%;font-size:{{ fr.jpFs }};font-weight:800;line-height:1.3;')
rep('<b style="font-size:{{ fr.jpBig }};font-weight:800;line-height:1.25;', '<b style="word-break:auto-phrase;overflow-wrap:anywhere;max-width:100%;font-size:{{ fr.jpBig }};font-weight:800;line-height:1.25;')
rep('<span style="font-size:17px;font-weight:700">{{ jp2.sel.ko }}</span>', '<span style="font-size:23px;font-weight:700;line-height:1.35">{{ jp2.sel.ko }}</span>')
rep('height:70px;border-radius:35px;background:#fff', 'height:58px;border-radius:29px;background:#fff')
rep('flex:1;min-width:0;height:56px;border:0;background:transparent', 'flex:1;min-width:0;height:48px;border:0;background:transparent')
rep('flex:none;width:58px;height:58px;border-radius:50%;border:0;background:linear-gradient(135deg,#3B5BDB,#6C7FE8)', 'flex:none;width:46px;height:46px;border-radius:50%;border:0;background:linear-gradient(135deg,#3B5BDB,#6C7FE8)')
rep('flex:none;width:48px;height:48px;border-radius:50%;border:1.5px solid #F3C3CB', 'flex:none;width:40px;height:40px;border-radius:50%;border:1.5px solid #F3C3CB')
# 걷기 완료 상태에서는 종료(빨간) 버튼 숨김: 요약 버튼 하나만
_sb = re.search(r'<button onClick="\{\{ stop \}\}" style="flex:none;width:40px;height:40px;[^>]*>.*?</button>', dc, re.S)
assert _sb
dc = dc.replace(_sb.group(0), '<sc-if value="{{ ctl.live }}" hint-placeholder-val="{{ true }}">' + _sb.group(0) + '</sc-if>', 1)
# 홈: 경유지 개수가 날짜마다 달라도 카드 높이가 변하지 않게(아래 날짜 이동 카드가 위아래로 안 움직임) — 5줄 고정 + 안쪽 스크롤
_a = dc.index('<sc-for list="{{ wps }}"')
_b = dc.index('</sc-for>', _a) + len('</sc-for>')
_blk = dc[_a:_b].replace('align-items:center;min-height:44px;cursor:pointer', 'align-items:center;flex:1 0 44px;cursor:pointer')
assert 'flex:1 0 44px' in _blk
dc = dc[:_a] + '<div style="height:226px;display:flex;flex-direction:column;overflow-y:auto;scrollbar-width:none;overscroll-behavior-y:auto;touch-action:pan-y;flex:none">' + _blk + '</div>' + dc[_b:]
rep('<span style="flex:none;height:46px;min-width:46px;padding:0 10px;border-radius:14px;background:{{ dn2.chipBg }}', '<span onClick="{{ dn2.goToday }}" style="cursor:pointer;flex:none;height:46px;min-width:46px;padding:0 10px;border-radius:14px;background:{{ dn2.chipBg }}')
# 하루 자세히 사진칸: 부모에 position:relative가 없어 slot(absolute inset:0)이 화면 전체로 퍼지던 문제
rep('<span style="grid-column:{{ p.gc }};min-height:110px;border-radius:18px;', '<span style="position:relative;overflow:hidden;grid-column:{{ p.gc }};min-height:110px;border-radius:18px;')
# 한 줄 입력칸: textarea 자식 바인딩이 [object Object]로 나오던 문제 → value 속성
rep('onChange="{{ dd2.onNote }}" style="width:100%;box-sizing:border-box;border:1px solid #DCE0F7;border-radius:14px;padding:10px 12px;font:600 15px Pretendard Variable,Pretendard,sans-serif;color:#18324F;background:#fff;resize:none;outline:none">{{ dd2.noteV }}</textarea>', 'value="{{ dd2.noteV }}" onChange="{{ dd2.onNote }}" style="width:100%;box-sizing:border-box;border:1px solid #DCE0F7;border-radius:14px;padding:10px 12px;font:600 15px Pretendard Variable,Pretendard,sans-serif;color:#18324F;background:#fff;resize:none;outline:none"></textarea>')
# 걷기 모드: 팝업 형태 — 좌우 여백은 블러 처리, 눌러서 닫기
rep('<div data-screen-label="걷기 모드" style="position:absolute;inset:0;z-index:30;background:linear-gradient(180deg,#FFFFFF 0%,#F2F3FF 100%);padding:calc(env(safe-area-inset-top) + 12px) 20px calc(env(safe-area-inset-bottom) + 26px);display:flex;justify-content:center">\n<div style="width:100%;max-width:{{ fr.modeW }};display:flex;flex-direction:column;gap:14px">',
 '<div data-screen-label="걷기 모드" style="position:absolute;inset:0;z-index:30;padding:calc(env(safe-area-inset-top) + 12px) 14px calc(env(safe-area-inset-bottom) + 14px);display:flex;justify-content:center">\n<div onClick="{{ closeMode }}" aria-label="닫기" style="position:absolute;inset:0;background:rgba(24,36,64,.28);backdrop-filter:blur(14px) saturate(1.1);-webkit-backdrop-filter:blur(14px) saturate(1.1);cursor:pointer"></div>\n<div style="position:relative;width:100%;max-width:{{ fr.modeW }};display:flex;flex-direction:column;gap:14px;background:linear-gradient(180deg,#FFFFFF 0%,#F2F3FF 100%);border-radius:32px;padding:18px 20px 22px;box-shadow:0 24px 70px rgba(20,30,80,.35);overflow:hidden">')
# 홈 히어로: 아래쪽 어두운 막을 옅게 → 배경 사진이 더 보이게(글자는 그림자로 가독성 유지)
rep('rgba(14,18,50,.5) 62%,rgba(14,18,50,.86) 100%)', 'rgba(14,18,50,.14) 62%,rgba(14,18,50,.34) 100%)')
rep('border-radius:20px;background:rgba(255,255,255,.16);backdrop-filter:blur(16px) saturate(1.3)', 'border-radius:20px;background:rgba(14,18,50,.05);backdrop-filter:blur(2px) saturate(1.2)')
# 홈: 오늘 지나는 명물(구버전의 "오늘 지나는 곳") 카드
_pc = """<sc-if value="{{ plc.has }}" hint-placeholder-val="{{ true }}">
<div style="padding:0 16px;margin-top:12px"><div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:26px;padding:16px 0 14px;display:flex;flex-direction:column;gap:10px">
<span style="display:flex;align-items:baseline;justify-content:space-between;padding:0 18px"><b style="font-size:18px;font-weight:800;letter-spacing:-.03em">오늘 지나는 명물</b><span style="font-size:13px;color:#4A5D78">{{ plc.n }} · 눌러서 지도</span></span>
<div data-hscroll="1" style="display:flex;gap:12px;overflow-x:auto;scrollbar-width:none;scroll-snap-type:x mandatory;touch-action:pan-x pan-y;scroll-padding:0 18px;padding:4px 18px 6px">
<sc-for list="{{ plc.list }}" as="q" hint-placeholder-count="3"><div onClick="{{ q.open }}" style="flex:none;width:280px;scroll-snap-align:start;cursor:pointer;box-sizing:border-box;border-radius:22px;padding:10px 10px 14px;background:#F6F7FB;display:flex;flex-direction:column;gap:10px;opacity:{{ q.op }}">
<span style="position:relative;height:150px;border-radius:16px;background:{{ q.img }};flex:none;display:block"><span style="position:absolute;left:8px;top:8px;height:30px;padding:0 12px;border-radius:99px;background:rgba(255,255,255,.95);display:flex;align-items:center;font-size:14px;font-weight:800;color:#5B3FD0;white-space:nowrap;box-shadow:0 3px 10px rgba(20,30,80,.2)">{{ q.badge }}</span><b style="position:absolute;right:8px;top:8px;width:30px;height:30px;border-radius:9px;background:linear-gradient(135deg,#5428E8,#9A63F5);color:#fff;font-size:15px;display:grid;place-items:center;box-shadow:0 3px 10px rgba(20,30,80,.2)">{{ q.n }}</b></span>
<span style="display:flex;flex-direction:column;align-items:center;gap:2px;text-align:center;padding:0 4px"><b style="max-width:100%;font-size:19px;font-weight:800;letter-spacing:-.03em;color:{{ q.nf }};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ q.name }}</b><span style="max-width:100%;font-size:14px;font-weight:600;color:{{ q.df }};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ q.jp }} · {{ q.cat }}</span></span>
</div></sc-for>
</div></div></div>
</sc-if>
"""
rep('</button>\n</div>\n</div>\n</div>\n\n<sc-if value="{{ mapFull }}" hint-placeholder-val="{{ false }}">\n<div data-screen-label="지도 전체 화면"', '</button>\n</div>\n</div>\n' + _pc + '</div>\n\n<sc-if value="{{ mapFull }}" hint-placeholder-val="{{ false }}">\n<div data-screen-label="지도 전체 화면"')
_ra = """<sc-if value="{{ restAsk }}" hint-placeholder-val="{{ false }}">
<div data-screen-label="휴식일 확인" style="position:absolute;inset:0;z-index:60;display:flex;justify-content:center;align-items:center;padding:20px">
<div onClick="{{ restNo }}" style="position:absolute;inset:0;background:rgba(20,24,60,.5);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px)"></div>
<div style="position:relative;width:100%;max-width:460px;background:#fff;border-radius:28px;padding:24px 22px 20px;display:flex;flex-direction:column;gap:16px;box-shadow:0 24px 60px rgba(10,14,50,.4);animation:sheetUp .22s ease-out">
<b style="font-size:24px;font-weight:800;letter-spacing:-.03em;color:#18243F;text-align:center">휴식일로 바꿀까요?</b>
<span style="font-size:18px;line-height:1.6;color:#3A4D68;text-align:center"><b style="color:#1C7ED6">{{ restLbl }}</b>을 쉬는 날로 바꾸고,<br>그 이후 일정이 하루씩 미뤄집니다.</span>
<div style="display:flex;gap:10px">
<button onClick="{{ restNo }}" style="flex:1;height:56px;border-radius:28px;border:1px solid #DCE0F7;background:#fff;color:#4A5D78;font:800 18px Pretendard Variable,Pretendard,sans-serif;cursor:pointer">취소</button>
<button onClick="{{ restYes }}" style="flex:1.3;height:56px;border-radius:28px;border:0;background:linear-gradient(135deg,#1C7ED6,#4DA3F0);color:#fff;font:800 18px Pretendard Variable,Pretendard,sans-serif;cursor:pointer;box-shadow:0 10px 22px rgba(28,126,214,.35)">휴식일로 변경</button>
</div></div></div>
</sc-if>
"""
_pp = """<sc-if value="{{ plc.pop.open }}" hint-placeholder-val="{{ false }}">
<div data-screen-label="명물 팝업" style="position:absolute;inset:0;z-index:44;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;overflow:hidden">
<div style="position:absolute;inset:-24px;background:{{ plc.pop.img }};filter:{{ dkBlur }}"><i style="position:absolute;width:70%;height:46%;left:-10%;bottom:8%;border-radius:50%;background:rgba(24,30,80,.28);filter:blur(30px)"></i><i style="position:absolute;width:60%;height:40%;right:-12%;bottom:18%;border-radius:50%;background:rgba(24,30,80,.22);filter:blur(30px)"></i><i style="position:absolute;width:44%;height:30%;right:12%;top:10%;border-radius:50%;background:rgba(255,255,255,.35);filter:blur(36px)"></i></div><div onClick="{{ plc.pop.close }}" style="position:absolute;inset:0;background:rgba(20,24,60,.45);backdrop-filter:blur(2.5px);-webkit-backdrop-filter:blur(2.5px)"></div>
<div style="position:relative;z-index:2;width:calc(100% - 24px);max-width:{{ fr.spotW }};max-height:calc(100% - 28px);overflow-y:auto;scrollbar-width:none;margin-bottom:calc(env(safe-area-inset-bottom) + 10px);background:#fff;border-radius:28px;padding:16px 16px 14px;display:flex;flex-direction:column;gap:18px;box-shadow:0 24px 60px rgba(10,14,50,.35);animation:sheetUp .28s ease-out">
<div style="position:relative;min-height:clamp(170px,28vh,360px);border-radius:22px;overflow:hidden;background:{{ plc.pop.img }};flex:none"><span style="position:absolute;left:12px;top:12px;height:34px;padding:0 14px;border-radius:99px;background:rgba(255,255,255,.95);display:flex;align-items:center;font-size:16px;font-weight:800;color:#5B3FD0;box-shadow:0 4px 12px rgba(20,30,80,.2)">{{ plc.pop.badge }}</span><span style="position:absolute;right:12px;top:12px;white-space:nowrap;font-size:14px;font-weight:800;padding:4px 9px;border-radius:99px;background:rgba(20,24,60,.45);color:#fff">{{ plc.pop.n }} / {{ plc.pop.total }}</span><span style="position:absolute;left:12px;right:12px;bottom:8px;font-size:14px;font-weight:600;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.7);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ plc.pop.credit }}</span></div>
<div style="display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center"><b style="font-size:30px;font-weight:800;letter-spacing:-.04em;line-height:1.2;color:#18243F">{{ plc.pop.name }}</b><span style="font-size:16px;font-weight:600;color:#6B7A90">{{ plc.pop.jp }} · {{ plc.pop.cat }}</span></div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><span style="border-radius:16px;background:#F6F7FB;border:1px solid #E6E9F5;padding:12px 8px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;min-width:0"><span style="display:flex;align-items:center;justify-content:center;gap:4px;font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap"><span style="font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:'liga';font-variation-settings:'FILL' 1,'wght' 500;font-size:16px;color:#5B6FD4">straighten</span>남은 거리</span><b style="font-size:clamp(17px,5vw,20px);font-weight:800;letter-spacing:-.03em;color:#18324F;white-space:nowrap">{{ plc.pop.remain }}</b></span><span style="border-radius:16px;background:#F6F7FB;border:1px solid #E6E9F5;padding:12px 8px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;min-width:0"><span style="display:flex;align-items:center;justify-content:center;gap:4px;font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap"><span style="font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:'liga';font-variation-settings:'FILL' 1,'wght' 500;font-size:16px;color:#5B6FD4">schedule</span>예상 시간</span><b style="font-size:clamp(17px,5vw,20px);font-weight:800;letter-spacing:-.03em;color:#18324F;white-space:nowrap">{{ plc.pop.walkT }}</b></span><span style="border-radius:16px;background:#F6F7FB;border:1px solid #E6E9F5;padding:12px 8px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;min-width:0"><span style="display:flex;align-items:center;justify-content:center;gap:4px;font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap"><span style="font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:'liga';font-variation-settings:'FILL' 1,'wght' 500;font-size:16px;color:#5B6FD4">my_location</span>현재 위치와</span><b style="font-size:clamp(17px,5vw,20px);font-weight:800;letter-spacing:-.03em;color:#18324F;white-space:nowrap">{{ plc.pop.fromMe }}</b></span></div>
<p style="margin:0;text-align:center;font-size:18px;line-height:1.65;color:#3A4D68;text-wrap:pretty">{{ plc.pop.long }}</p>
<div style="position:relative;height:clamp(110px,18vh,230px);border-radius:18px;overflow:hidden;background:#E8EBF7;flex:none"><div data-v8map="pop" data-k="{{ plc.pop.mapKey }}" style="position:absolute;inset:0;z-index:0"></div><span style="position:absolute;left:10px;bottom:10px;z-index:500;height:36px;padding:0 14px;border-radius:99px;background:rgba(255,255,255,.95);box-shadow:0 4px 12px rgba(30,40,100,.2);display:flex;align-items:center;gap:12px;font-size:15px;font-weight:700;color:#18324F;white-space:nowrap"><span style="display:flex;align-items:center;gap:6px"><i style="width:12px;height:12px;border-radius:50%;background:#3B5BDB;border:2px solid #fff;box-shadow:0 0 0 1.5px #3B5BDB"></i>내 위치</span><span style="display:flex;align-items:center;gap:6px"><i style="width:12px;height:12px;border-radius:50%;background:#7B46F0;border:2px solid #fff;box-shadow:0 0 0 1.5px #7B46F0"></i>이 장소</span></span></div>
<div style="display:flex;align-items:center;gap:8px;padding-top:14px;border-top:1px solid #EEF0F7">
<button onClick="{{ plc.pop.prev }}" aria-label="이전 명물" style="position:relative;flex:none;width:132px;height:96px;border-radius:16px;border:0;padding:0;overflow:hidden;background:{{ plc.pop.pImg }};cursor:pointer;opacity:{{ plc.pop.pO }};box-shadow:0 4px 12px rgba(30,40,100,.2)"><span style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,18,50,.1) 0%,rgba(14,18,50,.2) 40%,rgba(14,18,50,.8) 100%)"></span><span style="position:absolute;left:6px;right:6px;top:4px;display:flex;align-items:center;justify-content:flex-start;gap:2px;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.6)"><span style="font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:'liga';font-variation-settings:'FILL' 1,'wght' 500;font-size:26px;color:#fff">chevron_left</span><b style="font-size:16px;color:#fff">{{ plc.pop.pN }}</b></span><b style="position:absolute;left:8px;right:8px;bottom:6px;font-size:14px;font-weight:800;line-height:1.2;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.7);text-align:left;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">{{ plc.pop.pName }}</b></button>
<span style="flex:1"></span>
<button onClick="{{ plc.pop.map }}" style="flex:none;white-space:nowrap;height:48px;padding:0 18px;border:0;border-radius:24px;background:#EDF0FF;display:flex;align-items:center;gap:4px;font:800 15px 'Pretendard Variable',Pretendard,sans-serif;color:#3B5BDB;cursor:pointer"><span style="font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:'liga';font-variation-settings:'FILL' 1,'wght' 500;font-size:19px;color:#3B5BDB">map</span>구글 지도</button>
<span style="flex:1"></span>
<button onClick="{{ plc.pop.next }}" aria-label="다음 명물" style="position:relative;flex:none;width:132px;height:96px;border-radius:16px;border:0;padding:0;overflow:hidden;background:{{ plc.pop.nImg }};cursor:pointer;opacity:{{ plc.pop.nO }};box-shadow:0 4px 12px rgba(30,40,100,.2)"><span style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,18,50,.1) 0%,rgba(14,18,50,.2) 40%,rgba(14,18,50,.8) 100%)"></span><span style="position:absolute;left:6px;right:6px;top:4px;display:flex;align-items:center;justify-content:flex-end;gap:2px;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.6)"><span style="font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:'liga';font-variation-settings:'FILL' 1,'wght' 500;font-size:26px;color:#fff">chevron_right</span><b style="font-size:16px;color:#fff">{{ plc.pop.nN }}</b></span><b style="position:absolute;left:8px;right:8px;bottom:6px;font-size:14px;font-weight:800;line-height:1.2;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.7);text-align:right;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">{{ plc.pop.nName }}</b></button>
</div>
</div></div>
</sc-if>
"""
rep('488km</span></b><span style="flex:none;width:34px;height:34px;border-radius:50%;background:#EDF0FF;display:grid;place-items:center">','488km</span></b><span onClick="{{ tt.open }}" role="button" aria-label="전체 종주 자세히 보기" style="cursor:pointer;flex:none;width:44px;height:44px;margin:-5px -5px -5px 0;border-radius:50%;background:#EDF0FF;display:grid;place-items:center">')
rep('<sc-if value="{{ spotOpen }}" hint-placeholder-val="{{ false }}">\n<div data-screen-label="장소 팝업"', _ra + _pp + '<sc-if value="{{ tt.on }}" hint-placeholder-val="{{ false }}">\n<div data-screen-label="전체 종주 팝업" style="position:absolute;inset:0;z-index:44;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;overflow:hidden">\n\n<div onClick="{{ tt.close }}" style="position:absolute;inset:0;background:rgba(20,24,60,.45);backdrop-filter:blur(2.5px);-webkit-backdrop-filter:blur(2.5px)"></div>\n<div style="position:relative;z-index:2;width:calc(100% - 24px);max-width:{{ fr.spotW }};max-height:calc(100% - 28px);overflow-y:auto;scrollbar-width:none;margin-bottom:calc(env(safe-area-inset-bottom) + 10px);background:#fff;border-radius:28px;padding:16px 16px 14px;display:flex;flex-direction:column;gap:18px;box-shadow:0 24px 60px rgba(10,14,50,.35);animation:sheetUp .28s ease-out">\n<div style="position:relative;border-radius:22px;background:linear-gradient(160deg,#EFF7FF,#FFFFFF);border:1px solid #DCEEFF;padding:52px 16px 16px;display:flex;flex-direction:column;gap:10px;flex:none"><span style="position:absolute;left:12px;top:12px;height:34px;padding:0 14px;border-radius:99px;background:#fff;display:flex;align-items:center;font-size:16px;font-weight:800;color:#005FCC;box-shadow:0 4px 12px rgba(20,30,80,.12)">{{ tt.pct }} 완주</span><span style="position:absolute;right:12px;top:12px;white-space:nowrap;font-size:14px;font-weight:800;padding:4px 9px;border-radius:99px;background:rgba(20,24,60,.45);color:#fff">{{ tt.st }} / 53</span><div style="display:grid;grid-template-columns:repeat(18,minmax(0,1fr));gap:5px"><sc-for list="{{ jn.dots }}" as="d" hint-placeholder-count="53"><i style="aspect-ratio:1;border-radius:50%;background:{{ d.c }};box-shadow:{{ d.sh }}"></i></sc-for></div><span style="display:flex;justify-content:space-between;font-size:14px;font-weight:700;color:#475569"><span>시나가와 品川</span><span>교토 京都</span></span></div>\n<div style="display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center"><b style="font-size:30px;font-weight:800;letter-spacing:-.04em;line-height:1.2;color:#18243F">전체 종주</b><span style="font-size:16px;font-weight:600;color:#6B7A90">品川 → 京都 · 도카이도 53次</span></div>\n<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><span style="border-radius:16px;background:#F6F7FB;border:1px solid #E6E9F5;padding:12px 8px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;min-width:0"><span style="display:flex;align-items:center;justify-content:center;gap:4px;font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap"><span style="font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'FILL\' 1,\'wght\' 500;font-size:16px;color:#5B6FD4">footprint</span>걸은 거리</span><b style="font-size:clamp(17px,5vw,20px);font-weight:800;letter-spacing:-.03em;color:#18324F;white-space:nowrap">{{ tt.km }} km</b></span><span style="border-radius:16px;background:#F6F7FB;border:1px solid #E6E9F5;padding:12px 8px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;min-width:0"><span style="display:flex;align-items:center;justify-content:center;gap:4px;font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap"><span style="font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'FILL\' 1,\'wght\' 500;font-size:16px;color:#5B6FD4">straighten</span>남은 거리</span><b style="font-size:clamp(17px,5vw,20px);font-weight:800;letter-spacing:-.03em;color:#18324F;white-space:nowrap">{{ tt.leftKm }} km</b></span><span style="border-radius:16px;background:#F6F7FB;border:1px solid #E6E9F5;padding:12px 8px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;min-width:0"><span style="display:flex;align-items:center;justify-content:center;gap:4px;font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap"><span style="font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'FILL\' 1,\'wght\' 500;font-size:16px;color:#5B6FD4">today</span>남은 일수</span><b style="font-size:clamp(17px,5vw,20px);font-weight:800;letter-spacing:-.03em;color:#18324F;white-space:nowrap">{{ tt.left }}</b></span></div>\n<div style="display:flex;flex-direction:column;gap:8px"><span style="height:10px;border-radius:99px;background:rgba(91,111,212,.15);overflow:hidden"><span style="display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#3B5BDB,#8B9CF0);width:{{ tt.w }}"></span></span><span style="display:flex;justify-content:space-between;align-items:center;font-size:14px;color:#4A5D78"><span>시나가와</span><b style="color:#3B5BDB">{{ tt.km }} / 488km · {{ tt.st }} / 53 역참</b><span>교토</span></span></div>\n<div style="display:flex;flex-direction:column;gap:10px"><b style="font-size:16px;font-weight:800;color:#1A1D20">주차별 거리</b><sc-for list="{{ jn.weeks }}" as="w" hint-placeholder-count="5"><button onClick="{{ w.goT }}" style="display:grid;grid-template-columns:44px minmax(0,1fr) 76px;gap:10px;align-items:center;border:0;background:transparent;padding:0;cursor:pointer;text-align:left;font-family:inherit"><b style="font-size:15px;font-weight:800;color:#005FCC">{{ w.label }}</b><span style="display:flex;flex-direction:column;gap:4px;min-width:0"><span style="font-size:14px;color:#475569;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ w.path }}</span><span style="height:8px;border-radius:99px;background:rgba(57,121,232,.14);overflow:hidden"><span style="display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#3979E8,#55A9F5);width:{{ w.w }}"></span></span></span><b style="font-size:16px;font-weight:800;color:#1A1D20;text-align:right;white-space:nowrap">{{ w.km }}</b></button></sc-for></div>\n<div style="display:flex;align-items:center;gap:8px;padding-top:14px;border-top:1px solid #EEF0F7"><span style="flex:1"></span><button onClick="{{ tt.goJ }}" style="flex:none;white-space:nowrap;height:48px;padding:0 20px;border:0;border-radius:24px;background:#EDF0FF;display:flex;align-items:center;gap:4px;font:800 15px \'Pretendard Variable\',Pretendard,sans-serif;color:#3B5BDB;cursor:pointer"><span style="font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'FILL\' 1,\'wght\' 500;font-size:19px;color:#3B5BDB">route</span>전체 여정 보기</button><span style="flex:1"></span><button onClick="{{ tt.close }}" aria-label="팝업 닫기" style="flex:none;width:48px;height:48px;border-radius:50%;border:0;background:linear-gradient(120deg,#5B6FD4,#8B9CF0);box-shadow:0 8px 18px rgba(91,111,212,.35);display:grid;place-items:center;cursor:pointer"><span style="font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'FILL\' 1,\'wght\' 500;font-size:24px;color:#fff">close</span></button></div>\n</div></div>\n</sc-if>\n' + '<sc-if value="{{ spotOpen }}" hint-placeholder-val="{{ false }}">\n<div data-screen-label="장소 팝업"')
# 홈 사진 히어로 좌우 날짜 이동 버튼(반투명 흰색)
_ic = "font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'wght\' 600;font-size:26px;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.35)"
_b1 = lambda fn, ic, op, lab: '<button onClick="{{ dn2.%s }}" aria-label="%s" style="width:56px;height:44px;border:0;background:transparent;display:grid;place-items:center;cursor:pointer;opacity:{{ dn2.%s }}"><span style="%s">%s</span></button>' % (fn, lab, op, _ic, ic)
_hb2_old = '<span style="position:absolute;right:18px;top:-44px;display:flex;align-items:center;border-radius:18px 18px 0 0;background:rgba(14,18,50,.05);backdrop-filter:blur(2px) saturate(1.2);-webkit-backdrop-filter:blur(2px) saturate(1.2);border:1px solid rgba(255,255,255,.32);border-bottom:0">' + _b1('prev','chevron_left','pO','이전 날') + '<i style="width:1px;height:22px;background:rgba(255,255,255,.32)"></i>' + _b1('next','chevron_right','nO','다음 날') + '</span>'
_hb2 = ''
rep('border-radius:20px;background:rgba(14,18,50,.05);backdrop-filter:blur(2px) saturate(1.2);-webkit-backdrop-filter:blur(16px) saturate(1.3);border:1px solid rgba(255,255,255,.32);padding:12px 14px;display:flex;flex-direction:column;gap:10px">', 'position:relative;border-radius:20px;background:rgba(14,18,50,.05);backdrop-filter:blur(2px) saturate(1.2);-webkit-backdrop-filter:blur(2px) saturate(1.2);border:1px solid rgba(255,255,255,.32);padding:12px 14px;display:flex;flex-direction:column;gap:10px">' + _hb2)
rep('<div style="display:flex;flex-direction:column;gap:3px;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.3)">\n<span style="font-size:13px;font-weight:700;opacity:.92">{{ hr.when }}</span>', '<div style="display:flex;flex-direction:column;gap:3px;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.3)">\n<span style="font-size:13px;font-weight:700;opacity:.92">{{ hr.when }}</span>')
# 사진일기 팝업: 큰 사진 탭 → 전체 화면 보기 / 사진 없음 안내
rep('<div style="position:relative;min-height:{{ fr.spotH }};border-radius:22px;overflow:hidden;background:{{ dpv.img }};flex:none;', '<div onClick="{{ dpv.openFs }}" aria-label="사진 크게 보기" style="cursor:zoom-in;position:relative;min-height:{{ fr.spotH }};border-radius:22px;overflow:hidden;background:{{ dpv.img }};flex:none;')
rep('<sc-if value="{{ dpv.hasPh }}" hint-placeholder-val="{{ true }}"><div style="display:grid;grid-template-columns:repeat(4', '<sc-if value="{{ dpv.noPh }}" hint-placeholder-val="{{ false }}"><div style="border-radius:16px;background:#F3F5FF;padding:12px 14px;font-size:14px;font-weight:600;color:#4A5D78;line-height:1.5">이 날 올린 사진이 아직 없어요. 오른쪽 위 카메라 버튼이나 기록 탭에서 올리면 여기 나와요.</div></sc-if>\n<sc-if value="{{ dpv.hasPh }}" hint-placeholder-val="{{ true }}"><div style="display:grid;grid-template-columns:repeat(4')
_fs = """<sc-if value="{{ dpv.fsOpen }}" hint-placeholder-val="{{ false }}">
<div data-screen-label="사진 전체 보기" onClick="{{ dpv.closeFs }}" style="position:absolute;inset:0;z-index:60;background:#080A18;display:flex;align-items:center;justify-content:center;cursor:zoom-out">
<div style="position:absolute;inset:calc(env(safe-area-inset-top) + 12px) 12px calc(env(safe-area-inset-bottom) + 12px);background:{{ dpv.fsBg }};filter:{{ dkImg }}"></div>
<button onClick="{{ dpv.closeFs }}" aria-label="닫기" style="position:absolute;right:16px;top:calc(env(safe-area-inset-top) + 16px);width:48px;height:48px;border-radius:50%;border:0;background:rgba(255,255,255,.9);font-size:22px;font-weight:800;color:#18324F;cursor:pointer">✕</button>
</div>
</sc-if>
"""
rep('<sc-if value="{{ plc.pop.open }}" hint-placeholder-val="{{ false }}">', _fs + '<sc-if value="{{ plc.pop.open }}" hint-placeholder-val="{{ false }}">')
rep('scrollbar-width:none;padding:calc(env(safe-area-inset-top) + 12px) 0 calc(env(safe-area-inset-bottom) + 110px)">', 'scrollbar-width:none;padding:calc(env(safe-area-inset-top) + 12px) 0 calc(env(safe-area-inset-bottom) + {{ padM }})">')
rep('scrollbar-width:none;padding-bottom:110px">', 'scrollbar-width:none;padding-bottom:{{ padB }}">')
# 지도 화면 중복 범례 정리: 아래쪽 범례 삭제, 위 범례에 '교통 구간' 추가
_i = dc.index('<div style="display:flex;gap:12px;flex-wrap:wrap;padding:6px 12px;border-radius:14px;background:rgba(255,255,255,.92);')
_j = dc.index('교통 구간</span></div>', _i) + len('교통 구간</span></div>')
dc = dc[:_i] + dc[_j:]
dc = dc.replace('<i style="width:10px;height:10px;border-radius:50%;background:#7048E8"></i>도착</span>', '<i style="width:10px;height:10px;border-radius:50%;background:#7048E8"></i>도착</span><span style="display:flex;align-items:center;gap:5px"><i style="width:16px;height:4px;border-radius:2px;background:repeating-linear-gradient(90deg,#9775FA 0 4px,transparent 4px 7px)"></i>교통</span>')
rep('<span style="position:absolute;left:74px;top:calc(env(safe-area-inset-top) + 20px);display:flex;align-items:center;gap:10px;height:32px;', '<span style="position:absolute;left:74px;right:12px;overflow-x:auto;scrollbar-width:none;top:calc(env(safe-area-inset-top) + 20px);display:flex;align-items:center;gap:10px;height:32px;')
# 여정 탭 맨 위: 일정 관리 큰 버튼(더보기에서 이동)
rep('<span style="font-size:13px;color:#6B7A90">시나가와 → 교토 · 31일 · 488km</span></div>', '<span style="font-size:13px;color:#6B7A90">시나가와 → 교토 · 31일 · 488km</span></div>\n<div style="padding:0 16px 12px"><button onClick="{{ goPlanSub }}" style="width:100%;min-height:64px;border:0;border-radius:22px;background:linear-gradient(135deg,#3B5BDB,#6C8CF5);color:#fff;box-shadow:0 10px 26px rgba(59,91,219,.3);display:flex;align-items:center;gap:14px;padding:12px 18px;cursor:pointer;text-align:left;font-family:inherit"><span style="' + _ic + 'font-size:30px;color:#fff">edit_calendar</span><span style="flex:1;display:flex;flex-direction:column;gap:2px"><b style="font-size:19px;font-weight:800">일정 관리</b><span style="font-size:14px;font-weight:600;opacity:.9">날짜별 목적지 · 쉬는 날 · 숙소</span></span><span style="' + _ic + 'font-size:26px;color:#fff">chevron_right</span></button></div>')
# 지도 범례: 마커 색과 동일(출발 초록·다음 파랑·도착 보라)
dc = dc.replace('<i style="width:10px;height:10px;border-radius:50%;background:#7048E8"></i>다음</span>', '<i style="width:10px;height:10px;border-radius:50%;background:#2F9E44"></i>출발</span><span style="display:flex;align-items:center;gap:5px"><i style="width:10px;height:10px;border-radius:50%;background:#3B5BDB"></i>다음</span><span style="display:flex;align-items:center;gap:5px"><i style="width:10px;height:10px;border-radius:50%;background:#7048E8"></i>도착</span>')
# 걷기 화면: 걸은 거리 = 실제 측정값, 아래에 걷기/교통(이동) 거리 구분
rep('{{ pg.walked }}</b>\n<span style="font-size:22px;font-weight:700;color:#4A5D78">km</span>\n</div>', '{{ pg.walked }}</b>\n<span style="font-size:22px;font-weight:700;color:#4A5D78">km</span>\n<span style="margin-top:12px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;width:100%"><span style="padding:10px 6px;border-radius:16px;background:rgba(24,50,79,.06);display:flex;flex-direction:column;gap:2px"><span style="font-size:13px;font-weight:700;color:#4A5D78">총 이동</span><b style="font-size:20px;color:#18324F">{{ pg.mvTot }}km</b></span><span style="padding:10px 6px;border-radius:16px;background:#EDF0FF;display:flex;flex-direction:column;gap:2px"><span style="font-size:13px;font-weight:700;color:#3B5BDB">걷기</span><b style="font-size:20px;color:#2C3FA8">{{ pg.wkT }}km</b></span><span style="padding:10px 6px;border-radius:16px;background:#F3F0FF;display:flex;flex-direction:column;gap:2px"><span style="font-size:13px;font-weight:700;color:#7048E8">교통</span><b style="font-size:20px;color:#5A33C9">{{ pg.trT }}km</b></span></span>\n</div>')
# 하루 기록: 날짜 이동 카드를 하단(탭바·걷기바 바로 위)에 고정
_k = dc.index('<div style="padding:0 16px 12px"><div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:24px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0;flex-direction:row;align-items:center;padding:10px 10px 10px 12px">')
_e = dc.index('</div></div>', _k) + len('</div></div>')
_blk = dc[_k:_e]
assert 'lgd.prev' in _blk
_new = _blk.replace('<div style="padding:0 16px 12px">', '<div style="position:fixed;left:16px;right:16px;bottom:{{ lgd.fixBot }};z-index:4;max-width:900px;margin:0 auto">', 1)
dc = dc[:_k] + _new + dc[_e:]
_t = '</div>\n</div>\n</sc-if>\n<sc-if value="{{ tb.more }}"'
assert dc.count(_t) == 1
dc = dc.replace(_t, '<div style="height:{{ lgd.spacer }}"></div>' + _t)
# 더보기: 메뉴 6개를 화면 아래쪽으로(엄지 닿는 곳)
_ma = dc.index('<sc-if value="{{ tb.more }}"')
_old = '<div style="display:flex;flex-direction:column;gap:12px;padding:0 16px">\n<div style="display:grid;grid-template-columns:{{ fr.menuCols }};gap:10px">'
assert dc.count(_old) == 1 and dc.index(_old) > _ma
dc = dc.replace(_old, '<div style="display:flex;flex-direction:column;gap:12px;padding:0 16px;min-height:calc(100lvh - 176px)">\n<div style="order:2;flex:1;margin-top:auto;min-height:150px;max-height:270px;display:grid;grid-auto-rows:1fr;grid-template-columns:{{ fr.menuCols }};gap:12px">')
dc = dc.replace('font-family:inherit;min-height:132px">', 'font-family:inherit;min-height:112px">')
_m0 = dc.index('<sc-for list="{{ mo2 }}"'); _m1 = dc.index('</sc-for>', _m0)
_seg = dc[_m0:_m1].replace('min-height:112px', 'min-height:64px;padding:10px 12px;gap:10px').replace('border-radius:24px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0;gap:12px', 'border-radius:24px;padding:16px;display:flex;flex-direction:row;align-items:center;min-width:0')
_seg = _seg.replace('display:flex;justify-content:space-between;align-items:flex-start;width:100%', 'display:flex;flex:none;align-items:center')
_seg = re.sub(r'<span style="width:30px;height:30px;border-radius:50%;background:#F3F5FF;display:grid;place-items:center">.*?</span></span>', '', _seg, count=1, flags=re.S)
_seg = _seg.replace('white-space:nowrap;overflow:hidden;text-overflow:ellipsis', 'line-height:1.3')
_seg = _seg.replace('<span style="display:flex;flex-direction:column;gap:2px"><b', '<span style="display:flex;flex-direction:column;gap:2px;min-width:0;flex:1"><b')
dc = dc[:_m0] + _seg + dc[_m1:]
# 더보기 상단: 오늘 날씨 + 이번 주 날씨 + 일출·일몰 요약 카드
_anchor = '<div style="display:flex;flex-direction:column;gap:12px;padding:0 16px;min-height:calc(100lvh - 176px)">\n'
assert dc.count(_anchor) == 1
_ic = "font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:'liga';font-variation-settings:'FILL' 1,'wght' 500;"
_wcard = ('<div style="border-radius:24px;padding:14px 16px;background:linear-gradient(135deg,#1C7ED6,#4DABF7);box-shadow:0 12px 26px rgba(28,126,214,.28);color:#fff;display:flex;flex-direction:column;gap:8px;min-width:0">'
  '<span style="display:flex;align-items:center;justify-content:space-between;gap:10px"><span style="display:flex;flex-direction:column;gap:2px;min-width:0"><span style="font-size:13px;font-weight:700;opacity:.9">{{ wxCard.place }}</span><b style="font-size:44px;font-weight:800;letter-spacing:-.05em;line-height:1.05">{{ wxCard.t }}</b><span style="font-size:14px;font-weight:700">{{ wxCard.desc }}</span></span><span style="' + _ic + 'flex:none;width:48px;height:48px;overflow:hidden;font-size:46px;color:#FFE08A">{{ wxCard.icon }}</span></span>'
  '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px"><sc-for list="{{ wxd2 }}" as="x" hint-placeholder-count="4"><span style="background:rgba(255,255,255,.2);border-radius:14px;padding:8px 6px;display:flex;flex-direction:column;align-items:center;gap:2px;min-width:0"><span style="font-size:11px;font-weight:700;white-space:nowrap;opacity:.9">{{ x.k }}</span><b style="font-size:17px;font-weight:800;white-space:nowrap">{{ x.v }}</b></span></sc-for></div>'
  '<div style="display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:3px"><sc-for list="{{ wx2 }}" as="d" hint-placeholder-count="7"><span style="display:flex;flex-direction:column;align-items:center;gap:3px;padding:5px 0;border-radius:12px;background:rgba(255,255,255,.92);color:#18324F"><b style="font-size:16px">{{ d.name }}</b><span style="' + _ic + 'font-size:26px;color:{{ d.ic }}">{{ d.icon }}</span><span style="display:flex;align-items:baseline;gap:4px;white-space:nowrap"><b style="font-size:19px;font-weight:800">{{ d.hi }}°</b><span style="font-size:15px;font-weight:700;color:#5B6B82">{{ d.lo }}°</span></span><span style="font-size:14px;font-weight:800;color:{{ d.rc }}">{{ d.rain }}</span></span></sc-for></div></div>\n')
dc = dc.replace(_anchor, _anchor + _wcard)
# 사진 일기 팝업: 사진 추가(업로드) 버튼
_ico2 = "font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:'liga';font-variation-settings:'FILL' 1,'wght' 500;"
_up = ('<label aria-label="사진 추가" style="flex:none;width:48px;height:48px;border-radius:50%;border:1px solid #C9D3FF;background:#EDF0FF;display:grid;place-items:center;cursor:pointer;opacity:{{ dpv.upO }}"><input type="file" accept="image/*" multiple onChange="{{ dpv.upload }}" style="display:none"><span style="' + _ico2 + 'font-size:24px;color:#3B5BDB">add_a_photo</span></label>')
_dk = '<button onClick="{{ dpv.detail }}"'
assert dc.count(_dk) == 1
dc = dc.replace(_dk, _up + _dk)
# 사진 일기 팝업: 썸네일 한 줄에 5장
rep('<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px"><sc-for list="{{ dpv.thumbs }}"', '<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px"><sc-for list="{{ dpv.thumbs }}"')
# 일정 관리 화면: 하루 목적지 + 쉬는 날 선택 카드(디자인 마크업에 없어 추가)
_k = dc.index('이동 방식</b>'); _c = dc.rindex('<div style="background:#fff', 0, _k)
_card = ('<div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:24px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0">'
  '<span style="display:flex;align-items:baseline;justify-content:space-between;gap:8px"><b style="font-size:18px;font-weight:800;letter-spacing:-.03em">DAY {{ pl2.n }} · {{ pl2.date }}</b><span style="font-size:13px;font-weight:700;color:#3B5BDB">{{ pl2.goal }}</span></span>'
  '<span style="display:flex;padding:4px;border-radius:99px;background:#EEF0FA"><button onClick="{{ pl2.goWalk }}" style="flex:1;height:48px;border:0;border-radius:99px;background:{{ pl2.wBg }};color:{{ pl2.wFg }};box-shadow:{{ pl2.wSh }};font:800 16px Pretendard Variable,Pretendard,sans-serif;cursor:pointer">걷는 날</button><button onClick="{{ pl2.goRest }}" style="flex:1;height:48px;border:0;border-radius:99px;background:{{ pl2.rBg }};color:{{ pl2.rFg }};font:800 16px Pretendard Variable,Pretendard,sans-serif;cursor:pointer">쉬는 날</button></span>'
  '<b style="font-size:14px;color:#4A5D78">어디까지 갈까요 (도착 역참)</b>'
  '<div style="display:flex;gap:8px;flex-wrap:wrap"><button onClick="{{ pl2.allWalk }}" style="flex:1;min-width:140px;height:46px;border-radius:14px;border:1.5px solid #C9D3FF;background:#fff;color:#3B5BDB;font:800 14px Pretendard Variable,Pretendard,sans-serif;cursor:pointer">교통 안 타기 (전부 걷기)</button><button onClick="{{ pl2.reset }}" style="flex:1;min-width:140px;height:46px;border-radius:14px;border:1.5px solid #F3C3CB;background:#fff;color:#B8364A;font:800 14px Pretendard Variable,Pretendard,sans-serif;cursor:pointer">이 날 되돌리기</button><a href="{{ pl2.agoda }}" target="_blank" rel="noopener" style="flex:1 1 100%;height:46px;border-radius:14px;background:#EDF0FF;color:#3B5BDB;font:800 14px Pretendard Variable,Pretendard,sans-serif;display:flex;align-items:center;justify-content:center;text-decoration:none">이 날 도착지 숙소 찾기 (아고다) ↗</a></div>'
  '<div style="display:flex;flex-direction:column;gap:6px"><sc-for list="{{ pl2.ends }}" as="e" hint-placeholder-count="5"><button onClick="{{ e.pick }}" style="display:flex;align-items:center;gap:12px;min-height:56px;padding:6px 14px;border-radius:16px;border:1.5px solid {{ e.bd }};background:{{ e.bg }};cursor:pointer;font-family:inherit;text-align:left"><i style="flex:none;width:22px;height:22px;border-radius:50%;border:{{ e.ring }};display:grid;place-items:center"><i style="width:12px;height:12px;border-radius:50%;background:{{ e.dot }}"></i></i><span style="flex:1;min-width:0;display:flex;flex-direction:column"><b style="font-size:17px;color:#18324F">{{ e.name }}</b><span style="font-size:12px;color:#6B7A90">{{ e.jp }}</span></span><b style="flex:none;font-size:15px;color:#3B5BDB">{{ e.km }}</b></button></sc-for></div></div>')
dc = dc[:_c] + _card + dc[_c:]
# 일정 변경 시트: 누르면 실제 동작
_pi = dc.index('{{ p.bg }}'); _pb = dc.rindex('<button style="', 0, _pi)
dc = dc[:_pb] + '<button onClick="{{ p.run }}" style="' + dc[_pb + len('<button style="'):]

# 지도 탭: 약국 칩 오른쪽 "구글지도 보기" (외부 구글 지도 열기)
rep('{{ c.n }}</span></button></sc-for></div>', '{{ c.n }}</span></button></sc-for><button onClick="{{ amen.openGm }}" style="flex:none;white-space:nowrap;height:42px;padding:0 16px;border-radius:99px;border:0;background:linear-gradient(135deg,#5428E8,#9A63F5);color:#fff;display:flex;align-items:center;gap:6px;font:800 14px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer;box-shadow:0 6px 16px rgba(84,40,232,.3)"><span class="material-symbols-rounded" style="font-size:20px">open_in_new</span>구글지도 보기</button></div>')

# 몸 상태: 3항목(최대 15), 입력칸 항상 표시 + 선택 즉시 저장 (저장 버튼 제거)
rep('<div style="display:flex;justify-content:flex-end"><button onClick="{{ lg2.toggleCond }}"', '<div style="display:none"><button onClick="{{ lg2.toggleCond }}"')
rep('>/ 25<', '>/ 15<')
rep('hint-placeholder-count="5"><div style="display:grid;grid-template-columns:56px', 'hint-placeholder-count="3"><div style="display:grid;grid-template-columns:76px')
rep('<b style="font-size:14px">{{ r.label }}</b><sc-for list="{{ r.v }}"', '<b style="font-size:14px;white-space:nowrap">{{ r.label }}</b><sc-for list="{{ r.v }}"')
rep('grid-template-columns:64px repeat(3,minmax(0,1fr))', 'grid-template-columns:76px repeat(3,minmax(0,1fr))')

rep('<span style="display:flex;justify-content:space-between;font-size:12px;color:#6B7A90">\n</div>\n</sc-if>', '</div>\n</sc-if>')
# 지도 탭(구글 지도): 구글이 그리는 출발·도착 마커는 색을 바꿀 수 없어 범례 제거
import re as _re2
_m = _re2.search(r'<span style="position:absolute;left:74px;right:12px;overflow-x:auto[^\n]*\n', dc)
assert _m, 'legend'
dc = dc[:_m.start()] + dc[_m.end():]
# 몸 상태 카드가 닫히지 않아 아래 카드(지출·수면·체중)가 그 안에 들어가 같이 접히던 문제
rep('\n\n</div>\n</sc-if>\n<div style="height:{{ lgd.spacer }}">', '\n\n<div style="height:{{ lgd.spacer }}">')
rep('</sc-if>\n</div>\n<div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:24px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0">\n<button onClick="{{ lgc.exp.toggle }}"', '</sc-if>\n</div>\n</sc-if>\n</div>\n<div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:24px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0">\n<button onClick="{{ lgc.exp.toggle }}"')
# 오늘 지출: 항목 메모 입력(무엇을 먹었는지·어디서 자는지 등)
rep('<div style="display:flex;gap:6px;flex-wrap:wrap"><sc-for list="{{ lg2.cats }}" as="c" hint-placeholder-count="4"><button onClick="{{ c.pick }}" style="flex:none;white-space:nowrap;height:40px;padding:0 14px;border-radius:99px;border:1px solid {{ c.bd }};background:{{ c.bg }};color:{{ c.fg }};font:700 14px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer">{{ c.label }}</button></sc-for></div>',
 '<div style="display:flex;gap:6px;flex-wrap:wrap"><sc-for list="{{ lg2.cats }}" as="c" hint-placeholder-count="4"><button onClick="{{ c.pick }}" style="flex:none;white-space:nowrap;height:40px;padding:0 14px;border-radius:99px;border:1px solid {{ c.bd }};background:{{ c.bg }};color:{{ c.fg }};font:700 14px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer">{{ c.label }}</button></sc-for></div>\n<input value="{{ lg2.nnote }}" onChange="{{ lg2.onNote }}" placeholder="내용 (예: 라멘, 가케가와 호텔)" style="width:100%;box-sizing:border-box;height:46px;border-radius:14px;border:1px solid #DCE0F7;background:#F6F7FF;padding:0 14px;font:600 15px \'Pretendard Variable\',Pretendard,sans-serif;color:#18324F">')

rep('<sc-if value="{{ sb2.plan }}" hint-placeholder-val="{{ false }}">', '<sc-if value="{{ sb2.glance }}" hint-placeholder-val="{{ false }}">\n<div style="display:flex;flex-direction:column;gap:18px;padding:0 16px 110px"><sc-for list="{{ jn.gw }}" as="w" hint-placeholder-count="5">\n<div id="{{ w.id }}" style="display:flex;flex-direction:column;gap:10px;scroll-margin-top:64px">\n<div style="display:flex;align-items:baseline;gap:10px;padding:0 4px"><b style="font-size:20px;font-weight:800;letter-spacing:-.03em;color:#20202A">{{ w.label }}</b><span style="font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ w.sub }}</span><span style="flex:1"></span><b style="flex:none;font-size:15px;color:#5B32D6">{{ w.km }}</b></div>\n<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px"><sc-for list="{{ w.days }}" as="g" hint-placeholder-count="7"><button onClick="{{ g.open }}" style="display:flex;flex-direction:column;padding:0;text-align:left;border-radius:24px;border:{{ g.bd }};background:{{ g.cbg }};box-shadow:0 8px 22px rgba(40,50,140,.10);cursor:pointer;font-family:inherit;color:#18324F;min-width:0;overflow:hidden"><span style="position:relative;display:block;height:132px;background:{{ g.img }};flex:none"><span style="position:absolute;inset:0;background:{{ g.ov }}"></span><span style="position:absolute;left:10px;top:10px;height:32px;padding:0 12px;border-radius:99px;background:{{ g.nb }};color:{{ g.nf }};display:flex;align-items:center;font-size:15px;font-weight:800;letter-spacing:.02em">DAY {{ g.n }}</span><span style="position:absolute;right:10px;top:10px;height:30px;padding:0 12px;border-radius:99px;background:{{ g.sb }};color:{{ g.sf }};display:flex;align-items:center;font-size:13px;font-weight:800">{{ g.st }}</span><b style="position:absolute;left:12px;right:12px;bottom:10px;font-size:19px;font-weight:800;color:#fff;letter-spacing:-.03em;text-shadow:0 1px 4px rgba(0,0,0,.4);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ g.path }}</b></span><span style="display:flex;flex-direction:column;gap:8px;padding:12px 14px 14px"><span style="display:flex;align-items:baseline;justify-content:space-between;gap:8px"><span style="display:flex;align-items:center;gap:8px;font-size:15px;font-weight:700;color:#4A5D78;white-space:nowrap">{{ g.date }}<sc-if value="{{ g.hv }}" hint-placeholder-val="{{ false }}"><span style="font-size:12px;font-weight:800;padding:3px 8px;border-radius:99px;background:#FDE9EC;color:#B8364A">30km 초과</span></sc-if></span><b style="font-size:20px;font-weight:800;color:{{ g.kc }};white-space:nowrap">{{ g.km }}</b></span><span style="display:flex;align-items:center;gap:8px;min-width:0"><span style="flex:none;width:26px;height:26px;border-radius:9px;background:{{ g.lb }};display:grid;place-items:center">@@IC@@font-size:16px;color:{{ g.lf }}">hotel</span></span><span style="flex:1;min-width:0;font-size:14px;font-weight:700;color:{{ g.lf }};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ g.lodge }}</span></span></span></button></sc-for></div>\n</div>\n</sc-for></div>\n</sc-if>\n'.replace('@@IC@@', '<span style="' + _ic) + '<sc-if value="{{ sb2.plan }}" hint-placeholder-val="{{ false }}">')
rep('<input value="{{ f.v }}" onChange="{{ f.on }}" placeholder="" style="height:46px;border-radius:14px;border:1px solid #DCE0F7;background:#F8F9FF;padding:0 12px;font:600 15px \'Pretendard Variable\',Pretendard,sans-serif;color:#18324F;outline:none;min-width:0;"></label>', '<span style="display:flex;gap:8px;align-items:center"><sc-if value="{{ f.isPrice }}" hint-placeholder-val="{{ false }}"><span style="flex:none;display:flex;padding:3px;border-radius:99px;background:#EEF0FA"><sc-for list="{{ f.curs }}" as="c" hint-placeholder-count="2"><button onClick="{{ c.pick }}" style="height:40px;width:46px;border:0;border-radius:99px;background:{{ c.bg }};color:{{ c.fg }};font:800 14px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer;box-shadow:{{ c.sh }}">{{ c.label }}</button></sc-for></span></sc-if><input value="{{ f.v }}" onChange="{{ f.on }}" placeholder="" style="flex:1;height:46px;border-radius:14px;border:1px solid #DCE0F7;background:#F8F9FF;padding:0 12px;font:600 15px \'Pretendard Variable\',Pretendard,sans-serif;color:#18324F;outline:none;min-width:0;"><sc-if value="{{ f.isNote }}" hint-placeholder-val="{{ false }}"><button onClick="{{ pl2.lsave }}" style="flex:none;white-space:nowrap;height:46px;padding:0 18px;border:0;border-radius:14px;background:{{ pl2.lsBtnBg }};color:{{ pl2.lsBtnFg }};font:800 15px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer">{{ pl2.lsBtnT }}</button></sc-if></span></label>')
rep('{{ dd2.lodge }}</b></span>', '{{ dd2.lodge }}</b><sc-if value="{{ dd2.hasLodgeSub }}" hint-placeholder-val="{{ false }}"><span style="font-size:13px;font-weight:600;color:#6B7A90;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ dd2.lodgeSub }}</span></sc-if></span>')
rep('<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><sc-for list="{{ pl2.sum }}"', '<div style="background:{{ pl2.lw.bg }};border-radius:20px;padding:14px 16px;display:flex;flex-direction:column;gap:8px"><span style="display:flex;align-items:center;gap:8px;font-size:16px;font-weight:800;color:{{ pl2.lw.fg }}"><span style="@@IC@@font-size:24px;color:{{ pl2.lw.fg }}">{{ pl2.lw.icon }}</span>{{ pl2.lw.title }}</span><sc-for list="{{ pl2.lw.rows }}" as="r" hint-placeholder-count="3"><button onClick="{{ r.go }}" style="display:flex;align-items:center;gap:10px;height:44px;padding:0 12px;border:0;border-radius:14px;background:rgba(255,255,255,.75);cursor:pointer;font-family:inherit;color:#18324F;text-align:left"><b style="flex:none;font-size:14px;color:#5B32D6">DAY {{ r.n }}</b><span style="flex:1;min-width:0;font-size:15px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ r.name }} <span style="font-size:13px;font-weight:600;color:#6B7A90">{{ r.date }}</span></span><span style="flex:none;white-space:nowrap;font-size:13px;font-weight:800;padding:4px 10px;border-radius:99px;background:{{ r.sb }};color:{{ r.sf }}">{{ r.st }}</span></button></sc-for></div>\n'.replace('@@IC@@', _ic) + '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><sc-for list="{{ pl2.sum }}"')
# 전체 여정: 53역참 진행 카드 삭제 → 날짜별 플랜 + 역참 카드(좌우 날짜 이동)
import re as _re3
_m3 = _re3.search(r'<div style="background:#fff;[^\n]*\n<span style="display:flex;align-items:baseline;justify-content:space-between;gap:8px"><b[^\n]*>53역참 진행</b>.*?\n</div>\n', dc, _re3.S)
assert _m3, '53card'
dc = dc[:_m3.start()] + ('<div style="background:linear-gradient(160deg,#fff,#F6F1FF);border:1px solid #E8E1FB;box-shadow:0 10px 28px rgba(84,40,232,.10);border-radius:24px;padding:16px;display:flex;flex-direction:column;gap:14px;min-width:0">\n<div style="display:flex;align-items:center;gap:10px"><button onClick="{{ jc.prev }}" style="flex:none;width:44px;height:44px;border-radius:14px;border:0;background:#fff;box-shadow:0 3px 10px rgba(40,50,140,.12);cursor:pointer;opacity:{{ jc.prevO }}"><span style="@@IC@@font-size:24px;color:#5B32D6">chevron_left</span></button><span style="flex:1;min-width:0;display:flex;align-items:center;justify-content:center;gap:8px;white-space:nowrap"><b style="font-size:14px;font-weight:800;color:#5B32D6;letter-spacing:.06em">DAY {{ jc.n }}</b><span style="font-size:14px;font-weight:700;color:#6B7A90">{{ jc.date }}</span><span style="font-size:13px;font-weight:800;padding:4px 10px;border-radius:99px;background:{{ jc.sb }};color:{{ jc.sf }}">{{ jc.st }}</span></span><button onClick="{{ jc.next }}" style="flex:none;width:44px;height:44px;border-radius:14px;border:0;background:#fff;box-shadow:0 3px 10px rgba(40,50,140,.12);cursor:pointer;opacity:{{ jc.nextO }}"><span style="@@IC@@font-size:24px;color:#5B32D6">chevron_right</span></button></div>\n<div style="display:flex;flex-direction:column;gap:4px"><b style="font-size:22px;font-weight:800;letter-spacing:-.03em;color:#20202A">{{ jc.title }}</b><span style="font-size:13px;color:#85859A;line-height:1.45">{{ jc.jpPath }}</span></div>\n<div style="display:grid;grid-template-columns:18px minmax(0,1fr);gap:8px;align-items:stretch"><b style="writing-mode:vertical-rl;transform:rotate(180deg);font-size:11px;letter-spacing:.14em;color:#85859A;text-align:center">PLAN</b><div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-radius:16px;background:#fff;border:1px solid #E8E7EF"><sc-for list="{{ jc.plan }}" as="x" hint-placeholder-count="3"><span style="display:flex;flex-direction:column;align-items:center;gap:3px;padding:12px 4px;min-width:0"><b style="font-size:17px;font-weight:800;color:#20202A;white-space:nowrap">{{ x.v }}</b><span style="font-size:13px;color:#85859A;white-space:nowrap">{{ x.k }}</span></span></sc-for></div></div>\n<div style="display:grid;grid-template-columns:18px minmax(0,1fr);gap:8px;align-items:stretch"><b style="writing-mode:vertical-rl;transform:rotate(180deg);font-size:11px;letter-spacing:.14em;color:#5B32D6;text-align:center">ACTUAL</b><div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-radius:16px;background:#fff;border:1px solid #CDBBFF"><sc-for list="{{ jc.act }}" as="x" hint-placeholder-count="3"><span style="display:flex;flex-direction:column;align-items:center;gap:3px;padding:12px 4px;min-width:0"><b style="font-size:17px;font-weight:800;color:#5B32D6;white-space:nowrap">{{ x.v }}</b><span style="font-size:13px;color:#85859A;white-space:nowrap">{{ x.k }}</span></span></sc-for></div></div>\n<div style="background:#fff;border:1px solid #E8E7EF;border-radius:20px;padding:14px 14px 6px;display:flex;flex-direction:column"><span style="font-size:12px;font-weight:800;letter-spacing:.08em;color:#85859A;margin-bottom:8px">WAYPOINTS · 이 날 지나는 역참</span><sc-for list="{{ jc.wps }}" as="w" hint-placeholder-count="5"><div style="display:grid;grid-template-columns:30px minmax(0,1fr) auto;gap:12px;align-items:center;min-height:50px;position:relative"><span style="position:relative;display:flex;justify-content:center;align-self:stretch;align-items:center"><span style="position:absolute;top:0;bottom:0;width:3px;background:{{ w.line }};border-radius:2px"></span><span style="position:relative;width:28px;height:28px;border-radius:50%;background:{{ w.bg }};color:{{ w.fg }};display:grid;place-items:center;font-size:13px;font-weight:800;box-shadow:0 0 0 3px #fff">{{ w.lab }}</span></span><span style="display:flex;align-items:baseline;gap:6px;min-width:0"><b style="font-size:16px;white-space:nowrap">{{ w.ko }}</b><span style="font-size:13px;color:#85859A;white-space:nowrap">{{ w.jp }}</span></span><b style="font-size:14px;color:#4A5D78;white-space:nowrap">{{ w.km }}</b></div></sc-for></div>\n<button onClick="{{ jc.detail }}" style="height:46px;border-radius:99px;border:0;background:linear-gradient(135deg,#5428E8,#9A63F5);color:#fff;font:800 15px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer;box-shadow:0 8px 20px rgba(84,40,232,.3)">DAY {{ jc.n }} 자세히 보기</button>\n</div>\n').replace('@@IC@@', _ic) + dc[_m3.end():]
rep('<span>{{ tt.st }} / 53 역참 · 남은 {{ tt.left }}</span>', '<span>남은 {{ tt.left }}</span>')

# 전체 여정: 좌 = 전체 일정, 우 = 요약·날짜별 플랜·웨이포인트 / 일정 관리 버튼은 맨 아래
import re as _re4
_bs = dc.index('<div style="padding:0 16px 12px"><button onClick="{{ goPlanSub }}"')
_be = dc.index('</button></div>', _bs) + len('</button></div>')
_btn = dc[_bs:_be]
dc = dc[:_bs] + dc[_be:]
_gs = dc.index('<div style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;padding:0 16px;align-items:stretch">', dc.index('{{ jc.prev }}') - 12000)
_colopen = '<div style="display:flex;flex-direction:column;gap:12px;min-width:0">'
_ca = dc.index(_colopen, _gs)
_cb = dc.index(_colopen, dc.index('{{ jn.weeks }}', _ca))
def _end(t, st):
    d = 0
    for m in _re4.finditer(r'<(/?)div\b[^>]*>', t[st:]):
        d += -1 if m.group(1) else 1
        if d == 0: return st + m.end()
_ea = _end(dc, _ca); _eb = _end(dc, _cb)
assert _ea <= _cb, (_ea, _cb)
_A = dc[_ca:_ea]; _B = dc[_cb:_eb]
dc = dc[:_ca] + _B + dc[_ea:_cb] + _A + dc[_eb:]
_ge = _end(dc, _gs)
dc = dc[:_ge] + '\n' + _btn.replace('padding:0 16px 12px', 'padding:12px 16px 24px') + dc[_ge:]

rep('<button onClick="{{ back2 }}" aria-label="뒤로 가기"', '<sc-if value="{{ sb2.glance }}" hint-placeholder-val="{{ false }}"><div style="position:absolute;left:0;right:0;bottom:calc(env(safe-area-inset-bottom) + 22px);z-index:3;padding:0 16px;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;pointer-events:none"><div style="pointer-events:auto;height:60px;max-width:calc(100% - 0px);box-sizing:border-box;display:flex;align-items:center;gap:2px;padding:6px;gap:6px;border-radius:30px;background:rgba(255,255,255,.92);border:1px solid #E1D8FB;backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);box-shadow:0 12px 26px rgba(40,50,140,.16)"><sc-for list="{{ jn.gj }}" as="c" hint-placeholder-count="5"><button onClick="{{ c.go }}" style="flex:1;min-width:0;white-space:nowrap;height:48px;padding:0 4px;border:0;border-radius:24px;background:{{ c.bg }};color:{{ c.fg }};box-shadow:{{ c.sh }};font:800 16px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer;transition:background .2s">{{ c.label }}</button></sc-for></div></div></sc-if>\n' + '<button onClick="{{ back2 }}" aria-label="뒤로 가기"')
# 전체 여정: 상단 전체 폭에 전체 이동 거리 + 통계 띠 (좌 전체 일정 / 우 날짜 플랜이 첫 화면에 보이도록)
_s0 = dc.index('<div style="border-radius:28px;padding:20px;background:linear-gradient(120deg,#5B6FD4,#8B9CF0,#C9B8F5)', dc.index('{{ jc.prev }}') - 14000)
_s1 = _end(dc, _s0)
_summary = dc[_s0:_s1]
_trk = '<span style="height:8px;border-radius:99px;background:rgba(255,255,255,.3);overflow:hidden;margin-top:4px"><span style="display:block;height:100%;border-radius:99px;background:#fff;width:{{ tt.w }}"></span></span>'
assert _trk in _summary, 'trk'
_summary = _summary.replace(_trk, '<div style="position:relative;margin:6px 6px 0;height:118px"><span style="position:absolute;left:0;right:0;top:50px;height:6px;border-radius:99px;background:rgba(255,255,255,.3)"></span><span style="position:absolute;left:0;top:50px;height:6px;border-radius:99px;background:#fff;width:{{ jr.fill }};transition:width .5s ease"></span><sc-for list="{{ jr.dots }}" as="q" hint-placeholder-count="31"><span style="position:absolute;left:{{ q.x }};top:53px;width:{{ q.big }}px;height:{{ q.big }}px;transform:translate(-50%,-50%);border-radius:50%;background:{{ q.bg }};border:2px solid {{ q.bd }};box-sizing:border-box"></span></sc-for><span style="position:absolute;left:{{ jr.fill }};top:0;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:3px;transition:left .5s ease"><span style="white-space:nowrap;font-size:13px;font-weight:800;padding:3px 10px;border-radius:99px;background:#fff;color:#5B32D6;box-shadow:0 4px 12px rgba(40,30,120,.25)">{{ jr.curT }} · {{ jr.curKm }}</span><span style="width:34px;height:34px;border-radius:50%;background:#fff;display:grid;place-items:center;box-shadow:0 4px 12px rgba(40,30,120,.3);margin-top:-2px"><span style="@@IC@@font-size:22px;color:#5B32D6">directions_walk</span></span></span><sc-for list="{{ jr.labels }}" as="q" hint-placeholder-count="4"><span style="position:absolute;left:{{ q.x }};top:72px;transform:translateX(-50%);font-size:13px;font-weight:700;white-space:nowrap;opacity:.95">{{ q.t }}</span></sc-for><span style="position:absolute;left:0;top:96px;font-size:13px;font-weight:800;white-space:nowrap">출발 {{ jr.a }}</span><span style="position:absolute;right:0;top:96px;font-size:13px;font-weight:800;white-space:nowrap">도착 {{ jr.b }}</span></div>'.replace('@@IC@@', _ic))
dc = dc[:_s0] + dc[_s1:]
_t0 = dc.index('<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px"><sc-for list="{{ jn.stats }}"')
_t1 = _end(dc, _t0)
_stats = dc[_t0:_t1].replace('repeat(2,minmax(0,1fr))', 'repeat(auto-fit,minmax(140px,1fr))', 1)
dc = dc[:_t0] + dc[_t1:]
_summary = _summary.replace('font-size:40px;font-weight:800', 'font-size:48px;font-weight:800', 1)
_g0 = dc.index('<div style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;padding:0 16px;align-items:stretch">', dc.index('{{ jc.prev }}') - 14000)
dc = dc[:_g0] + '<div style="padding:0 16px 12px;display:flex;flex-direction:column;gap:10px">' + _summary + _stats + '</div>\n' + dc[_g0:]


# 오늘 지출: 분류 → 내용 → 금액 순서로 재배치 + 총 지출(오늘/누적/평균/분류별) 요약
_a = dc.index('<div style="display:flex;gap:8px;align-items:center">\n<div style="flex:none;display:flex;padding:3px')
_b = dc.index('placeholder="내용 (예: 라멘, 가케가와 호텔)"')
_b = dc.index('>', _b) + 1
_blk = dc[_a:_b]
_row = _blk[:_blk.index('</div>\n<div style="display:flex;gap:6px;flex-wrap:wrap">')+6]
_chips = _blk[len(_row)+1:_blk.index('</sc-for></div>', len(_row))+len('</sc-for></div>')]
_memo = _blk[_blk.index('<input value="{{ lg2.nnote }}"'):]
_memo = _memo.replace('height:46px;border-radius:14px', 'height:50px;border-radius:14px').replace('font:600 15px', 'font:600 16px')
_row = _row.replace('height:46px;border-radius:14px', 'height:54px;border-radius:14px').replace('height:46px;padding:0 16px', 'height:54px;padding:0 20px').replace('font-size:18px;font-weight:800', 'font-size:20px;font-weight:800')
_sum = ('<div style="border-radius:18px;padding:14px 16px;background:linear-gradient(135deg,#5428E8,#9A63F5);color:#fff;display:flex;flex-direction:column;gap:10px">'
 '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">'
 '<div style="display:flex;flex-direction:column;gap:2px;min-width:0"><span style="font-size:13px;opacity:.85">오늘</span><b style="font-size:19px;white-space:nowrap">{{ lg2.total }}</b></div>'
 '<div style="display:flex;flex-direction:column;gap:2px;min-width:0"><span style="font-size:13px;opacity:.85">총 누적</span><b style="font-size:19px;white-space:nowrap">{{ lg2.cum }}</b></div>'
 '<div style="display:flex;flex-direction:column;gap:2px;min-width:0"><span style="font-size:13px;opacity:.85">하루 평균</span><b style="font-size:19px;white-space:nowrap">{{ lg2.avgE }}</b></div></div>'
 '<div style="display:flex;gap:6px;flex-wrap:wrap"><sc-for list="{{ lg2.catT }}" as="q" hint-placeholder-count="4"><span style="background:rgba(255,255,255,.2);border-radius:99px;padding:5px 10px;font-size:13px;font-weight:700;white-space:nowrap">{{ q.k }} {{ q.v }}</span></sc-for></div>'
 '<div style="display:flex;align-items:flex-end;gap:4px;height:84px"><sc-for list="{{ lg2.expBars }}" as="b" hint-placeholder-count="14"><span style="flex:1;min-width:0;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:3px"><i style="display:block;width:100%;height:{{ b.h }};border-radius:5px 5px 2px 2px;background:#fff;opacity:{{ b.o }}"></i><span style="font-size:12px;font-weight:700;opacity:.85">{{ b.l }}</span></span></sc-for></div></div>')
_new = _sum + '\n' + _chips + '\n' + _memo + '\n' + _row
dc = dc[:_a] + _new + dc[_b:]
_cl = re.search(r'<span style="display:flex;justify-content:space-between;font-size:13px;color:#4A5D78;padding-top:8px;border-top:1px solid #EEF0F7"><span>[^<]*</span><b[^>]*>\{\{ lg2.cum \}\}</b></span>', dc)
assert _cl, 'cumline'
dc = dc[:_cl.start()] + dc[_cl.end():]


# 체중 그래프: 점(1개여도 표시)
_si = dc.index('<svg viewBox="0 0 300 110" preserveAspectRatio="none" style="width:100%;height:120px;display:block"><line x1="0" y1="{{ lg2.wtBase }}"')
_se = dc.index('</svg>', _si) + 6
dc = dc[:_si] + '<div style="position:relative">' + dc[_si:_se] + '<sc-for list="{{ lg2.wtDots }}" as="d" hint-placeholder-count="3"><span style="position:absolute;left:{{ d.x }}%;top:{{ d.y }}%;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;background:#1C7ED6;border:2px solid #fff;box-shadow:0 1px 4px rgba(28,126,214,.5)"></span></sc-for></div>' + dc[_se:]


# 전체 여정: 주차별 거리를 5개 가로 버튼으로 (좌 전체 일정 / 우 날짜 플랜 높이 동일)
_wi = dc.index('<b style="font-size:18px;font-weight:800;letter-spacing:-.03em">주차별 거리</b>')
_wc = dc.rindex('<div style="flex:1;background:#fff;', 0, _wi)
_we = _end(dc, _wc)
dc = dc[:_wc] + dc[_we:]
_wk = ('<div style="padding:0 16px"><div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:24px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0">'
 '<span style="display:flex;align-items:baseline;justify-content:space-between;gap:8px"><b style="font-size:18px;font-weight:800;letter-spacing:-.03em">주차별 거리</b><span style="font-size:13px;color:#6B7A90">눌러서 그 주 시작일 보기</span></span>'
 '<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px"><sc-for list="{{ jn.weeks }}" as="w" hint-placeholder-count="5">'
 '<button onClick="{{ w.go }}" style="display:flex;flex-direction:column;align-items:center;gap:6px;min-width:0;padding:12px 6px;border-radius:18px;border:1px solid #DCE0F7;background:#F6F7FF;cursor:pointer;font-family:\'Pretendard Variable\',Pretendard,sans-serif;color:#18324F">'
 '<b style="font-size:16px">{{ w.label }}</b><b style="font-size:15px;white-space:nowrap">{{ w.km }}</b>'
 '<span style="width:100%;height:8px;border-radius:99px;background:#EEF0FA;overflow:hidden"><span style="display:block;height:100%;border-radius:99px;background:{{ w.c }};width:{{ w.w }}"></span></span>'
 '<span style="font-size:12px;font-weight:800;padding:3px 8px;border-radius:99px;background:{{ w.sb }};color:{{ w.sf }};white-space:nowrap">{{ w.st }}</span></button></sc-for></div></div></div>')
_gs2 = dc.index('<div style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;padding:0 16px;align-items:stretch">', dc.index('{{ jc.prev }}') - 14000)
_ge2 = _end(dc, _gs2)
dc = dc[:_ge2] + '\n' + _wk + dc[_ge2:]


# 여정: 우측 카드가 좌측 높이만큼 채우고, 주차 버튼에 구간 표시, 위와 간격
rep('<div style="background:linear-gradient(160deg,#fff,#F6F1FF);border:1px solid #E8E1FB;', '<div style="flex:1;background:linear-gradient(160deg,#fff,#F6F1FF);border:1px solid #E8E1FB;')
rep('<div style="background:#fff;border:1px solid #E8E7EF;border-radius:20px;padding:14px 14px 6px;display:flex;flex-direction:column">', '<div style="flex:1;background:#fff;border:1px solid #E8E7EF;border-radius:20px;padding:14px 14px 6px;display:flex;flex-direction:column;justify-content:center">')
rep('<div style="padding:0 16px"><div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:24px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0"><span style="display:flex;align-items:baseline;justify-content:space-between;gap:8px"><b style="font-size:18px;font-weight:800;letter-spacing:-.03em">주차별 거리</b>', '<div style="padding:14px 16px 0"><div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:24px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0"><span style="display:flex;align-items:baseline;justify-content:space-between;gap:8px"><b style="font-size:18px;font-weight:800;letter-spacing:-.03em">주차별 거리</b>')
rep('<b style="font-size:16px">{{ w.label }}</b><b style="font-size:15px;white-space:nowrap">{{ w.km }}</b>', '<b style="font-size:16px">{{ w.label }}</b><b style="font-size:15px;white-space:nowrap">{{ w.km }}</b><span style="font-size:13px;color:#4A5D78;line-height:1.35;text-align:center;word-break:keep-all">{{ w.path }}</span>')


# 일정 관리: 출발일 입력 (기본 12/4) — 모든 날짜 계산이 이 값을 따름
_dc_card = '<div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:24px;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:12px"><span style="display:flex;flex-direction:column;gap:2px"><b style="font-size:17px">출발일</b><span style="font-size:13px;color:#6B7A90">바꾸면 모든 날짜가 같이 움직여요</span></span><input type="date" value="{{ pl2.sd }}" onChange="{{ pl2.sdSet }}" style="height:48px;border-radius:14px;border:1px solid #DCE0F7;background:#F6F7FF;padding:0 12px;font:700 16px \'Pretendard Variable\',Pretendard,sans-serif;color:#18324F"></span></div>'
_ls = dc.index('<div style="background:{{ pl2.lw.bg }};')
_le = _end(dc, _ls)
dc = dc[:_le] + '\n' + _dc_card + dc[_le:]


# 주차 버튼 디자인: 보라 그라데이션 라벨 + 보라 거리, 예정 칩 제거
_ws = dc.index('<button onClick="{{ w.go }}"'); _we = dc.index('</button>', _ws) + 9
dc = dc[:_ws] + ('<button onClick="{{ w.go }}" style="display:flex;flex-direction:column;align-items:center;gap:8px;min-width:0;padding:14px 6px;border-radius:20px;border:1px solid #E1D8FB;background:linear-gradient(160deg,#fff,#F3EEFF);box-shadow:0 6px 16px rgba(84,40,232,.08);cursor:pointer;font-family:\'Pretendard Variable\',Pretendard,sans-serif;color:#18324F">'
 '<b style="font-size:15px;color:#fff;padding:4px 14px;border-radius:99px;background:linear-gradient(135deg,#5428E8,#9A63F5)">{{ w.label }}</b>'
 '<b style="font-size:19px;font-weight:800;color:#5B32D6;white-space:nowrap;letter-spacing:-.02em">{{ w.km }}</b>'
 '<span style="font-size:13px;color:#4A5D78;line-height:1.35;text-align:center;word-break:keep-all">{{ w.path }}</span>'
 '<span style="width:100%;height:8px;border-radius:99px;background:#E7E0FA;overflow:hidden"><span style="display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#5428E8,#9A63F5);width:{{ w.w }}"></span></span>'
 '<sc-if value="{{ w.show }}" hint-placeholder-val="{{ false }}"><span style="font-size:12px;font-weight:800;padding:3px 10px;border-radius:99px;background:{{ w.sb }};color:{{ w.sf }};white-space:nowrap">{{ w.st }}</span></sc-if></button>') + dc[_we:]


# 환율: 500엔~1만엔 원화 환산표
_q = dc.index('{{ fx2.quick }}'); _qe = dc.index('</sc-for></div>', _q) + len('</sc-for></div>')
dc = dc[:_qe] + ('\n<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><sc-for list="{{ fx2.tbl }}" as="r" hint-placeholder-count="6"><span style="display:flex;flex-direction:column;align-items:center;gap:3px;padding:10px 4px;border-radius:16px;background:linear-gradient(160deg,#fff,#F3EEFF);border:1px solid #E1D8FB"><b style="font-size:15px;color:#4A5D78">{{ r.y }}</b><b style="font-size:17px;color:#5B32D6;white-space:nowrap">{{ r.w }}</b></span></sc-for></div>') + dc[_qe:]




# 일정 관리: 되돌리기/변경 저장 버튼 — 화면 하단 중앙 고정
rep('<div style="flex:1;display:flex;gap:8px"><button onClick="{{ pl2.reset }}"', '<div style="height:76px"></div><div style="position:fixed;left:0;right:0;bottom:calc(env(safe-area-inset-bottom) + 22px);z-index:4;display:flex;justify-content:center;pointer-events:none"><div style="pointer-events:auto;display:flex;gap:8px;width:min(440px,calc(100% - 300px));min-width:280px;padding:8px;border-radius:35px;background:rgba(255,255,255,.92);border:1px solid #E1D8FB;box-shadow:0 12px 28px rgba(40,50,140,.18);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)"><button onClick="{{ pl2.reset }}"')
_k = dc.index('{{ pl2.saveLabel }}</button></div>') + len('{{ pl2.saveLabel }}</button></div>')
dc = dc[:_k] + '</div>' + dc[_k:]


# 일정 관리 상단 날짜 탭: 점 대신 글자 라벨(날짜/휴식/변경/오늘), 휴식일은 하늘색 칩, 좌우 스크롤 힌트(우측 페이드+화살표)
_ts = dc.index('<div style="display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:0 16px 4px">\n<sc-for list="{{ pl2.days }}"')
_te = dc.index('</sc-for>\n</div>', _ts) + len('</sc-for>\n</div>')
dc = dc[:_ts] + ('<div style="position:relative"><div id="pl-days" onScroll="{{ pl2.daysScroll }}" style="display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:0 56px 6px 16px;scroll-snap-type:x proximity">\n'
 '<sc-for list="{{ pl2.days }}" as="d" hint-placeholder-count="8"><button onClick="{{ d.pick }}" style="flex:none;scroll-snap-align:start;width:64px;height:78px;border-radius:22px;border:1px solid {{ d.bd }};background:{{ d.bg }};backdrop-filter:blur(22px) saturate(1.4);-webkit-backdrop-filter:blur(22px) saturate(1.4);color:{{ d.fg }};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;cursor:pointer;font-family:inherit;box-shadow:{{ d.sh }}"><span style="font-size:12px;font-weight:800;opacity:.85">DAY</span><b style="font-size:22px;line-height:1.1">{{ d.n }}</b><span style="font-size:12px;font-weight:800;color:{{ d.sc }};white-space:nowrap">{{ d.sub }}</span></button></sc-for>\n</div>'
 '<div style="position:absolute;right:0;top:0;bottom:6px;width:64px;pointer-events:none;background:linear-gradient(90deg,rgba(236,238,255,0),rgba(236,238,255,.95) 70%)"></div>'
 '<button onClick="{{ pl2.daysMore }}" aria-label="다음 날짜 보기" style="position:absolute;right:12px;top:50%;margin-top:-22px;width:40px;height:40px;border-radius:50%;border:0;background:#fff;box-shadow:0 4px 12px rgba(40,50,140,.22);display:grid;place-items:center;cursor:pointer"><span style="@@IC@@font-size:24px;color:#5B32D6">chevron_right</span></button></div>'
 '<div style="display:flex;justify-content:center;gap:8px;padding-top:2px"><i id="pd-dot-0" style="width:28px;height:10px;border-radius:99px;background:linear-gradient(135deg,#5428E8,#9A63F5)"></i><i id="pd-dot-1" style="width:10px;height:10px;border-radius:99px;background:#C9C4EE"></i><i id="pd-dot-2" style="width:10px;height:10px;border-radius:99px;background:#C9C4EE"></i><i id="pd-dot-3" style="width:10px;height:10px;border-radius:99px;background:#C9C4EE"></i><i id="pd-dot-4" style="width:10px;height:10px;border-radius:99px;background:#C9C4EE"></i></div>').replace('@@IC@@', _ic) + dc[_te:]


# 일정 관리 요약 타일: 정사각형에 가깝게 키우고 그라데이션/아이콘 배지
_ss = dc.index('<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><sc-for list="{{ pl2.sum }}"')
_se = dc.index('</sc-for></div>', _ss) + len('</sc-for></div>')
dc = dc[:_ss] + ('<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;padding-top:6px"><sc-for list="{{ pl2.sum }}" as="x" hint-placeholder-count="3"><span style="min-height:150px;box-sizing:border-box;overflow:hidden;border-radius:26px;padding:16px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;background:{{ x.g }};border:1px solid #E1D8FB;box-shadow:0 10px 24px rgba(84,40,232,.12)">'
 '<span style="width:44px;height:44px;border-radius:15px;background:{{ x.bg }};display:grid;place-items:center"><span style="@@IC@@font-size:26px;color:{{ x.ic }}">{{ x.icon }}</span></span>'
 '<span style="display:flex;flex-direction:column;gap:3px;min-width:0"><span style="font-size:14px;font-weight:700;color:{{ x.sf }};white-space:nowrap">{{ x.k }}</span><b style="font-size:28px;font-weight:800;letter-spacing:-.03em;color:{{ x.fg }};white-space:nowrap">{{ x.v }}</b><span style="font-size:13px;font-weight:700;color:{{ x.sf }};overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ x.sub }}</span></span></span></sc-for></div>').replace('@@IC@@', _ic) + dc[_se:]


dc = dc.replace('cursor:pointer">되돌리기</button>', 'cursor:pointer">이 날 되돌리기</button>')

# 전체 여정 상단: 날짜별 사진 배경 + 우측 상단 진행 요약 + 사진 스트립 (일본어·점 인포그래픽 제거)
_bs0 = dc.index('<div style="border-radius:28px;padding:20px;background:linear-gradient(120deg,#5B6FD4,#8B9CF0,#C9B8F5)', dc.index('{{ jc.prev }}') - 14000)
_bs1 = _end(dc, _bs0)
dc = dc[:_bs0] + ('<div style="position:relative;overflow:hidden;border-radius:28px;color:#fff;box-shadow:inset 0 1px 0 rgba(255,255,255,.45),0 14px 30px rgba(84,40,232,.30);min-width:0">'
 '<div style="position:absolute;inset:0;background:{{ jr.bg }}"></div>'
 '<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(84,40,232,.55),rgba(70,35,190,.5) 45%,rgba(28,14,90,.9))"></div>'
 '<div style="position:relative;padding:20px;display:flex;flex-direction:column;gap:14px;text-shadow:0 1px 3px rgba(20,10,80,.4)">'
 '<div style="display:flex;align-items:center;justify-content:space-between;gap:10px"><span style="font-size:16px;font-weight:800">{{ jr.a }} → {{ jr.b }}</span><span style="white-space:nowrap;font-size:14px;font-weight:800;padding:6px 14px;border-radius:99px;background:rgba(255,255,255,.22);border:1px solid rgba(255,255,255,.45);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)">{{ tt.pct }} 완주 · 남은 {{ tt.left }}</span></div>'
 '<b style="font-size:52px;font-weight:800;letter-spacing:-.05em;line-height:1.05">{{ tt.km }}<span style="font-size:18px;font-weight:700"> / 488km</span></b>'
 '<div style="display:flex;flex-direction:column;gap:8px"><div style="position:relative;height:12px;border-radius:99px;background:rgba(255,255,255,.3)"><span style="position:absolute;left:0;top:0;bottom:0;border-radius:99px;background:#fff;width:{{ jr.fill }};transition:width .5s ease"></span></div>'
 '<span style="display:flex;justify-content:space-between;font-size:14px;font-weight:800"><span>출발 {{ jr.a }}</span><span>{{ jr.curT }} · {{ jr.curKm }}</span><span>도착 {{ jr.b }}</span></span></div>'
 '<div style="display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:2px 0 4px"><sc-for list="{{ jr.strip }}" as="q" hint-placeholder-count="12"><button id="{{ q.sid }}" onClick="{{ q.go }}" style="flex:none;position:relative;width:64px;height:76px;border-radius:18px;border:2px solid {{ q.bd }};background:{{ q.img }};opacity:{{ q.op }};box-shadow:{{ q.sh }};cursor:pointer;padding:0;overflow:hidden"><span style="position:absolute;left:0;right:0;bottom:0;padding:14px 0 4px;background:linear-gradient(180deg,rgba(0,0,0,0),rgba(20,10,70,.85));font:800 15px \'Pretendard Variable\',Pretendard,sans-serif;color:#fff">{{ q.n }}</span></button></sc-for></div>'
 '</div></div>') + dc[_bs1:]


# 이동 방식: 열차/버스/택시 선택 제거 (어디에도 기록되지 않음)
_ms = dc.index('<sc-if value="{{ pl2.hasTr }}" hint-placeholder-val="{{ false }}"><div style="display:flex;flex-direction:column;gap:8px;padding-top:10px;border-top:1px solid #EEF0F7"><b style="font-size:14px;color:#4A5D78">교통 수단</b>')
_me = dc.index('</sc-if>', _ms) + len('</sc-if>')
dc = dc[:_ms] + dc[_me:]


# 홈 경유지 팝업: 설명 2줄 고정(높이 일정), 상세 정보 보기 = 전체 설명 펼치기
rep('<p style="margin:0;font-size:15px;line-height:1.6;color:#3A4D68;text-wrap:pretty">{{ sp.desc }}</p>', '<p style="margin:0;font-size:15px;line-height:1.6;color:#3A4D68;text-wrap:pretty;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:{{ sp.lc }};overflow:hidden;min-height:{{ sp.mh }}">{{ sp.desc }}</p>')
rep("""<button style="flex:none;white-space:nowrap;height:48px;padding:0 6px;border:0;background:transparent;display:flex;align-items:center;gap:4px;font:800 15px 'Pretendard Variable',Pretendard,sans-serif;color:#3B5BDB;cursor:pointer">""", """<button onClick="{{ sp.toggleFull }}" style="flex:none;white-space:nowrap;height:48px;padding:0 6px;border:0;background:transparent;display:flex;align-items:center;gap:4px;font:800 15px 'Pretendard Variable',Pretendard,sans-serif;color:#3B5BDB;cursor:pointer">""")
rep('</span>상세 정보 보기<span', '</span>{{ sp.fullT }}<span')


# 기록 탭: 오늘의 기분·사진 카드 (몸 상태 카드 위)
_mi = dc.index('<button onClick="{{ lgc.cond.toggle }}"')
_mc = dc.rindex('<div style="background:#fff;', 0, _mi)
_card = ('<div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:24px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0">\n'
 '<button onClick="{{ lgc.mood.toggle }}" style="width:100%;border:0;background:transparent;padding:0;display:flex;align-items:center;gap:10px;text-align:left;cursor:pointer;font-family:inherit;color:#18324F"><b style="flex:none;font-size:18px;font-weight:800;letter-spacing:-.03em">오늘의 기분 · 사진</b><span style="flex:1;min-width:0;text-align:right;font-size:14px;font-weight:800;color:{{ lgc.mood.c }};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ lgc.mood.sum }}</span><span style="flex:none;width:32px;height:32px;border-radius:50%;background:#F3F5FF;display:grid;place-items:center;transform:{{ lgc.mood.rot }};transition:transform .2s"><span style="@@IC@@font-size:22px;color:#3B5BDB">expand_more</span></span></button>\n'
 '<sc-if value="{{ lgc.mood.open }}" hint-placeholder-val="{{ true }}"><div style="display:flex;flex-direction:column;gap:12px">'
 '<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px"><sc-for list="{{ lg2.mood.chips }}" as="c" hint-placeholder-count="5"><button onClick="{{ c.pick }}" style="height:72px;border-radius:18px;border:1px solid {{ c.bd }};background:{{ c.bg }};color:{{ c.fg }};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font:800 14px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer;padding:0"><span style="font-size:28px;line-height:1">{{ c.e }}</span>{{ c.l }}</button></sc-for></div>'
 '<input value="{{ lg2.mood.note }}" onChange="{{ lg2.mood.onNote }}" placeholder="오늘 한 줄 (예: 후지산이 보였다)" style="width:100%;box-sizing:border-box;height:50px;border-radius:14px;border:1px solid #DCE0F7;background:#F6F7FF;padding:0 14px;font:600 16px \'Pretendard Variable\',Pretendard,sans-serif;color:#18324F;outline:none">'
 '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><sc-for list="{{ lg2.mood.photos }}" as="p" hint-placeholder-count="2"><div style="position:relative;aspect-ratio:1/1;border-radius:18px;background:{{ p.bg }};overflow:hidden"><button onClick="{{ p.del }}" aria-label="사진 삭제" style="position:absolute;top:6px;right:6px;width:34px;height:34px;border-radius:50%;border:0;background:rgba(20,10,70,.6);color:#fff;font:800 16px sans-serif;cursor:pointer;padding:0">✕</button></div></sc-for>'
 '<sc-if value="{{ lg2.mood.canAdd }}" hint-placeholder-val="{{ true }}"><button onClick="{{ lg2.mood.add }}" style="min-width:0;overflow:hidden;aspect-ratio:1/1;border-radius:18px;border:2px dashed #C9C4EE;background:#F6F4FF;color:#5B32D6;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;font:800 14px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer;padding:0"><span style="@@IC@@font-size:30px;color:#5B32D6">add_a_photo</span>사진 추가</button></sc-if></div>'
 '<input id="ph-in" type="file" accept="image/*" multiple onChange="{{ lg2.mood.onPhoto }}" style="display:none">'
 '</div></sc-if></div>\n').replace('@@IC@@', _ic)
dc = dc[:_mc] + _card + dc[_mc:]


# 사진 일기: 날짜별 여러 장 콜라주(1~4장) + 기분 칩 + 사진 수
rep('<span style="position:relative;display:grid;place-items:center;width:100%;aspect-ratio:4/3;filter:{{ dkImg }};background:{{ d.grad }}">', '<span style="position:relative;display:grid;place-items:center;width:100%;aspect-ratio:4/3;filter:{{ dkImg }};background:{{ d.grad }};overflow:hidden"><span style="position:absolute;inset:0;display:grid;gap:2px;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr"><sc-for list="{{ d.pics }}" as="p" hint-placeholder-count="1"><span style="grid-area:{{ p.ga }};background:{{ p.bg }};min-width:0;min-height:0"></span></sc-for></span>')
rep('<span style="position:absolute;left:10px;top:10px;font-size:12px;font-weight:800;padding:4px 9px;border-radius:99px;background:rgba(255,255,255,.92);color:#3B5BDB">DAY {{ d.n }}</span>', '<span style="position:absolute;left:10px;top:10px;font-size:14px;font-weight:800;padding:4px 10px;border-radius:99px;background:rgba(255,255,255,.92);color:#5B32D6">DAY {{ d.n }}</span><sc-if value="{{ d.hasMood }}" hint-placeholder-val="{{ false }}"><span style="position:absolute;right:10px;top:8px;font-size:22px;line-height:1;padding:5px 8px;border-radius:99px;background:rgba(255,255,255,.92)">{{ d.mood }}</span></sc-if>')


# 경유지 팝업: 텍스트 중앙 정렬 (제목·설명·지표), 배지는 좌상단으로
_b0 = dc.index('<span style="flex:none;white-space:nowrap;height:28px;padding:0 10px 0 7px;border-radius:99px;background:rgba(255,255,255,.95);')
_b1 = dc.index('{{ sp.badge }}</span>', _b0) + len('{{ sp.badge }}</span>')
_badge = dc[_b0:_b1]
dc = dc[:_b0] + dc[_b1:]
_badge = _badge.replace('<span style="flex:none;white-space:nowrap;height:28px;', '<span style="position:absolute;left:12px;top:12px;flex:none;white-space:nowrap;height:28px;', 1)
_cnt = '<span style="position:absolute;right:12px;top:12px;flex:none;white-space:nowrap;font-size:12px;font-weight:800;padding:4px 9px;border-radius:99px;background:rgba(20,24,60,.45);color:#fff">{{ sp.imgN }} / 4</span>'
assert dc.count(_cnt) == 1
dc = dc.replace(_cnt, _cnt + _badge)
rep('<div style="position:relative;display:flex;align-items:flex-end;justify-content:space-between;gap:10px;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.35)">\n<span style="display:flex;flex-direction:column;gap:4px;min-width:0">', '<div style="position:relative;display:flex;align-items:flex-end;justify-content:center;text-align:center;gap:10px;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.35)">\n<span style="display:flex;flex-direction:column;align-items:center;gap:4px;min-width:0">')
rep('padding:9px 12px;display:flex;flex-direction:column;gap:2px;min-width:0"><span style="display:flex;align-items:center;gap:4px;font-size:12px;font-weight:700;color:#4A5D78;white-space:nowrap">', 'padding:9px 12px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:2px;min-width:0"><span style="display:flex;align-items:center;justify-content:center;gap:4px;font-size:12px;font-weight:700;color:#4A5D78;white-space:nowrap">')
rep('line-height:1.6;color:#3A4D68;text-wrap:pretty;display:-webkit-box;', 'line-height:1.6;color:#3A4D68;text-align:center;text-wrap:pretty;display:-webkit-box;')

# ───────────────────────── 5. 로직: 기존 앱 로직 + 새 화면 값 ─────────────────────────
oa = old.index('<script type="text/x-dc"'); ob = old.index('>', oa) + 1; oe = old.index('</script>', ob)
OLD = old[ob:oe]
OLD = rep('  renderVals() {', '  oldVals() {', src=OLD)
OLD = rep('\n    return {\n      morePlaces:', '\n    return { _x: { dd, n, stage, reached, done, isToday, isPast, walked, remain, steps, mins, hcT, stationsDone, posKmF, eta, today, view, places, hcH, hcR, recLabel, recIso, iso: (() => { const q = new Date(); return q.getFullYear()+"-"+String(q.getMonth()+1).padStart(2,"0")+"-"+String(q.getDate()).padStart(2,"0"); })() },\n      morePlaces:', src=OLD)
OLD = rep("synced: v.synced || '' };", "synced: v.synced || '', sleep: v.sleepMin == null ? null : v.sleepMin, weight: v.weight == null ? null : v.weight };", src=OLD)
PERSIST_OLD = "'bodyLog', "
OLD = rep("if (this.dayInfo().diff < 0) return 0; ", "", src=OLD)  # 출발 전에도 걷기 상태(테스트) 허용
OLD = rep("const hc = { days, snaps: j.snaps || [], locs: j.locs || {}, at: Date.now() };", "const hc = { days, snaps: j.snaps || [], locs: j.locs || {}, live: j.live || null, smin: j.smin || [], at: Date.now() };", src=OLD)
OLD = rep("this._hcT = setTimeout(() => this.loadHc(), 5 * 6e4);", "this._hcT = setTimeout(() => this.loadHc(), 2 * 6e4);", src=OLD)
OLD = rep(PERSIST_OLD, "'bodyLog', 'sd', 'expLog', 'wLog', 'moodLog', 'noteLog', 'walk', 'wsrc', 'wStart', 'wPauseAt', 'wPausedMs', 'wDay', 'stageDate', 'dark', 'nfxDir', 'jc', 'wNoAuto', 'ntab', 'sub', 'dayN', 'lo', 'pd', 'sf', 'trm', 'jpBig', 'cur', 'ji', 'jfav', ", src=OLD)
na = dc.index('<script type="text/x-dc"'); nb = dc.index('>', na) + 1; ne = dc.index('</script>', nb)
NEWJS = open(os.path.join(HERE, 'v9_logic.js'), encoding='utf-8').read()
HEROS = sorted(os.listdir(os.path.join(ROOT, 'assets', 'hero')))
NEWJS = NEWJS.replace('__WIDE__', WIDE).replace('__HEROS__', json.dumps(HEROS))
i0 = NEWJS.index('  renderVals() {')
NINIT = NEWJS[:i0]
RV = NEWJS[i0:]
OLD = rep("  state = { theme: null,", "  state = { ...this.nInit(), theme: null,", src=OLD)
OLD = rep("  componentDidMount() {", "  componentDidMount() { try { window.addEventListener('popstate', () => this.hwBack()); } catch (e) {} try { if (this.state.stageDate !== this.todayIso()) this.setState({ stage: this.dayInfo().diff < 0 ? 0 : 0, stageDate: this.todayIso(), walk: null }); } catch (e) {} try { this._tk = setInterval(() => { if (this.state.walk === 'walking') { this._c = (this._c || 0) + 1; if (this.state.mode || this._c % 15 === 0) this.setState({ tick: Date.now() }); } if ((this._ac = (this._ac || 0) + 1) % 10 === 0) this.autoWatch(); }, 1000); setTimeout(() => this.autoWatch(), 4000); setTimeout(() => this.loadSlots(), 1500); setInterval(() => this.loadSlots(), 20000); } catch (e) {}", src=OLD)
METH = '''
  loadSlots() { try { fetch('.image-slots.state.json').then(r => r.ok ? r.json() : {}).then(async j => { const C = this._sb = this._sb || {}, m = {}; for (const k of Object.keys(j || {})) { const v = j[k], u = typeof v === 'string' ? v : v && v.u; if (!u) continue; if (!C[k] || C[k].n !== u.length) { try { const b = await (await fetch(u)).blob(); C[k] = { n: u.length, url: URL.createObjectURL(b) }; } catch (e) { continue; } } m[k] = C[k].url; } this.setState({ slotImgs: m }); }).catch(() => {}); } catch (e) {} }
  autoWatch() { try {
    const S = this.state, iso = this.todayIso(), LV = S.hc && S.hc.live; if (!LV) return;
    const hm = t => { const d = new Date(t); return String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0'); };
    const ex = LV.last_exercise;
    if (ex && ex.end) { let seen = null; try { seen = localStorage.getItem('tk-ex-seen'); } catch (e) {}
      if (seen !== ex.end) { try { localStorage.setItem('tk-ex-seen', ex.end); } catch (e) {}
        if (seen != null) { const running = (S.walk === 'walking' || S.walk === 'paused') && S.wStart && Date.parse(ex.end) > S.wStart;
          this.setState({ toast: { a: '와치 걷기 기록 도착', b: hm(ex.start) + ' ~ ' + hm(ex.end) + ' · ' + Math.round((ex.sec || 0) / 60) + '분 · ' + (ex.steps || 0) + '걸음' + (running ? ' · 정지 버튼으로 마무리' : '') } }); setTimeout(() => this.setState({ toast: null }), 6000); return; } } }
    if (S.walk === 'walking' || S.walk === 'paused') return;
    if (S.wNoAuto === iso || (S.stageDate === iso && S.stage > 0)) return;
    const recv = LV.last_recv ? Date.parse(LV.last_recv) : 0; if (!recv || Date.now() - recv > 40 * 6e4) return;
    const lastStep = LV.last_step_at ? Date.parse(LV.last_step_at) : 0;
    if ((LV.steps_30m || 0) < 150 || !lastStep || Date.now() - lastStep > 30 * 6e4) return;
    this.setState({ walk: 'walking', wsrc: 'watch', wStart: Date.now() - 5 * 6e4, wPausedMs: 0, wPauseAt: null, wDay: iso, stageDate: iso, stage: Math.max(1, S.stage || 0), toast: { a: '와치 걷기 감지', b: '최근 30분 ' + (LV.steps_30m || 0) + '걸음 · 기록을 시작했어요' } }); setTimeout(() => this.setState({ toast: null }), 5000);
  } catch (e) {} }
  todayIso() { const q = new Date(); return q.getFullYear() + '-' + String(q.getMonth() + 1).padStart(2, '0') + '-' + String(q.getDate()).padStart(2, '0'); }
  closeSheet() { this.setState({ sheet: null }); }
  closeSub() { this.setState({ sub: null }); }
  hwBack() { const s = this.state; if (s.sheet) this.closeSheet(); else if (s.spot != null) this.setState({ spot: null }); else if (s.mode) this.setState({ mode: false }); else if (s.sub) this.closeSub(); else if (s.mapFull) this.setState({ mapFull: false }); else if (s.ntab && s.ntab !== 'home') this.setState({ ntab: 'home' }); }
'''
ce = OLD.rindex('}')
OLD = OLD[:ce] + '\n' + NINIT + METH + RV.rstrip() + '\n' + OLD[ce:]
_hi = old.index('var HOTELS = ') + len('var HOTELS = ')
_ho, _hend = json.JSONDecoder().raw_decode(old[_hi:])
dc = dc[:nb] + '\nwindow.TK_HOTELS = ' + json.dumps(_ho, ensure_ascii=False) + ';\n' + OLD + dc[ne:]

# ───────────────────────── 6. 지도(Leaflet) + 기존 보조 기능 ─────────────────────────
MAP_JS = v8src[v8src.index('MAP_JS = r"""') + len('MAP_JS = r"""'):]
MAP_JS = MAP_JS[:MAP_JS.index('"""\n')]
_PV = "      if (el.getAttribute('data-v8map') === 'pop') { if (D.popLL) { L.marker(D.popLL, { icon: L.divIcon({ className: '', html: pin('★', '#7B46F0', '#fff', '#fff', 30), iconSize: [0, 0] }) }).addTo(el._lay); var bb = [D.popLL]; if (D.meAny) { L.circleMarker(D.meAny, { radius: 8, color: '#fff', weight: 3, fillColor: '#3B5BDB', fillOpacity: 1 }).addTo(el._lay); L.polyline([D.meAny, D.popLL], { color: '#3B5BDB', weight: 3, dashArray: '3 8' }).addTo(el._lay); bb.push(D.meAny); } try { if (bb.length > 1) el._map.fitBounds(L.latLngBounds(bb), { padding: [34, 34], maxZoom: 16 }); else el._map.setView(D.popLL, 15); } catch (e) {} } return; }\n"
_PA = "      if (el.getAttribute('data-v8map') === 'log')"
assert MAP_JS.count(_PA) == 1
MAP_JS = MAP_JS.replace(_PA, _PV + _PA)
MAP_JS = MAP_JS.replace("(D.me || (D.stops && D.stops[0] && D.stops[0].ll) || [35.62, 139.74])", "(D.logC || D.me || (D.stops && D.stops[0] && D.stops[0].ll) || [35.62, 139.74])")
ns = {'old': old}
ks = v8src.index('def old_script(marker):')
ke = v8src.index("KEEP.append(FS)") + len("KEEP.append(FS)")
exec(v8src[ks:ke], ns)
KEEP, FS = ns['KEEP'], ns['FS']
# 기록 탭: 계획 대비 누적 거리 → 그 날 걸은 GPS 길(지도)
_i = dc.index('{{ lg2.planPts }}'); _sa = dc.rindex('<svg viewBox="0 0 300 140"', 0, _i)
_e = dc.index('{{ lg2.cumNote }}</b></span>', _i) + len('{{ lg2.cumNote }}</b></span>')
_la = dc.rindex('<span style="display:flex;align-items:baseline', 0, _sa)
_hd = dc[_la:_sa].replace('계획 대비 누적 거리', '걸은 길 · GPS').replace('{{ lg2.cumTitle }}', '{{ lg2.gpsN }}')
_map = '<div data-v8map="log" data-k="log" style="position:relative;height:240px;border-radius:18px;overflow:hidden;background:#EEF2F8;border:1px solid #E6E9F7;isolation:isolate;z-index:0"></div>'
_lg = '<span style="display:flex;gap:14px;font-size:12px;color:#4A5D78;flex-wrap:wrap;align-items:center"><span style="display:flex;align-items:center;gap:5px"><i style="width:10px;height:10px;border-radius:50%;background:#20A85A"></i>출발</span><span style="display:flex;align-items:center;gap:5px"><i style="width:10px;height:10px;border-radius:50%;background:#E8453C"></i>현재·도착</span><b style="margin-left:auto;color:#18324F">{{ lg2.gpsNote }}</b></span>'
dc = dc[:_la] + _hd + _map + _lg + dc[_e:]
# 장소 팝업: 경유지 선택 버튼을 위쪽 → 카드 아래(엄지 닿는 하단)로
_t0 = dc.index('<div style="position:absolute;left:0;right:0;top:calc(env(safe-area-inset-top) + 14px);z-index:2;display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:0 16px">')
_t1 = dc.index('</div>', dc.index('{{ sp.tabs }}', _t0)) + len('</div>')
_tabs = dc[_t0:_t1].replace('position:absolute;left:0;right:0;top:calc(env(safe-area-inset-top) + 14px);z-index:2;display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:0 16px', 'position:relative;flex:none;width:100%;box-sizing:border-box;z-index:2;display:flex;flex-wrap:wrap;justify-content:center;gap:8px;padding:0 12px calc(env(safe-area-inset-bottom) + 30px)', 1)
dc = dc[:_t0] + dc[_t1:]
_c0 = dc.index('<div onClick="{{ keep }}" style="position:relative;z-index:2;width:calc(100% - 24px);max-width:{{ fr.spotW }};max-height:calc(100% - 120px)', _t0 - 50)
_c0b = dc.index('margin-bottom:14px;background:#fff;border-radius:28px', _c0)
dc = dc[:_c0b] + 'margin-bottom:10px;background:#fff;border-radius:28px' + dc[_c0b + len('margin-bottom:14px;background:#fff;border-radius:28px'):]
dc = dc.replace('max-height:calc(100% - 120px);overflow-y:auto', 'max-height:calc(100% - 110px);overflow-y:auto', 1)
_end = dc.index('</sc-if>', _c0)
_close = dc.rindex('</div>\n</div>', _c0, _end)  # 카드 닫힘 + 팝업 루트 닫힘
dc = dc[:_close + len('</div>\n')] + _tabs + '\n' + dc[_close + len('</div>\n'):]
# 장소 팝업 버튼: 지나온 곳(✓·흐리게) / 남은 곳(현재 위치와의 거리 표시)
rep("-webkit-backdrop-filter:blur(12px)\"><span style=\"width:20px;height:20px;border-radius:50%;background:{{ t.nb }};color:{{ t.nf }};font-size:11px;display:grid;place-items:center\">{{ t.n }}</span>{{ t.label }}</button>", "-webkit-backdrop-filter:blur(12px);opacity:{{ t.op }}\"><span style=\"width:20px;height:20px;border-radius:50%;background:{{ t.nb }};color:{{ t.nf }};font-size:11px;display:grid;place-items:center\">{{ t.n }}</span>{{ t.label }}<span style=\"font-size:12px;font-weight:700;opacity:.8\">{{ t.dist }}</span></button>")
# 일본어: 분류 버튼(필수·이동·숙소…)을 위쪽 → 뒤로 버튼 위(엄지 닿는 하단)로
_k0 = dc.rindex('<div style="display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;margin:0 -16px;padding:0 16px"><sc-for list="{{ jp2.cats }}"')
_k1 = dc.index('</sc-for></div>', _k0) + len('</sc-for></div>')
_cats = dc[_k0:_k1].replace('margin:0 -16px;padding:0 16px', 'position:absolute;left:0;right:0;bottom:86px;z-index:3;padding:18px 16px 8px;margin:0;background:linear-gradient(to top,rgba(238,240,255,.97) 55%,rgba(238,240,255,0))', 1)
dc = dc[:_k0] + dc[_k1:]
_bk = dc.index('<button onClick="{{ back2 }}"')
dc = dc[:_bk] + '<sc-if value="{{ sb2.jp }}" hint-placeholder-val="{{ false }}">' + _cats + '</sc-if>\n' + dc[_bk:]
# 목록이 하단 버튼에 가려지지 않게 여백
_j = dc.index('<sc-if value="{{ sb2.jp }}" hint-placeholder-val="{{ false }}">\n<div style="display:flex;flex-direction:column;gap:12px;padding:0 16px">')
dc = dc[:_j] + dc[_j:].replace('<div style="display:flex;flex-direction:column;gap:12px;padding:0 16px">', '<div style="display:flex;flex-direction:column;gap:12px;padding:0 16px 80px">', 1)
# 날씨: 일출·일몰·지금·강수 타일을 크게(빈 여백 채움)
_w0 = dc.rindex('<div style="flex:1;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px"><sc-for list="{{ wxd2 }}"')
_w1 = dc.index('</sc-for></div>', _w0) + len('</sc-for></div>')
_blk = dc[_w0:_w1]
for _a, _b in [
  ('gap:10px"><sc-for', 'grid-auto-rows:1fr;gap:12px"><sc-for'),
  ('border-radius:20px;padding:12px 14px;display:flex;flex-direction:column;gap:4px;min-width:0', 'border-radius:22px;padding:18px 16px;display:flex;flex-direction:column;justify-content:center;gap:8px;min-width:0'),
  ('gap:5px;font-size:12px;font-weight:700;color:#4A5D78', 'gap:6px;font-size:15px;font-weight:700;color:#4A5D78'),
  ("font-size:16px;color:#5B6FD4\">{{ x.icon }}", "font-size:26px;color:#5B6FD4\">{{ x.icon }}"),
  ('font-size:20px;font-weight:800;letter-spacing:-.03em;white-space:nowrap">{{ x.v }}', 'font-size:40px;font-weight:800;letter-spacing:-.04em;line-height:1.05;white-space:nowrap">{{ x.v }}'),
]:
    assert _blk.count(_a) == 1, _a[:60]
    _blk = _blk.replace(_a, _b)
dc = dc[:_w0] + _blk + dc[_w1:]
# 장소 팝업: 사진 위 "장소 사진" 표시·카메라 아이콘 제거
_m = re.search(r'<span style="position:absolute;left:50%;top:30%;transform:translate\(-50%,-50%\);[^>]*><span[^>]*>photo_camera</span>장소 사진</span>', dc)
assert _m
dc = dc.replace(_m.group(0), '', 1)
_n = len(re.findall(r'<span style="font-family:\'Material Symbols Rounded\';[^>]*>photo_camera</span>', dc))
dc = re.sub(r'(<button onClick="\{\{ [gp]\.pick \}\}"[^>]*>)<span style="font-family:\'Material Symbols Rounded\';[^>]*>photo_camera</span>(</button>)', r'\1\2', dc)
_m2 = re.search(r'<div style="display:flex;flex-direction:column;align-items:center;gap:4px;color:#fff;font-size:13px;font-weight:700"><span[^>]*>photo_camera</span>장소 사진</span></div>', dc)
if _m2: dc = dc.replace(_m2.group(0), '', 1)
print('camera icons before/after', _n, len(re.findall(r'>photo_camera</span>', dc)))
# 하루 기록: 걸은 길(GPS) 지도를 시간대별 걸음 바로 아래로 이동
_la = dc.index('<sc-if value="{{ tb.log }}"'); _lb = dc.index('<sc-if value="{{ tb.more }}"')
_blk = dc[_la:_lb]
_ms = _blk.rindex('<div style="flex:1;background:#fff', 0, _blk.index('걸은 길 · GPS'))
_me = _blk.index('{{ lg2.gpsNote }}</b></span>\n</div>', _ms) + len('{{ lg2.gpsNote }}</b></span>\n</div>')
_card = _blk[_ms:_me].replace('<div style="flex:1;background:#fff', '<div style="background:#fff', 1)
_blk = _blk[:_ms] + _blk[_me:]
_hs = _blk.rindex('<div style="background:#fff', 0, _blk.index('걷는 동안 심박'))
_blk = _blk[:_hs] + _card + '\n' + _blk[_hs:]
dc = dc[:_la] + _blk + dc[_lb:]
# 일본어: 카테고리 버튼 크게·중앙정렬, 목록 아래 여백
rep('display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;position:absolute;left:0;right:0;bottom:86px;z-index:3;padding:18px 16px 8px;', 'display:flex;gap:10px;justify-content:safe center;overflow-x:auto;scrollbar-width:none;position:absolute;left:0;right:0;bottom:86px;z-index:3;padding:18px 16px 10px;')
_j0 = dc.index('<sc-for list="{{ jp2.cats }}"'); _j1 = dc.index('</sc-for>', _j0)
dc = dc[:_j0] + dc[_j0:_j1].replace('height:40px;padding:0 14px;border-radius:99px;border:1px solid', 'height:54px;padding:0 24px;border-radius:99px;border:1.5px solid').replace("font:700 14px", "font:800 19px") + dc[_j1:]
dc = dc.replace('grid-template-columns:{{ fr.jpCols }};gap:10px"', 'grid-template-columns:{{ fr.jpCols }};gap:10px"', 1)
dc = dc.replace('<span style="font-size:23px;font-weight:700;line-height:1.35">{{ jp2.sel.ko }}</span>', '<span style="font-size:28px;font-weight:700;line-height:1.35">{{ jp2.sel.ko }}</span>', 1)
# 주간 날씨(더보기 카드·날씨 화면): 온도·이름 글자 키움
def _wk(dc, start):
    _wi = dc.index('<sc-for list="{{ wx2 }}" as="d"', start)
    _wj = dc.index('</sc-for>', _wi)
    _wb = dc[_wi:_wj]
    for a, b in [('<b style="font-size:14px">{{ d.name }}</b>', '<b style="font-size:16px">{{ d.name }}</b>'), ('<b style="font-size:13px">{{ d.name }}</b>', '<b style="font-size:16px">{{ d.name }}</b>'), ('font-size:20px;color:{{ d.ic }}', 'font-size:26px;color:{{ d.ic }}'), ('font-size:22px;color:{{ d.ic }}', 'font-size:26px;color:{{ d.ic }}'), ('<b style="font-size:13px">{{ d.hi }}°</b><span style="font-size:13px;color:#6B7A90">{{ d.lo }}°</span>', '<span style="display:flex;align-items:baseline;gap:4px;white-space:nowrap"><b style="font-size:19px;font-weight:800">{{ d.hi }}°</b><span style="font-size:15px;font-weight:700;color:#5B6B82">{{ d.lo }}°</span></span>'), ('<b style="font-size:14px">{{ d.hi }}°</b><span style="font-size:14px;color:#6B7A90">{{ d.lo }}°</span>', '<span style="display:flex;align-items:baseline;gap:4px;white-space:nowrap"><b style="font-size:19px;font-weight:800">{{ d.hi }}°</b><span style="font-size:15px;font-weight:700;color:#5B6B82">{{ d.lo }}°</span></span>')]:
        _wb = _wb.replace(a, b)
    return dc[:_wi] + _wb + dc[_wj:], _wi + 10
print('WX2 before', dc.count('list="{{ wx2 }}"'), dc.count('<b style="font-size:14px">{{ d.name }}</b>'))
_p = 0
while True:
    try:
        dc, _p = _wk(dc, _p)
    except ValueError:
        break
print('WX2 after', dc.count('<b style="font-size:14px">{{ d.name }}</b>'), dc.count('<b style="font-size:16px">{{ d.name }}</b>'))
# 접근성: 12px 이하 글자 키움(시력 고려) — 10·11→13, 12→14. 지도 마커(MAP_JS)는 제외
import re as _re
def _fz(m):
    v = float(m.group(2)); nv = 13 if v < 12 else 14 if v < 13 else v
    return m.group(1) + (str(int(nv)) if nv == int(nv) else str(nv)) + 'px'
dc = _re.sub(r'(font-size:)(\d+(?:\.\d+)?)px', lambda m: _fz(m) if float(m.group(2)) < 13 else m.group(0), dc)
dc = _re.sub(r'(font:\d+ )(\d+(?:\.\d+)?)px', lambda m: _fz(m) if float(m.group(2)) < 13 else m.group(0), dc)
dc = _re.sub(r"(font:\s*'?\d+'? )(\d+)px", lambda m: _fz(m) if float(m.group(2)) < 13 else m.group(0), dc)
dc = _re.sub(r'<(button|a)\b[^>]*>', lambda m: m.group(0).replace('height:36px', 'height:44px'), dc)
# 상단 작은 버튼(36px)을 44px로
dc = dc.replace('flex:none;width:36px;height:36px;border-radius:50%;border:1px solid rgba(255,255,255,.95);background:rgba(255,255,255,.9)', 'flex:none;width:44px;height:44px;border-radius:50%;border:1px solid rgba(255,255,255,.95);background:rgba(255,255,255,.9)')
dc = dc.replace('white-space:nowrap;height:36px;padding:0 12px;border-radius:99px;border:1px solid rgba(255,255,255,.95);background:rgba(255,255,255,.9)', 'white-space:nowrap;height:44px;padding:0 14px;border-radius:99px;border:1px solid rgba(255,255,255,.95);background:rgba(255,255,255,.9)')
dc = dc.replace('</body>', MAP_JS + ''.join(KEEP) + '</body>', 1)
# 걷기/교통 구분: 위치 점이 드문드문(1~5분) 들어와도 구간 속도로 판정 — 5점 평균은 짧은 이동을 걷기로 희석함
_OLDM = "mode[i] = (sd / (st / 3600) >= 12 || d[i] >= 3) ? 'v' : 'w'; }"
assert dc.count(_OLDM) == 1
dc = dc.replace(_OLDM, "var a3 = 0, b3 = 0; for (j = Math.max(1, i - 1); j <= Math.min(n - 1, i + 1); j++) { a3 += d[j]; b3 += t[j]; } var w3 = a3 / (b3 / 3600), sp = d[i] / (t[i] / 3600); mode[i] = ((sp >= 9 && t[i] <= 900) || w3 >= 8 || sd / (st / 3600) >= 12 || d[i] >= 3) ? 'v' : 'w'; }")
# 걸음수 기반 구분: 분 단위 걸음 기록이 있는 구간은 '걸음이 잡히면 걷기, 이동했는데 걸음이 없으면 교통'
_OLDX = "var runs = [], cur = null;"
assert dc.count(_OLDX) == 1
dc = dc.replace(_OLDX, "var SM = window.__smin, SE = window.__sminTo || 0; if (SM && SM.length) for (i = 1; i < n; i++) { var s0 = pts[i - 1][2], s1 = pts[i][2]; if (!s0 || !s1 || s1 > SE) continue; var c = 0, k; for (k = 0; k < SM.length; k++) { if (SM[k][0] >= s0 - 59 && SM[k][0] < s1) c += SM[k][1]; } var spm = c / Math.max(1, (s1 - s0) / 60); mode[i] = spm >= 20 ? 'w' : (d[i] >= 0.1 ? 'v' : 'w'); } " + _OLDX)
# 한 구간 안에서 걷다가 교통을 탄 경우: 걸음수로 걸은 거리를 추정해 구간을 둘로 쪼갬
_OLDF = "window.tkSeg = function (pts) {"
assert dc.count(_OLDF) == 1
_SPL = """function tkSplit(pts) {
    var SM = window.__smin, SE = window.__sminTo || 0, R = Math.PI / 180;
    if (!SM || !SM.length || pts.length < 2) return pts;
    var out = [pts[0]], i, k;
    for (i = 1; i < pts.length; i++) {
      var a = pts[i - 1], b = pts[i], s0 = a[2], s1 = b[2];
      if (s0 && s1 && s1 <= SE && s1 - s0 > 150) {
        var x = Math.sin((b[0] - a[0]) * R / 2), y = Math.sin((b[1] - a[1]) * R / 2), d = 12742 * Math.asin(Math.sqrt(x * x + Math.cos(a[0] * R) * Math.cos(b[0] * R) * y * y));
        var ws = 0, wn = 0, tmin = 1e12, tmax = 0;
        for (k = 0; k < SM.length; k++) { if (SM[k][0] >= s0 - 59 && SM[k][0] < s1 && SM[k][1] >= 25) { ws += SM[k][1]; wn++; tmin = Math.min(tmin, SM[k][0]); tmax = Math.max(tmax, SM[k][0] + 60); } }
        var wk = ws * 0.00072;
        if (wn && wk > 0.05 && d - wk > 0.15) {
          var first = (tmin + tmax) / 2 < (s0 + s1) / 2, f = first ? wk / d : 1 - wk / d, ts = first ? Math.min(s1 - 30, Math.max(s0 + 30, tmax)) : Math.max(s0 + 30, Math.min(s1 - 30, tmin));
          out.push([a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, ts]);
        }
      }
      out.push(b);
    }
    return out;
  }
  """
dc = dc.replace(_OLDF, _SPL + _OLDF)
_OLDN = "var n = pts.length, R = Math.PI / 180, d = [], t = [], i, j;"
assert dc.count(_OLDN) == 1
dc = dc.replace(_OLDN, "pts = tkSplit(pts); " + _OLDN)
# 버스처럼 자주 서는 경우: 3점 평균 8km/h↑도 교통, 교통 사이에 낀 짧은 정차·걷기(0.3km 미만)는 교통으로 이어 붙임
_OLDR = "runs.forEach(function (r) { if (r.m === 'v' && r.km < 0.15) r.m = 'w'; });"
assert dc.count(_OLDR) == 1
dc = dc.replace(_OLDR, "for (i = 1; i < runs.length - 1; i++) { if (runs[i].m === 'w' && runs[i].km < 0.3 && runs[i - 1].m === 'v' && runs[i + 1].m === 'v') runs[i].m = 'v'; } " + _OLDR)

os.makedirs(OUT, exist_ok=True)

# 전체 여정 헤더: 상단 카드와 중복되는 부제 제거
_sub = '<span style="font-size:13px;color:#6B7A90">시나가와 → 교토 · 31일 · 488km</span>'
assert dc.count(_sub) >= 1
dc = dc.replace(_sub, '')
# 일본어 상단 문구는 홈에만 남김
_eb = '<span style="font-size:13px;font-weight:800;letter-spacing:.02em;color:#5B6FD4">東海道 53の休符</span>'
_i1 = dc.index(_eb) + len(_eb)
assert dc.count(_eb) >= 2
dc = dc[:_i1] + dc[_i1:].replace(_eb, '')
# 일본어: 교토만 묻는 문장이 아니므로 ○○로
for _a, _b in [('すみません、京都へはこの道でいいですか？', 'すみません、○○へはこの道でいいですか？'), ('스미마센, 쿄-토에와 코노 미치데 이이데스카?', '스미마센, ○○에와 코노 미치데 이이데스카?'), ('실례합니다, 교토는 이 길로 가면 되나요?', '실례합니다, ○○는 이 길로 가면 되나요?')]:
    assert dc.count(_a) >= 1, _a
    dc = dc.replace(_a, _b)
# 출발일(__SD) 반영: 하드코딩된 12/4 기준 날짜 계산을 전역 값으로 치환
_sd = "<script>var __SD=[2026,11,4],__SDI='2026-12-04';try{var _v=null;try{_v=(JSON.parse(localStorage.getItem('tk-v15-data')||'{}')||{}).sd||null}catch(e){}_v=_v||localStorage.getItem('tokaido-start');if(/^\\d{4}-\\d{2}-\\d{2}$/.test(_v)){var _p=_v.split('-');__SD=[+_p[0],+_p[1]-1,+_p[2]];__SDI=_v}}catch(e){}</script>\n"
dc = _re2.sub(r'new Date\(2026, 11, 3 ?\+ ?', 'new Date(__SD[0], __SD[1], __SD[2] - 1 + ', dc)
dc = dc.replace('2026, 11, 4 + ', '__SD[0], __SD[1], __SD[2] + ')
dc = dc.replace('new Date(2026, 11, 4)', 'new Date(__SD[0], __SD[1], __SD[2])')
dc = dc.replace("'2026-12-04'", '__SDI')
dc = dc.replace('dtx = new Date(2026, 11, dn)', 'dtx = new Date(__SD[0], __SD[1], __SD[2] - 4 + dn)')
dc = dc.replace("'12/4 ", "(__SD[1]+1)+'/'+__SD[2]+' ")
dc = dc.replace('<head>', '<head>\n' + _sd, 1)
# 경유지 팝업: 제목·박스를 사진 아래로(명물 팝업과 같은 톤)
_s0 = dc.index('<div style="position:relative;display:flex;align-items:flex-end;justify-content:center;text-align:center;gap:10px;color:#fff;text-shadow')
_s1 = dc.index('</sc-for>\n</div>\n</div>', _s0) + len('</sc-for>\n</div>\n</div>')
_G = '<span style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,18,50,0) 30%,rgba(14,18,50,.35) 55%,rgba(14,18,50,.78) 100%)"></span>'
_sg = dc.rindex(_G, 0, _s0)
_new = '</div>\n<div style="display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center"><b style="font-size:30px;font-weight:800;letter-spacing:-.04em;line-height:1.2;color:#18243F">{{ sp.name }}</b><span style="font-size:16px;font-weight:600;color:#6B7A90">{{ sp.jp }} · {{ sp.sub }}</span></div>\n<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><sc-for list="{{ sp.metrics }}" as="m" hint-placeholder-count="3">' + '<span style="border-radius:16px;background:#F6F7FB;border:1px solid #E6E9F5;padding:12px 8px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;min-width:0"><span style="display:flex;align-items:center;justify-content:center;gap:4px;font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap"><span style="font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'FILL\' 1,\'wght\' 500;font-size:16px;color:#5B6FD4">{{ m.icon }}</span>{{ m.k }}</span><b style="font-size:clamp(17px,5vw,20px);font-weight:800;letter-spacing:-.03em;color:{{ m.c }};white-space:nowrap">{{ m.v }}</b></span>' + '</sc-for></div>'
dc = dc[:_sg] + dc[_sg + len(_G):_s0] + _new + dc[_s1:]
# 상세 시트: 걸음·심박 / 남은 시간·걸은 시간 같은 높이
dc = dc.replace('data-screen-label="상세 시트" style="width:100%;max-width:{{ fr.sheetW }};max-height:86%;', 'data-screen-label="상세 시트" style="width:100%;max-width:{{ fr.sheetW }};max-height:86%;min-height:min(86%,{{ sh.minH }});box-sizing:border-box;', 1)
# ── 디자인 가이드: 주 버튼(높이 44px 이상 button/a)만 Primary Blue 그라데이션, 나머지 색은 유지
_PG = 'linear-gradient(120deg,#3979E8,#55A9F5,#8AD8E8)'
_VG = ['linear-gradient(135deg,#5428E8,#9A63F5)', 'linear-gradient(135deg,#7048E8,#9775FA)', 'linear-gradient(135deg,#3B5BDB,#6C7FE8)', 'linear-gradient(135deg,#3B5BDB,#6C8CF5)', 'linear-gradient(120deg,#5B6FD4,#8B9CF0)', 'linear-gradient(135deg,#5B6FD4,#8B9CF0)', 'linear-gradient(135deg,#1C7ED6,#4DA3F0)']
def _btn(m):
    s = m.group(0)
    if not re.search(r'height:(4[4-9]|[5-6]\d)px', s): return s
    if re.search(r'width:(4[4-9]|5\d)px;height', s) and 'border-radius:50%' in s: return s  # 원형 아이콘 버튼 제외
    for g in _VG:
        if 'background:' + g in s:
            s = s.replace('background:' + g, 'background:' + _PG)
            s = re.sub(r'box-shadow:0 (\d+)px (\d+)px rgba\([^)]*\)', r'box-shadow:0 \1px \2px rgba(57,121,232,.3)', s)
    return s
dc = re.sub(r'<(?:button|a)\b[^>]*>', _btn, dc)
# ── 홈 상단: 구버전 헤더(TOKAIDO WALK · DAY · 날씨) + 히어로 날짜 이동 알약
_IC = "font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:'liga';font-variation-settings:'FILL' 1,'wght' 500;"
_i = dc.index('東海道 53の休符</span>'); _o = dc[dc.rindex('<span', 0, _i):_i + len('東海道 53の休符</span>')]
dc = dc.replace(_o, '<span style="display:flex;align-items:center;gap:8px;min-width:0;flex-wrap:wrap"><b style="font-family:\'DM Sans\',\'Pretendard Variable\',Pretendard,sans-serif;font-size:17px;font-weight:800;letter-spacing:.14em;color:#1A1D20;white-space:nowrap">TOKAIDO <span style="color:#7544ED">WALK</span></b><span style="flex:none;height:30px;padding:0 12px;border-radius:99px;background:#172338;color:#fff;font-size:14px;font-weight:800;letter-spacing:.04em;display:flex;align-items:center;white-space:nowrap">DAY&nbsp;{{ hr.day }}&nbsp;/&nbsp;31</span><span style="flex:none;height:34px;padding:0 12px 0 9px;border-radius:99px;background:#fff;border:1px solid #E2E8F0;display:flex;align-items:center;gap:5px;font-size:14px;font-weight:800;color:#1A1D20;white-space:nowrap"><span style="' + _IC + 'font-size:19px;color:#F5A524">{{ hr.wx.icon }}</span>{{ hr.wx.t }}<span style="font-weight:600;color:#64748B">/ {{ hr.wx.lo }}</span></span></span>', 1)
# 히어로 왼쪽 위 칩
_o = '<span style="flex:none;white-space:nowrap;height:32px;padding:0 12px;border-radius:99px;background:rgba(255,255,255,.22);border:1px solid rgba(255,255,255,.42);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);display:flex;align-items:center;gap:6px;font-size:13px;font-weight:800;color:#fff">DAY {{ hr.day }}<span style="font-weight:600;opacity:.8">/ 31</span></span>'
assert dc.count(_o) == 1
dc = dc.replace(_o, '<span style="flex:none;white-space:nowrap;height:34px;padding:0 14px;border-radius:99px;background:rgba(14,18,40,.45);border:1px solid rgba(255,255,255,.38);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);display:flex;align-items:center;font-family:\'DM Sans\',\'Pretendard Variable\',sans-serif;font-size:13px;font-weight:800;letter-spacing:.14em;color:#fff">TODAY\'S JOURNEY · DAY{{ hr.day }}</span>', 1)
# 히어로 오른쪽 위: 날씨 칩 → 날짜 이동 알약
_a = dc.index('<span style="flex:none;white-space:nowrap;height:32px;padding:0 11px 0 8px;border-radius:99px;background:rgba(255,255,255,.22)')
_b = dc.index('</span>\n</span>', _a)
_nb = lambda fn, ch, op, lab: '<button onClick="{{ dn2.%s }}" aria-label="%s" style="flex:none;width:50px;height:46px;border-radius:14px;border:1px solid rgba(255,255,255,.4);background:rgba(255,255,255,.12);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.4);font:700 26px/1 \'DM Sans\',sans-serif;display:grid;place-items:center;cursor:pointer;opacity:{{ dn2.%s }}">%s</button>' % (fn, lab, op, ch)
dc = dc[:_a] + '<span style="display:flex;align-items:center;gap:6px">' + _nb('prev', '‹', 'pO', '이전 날') + '<span style="flex:none;height:46px;padding:0 10px 0 16px;border-radius:14px;background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.45);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);display:flex;align-items:center;gap:8px;font-size:16px;font-weight:800;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.4);white-space:nowrap">{{ dn2.lbl }}<sc-if value="{{ dn2.hasRel }}" hint-placeholder-val="{{ true }}"><span style="height:26px;padding:0 10px;border-radius:99px;background:' + _PG + ';color:#fff;font-size:13px;font-weight:800;display:flex;align-items:center">{{ dn2.cur.rel }}</span></sc-if></span>' + _nb('next', '›', 'nO', '다음 날') + '</span>' + dc[_b + len('</span>'):]
# ── 홈 지도: 가이드/구버전 표시 — 지나온 길(초록·실제 GPS) / 앞으로 갈 길(파랑·다음 거점부터), 방문 ✓, 명물 주황 번호
_mr = [
 ("var pts = D.route || []; if (pts.length > 1) { L.polyline(pts, { color: '#fff', weight: 10, opacity: .9 }).addTo(el._lay); L.polyline(pts, { color: '#3B5BDB', weight: 6, opacity: .95 }).addTo(el._lay); }",
  "var pts = D.route || [], _sa = D.stops || [], _pv = null; for (var _q = 0; _q < _sa.length; _q++) { if (_sa[_q].past || _q === 0) _pv = _sa[_q].ll; } var _from = D.me || _pv, _fi = 0; if (_from && pts.length > 1) { var _bd = 1e9; pts.forEach(function (q, k) { var d = (q[0]-_from[0])*(q[0]-_from[0]) + (q[1]-_from[1])*(q[1]-_from[1]); if (d < _bd) { _bd = d; _fi = k; } }); } var fut = pts.slice(_fi); if (_from && D.me) fut = [D.me].concat(fut); if (fut.length > 1) { L.polyline(fut, { color: '#fff', weight: 10, opacity: .9 }).addTo(el._lay); L.polyline(fut, { color: '#0088FF', weight: 6, opacity: .95 }).addTo(el._lay); }"),
 ("L.polyline(r.pts, r.m === 'v' ? { color: '#F08A24', weight: 5, dashArray: '2 9', lineCap: 'round' } : { color: '#7048E8', weight: 5 }).addTo(el._lay); });\n      (D.stops",
  "L.polyline(r.pts, r.m === 'v' ? { color: '#F08A24', weight: 5, dashArray: '2 9', lineCap: 'round' } : { color: '#16A34A', weight: 6 }).addTo(el._lay); });\n      (D.stops"),
 ("html: pin(st ? 'A' : en ? 'B' : String(i), st ? '#2F9E44' : en ? '#7048E8' : s.nx ? '#3B5BDB' : s.past ? '#8B9CF0' : '#fff', st || en || s.nx || s.past ? '#fff' : '#4A5D78', st || en || s.nx || s.past ? '#fff' : '#C5CCEE', st || en || s.nx ? 32 : 24)",
  "html: pin(st ? 'A' : en ? 'B' : s.past ? '✓' : String(i), st ? '#16A34A' : en ? '#7C3AED' : s.past ? '#16A34A' : s.nx ? '#0088FF' : '#fff', st || en || s.nx || s.past ? '#fff' : '#0088FF', st || en || s.nx || s.past ? '#fff' : '#0088FF', st || en || s.nx ? 34 : 28)"),
 ("background:' + (p.passed ? '#20A85A' : '#fff') + ';border:2px solid ' + (p.passed ? '#fff' : '#7B46F0') + ';display:grid;place-items:center;box-shadow:0 2px 6px rgba(0,0,0,.25)\"><b style=\"rotate:-45deg;font:800 12px Pretendard,sans-serif;color:' + (p.passed ? '#fff' : '#7B46F0') + '\">' + p.n + '</b>",
  "background:' + (p.passed ? '#16A34A' : '#EA580C') + ';border:2px solid #fff;display:grid;place-items:center;box-shadow:0 2px 6px rgba(0,0,0,.25)\"><b style=\"rotate:-45deg;font:800 12px Pretendard,sans-serif;color:#fff\">' + (p.passed ? '✓' : p.n) + '</b>"),
]
for _a, _b in _mr:
    assert dc.count(_a) == 1, _a[:60]
    dc = dc.replace(_a, _b)
_lo = '<span style="display:flex;align-items:center;gap:5px"><i style="width:16px;height:4px;border-radius:2px;background:#3B5BDB"></i>걸은 길</span><span style="display:flex;align-items:center;gap:5px"><i style="width:16px;height:0;border-top:4px dotted #3B5BDB"></i>남은 길</span><span style="display:flex;align-items:center;gap:5px"><i style="width:10px;height:10px;border-radius:50%;background:#2F9E44"></i>출발</span><span style="display:flex;align-items:center;gap:5px"><i style="width:10px;height:10px;border-radius:50%;background:#3B5BDB"></i>다음</span><span style="display:flex;align-items:center;gap:5px"><i style="width:10px;height:10px;border-radius:50%;background:#7048E8"></i>도착</span>'
_ln = '<span style="display:flex;align-items:center;gap:5px"><i style="width:18px;height:5px;border-radius:3px;background:#16A34A"></i>지나온 길</span><span style="display:flex;align-items:center;gap:5px"><i style="width:18px;height:5px;border-radius:3px;background:#0088FF"></i>앞으로 갈 길</span><span style="display:flex;align-items:center;gap:5px"><i style="width:11px;height:11px;border-radius:3px;rotate:45deg;background:#EA580C"></i>명물</span>'
assert dc.count(_lo) == 1
dc = dc.replace(_lo, _ln)
# ── 기록: 수면·체중 그래프를 구버전 표현으로(대표값+칩, 기준선 위/아래 막대, 기준선·면 채움 꺾은선)
_a = dc.index('<div style="position:relative;height:140px;display:flex;align-items:flex-end;gap:8px"><span style="position:absolute;left:0;right:0;bottom:{{ lg2.sleepLine }}')
_b = dc.index('</sc-for></div>', _a) + len('</sc-for></div>')
_chip = 'flex:none;height:28px;padding:0 10px;border-radius:99px;display:flex;align-items:center;font-size:14px;font-weight:800;white-space:nowrap'
dc = dc[:_a] + ('<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap"><b style="font-family:\'DM Sans\',\'Pretendard Variable\',sans-serif;font-size:34px;font-weight:800;letter-spacing:-.04em;line-height:1;color:#1A1D20">{{ lg2.sl.avg }}<span style="font-size:15px;font-weight:700;color:#475569;margin-left:2px">h 평균</span></b>'
  '<span style="' + _chip + ';background:#F1ECFF;color:#5B32D6">{{ lg2.sl.hi }}</span><span style="' + _chip + ';background:#FFF3D8;color:#B45309">{{ lg2.sl.lo }}</span></div>'
  '<div style="position:relative;height:120px;display:flex;gap:10px;padding:0 4px"><span style="position:absolute;left:0;right:0;top:60px;border-top:2px dashed #9A63F5;opacity:.8"></span><span style="position:absolute;right:0;top:60px;transform:translateY(-100%);font-size:14px;font-weight:800;color:#7544ED;padding-bottom:3px">기준 7h</span>'
  '<sc-for list="{{ lg2.sl.bars }}" as="b" hint-placeholder-count="7"><span style="position:relative;flex:1;min-width:0;max-width:26px;margin:0 auto;height:100%"><i style="position:absolute;left:0;right:0;top:{{ b.top }};height:{{ b.h }};border-radius:{{ b.r }};background:{{ b.c }}"></i></span></sc-for></div>'
  '<div style="display:flex;gap:10px;padding:0 4px"><sc-for list="{{ lg2.sl.bars }}" as="b" hint-placeholder-count="7"><span style="flex:1;min-width:0;text-align:center;font-size:14px;font-weight:700;color:#64748B">{{ b.l }}</span></sc-for></div>') + dc[_b:]
_a = dc.index('<div style="position:relative"><svg viewBox="0 0 300 110" preserveAspectRatio="none" style="width:100%;height:120px;display:block"><line x1="0" y1="{{ lg2.wtBase }}"')
_b = dc.index('</sc-for></div>', _a) + len('</sc-for></div>')
dc = dc[:_a] + ('<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap"><b style="font-family:\'DM Sans\',\'Pretendard Variable\',sans-serif;font-size:34px;font-weight:800;letter-spacing:-.04em;line-height:1;color:#1A1D20">{{ lg2.w2.now }}<span style="font-size:15px;font-weight:700;color:#475569;margin-left:2px">kg 현재</span></b><span style="' + _chip + ';background:{{ lg2.w2.dBg }};color:{{ lg2.w2.dFg }}">{{ lg2.w2.diff }}</span></div>'
  '<div style="position:relative;margin-top:6px"><svg viewBox="0 0 300 110" preserveAspectRatio="none" style="width:100%;height:130px;display:block;overflow:visible"><polygon points="{{ lg2.w2.area }}" fill="rgba(154,99,245,.16)"></polygon><line x1="0" y1="{{ lg2.wtBase }}" x2="300" y2="{{ lg2.wtBase }}" stroke="#9A63F5" stroke-width="2" stroke-dasharray="6 5" vector-effect="non-scaling-stroke"></line><polyline points="{{ lg2.wtPts }}" fill="none" stroke="#7544ED" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"></polyline></svg>'
  '<span style="position:absolute;right:0;top:calc({{ lg2.wtBase }} / 110 * 130px);transform:translateY(-110%);font-size:14px;font-weight:800;color:#7544ED">처음 {{ lg2.w2.base }}kg</span>'
  '<sc-for list="{{ lg2.wtDots }}" as="d" hint-placeholder-count="3"><span style="position:absolute;left:{{ d.x }}%;top:{{ d.y }}%;width:16px;height:16px;margin:-8px 0 0 -8px;border-radius:50%;background:#fff;border:3.5px solid #7544ED;box-sizing:border-box"></span></sc-for></div>') + dc[_b:]
# ── 기록: 시간대별 걸음 → 구버전(시간별 계획 막대 안 실제 걸음 + 역참 통과 시각 깃발)
def _dend(s, i):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        d += 1 if m.group(0) == '<div' else -1
        if d == 0: return i + m.end()
_k = old.index('HOURLY STEPS'); _oa = old.rindex('<div style="background:linear-gradient(145deg,#FFFFFF 0%,#F2F7FC 100%)', 0, _k); _hs = old[_oa:_dend(old, _oa)]
_hs = _hs.replace('<div style="background:linear-gradient(145deg,#FFFFFF 0%,#F2F7FC 100%);border:1px solid #E8E7EF;border-radius:22px;box-shadow:0 4px 18px rgba(15,42,74,.025);padding:16px 18px;flex:none">', '<div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:24px;padding:16px;min-width:0">', 1)
_hs = _hs.replace('{{ hov.hourNote }}', '')
_h0 = _hs.index('<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px"><div style="min-width:0"><div style="font:700 var(--f12,12px)'); _h1 = _dend(_hs, _h0)
_hs = _hs[:_h0] + '<span style="display:flex;align-items:baseline;justify-content:space-between;gap:8px"><b style="font-size:18px;font-weight:800;letter-spacing:-.03em">시간대별 걸음</b><span style="font-size:14px;color:#6B7A90">{{ lg2.hourNote }}</span></span>' + _hs[_h1:].replace('position:relative;height:230px;width:1008px', 'position:relative;height:240px;width:max(100%,820px)')
_i = dc.index('<b style="font-size:18px;font-weight:800;letter-spacing:-.03em">시간대별 걸음</b>')
_a = dc.rindex('<div style="background:#fff;', 0, _i)
dc = dc[:_a] + _hs + dc[_dend(dc, _a):]
dc = dc.replace('data-screen-label="도카이도 홈 v2" style="', 'data-screen-label="도카이도 홈 v2" style="--f11:13px;--f12:14px;--f13:14px;--f16:17px;', 1)
# ── 환율: 구버전 계산기(자동 환율 표시 + 100엔 직접 입력 + ↻ 자동 환율)
_k = old.index('EXCHANGE · 환율'); _oa = old.rindex('<div style="background:#FFFFFF;border:1px solid #E8E7EF;border-radius:24px', 0, _k); _fx = old[_oa:_dend(old, _oa)]
_fx = _fx.replace('<div style="background:#FFFFFF;border:1px solid #E8E7EF;border-radius:24px;box-shadow:0 4px 18px rgba(15,42,74,.025);padding:16px 18px;flex:none">', '<div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:24px;padding:16px;min-width:0">', 1)
_fx = _fx.replace('justify-content:space-between;align-items:baseline"><div>', 'justify-content:space-between;align-items:flex-start;gap:10px;flex-wrap:wrap"><div>', 1).replace('width:92px;height:36px', 'width:100px;height:44px').replace('height:36px;padding:0 12px;border-radius:10px', 'height:44px;padding:0 12px;border-radius:10px')
for _a2, _b2 in [("font:700 26px 'DM Sans',sans-serif;color:#20202A", "font:600 24px 'DM Sans','Pretendard Variable',sans-serif;color:#1A1D20"),
    ("font:700 26px 'DM Sans',sans-serif;color:#4E27C5", "font:600 24px 'DM Sans','Pretendard Variable',sans-serif;color:#5B32D6"),
    ("font-size:var(--f12,12px);font-weight:700;color:#555568\">{{ fx.fromLabel }}", "font-size:14px;font-weight:500;color:#64748B\">{{ fx.fromLabel }}"),
    ("font-size:var(--f12,12px);font-weight:700;color:#555568\">{{ fx.toLabel }}", "font-size:14px;font-weight:500;color:#64748B\">{{ fx.toLabel }}"),
    ("font-size:var(--f15,15px);font-weight:700;color:#555568\">{{ fx.fromUnit }}", "font-size:15px;font-weight:500;color:#64748B\">{{ fx.fromUnit }}"),
    ("font-size:var(--f15,15px);font-weight:700;color:#555568\">{{ fx.toUnit }}", "font-size:15px;font-weight:500;color:#64748B\">{{ fx.toUnit }}"),
    ("font:700 var(--f13,13px) 'DM Sans',sans-serif;color:#555568;white-space:nowrap\">¥{{ t.a }}", "font:500 14px 'DM Sans','Pretendard Variable',sans-serif;color:#64748B;white-space:nowrap\">¥{{ t.a }}"),
    ("font:700 var(--f16,16px) 'DM Sans',sans-serif;color:#20202A;margin-top:2px;white-space:nowrap\">₩{{ t.b }}", "font:600 17px 'DM Sans','Pretendard Variable',sans-serif;color:#1A1D20;margin-top:3px;white-space:nowrap\">₩{{ t.b }}"),
    ("font:700 var(--f14,14px) 'DM Sans',sans-serif;color:#20202A;outline:none", "font:600 16px 'DM Sans','Pretendard Variable',sans-serif;color:#1A1D20;outline:none"),
    ("font-size:var(--f12,12px);font-weight:700;padding:4px 10px;border-radius:999px;background:{{ fx.rateSrcBg }}", "font-size:14px;font-weight:600;padding:5px 11px;border-radius:999px;background:{{ fx.rateSrcBg }}"),
    ("gap:6px;font-size:var(--f12,12px);color:#555568;white-space:nowrap\">100엔 =", "gap:6px;font-size:14px;color:#64748B;white-space:nowrap\">100엔 ="),

    ("border:1.5px solid #D5D3E0;background:#FFFFFF;padding:0 16px", "border:1px solid #E2E8F0;background:#FFFFFF;padding:0 16px"),
    ("border:1.5px solid #E5DBFF;padding:0 16px", "border:1px solid #E5DBFF;padding:0 16px")]:
    assert _fx.count(_a2) == 1, _a2
    _fx = _fx.replace(_a2, _b2)
_e0 = _fx.index('<div><div style="font:700 var(--f12,12px)'); _e1 = _dend(_fx, _e0)
_fx = _fx[:_e0] + '<b style="font-size:18px;font-weight:800;letter-spacing:-.03em;color:#18324F">환율 계산</b>' + _fx[_e1:]
_i = dc.index('<b style="font-size:18px;font-weight:800;letter-spacing:-.03em">환율 계산</b>')
_a = dc.rindex('<div style="background:#fff;', 0, _i)
dc = dc[:_a] + _fx + dc[_dend(dc, _a):]
# ── 역참 스탬프: 화면 구성은 그대로, 도장 칸만 구버전 양식(번호·도장 원·이름·✓/교통 표시)
_a = dc.index('<sc-for list="{{ stp2.list }}" as="t" hint-placeholder-count="20">')
_a0 = dc.rindex('<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px">', 0, _a)
_b = dc.index('</sc-for></div>', _a) + len('</sc-for></div>')
dc = dc[:_a0] + ('<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:8px"><sc-for list="{{ stp2.list }}" as="t" hint-placeholder-count="20">'
 '<button onClick="{{ t.pick }}" style="position:relative;aspect-ratio:1/1.1;border-radius:18px;border:1px solid {{ t.cbd }};background:{{ t.cbg }};box-shadow:{{ t.sh }};cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;padding:6px;font-family:inherit">'
 '<span style="position:absolute;left:9px;top:7px;font-size:13px;font-weight:800;color:{{ t.txt }}">{{ t.no }}</span>'
 '<span style="width:58px;height:58px;flex:none;border-radius:50%;border:3px {{ t.bs }} {{ t.ring }};color:{{ t.ring }};display:flex;align-items:center;justify-content:center;text-align:center;font:700 {{ t.fs }}px/1.05 \'Noto Serif JP\',serif;transform:rotate({{ t.rot }}deg);background:rgba(255,255,255,.6)">{{ t.jp }}</span>'
 '<span style="font-size:14px;font-weight:700;color:{{ t.txt }};white-space:nowrap">{{ t.ko }}</span>'
 '<sc-if value="{{ t.isW }}" hint-placeholder-val="{{ false }}"><span style="position:absolute;right:7px;top:7px;width:20px;height:20px;border-radius:50%;background:#B7791F;color:#fff;font-size:12px;font-weight:800;display:grid;place-items:center">✓</span></sc-if>'
 '<sc-if value="{{ t.isT }}" hint-placeholder-val="{{ false }}"><span style="position:absolute;right:6px;top:6px;height:20px;padding:0 7px;border-radius:99px;background:#0891B2;color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center">교통</span></sc-if>'
 '</button></sc-for></div>') + dc[_b:]
_lg0 = dc.index('<i style="width:10px;height:10px;border-radius:50%;background:#7048E8"></i>걸어서</span>')
_lgA = dc.rindex('<span style="display:flex;gap:12px;justify-content:center', 0, _lg0); _lgB = dc.index('남은 곳</span></span>', _lg0) + len('남은 곳</span></span>')
dc = dc[:_lgA] + '<span style="display:flex;gap:14px;justify-content:center;font-size:14px;color:#475569;flex-wrap:wrap"><span style="display:flex;align-items:center;gap:6px"><i style="width:12px;height:12px;border-radius:50%;border:2.5px solid #B7791F;background:#FFF6E5"></i>걸어서</span><span style="display:flex;align-items:center;gap:6px"><i style="width:12px;height:12px;border-radius:50%;border:2.5px solid #0891B2;background:#E6FAFF"></i>교통</span><span style="display:flex;align-items:center;gap:6px"><i style="width:12px;height:12px;border-radius:50%;border:2px dashed #C9CCD8"></i>남은 곳</span></span>' + dc[_lgB:]
# ── 사진 일기: 구버전 카드 구성(큰 사진 1 + 작은 사진 2, DAY·날짜·거리·상태, 경로, 한 줄)
_a = dc.index('<sc-for list="{{ diary2 }}" as="d" hint-placeholder-count="6">')
_b = dc.index('</button>\n</sc-for>', _a) + len('</button>\n</sc-for>')
dc = dc[:_a] + ('<sc-for list="{{ diary2 }}" as="d" hint-placeholder-count="6">'
 '<button onClick="{{ d.open }}" style="border-radius:24px;padding:12px;background:#fff;border:1px solid #E8E7EF;box-shadow:0 10px 28px rgba(40,50,140,.08);display:flex;flex-direction:column;gap:10px;text-align:left;cursor:pointer;color:#1A1D20;font-family:inherit;min-width:0">'
 '<span style="display:grid;grid-template-columns:2fr 1fr;grid-template-rows:1fr 1fr;gap:8px;height:clamp(170px,22vw,240px);filter:{{ dkImg }}"><sc-for list="{{ d.t3 }}" as="p" hint-placeholder-count="3"><span style="grid-area:{{ p.ga }};border-radius:14px;background:{{ p.bg }};border:{{ p.bd }};background-color:#ECECF2;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;color:#8C8CA0;font-size:14px;font-weight:600;min-width:0;min-height:0;overflow:hidden"><sc-if value="{{ p.emp }}" hint-placeholder-val="{{ true }}"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#8C8CA0" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="3"></rect><circle cx="8.5" cy="8.5" r="1.8"></circle><path d="M21 15l-5-5L5 21"></path></svg>사진</sc-if></span></sc-for></span>'
 '<span style="display:flex;align-items:center;gap:8px;padding:0 2px"><b style="font-family:\'DM Sans\',sans-serif;font-size:16px;font-weight:800;letter-spacing:.04em;color:#673DE6">DAY {{ d.n }}</b><span style="font-size:14px;color:#64748B;white-space:nowrap">{{ d.dt }} · {{ d.km }}</span><span style="flex:1"></span><sc-if value="{{ d.hasMood }}" hint-placeholder-val="{{ false }}"><span style="font-size:20px;line-height:1">{{ d.mood }}</span></sc-if><span style="flex:none;height:26px;padding:0 10px;border-radius:99px;background:{{ d.stB }};color:{{ d.stF }};font-size:14px;font-weight:800;display:flex;align-items:center">{{ d.stT }}</span></span>'
 '<b style="padding:0 2px;font-size:18px;font-weight:800;letter-spacing:-.03em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ d.path }}</b>'
 '<span style="border-radius:14px;background:#F5F1FF;padding:12px 14px;font-size:15px;line-height:1.5;color:{{ d.nc }}">{{ d.note }}</span>'
 '</button></sc-for>') + dc[_b:]
# ── 팝업 지표 박스 → 세로 알약 타일(흰 원형 아이콘 + 라벨 + 값) — 참고 이미지 방식
_pillre = re.compile(r'<span style="border-radius:16px;background:#F6F7FB;border:1px solid #E6E9F5;padding:12px 8px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;min-width:0"><span style="display:flex;align-items:center;justify-content:center;gap:4px;font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap"><span style="([^"]*?)font-size:16px;color:#5B6FD4">([^<]*)</span>([^<]*)</span>')
dc, _np = _pillre.subn(lambda m: '<span style="border-radius:32px;background:linear-gradient(180deg,#F1ECFF 0%,#FFFFFF 75%);border:1px solid #E6DEFF;padding:12px 6px 14px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px;min-width:0;box-shadow:0 8px 18px rgba(84,40,232,.08)"><span style="width:46px;height:46px;border-radius:50%;background:#fff;box-shadow:0 4px 12px rgba(84,40,232,.18);display:grid;place-items:center"><span style="' + m.group(1) + 'font-size:23px;color:#7544ED">' + m.group(2) + '</span></span><span style="font-size:14px;font-weight:700;color:#475569;white-space:nowrap">' + m.group(3) + '</span>', dc)
assert _np >= 3, _np
# ── 기록 탭 시험 적용: 알약 타일(심박 최저·평균·최고 / 지출 오늘·총 누적·하루 평균)
_ICS = "font-family:'Material Symbols Rounded';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:'liga';font-variation-settings:'FILL' 1,'wght' 500;"
def _pill(icon, k, v, ic='#E23D7A', bg='linear-gradient(180deg,#FFEAF2 0%,#FFFFFF 75%)', bd='#FFD3E3', sh='rgba(226,61,122,.16)'):
    return ('<span style="border-radius:32px;background:' + bg + ';border:1px solid ' + bd + ';padding:12px 6px 14px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px;min-width:0;box-shadow:0 8px 18px ' + sh.replace('.16', '.08') + '">'
            '<span style="width:46px;height:46px;border-radius:50%;background:#fff;box-shadow:0 4px 12px ' + sh + ';display:grid;place-items:center"><span style="' + _ICS + 'font-size:23px;color:' + ic + '">' + icon + '</span></span>'
            '<span style="font-size:14px;font-weight:700;color:#475569;white-space:nowrap">' + k + '</span>' + v + '</span>')
_o = '<sc-for list="{{ lg2.hrStat }}" as="h" hint-placeholder-count="3"><span style="border-radius:14px;background:#F5F3FF;padding:10px 12px;display:flex;flex-direction:column;gap:2px"><span style="font-size:14px;color:#4A5D78;font-weight:700">{{ h.k }}</span><b style="font-size:17px">{{ h.v }}<span style="font-size:14px;color:#6B7A90"> bpm</span></b></span></sc-for>'
assert dc.count(_o) == 1
dc = dc.replace(_o, '<sc-for list="{{ lg2.hrStat }}" as="h" hint-placeholder-count="3">' + _pill('{{ h.icon }}', '{{ h.k }}', '<b style="font-size:20px;font-weight:800;color:#1A1D20;white-space:nowrap">{{ h.v }}<span style="font-size:14px;font-weight:600;color:#64748B"> bpm</span></b>') + '</sc-for>')
_a = dc.index('<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px"><div style="display:flex;flex-direction:column;gap:2px;min-width:0"><span style="font-size:13px;opacity:.85">오늘</span>')
_b = dc.index('{{ lg2.avgE }}</b></div></div>', _a) + len('{{ lg2.avgE }}</b></div></div>')
_gp = lambda icon, k, v: ('<span style="border-radius:32px;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.38);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);padding:12px 6px 14px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px;min-width:0">'
  '<span style="width:46px;height:46px;border-radius:50%;background:#fff;box-shadow:0 4px 12px rgba(40,20,120,.25);display:grid;place-items:center"><span style="' + _ICS + 'font-size:23px;color:#6A3BEF">' + icon + '</span></span>'
  '<span style="font-size:14px;font-weight:700;opacity:.92;white-space:nowrap">' + k + '</span><b style="font-size:clamp(16px,4.6vw,20px);font-weight:800;white-space:nowrap">' + v + '</b></span>')
dc = dc[:_a] + '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px">' + _gp('today', '오늘', '{{ lg2.total }}') + _gp('savings', '총 누적', '{{ lg2.cum }}') + _gp('calendar_month', '하루 평균', '{{ lg2.avgE }}') + '</div>' + dc[_b:]
# ── 지도: 날짜를 바꾸면 다시 그리기(경로·경유지·명물·현재 위치가 바뀌면 키 변경)
_o = "var D = window.__v8, k = el.getAttribute('data-k') + '|' + (D.trk || '').length"
assert dc.count(_o) == 1
dc = dc.replace(_o, "var D = window.__v8, k = el.getAttribute('data-k') + '|' + (D.route || []).length + '|' + JSON.stringify((D.stops || []).map(function (s) { return [s.ll, !!s.past, !!s.nx]; })) + '|' + (D.places || []).length + '|' + JSON.stringify((D.places || []).map(function (p) { return !!p.passed; })) + '|' + (D.me ? D.me.join(',') : '') + '|' + (D.trk || '').length")
# ── 홈 상단 중복 정리: 헤더 DAY 칩은 "DAY n / 31"만, 히어로의 TODAY'S JOURNEY 칩 삭제(날짜·D-day는 히어로 날짜 줄에)
dc = dc.replace('DAY&nbsp;{{ hr.day }}&nbsp;/&nbsp;31', 'DAY&nbsp;{{ hr.dn }}&nbsp;/&nbsp;31', 1)
_i = dc.index("TODAY'S JOURNEY · DAY{{ hr.day }}</span>"); _a = dc.rindex('<span', 0, _i)
dc = dc[:_a] + '<span></span>' + dc[_i + len("TODAY'S JOURNEY · DAY{{ hr.day }}</span>"):]
# ── 지도: 같은 지점의 명물이 겹치지 않게 옆으로 펼치기
_o = "(D.places || []).forEach(function (p) { L.marker(p.ll, { icon: L.divIcon({ className: '', iconSize: [0, 0], html: '<div style=\"transform:translate(-50%,-50%);width:24px;"
assert dc.count(_o) == 1, dc.count(_o)
dc = dc.replace(_o, "var _pg = {}; (D.places || []).forEach(function (p) { var _ky = p.ll[0].toFixed(4) + ',' + p.ll[1].toFixed(4), _pn = _pg[_ky] = (_pg[_ky] || 0) + 1, _ox = (_pn - 1) * 24; L.marker(p.ll, { icon: L.divIcon({ className: '', iconSize: [0, 0], html: '<div style=\"transform:translate(calc(-50% + ' + _ox + 'px),-50%);width:24px;")
# ── 명물 실제 위치: 주소로 좌표 찾기(국토지리원 → OSM), 기기에 저장해 두고 다시 그림
_GEO = r"""<script>(function () {
  var KEY = 'tk-geo2', C = {}; try { C = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) {}
  window.__geo = {}; Object.keys(C).forEach(function (k) { if (C[k]) window.__geo[k] = C[k]; });
  var Q = [], busy = false, seen = {};
  function hav(a, b) { var R = 6371, r = Math.PI / 180, dl = (b[0] - a[0]) * r, dn = (b[1] - a[1]) * r, x = Math.sin(dl / 2) * Math.sin(dl / 2) + Math.cos(a[0] * r) * Math.cos(b[0] * r) * Math.sin(dn / 2) * Math.sin(dn / 2); return 2 * R * Math.asin(Math.sqrt(x)); }
  function clean(a) { return String(a).replace(/\s*(周辺|付近|一帯|エリア).*$/, '').split(/[・\/]/)[0].replace(/\s+/g, '').trim(); }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(C)); } catch (e) {} }
  function done(addr, ll) { C[addr] = ll || 0; if (ll) window.__geo[addr] = ll; save(); try { window.__tkApp && window.__tkApp.forceUpdate(); } catch (e) {} }
  function gsi(q) { return fetch('https://msearch.gsi.go.jp/address-search/AddressSearch?q=' + encodeURIComponent(q)).then(function (r) { return r.json(); }).then(function (j) { return j && j[0] && j[0].geometry ? [j[0].geometry.coordinates[1], j[0].geometry.coordinates[0]] : null; }); }
  function osm(q) { return fetch('https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=jp&q=' + encodeURIComponent(q)).then(function (r) { return r.json(); }).then(function (j) { return j && j[0] ? [+j[0].lat, +j[0].lon] : null; }); }
  function next() {
    if (busy || !Q.length) return; busy = true; var it = Q.shift(), q = clean(it[0]), near = it[1];
    var ok = function (ll) { return ll && (!near || hav(ll, near) < 25) ? ll : null; };
    gsi(q).then(ok).catch(function () { return null; }).then(function (ll) { return ll || osm(q).then(ok).catch(function () { return null; }); })
      .then(function (ll) { done(it[0], ll); }).catch(function () {}).then(function () { busy = false; setTimeout(next, 1100); });
  }
  window.__geoNeed = function (list) { (list || []).forEach(function (x) { if (!x || !x[0] || seen[x[0]] || C.hasOwnProperty(x[0])) return; seen[x[0]] = 1; Q.push(x); }); next(); };
})();</script>"""
_mi = dc.index('<script>(function () {\n  var TILE')
dc = dc[:_mi] + _GEO + dc[_mi:]
# ── 히어로 날짜 줄 삭제(날짜·D-day는 날짜 이동 알약에만)
_o = '<span style="font-size:13px;font-weight:700;opacity:.92">{{ hr.when }}</span>\n'
assert dc.count(_o) == 1, dc.count(_o)
dc = dc.replace(_o, '', 1)
# ── 홈 2열 높이 맞춤: 좌우 카드를 행 단위로 짝지어 같은 높이(걸은 거리|타일, 지도|경유지+다음 목적지, 숙소|전체 종주)
def _kids(s, a):
    e = _dend(s, a); i = s.index('>', a) + 1; out = []; d = 0; st = None
    for m in re.finditer(r'<(div|button|sc-if)\b[^>]*>|</(div|button|sc-if)>', s[i:e - 6]):
        if m.group(1):
            if d == 0: st = i + m.start()
            d += 1
        else:
            d -= 1
            if d == 0: out.append(s[st:i + m.end()])
    return out
_hh = dc.index('data-screen-label="홈 사진 히어로"')
_g0 = dc.index('<div style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;padding:0 16px;align-items:stretch;min-height:{{ fr.gridMin }}">', _hh)
_g1 = _dend(dc, _g0)
_cols = _kids(dc, _g0); assert len(_cols) == 2
_L = _kids(_cols[0], 0); _R = _kids(_cols[1], 0); assert len(_L) == 3 and len(_R) == 4, (len(_L), len(_R))
_R0 = _R[0].replace('<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px">', '<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-rows:1fr;gap:10px">', 1)
_R1 = _R[1].replace('<div style="background:rgba(255,255,255,.6);', '<div style="flex:1;background:rgba(255,255,255,.6);', 1)
_TRC = ('<div style="background:rgba(255,255,255,.6);border:1px solid rgba(255,255,255,.9);backdrop-filter:blur(22px) saturate(1.4);-webkit-backdrop-filter:blur(22px) saturate(1.4);box-shadow:0 8px 24px rgba(40,50,140,.08);border-radius:24px;padding:14px 16px;display:flex;flex-direction:column;gap:10px">'
  '<sc-if value="{{ tr.show }}" hint-placeholder-val="{{ false }}"><div style="display:flex;flex-direction:column;gap:6px"><span style="display:flex;align-items:center;gap:8px"><span style="font-size:14px;font-weight:800;padding:3px 10px;border-radius:99px;background:#E8F0FF;color:#2A5BC4">{{ tr.mode }}</span><b style="font-size:17px;font-weight:800">오늘 탈 것</b></span>'
  '<b style="font-size:17px">{{ tr.route }}</b><span style="font-size:15px;font-weight:700;color:#4A5D78">{{ tr.stat }}</span><span style="font-size:15px;font-weight:800;color:#2A5BC4">대략 {{ tr.fare }}</span></div></sc-if>'
  '<button onClick="{{ tr.help }}" style="width:100%;min-height:48px;border-radius:16px;border:1px solid #C9D6F5;background:#fff;color:#2A5BC4;font:800 15px Pretendard,sans-serif;display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer"><span style="font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;text-transform:none;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-size:20px">train</span>힘들 때 · 지금 위치에서 숙소까지 기차·버스</button></div>')
_new = ('<div style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;padding:0 16px;align-items:stretch">' + _L[0] + _R0 + _L[1]
        + '<div style="display:flex;flex-direction:column;gap:12px;min-width:0">' + _R1 + _R[2] + _TRC + '</div>' + _L[2] + _R[3] + '</div>')
dc = dc[:_g0] + _new + dc[_g1:]
# ── 기록 탭 2열 높이 맞춤: 체중 카드를 왼쪽 열 끝으로, 양쪽 마지막 카드가 남는 높이를 채움
_lg0 = dc.index('<sc-if value="{{ tb.log }}"')
_g0 = dc.index('<div style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;padding:0 16px;align-items:stretch">', _lg0)
_g1 = _dend(dc, _g0)
_cols = _kids(dc, _g0); assert len(_cols) == 2
_L = _kids(_cols[0], 0); _R = _kids(_cols[1], 0); assert len(_L) == 5 and len(_R) == 6, (len(_L), len(_R))
assert '체중 변화' in _R[4] and '수면 시간' in _R[3]
_R3 = _R[3].replace('<div style="background:#fff;', '<div style="flex:1;background:#fff;', 1)
_cs = '<div style="display:flex;flex-direction:column;gap:12px;min-width:0">'
dc = dc[:_g0] + '<div style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;padding:0 16px;align-items:stretch">' + _cs + ''.join(_L) + _R[4] + '</div>' + _cs + _R[0] + _R[1] + _R[2] + _R3 + '</div></div>' + _R[5] + dc[_g1:]
# ── 수면·체중 그래프 다시: 선·막대는 SVG(늘어남), 글자·점은 HTML(크기 고정)
_a = dc.index('<div style="position:relative;height:120px;display:flex;gap:10px;padding:0 4px"><span style="position:absolute;left:0;right:0;top:60px;border-top:2px dashed #9A63F5')
_b = dc.index('</sc-for></div>', dc.index('</sc-for></div>', _a) + 5) + len('</sc-for></div>')
_gl = ''.join('<line x1="0" y1="%d" x2="320" y2="%d" stroke="#EEF0F6" stroke-width="1" vector-effect="non-scaling-stroke"></line>' % (y, y) for y in (10, 40, 100, 130))
dc = dc[:_a] + ('<div style="position:relative;height:140px;margin-top:4px"><svg viewBox="0 0 320 140" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">' + _gl +
  '<line x1="0" y1="70" x2="320" y2="70" stroke="#9A63F5" stroke-width="1.6" stroke-dasharray="5 4" vector-effect="non-scaling-stroke"></line>'
  '<sc-for list="{{ lg2.sl.v }}" as="b" hint-placeholder-count="7"><rect x="{{ b.x }}" y="{{ b.y }}" width="12" height="{{ b.h }}" rx="2" fill="{{ b.c }}"></rect></sc-for></svg>'
  '<span style="position:absolute;right:0;top:50%;transform:translateY(-130%);font-size:14px;font-weight:800;color:#7544ED;background:rgba(255,255,255,.85);padding:0 2px">기준 7h</span></div>'
  '<div style="position:relative;height:20px"><sc-for list="{{ lg2.sl.v }}" as="b" hint-placeholder-count="7"><span style="position:absolute;left:{{ b.lp }};transform:translateX(-50%);font-size:14px;color:#64748B">{{ b.l }}</span></sc-for></div>') + dc[_b:]
_a = dc.index('<div style="position:relative;margin-top:6px"><svg viewBox="0 0 300 110" preserveAspectRatio="none"')
_b = dc.index('</sc-for></div>', _a) + len('</sc-for></div>')
dc = dc[:_a] + ('<div style="position:relative;height:150px;margin:6px 0 4px"><svg viewBox="0 0 320 140" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%">' + _gl +
  '<polygon points="{{ lg2.w3.area }}" fill="rgba(154,99,245,.14)"></polygon><line x1="0" y1="{{ lg2.w3.by }}" x2="320" y2="{{ lg2.w3.by }}" stroke="#9A63F5" stroke-width="1.6" stroke-dasharray="5 4" vector-effect="non-scaling-stroke"></line>'
  '<polyline points="{{ lg2.w3.pts }}" fill="none" stroke="#7544ED" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"></polyline></svg>'
  '<span style="position:absolute;right:0;top:{{ lg2.w3.byp }};transform:translateY(-130%);font-size:14px;font-weight:800;color:#7544ED;background:rgba(255,255,255,.85);padding:0 2px">{{ lg2.w3.lab }}</span>'
  '<sc-for list="{{ lg2.w3.dots }}" as="d" hint-placeholder-count="3"><span style="position:absolute;left:{{ d.lp }};top:{{ d.tp }};width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:#fff;border:3px solid #7544ED;box-sizing:border-box"></span></sc-for></div>') + dc[_b:]
# ── 여정: 주차별 거리 다시 디자인(원형 주차 번호·상태 칩·거리·구간·주간 진행률)
_wi = dc.index('<b style="font-size:18px;font-weight:800;letter-spacing:-.03em">주차별 거리</b>')
_wc = dc.rindex('<div style="background:#fff;', 0, _wi); _we = _dend(dc, _wc)
dc = dc[:_wc] + ('<div style="background:#fff;border:1px solid rgba(255,255,255,.95);box-shadow:0 10px 28px rgba(40,50,140,.10);border-radius:24px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0">'
 '<b style="font-size:18px;font-weight:800;letter-spacing:-.03em;color:#18324F">주차별 거리</b>'
 '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(132px,1fr));gap:10px"><sc-for list="{{ jn.weeks }}" as="w" hint-placeholder-count="5">'
 '<button onClick="{{ w.go }}" style="display:flex;flex-direction:column;gap:10px;min-width:0;padding:14px;border-radius:22px;border:{{ w.tbd }};background:{{ w.tbg }};box-shadow:0 6px 16px rgba(84,40,232,.06);cursor:pointer;text-align:left;font-family:inherit;color:#1A1D20">'
 '<span style="display:flex;align-items:center;justify-content:space-between;gap:6px"><span style="flex:none;width:40px;height:40px;border-radius:50%;background:#fff;box-shadow:0 3px 10px rgba(84,40,232,.18);display:flex;align-items:center;justify-content:center;padding:0;box-sizing:border-box;color:#5B32D6"><b style="font-size:17px;font-weight:800;line-height:1">{{ w.no }}</b><span style="font-size:12px;font-weight:700">주</span></span><span style="height:26px;padding:0 10px;border-radius:99px;background:{{ w.cb }};color:{{ w.cf }};font-size:13px;font-weight:800;display:flex;align-items:center;white-space:nowrap">{{ w.st }}</span></span>'
 '<b style="font-size:22px;font-weight:800;letter-spacing:-.03em;white-space:nowrap">{{ w.km }}</b>'
 '<span style="font-size:14px;line-height:1.35;color:#64748B;overflow-wrap:anywhere">{{ w.path }}</span>'
 '<span style="display:flex;align-items:center;gap:8px;margin-top:auto"><span style="flex:1;height:6px;border-radius:99px;background:#EEEAF8;overflow:hidden"><span style="display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#5428E8,#9A63F5);width:{{ w.pctT }}"></span></span><b style="font-size:13px;font-weight:800;color:#5B32D6;white-space:nowrap">{{ w.pctT }}</b></span>'
 '</button></sc-for></div></div>') + dc[_we:]
# ── 2열 화면 공통: 각 열 마지막 카드가 남는 높이를 채워 좌우 아래끝 맞춤
for _key in ['{{ sb2.plan }}', '{{ sb2.glance }}', '{{ sb2.day }}', '{{ sb2.info }}', '{{ sb2.stamp }}']:
    _p0 = dc.find('<sc-if value="' + _key + '"')
    if _p0 < 0: continue
    _gx = dc.find('grid-template-columns:{{ fr.cols }}', _p0)
    _pe = dc.find('</sc-if>', _p0)
    if _gx < 0: continue
    _g0 = dc.rindex('<div', 0, _gx)
    try: _cols = _kids(dc, _g0)
    except Exception: continue
    _new = []
    for _c in _cols:
        _ks = _kids(_c, 0) if _c.startswith('<div style="display:flex;flex-direction:column') else []
        if _ks:
            _cand = [k for k in _ks if k.startswith('<div style="') and 'position:fixed' not in k[:k.index('>')] and ('background' in k[:k.index('>')] or 'display:grid' in k[:k.index('>')])]
            _last = _cand[-1] if _cand else ''
            if _last and not _last.startswith('<div style="flex:1'):
                _c = _c.replace(_last, '<div style="flex:1;' + _last[len('<div style="'):], 1)
        _new.append(_c)
    _g1 = _dend(dc, _g0)
    _hd = dc[_g0:dc.index('>', _g0) + 1]
    dc = dc[:_g0] + _hd + ''.join(_new) + '</div>' + dc[_g1:]
# 일정 관리: 고정 버튼용 빈칸을 오른쪽 열 안 → 표 아래로(좌우 아래끝 맞춤)
assert dc.count('<div style="height:76px"></div>') == 1
dc = dc.replace('<div style="height:76px"></div>', '', 1)
_p0 = dc.index('<sc-if value="{{ sb2.plan }}"'); _gx = dc.index('grid-template-columns:{{ fr.cols }}', _p0); _g0 = dc.rindex('<div', 0, _gx); _g1 = _dend(dc, _g0)
dc = dc[:_g1] + '<div style="height:76px"></div>' + dc[_g1:]
# 여정 사진 줄: 고른 날을 확실히(크게·굵은 흰 테두리+보라 링·번호 보라 배경, 나머지 흐리게)
_o = 'style="flex:none;position:relative;width:64px;height:76px;border-radius:18px;border:2px solid {{ q.bd }};background:{{ q.img }};opacity:{{ q.op }};box-shadow:{{ q.sh }};cursor:pointer;padding:0;overflow:hidden"><span style="position:absolute;left:0;right:0;bottom:0;padding:14px 0 4px;background:linear-gradient(180deg,rgba(0,0,0,0),rgba(20,10,70,.85));'
assert dc.count(_o) == 1
dc = dc.replace(_o, 'style="flex:none;align-self:center;position:relative;width:{{ q.w }};height:{{ q.h }};border-radius:18px;border:{{ q.bw }} solid {{ q.bd }};background:{{ q.img }};opacity:{{ q.op }};box-shadow:{{ q.sh }};cursor:pointer;padding:0;overflow:hidden;margin:4px 2px;transition:all .15s"><span style="position:absolute;left:0;right:0;bottom:0;padding:5px 0 4px;background:{{ q.lb }};', 1)
# 날짜 자세히: '이 날 걸은 길' 지도가 남는 높이를 채워 오른쪽 '오늘 나의 하루'와 아래끝 맞춤 · 사진 칸 안내 글자 삭제
_i = dc.index('<b style="font-size:18px;font-weight:800;letter-spacing:-.03em">이 날 걸은 길</b>')
_o = '<div style="position:relative;height:200px;border-radius:18px;overflow:hidden;background:#EEF2F8;border:1px solid #E6E9F7">'
_j = dc.index(_o, _i); dc = dc[:_j] + '<div style="position:relative;flex:1;min-height:200px;border-radius:18px;overflow:hidden;background:#EEF2F8;border:1px solid #E6E9F7">' + dc[_j + len(_o):]
dc = dc.replace('placeholder="사진 추가"', 'placeholder=""')
# 홈 지도: Leaflet 패널(z-index 400)이 팝업 위로 올라와 배경을 누르면 지도로 이동하던 문제 → 지도 칸을 별도 쌓임 맥락으로
_o = '<div data-v8map="home" data-k="home" style="position:absolute;inset:0;pointer-events:none"'
assert dc.count(_o) == 1
dc = dc.replace(_o, '<div data-v8map="home" data-k="home" style="position:absolute;inset:0;pointer-events:none;z-index:0;isolation:isolate"', 1)
dc = dc.replace('<div data-v8map="log" data-k="log" style="position:absolute;inset:0"', '<div data-v8map="log" data-k="log" style="position:absolute;inset:0;z-index:0;isolation:isolate"')
# ── 사진 백업(Supabase Storage tk-photos): 저장 시 올리고, 처음 열 때 서버에만 있는 날을 내려받음. 인증 헤더는 동기화 스크립트의 것을 그대로 사용
_sy = "var URL_ = 'https://jmfvsusybouibqmdvtmy.supabase.co/functions/v1/tk-sync', H = "
_si = dc.index(_sy); _se = dc.index('};', _si) + 2
dc = dc[:_se] + ' window.__tkHdr = H;' + dc[_se:]
_PH = r"""<script>(function () {
  var U = 'https://jmfvsusybouibqmdvtmy.supabase.co/functions/v1/tk-photo';
  function hd() { return window.__tkHdr || {}; }
  function ls(k, v) { try { if (v === undefined) return JSON.parse(localStorage.getItem(k) || '{}'); localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return {}; } }
  var stT = 0;
  function st(msg, bad) { try { var e = document.getElementById('tk-ph-st'); if (!e) { e = document.createElement('div'); e.id = 'tk-ph-st'; e.setAttribute('role', 'status'); e.style.cssText = 'position:fixed;left:50%;transform:translateX(-50%);bottom:108px;z-index:9998;padding:10px 16px;border-radius:99px;font:700 14px Pretendard,system-ui,sans-serif;color:#fff;box-shadow:0 6px 18px rgba(0,0,0,.25);pointer-events:none;transition:opacity .2s'; document.body.appendChild(e); } e.textContent = msg; e.style.background = bad ? '#DC2626' : '#1C1B33'; e.style.opacity = '1'; clearTimeout(stT); stT = setTimeout(function () { e.style.opacity = '0'; }, bad ? 4000 : 2200); } catch (x) {} }
  function put(iso, arr) { var P = ls('tk-ph-pend'); P[iso] = 1; ls('tk-ph-pend', P); st('사진 백업 중…');
    return fetch(U + '?iso=' + iso, { method: 'PUT', headers: hd(), body: JSON.stringify(arr || []) }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function () { var P2 = ls('tk-ph-pend'); delete P2[iso]; ls('tk-ph-pend', P2); var T2 = ls('tk-ph-ts'); T2[iso] = Date.now(); ls('tk-ph-ts', T2); st('사진 백업 완료'); }).catch(function () { st('사진 백업 실패 · 연결되면 다시 시도해요', true); }); }
  window.__phPut = put;
  window.__phSync = function (local, apply) {
    if (!window.__tkHdr) return void setTimeout(function () { window.__phSync(local, apply); }, 1500);
    var P = ls('tk-ph-pend'); Object.keys(P).forEach(function (iso) { if (local[iso]) put(iso, local[iso]); });
    fetch(U, { headers: hd() }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (list) {
      var T = ls('tk-ph-ts'), have = {};
      (list || []).forEach(function (f) { have[f.iso] = 1; var loc = local[f.iso], lt = T[f.iso] || 0;
        if ((!loc || !loc.length || f.t > lt + 60000) && !ls('tk-ph-pend')[f.iso]) fetch(U + '?iso=' + f.iso, { headers: hd() }).then(function (r) { return r.json(); }).then(function (arr) { if (Array.isArray(arr) && arr.length) { apply(f.iso, arr); var T3 = ls('tk-ph-ts'); T3[f.iso] = f.t; ls('tk-ph-ts', T3); } }).catch(function () {}); });
      Object.keys(local).forEach(function (iso) { if (!have[iso] && local[iso] && local[iso].length) put(iso, local[iso]); });
    }).catch(function () {});
  };
})();</script>"""
_mi = dc.index('<script>(function () {\n  var TILE')
dc = dc[:_mi] + _PH + dc[_mi:]
# 기록 체중 카드: 왼쪽 열이 길 때 남는 높이를 그래프가 채우도록
_wk = dc.index('{{ lgc.wt.open }}')
_w1 = dc.index('<div style="display:flex;flex-direction:column;gap:12px">', _wk)
dc = dc[:_w1] + '<div style="flex:1;display:flex;flex-direction:column;gap:12px">' + dc[_w1+len('<div style="display:flex;flex-direction:column;gap:12px">'):]
_w2 = dc.index('<div style="position:relative;height:150px;margin:6px 0 4px">', _w1)
dc = dc[:_w2] + '<div style="position:relative;flex:1;min-height:150px;margin:6px 0 4px">' + dc[_w2+len('<div style="position:relative;height:150px;margin:6px 0 4px">'):]
# 기록 탭: GPS 기록이 없는 날은 그 날의 계획 경로를 흐린 점선으로 표시
_k0 = "var D = window.__v8, k = el.getAttribute('data-k') + '|' + "
assert dc.count(_k0) == 1
dc = dc.replace(_k0, _k0 + "(window.__dayRoute ? window.__dayRoute.length + ',' + window.__dayRoute[0] : '') + '|' + ")
_k1 = "} else { try { el._map.setView((D.logC || D.me || (D.stops && D.stops[0] && D.stops[0].ll) || [35.62, 139.74]), 13); } catch (e) {} }"
assert dc.count(_k1) == 1
dc = dc.replace(_k1, "} else if (window.__dayRoute && window.__dayRoute.length > 1) { try { L.polyline(window.__dayRoute, { color: '#673DE6', weight: 4, opacity: .4, dashArray: '6 8' }).addTo(el._lay); el._map.fitBounds(L.latLngBounds(window.__dayRoute), { padding: [24, 24], maxZoom: 15 }); } catch (e) {} } else { try { el._map.setView((D.logC || D.me || (D.stops && D.stops[0] && D.stops[0].ll) || [35.62, 139.74]), 13); } catch (e) {} }")
dc = dc.replace("OwnTracks 위치 기록이 없는 날이에요", "GPS 기록이 없는 날이에요 · 흐린 점선은 계획 경로")
# 최소 글자 크기 14px (시력 배려): <script> 밖의 마크업에서 10~13px → 14px
_parts = _re2.split(r'(<script[\s\S]*?</script>)', dc)
dc = ''.join(p_ if k_ % 2 else _re2.sub(r'font-size:(?:1[0-3]|[0-9])(?:\.\d+)?px', 'font-size:14px', p_) for k_, p_ in enumerate(_parts))
# 터치 영역 최소 44px
for _a, _b in [('width:36px;height:44px', 'width:44px;height:44px'), ('width:40px;height:40px;border-radius:50', 'width:44px;height:44px;border-radius:50'),
               ('height:38px;border-radius:12px;border:1px solid', 'height:44px;min-width:44px;border-radius:12px;border:1px solid'),
               ('height:40px;padding:0 14px;border-radius:99px', 'height:44px;padding:0 14px;border-radius:99px'),
               ('height:40px;width:46px', 'height:44px;width:48px'),
               ('white-space:nowrap;height:40px;padding:', 'white-space:nowrap;height:44px;padding:')]:
    print('tap', _a[:30], dc.count(_a))
    dc = dc.replace(_a, _b)
# 비상 연락처 카드: 가이드의 긴급 색 #DC2626 사용
_ek = dc.index('비상 연락처')
_ee = dc.index('설정', _ek)
_seg = dc[_ek:_ee]
_seg = _seg.replace('linear-gradient(135deg,#C92A42,#F06A7F)', 'linear-gradient(135deg,#DC2626,#F26B6B)').replace('#B8364A', '#DC2626').replace('#C92A42', '#DC2626')
dc = dc[:_ek] + _seg + dc[_ee:]
# 오프라인용 서비스 워커 등록
dc = dc.replace('</body>', "<script>if('serviceWorker' in navigator&&location.protocol==='https:'){window.addEventListener('load',function(){navigator.serviceWorker.register('/sw.js').catch(function(){})})}</script></body>", 1)
# 휴식일/멀리 있을 때: 내 위치에서 출발지까지 이어지는 파란 줄 방지
_b0 = "if (_from && D.me) fut = [D.me].concat(fut); if (fut.length > 1) {"
assert dc.count(_b0) == 1
dc = dc.replace(_b0, "var _span = pts.length > 1 ? Math.abs(pts[0][0]-pts[pts.length-1][0]) + Math.abs(pts[0][1]-pts[pts.length-1][1]) : 0; if (_span < 0.002) fut = []; else if (_from && D.me) { var _dm = Infinity; pts.forEach(function (q) { var dd2 = Math.pow(q[0]-D.me[0], 2) + Math.pow(q[1]-D.me[1], 2); if (dd2 < _dm) _dm = dd2; }); if (_dm < 0.0004) fut = [D.me].concat(fut); } if (fut.length > 1) {")
# 전체 일정 목록: 오른쪽 카드가 더 높을 때 빈칸 대신 행 높이를 늘려 채움
_l0 = '<div style="display:flex;flex-direction:column">\n<sc-for list="{{ jn.days }}" as="d" hint-placeholder-count="7">\n<button onClick="{{ d.open }}" style="display:grid;grid-template-columns:48px minmax(0,1fr) auto 20px;gap:12px;align-items:center;padding:11px 0;'
assert dc.count(_l0) == 1
dc = dc.replace(_l0, '<div style="flex:1;display:flex;flex-direction:column">\n<sc-for list="{{ jn.days }}" as="d" hint-placeholder-count="7">\n<button onClick="{{ d.open }}" style="flex:1;display:grid;grid-template-columns:48px minmax(0,1fr) auto 20px;gap:12px;align-items:center;padding:11px 0;')
# 명물 사진(위키미디어 커먼즈): build/spot_photos.json → 이름별 맵
import json as _js
_sp = _js.load(open(os.path.join(BASE, 'build/spots.json'), encoding='utf-8')) if 'BASE' in globals() else _js.load(open('build/spots.json', encoding='utf-8'))
try:
    _ph = _js.load(open('build/spot_photos.json', encoding='utf-8'))
except Exception:
    _ph = {}
_sph = {}
for _k, _v in _ph.items():
    _n = _sp[int(_k)]['ko']
    _sph[_n] = {'f': _v['file'], 'c': '사진: ' + _v['credit']}
dc = dc.replace('</head>', '<script>window.__SPH=' + _js.dumps(_sph, ensure_ascii=False) + ';</script></head>', 1)
_o = _re2.search(r'<span style="font-size:1[24]px;font-weight:700;color:rgba\(255,255,255,\.85\)">눌러서 크게 보기</span>', dc)
assert _o, 'jfav'
dc = dc[:_o.start()] + ('<span style="display:flex;gap:6px">' + '<button onClick="{{ jp2.toggleFav }}" aria-label="즐겨찾기" style="flex:none;white-space:nowrap;height:44px;min-width:44px;padding:0 14px;margin:-8px -4px 0 0;border-radius:99px;border:1px solid rgba(255,255,255,.55);background:rgba(255,255,255,.22);color:#fff;font:800 14px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer;z-index:3">{{ jp2.favT }}</button></span>') + dc[_o.end():]
_o = '<div style="padding:8px 20px 16px;display:flex;flex-direction:column;gap:4px"><b style="font-size:30px;font-weight:800;letter-spacing:-.04em">하루 기록</b></div>'
assert dc.count(_o) == 1, 'share'
dc = dc.replace(_o, '<div style="padding:8px 20px 16px;display:flex;align-items:center;justify-content:space-between;gap:8px"><b style="font-size:30px;font-weight:800;letter-spacing:-.04em">하루 기록</b><button onClick="{{ lg2.shareDay }}" aria-label="하루 요약 공유" style="flex:none;height:44px;padding:0 16px;border-radius:99px;border:1px solid #C5CCEE;background:#fff;color:#3B5BDB;font:800 14px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer">요약 공유</button></div>')
_o = _re2.findall(r'<span style="font-size:1[2-4]px;font-weight:700;color:\{\{ m\.sc \}\}"> \{\{ m\.s \}\}</span></b>', dc)
assert _o, 'metric-s'
dc = _re2.sub(r'<span style="font-size:1[2-4]px;font-weight:700;color:\{\{ m\.sc \}\}"> \{\{ m\.s \}\}</span></b>', lambda m: '<span style="display:block;font-size:14px;font-weight:700;color:{{ m.sc }}">{{ m.s }}</span></b>', dc)
# 스탬프 화면: 역참 도장 박스(제목·필터)는 고정하고 도장 목록만 박스 안에서 스크롤
_m = _re2.search(r'<div style="display:grid;grid-template-columns:[^"]*;gap:8px"><sc-for list="\{\{ stp2\.list \}\}"', dc)
assert _m, 'stamp-grid'
dc = dc[:_m.start()] + _m.group(0).replace('gap:8px"', 'gap:8px;overflow-y:auto;overscroll-behavior:contain;max-height:min(62vh,560px);padding:2px 2px 6px;-webkit-overflow-scrolling:touch"', 1) + dc[_m.end():]
# 일본어: 파파고 열기 버튼을 뒤로 버튼과 같은 높이로 좌측 하단에 고정
_bk = _re2.search(r'<button onClick="\{\{ back2 \}\}" aria-label="뒤로 가기"', dc)
assert _bk, 'back2'
dc = dc[:_bk.start()] + '<sc-if value="{{ sb2.jp }}" hint-placeholder-val="{{ false }}"><button onClick="{{ jp2.papago }}" aria-label="파파고 앱 열기" style="position:absolute;left:16px;bottom:calc(env(safe-area-inset-bottom) + 22px);z-index:3;height:60px;padding:0 22px;border-radius:30px;border:0;background:#03C75A;box-shadow:0 12px 26px rgba(3,199,90,.3);display:flex;align-items:center;color:#fff;font:800 16px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer">파파고 열기</button></sc-if>' + dc[_bk.start():]
# 더보기: 비상 연락처·설정 카드 안 여백 줄이기
_ma = dc.index('<sc-if value="{{ tb.more }}"')
_g = dc.index('<div style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;align-items:stretch">', _ma)
_blk = dc[_g:_g + 9000]
_k = 'border-radius:24px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0">'
assert _blk.count(_k) >= 2, 'more-cards'
_blk = _blk.replace(_k, 'border-radius:24px;padding:14px 16px;display:flex;flex-direction:column;gap:10px;min-width:0">', 2)
dc = dc[:_g] + _blk + dc[_g + 9000:]
# 홈: 다음 날 카드 + 날짜 변경 카드(반반)를 '오늘 지나는 명물' 아래로
_rowo = '<div style="display:grid;grid-template-columns:{{ fr.cols }};gap:12px;padding:12px 16px 0;align-items:stretch">\n<button onClick="{{ dn2.openNext }}"'
assert dc.count(_rowo) == 1
_rs = dc.index(_rowo)
_re = dc.index('\n</div>\n', dc.index('{{ dn2.next }}', _rs)) + len('\n</div>') 
_re = dc.index('\n</div>', _re) + len('\n</div>')
_row = dc[_rs:_re]
assert _row.count('<button onClick="{{ dn2.next }}"') == 1 and _row.endswith('</div>\n</div>')
dc = dc[:_rs] + dc[_re:]
_end = '</div>\n\n<sc-if value="{{ mapFull }}" hint-placeholder-val="{{ false }}">\n<div data-screen-label="지도 전체 화면"'
assert dc.count(_end) == 1
dc = dc.replace(_end, _row + '\n' + _end)
# 지도 탭: 우측 하단에 날짜 변경(이전/다음 날), 다음 목적지 카드와 한 줄로
_mo = '<sc-if value="{{ mapFull }}" hint-placeholder-val="{{ false }}">\n<button onClick="{{ openNext }}" style="width:100%;'
assert dc.count(_mo) == 1
_mi = dc.index(_mo)
_mc = dc.index('</button>\n</sc-if>', _mi) + len('</button>\n')
_ic = lambda n: '<span style="font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'FILL\' 1,\'wght\' 500;font-size:32px;color:#3B5BDB">' + n + '</span>'
_bt = lambda fn, op, n, lb: '<button onClick="{{ dn2.' + fn + ' }}" aria-label="' + lb + '" style="flex:none;width:60px;height:60px;border-radius:50%;border:0;background:#EDF0FF;display:grid;place-items:center;cursor:pointer;opacity:{{ dn2.' + op + ' }}">' + _ic(n) + '</button>'
_dc = '<div style="flex:none;width:208px;box-sizing:border-box;border-radius:22px;background:#fff;box-shadow:0 10px 26px rgba(40,50,140,.16);padding:6px;display:flex;align-items:center;justify-content:space-between;gap:2px">' + _bt('prev','pO','chevron_left','이전 날') + '<span onClick="{{ dn2.goToday }}" style="cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:1px;min-width:64px;line-height:1.15"><b style="font-size:16px;white-space:nowrap">{{ dn2.cur.n }}일차</b><span style="font-size:13px;font-weight:600;color:#6B7A90;white-space:nowrap">{{ dn2.cur.date }}</span></span>' + _bt('next','nO','chevron_right','다음 날') + '</div>'
_blk = dc[_mi:_mc].replace('<sc-if value="{{ mapFull }}" hint-placeholder-val="{{ false }}">\n<button onClick="{{ openNext }}" style="width:100%;', '<sc-if value="{{ mapFull }}" hint-placeholder-val="{{ false }}">\n<div style="display:flex;gap:8px;align-items:stretch"><button onClick="{{ openNext }}" style="flex:1;min-width:0;', 1) + _dc + '</div>\n'
dc = dc[:_mi] + _blk + dc[_mc:]
_cb = '<sc-if value="{{ mapFull }}" hint-placeholder-val="{{ false }}">\n<div style="display:flex;flex-direction:column;gap:8px">\n<div style="display:flex;gap:6px;overflow-x:auto;scrollbar-width:none"><sc-for list="{{ amen.chips }}"'
assert dc.count(_cb) == 1
dc = dc.replace(_cb, _cb.replace('<div style="display:flex;flex-direction:column;gap:8px">', '<div style="display:flex;flex-direction:column;gap:8px;width:calc(100% - 216px)">', 1), 1)
# 홈: 워치 연결·대기 중에도 하단 걷기 표시줄 표시
_ic2 = lambda n, c: '<span style="font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'FILL\' 1,\'wght\' 500;font-size:26px;color:' + c + '">' + n + '</span>'
_wait = '<sc-if value="{{ ctl.wait }}" hint-placeholder-val="{{ false }}"><div style="height:58px;border-radius:29px;background:#fff;box-shadow:0 12px 30px rgba(40,50,140,.18);border:1px solid rgba(255,255,255,.95);display:flex;align-items:center;gap:8px;padding:0 7px 0 6px"><span style="flex:1;min-width:0;display:flex;align-items:center;gap:12px;padding:0 10px"><span style="flex:none;width:12px;height:12px;border-radius:50%;background:#2F9E44;box-shadow:0 0 0 4px rgba(47,158,68,.18)"></span><span style="flex:1;min-width:0;display:flex;flex-direction:column;gap:1px"><b style="font-size:16px;font-weight:800;white-space:nowrap">{{ ctl.cLabel }}</b><span style="font-size:13px;color:#6B7A90;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ ctl.wsub }}</span></span></span><button onClick="{{ start }}" aria-label="폰에서 걷기 시작" style="flex:none;width:46px;height:46px;border-radius:50%;border:0;background:linear-gradient(135deg,#3B5BDB,#6C7FE8);display:grid;place-items:center;cursor:pointer;box-shadow:0 8px 18px rgba(59,91,219,.32)">' + _ic2('directions_walk', '#fff') + '</button></div></sc-if>\n'
_ca = '<sc-if value="{{ ctl.active }}" hint-placeholder-val="{{ true }}">'
assert dc.count(_ca) == 1
dc = dc.replace(_ca, _wait + _ca, 1)
# 지도 하단: 다음 목적지 카드를 칩 줄과 같은 폭(왼쪽 열)에 두고, 날짜 변경은 오른쪽에 크게
# 일정 관리: 요약 타일 3개를 왼쪽 열(이동 방식 아래)로 옮겨 빈 공간 줄이기
_t0 = '<div style="flex:1;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;padding-top:6px"><sc-for list="{{ pl2.sum }}"'
assert dc.count(_t0) == 1
_ts = dc.index(_t0); _te = dc.index('</sc-for></div>', _ts) + len('</sc-for></div>')
_tiles = dc[_ts:_te].replace('flex:1;display:grid','display:grid',1).replace('min-height:150px','min-height:128px').replace('padding:16px;display:flex;flex-direction:column;justify-content:space-between','padding:12px;display:flex;flex-direction:column;justify-content:space-between').replace('font-size:28px','font-size:21px').replace('white-space:nowrap','white-space:normal').replace('overflow:hidden;text-overflow:ellipsis;white-space:normal','white-space:normal')
dc = dc[:_ts] + dc[_te:]
_dist = dc.index('letter-spacing:-.03em">날짜별 거리</b>')
_ro = dc.rindex('<div style="display:flex;flex-direction:column;gap:12px;min-width:0">\n', 0, _dist)
_lc = dc.rindex('</div>\n', 0, _ro)
dc = dc[:_lc] + _tiles + '\n' + dc[_lc:]
# 스탬프: 범례(걸어서·교통·남은 곳)를 위쪽 제목 줄 오른쪽으로, 설명 문구 삭제
_h = re.search(r'(역참 도장</b>)<span style="[^"]*">누를 때마다 미방문 → 도보 → 교통</span>', dc)
assert _h
_k = dc.index('<span style="display:flex;gap:14px;justify-content:center;', _h.end())
_ke = dc.index('남은 곳</span></span>', _k) + len('남은 곳</span></span>')
_leg = dc[_k:_ke].replace('justify-content:center;', 'flex:none;justify-content:flex-end;flex-wrap:nowrap;white-space:nowrap;', 1).replace('gap:14px;', 'gap:10px;', 1)
dc = dc[:_k] + dc[_ke:]
dc = dc.replace(_h.group(0), _h.group(1) + _leg, 1)
# 환율 계산: 빠른 금액 칩이 박스를 벗어나지 않게 3열로
_fx = 'display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-top:12px">\n<sc-for list="{{ fx.table }}"'
assert dc.count(_fx) == 1
dc = dc.replace(_fx, _fx.replace('repeat(5,', 'repeat(3,'), 1)
# 새 버전 알림: 빌드 ID를 meta로 넣고, 주기적으로 서버의 index.html과 비교
import time as _tm
_bid = str(int(_tm.time()))
_VER = """<meta name="tk-build" content="%s"><script>(function(){var me=document.querySelector('meta[name="tk-build"]');if(!me)return;var cur=me.content,shown=false;
function chk(){if(shown||!navigator.onLine)return;fetch(location.pathname+'?v='+Date.now(),{cache:'no-store'}).then(function(r){return r.text()}).then(function(t){var m=t.match(/name="tk-build" content="(\\d+)"/);if(m&&m[1]!==cur){shown=true;var d=document.createElement('div');d.setAttribute('role','alert');d.style.cssText='position:fixed;left:12px;right:12px;top:12px;z-index:99999;display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:16px;background:#1C1B33;color:#fff;font:600 16px/1.4 Pretendard,system-ui,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.3)';d.innerHTML='<span style="flex:1">새 버전이 나왔어요</span><button style="min-height:44px;padding:0 18px;border:0;border-radius:12px;background:linear-gradient(135deg,#4F82E8,#2DB7F5);color:#fff;font:700 16px system-ui">새로고침</button>';d.querySelector('button').onclick=function(){location.reload()};document.body.appendChild(d)}}).catch(function(){})}
setInterval(chk,300000);document.addEventListener('visibilitychange',function(){if(!document.hidden)chk()});})();</script>""" % _bid
dc = dc.replace('<head>', '<head>\n' + _VER, 1)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(dc)
shutil.copy(os.path.join(ROOT, 'design', 'v9', 'support.js'), os.path.join(OUT, 'support.js'))
(os.path.abspath(OUT) != ROOT) and shutil.copy(os.path.join(ROOT, 'image-slot.js'), os.path.join(OUT, 'image-slot.js'))
print('wrote', os.path.relpath(OUT, ROOT) + '/index.html', len(dc))
