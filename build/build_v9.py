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
names = set(m.group(1).split(',')) | {'grid_view', 'edit_calendar', 'open_in_new', 'timer', 'flag', 'local_fire_department', 'thermostat', 'partly_cloudy_day', 'foggy', 'thunderstorm', 'umbrella', 'wb_twilight', 'delete', 'edit', 'close', 'expand_less', 'refresh', 'restart_alt', 'swap_vert', 'translate', 'watch', 'train', 'today', 'info', 'warning', 'add', 'remove', 'search', 'water_drop', 'air', 'undo', 'arrow_forward', 'visibility', 'keyboard_arrow_up', 'keyboard_arrow_down'}
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
<div onClick="{{ plc.pop.close }}" style="position:absolute;inset:0;background:rgba(20,24,60,.45);backdrop-filter:blur(2.5px);-webkit-backdrop-filter:blur(2.5px)"></div>
<div style="position:relative;z-index:2;width:calc(100% - 24px);max-width:{{ fr.spotW }};max-height:calc(100% - 28px);overflow-y:auto;scrollbar-width:none;margin-bottom:calc(env(safe-area-inset-bottom) + 10px);background:#fff;border-radius:28px;padding:16px 16px 14px;display:flex;flex-direction:column;gap:18px;box-shadow:0 24px 60px rgba(10,14,50,.35);animation:sheetUp .28s ease-out">
<div style="position:relative;min-height:clamp(170px,28vh,360px);border-radius:22px;overflow:hidden;background:{{ plc.pop.img }};flex:none"><span style="position:absolute;left:12px;top:12px;height:34px;padding:0 14px;border-radius:99px;background:rgba(255,255,255,.95);display:flex;align-items:center;font-size:16px;font-weight:800;color:#5B3FD0;box-shadow:0 4px 12px rgba(20,30,80,.2)">{{ plc.pop.badge }}</span><b style="position:absolute;right:12px;top:12px;width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,#5428E8,#9A63F5);color:#fff;font-size:17px;display:grid;place-items:center;box-shadow:0 4px 12px rgba(20,30,80,.2)">{{ plc.pop.n }}</b></div>
<div style="display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center"><b style="font-size:30px;font-weight:800;letter-spacing:-.04em;line-height:1.2;color:#18243F">{{ plc.pop.name }}</b><span style="font-size:16px;font-weight:600;color:#6B7A90">{{ plc.pop.jp }} · {{ plc.pop.cat }}</span></div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><span style="border-radius:16px;background:#F6F7FB;border:1px solid #E6E9F5;padding:12px 8px;display:flex;flex-direction:column;align-items:center;gap:4px;min-width:0"><span style="font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap">내 위치에서</span><b style="font-size:20px;font-weight:800;letter-spacing:-.03em;color:#18324F;white-space:nowrap">{{ plc.pop.fromMe }}</b></span><span style="border-radius:16px;background:#F6F7FB;border:1px solid #E6E9F5;padding:12px 8px;display:flex;flex-direction:column;align-items:center;gap:4px;min-width:0"><span style="font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap">걸어서</span><b style="font-size:20px;font-weight:800;letter-spacing:-.03em;color:#18324F;white-space:nowrap">{{ plc.pop.walkT }}</b></span><span style="border-radius:16px;background:#F6F7FB;border:1px solid #E6E9F5;padding:12px 8px;display:flex;flex-direction:column;align-items:center;gap:4px;min-width:0"><span style="font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap">도착 예상</span><b style="font-size:20px;font-weight:800;letter-spacing:-.03em;color:#18324F;white-space:nowrap">{{ plc.pop.etaT }}</b></span></div>
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
rep('<sc-if value="{{ spotOpen }}" hint-placeholder-val="{{ false }}">\n<div data-screen-label="장소 팝업"', _ra + _pp + '<sc-if value="{{ spotOpen }}" hint-placeholder-val="{{ false }}">\n<div data-screen-label="장소 팝업"')
# 홈 사진 히어로 좌우 날짜 이동 버튼(반투명 흰색)
_ic = "font-family:\'Material Symbols Rounded\';font-weight:normal;font-style:normal;line-height:1;letter-spacing:normal;white-space:nowrap;direction:ltr;-webkit-font-smoothing:antialiased;font-feature-settings:\'liga\';font-variation-settings:\'wght\' 600;font-size:26px;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.35)"
_b1 = lambda fn, ic, op, lab: '<button onClick="{{ dn2.%s }}" aria-label="%s" style="width:56px;height:44px;border:0;background:transparent;display:grid;place-items:center;cursor:pointer;opacity:{{ dn2.%s }}"><span style="%s">%s</span></button>' % (fn, lab, op, _ic, ic)
_hb2 = '<span style="position:absolute;right:18px;top:-44px;display:flex;align-items:center;border-radius:18px 18px 0 0;background:rgba(14,18,50,.05);backdrop-filter:blur(2px) saturate(1.2);-webkit-backdrop-filter:blur(2px) saturate(1.2);border:1px solid rgba(255,255,255,.32);border-bottom:0">' + _b1('prev','chevron_left','pO','이전 날') + '<i style="width:1px;height:22px;background:rgba(255,255,255,.32)"></i>' + _b1('next','chevron_right','nO','다음 날') + '</span>'
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
dc = dc.replace(_old, '<div style="display:flex;flex-direction:column;gap:12px;padding:0 16px;min-height:calc(100lvh - 197px)">\n<div style="order:2;margin-top:auto;display:grid;grid-template-columns:{{ fr.menuCols }};gap:12px">')
dc = dc.replace('font-family:inherit;min-height:132px">', 'font-family:inherit;min-height:112px">')
_m0 = dc.index('<sc-for list="{{ mo2 }}"'); _m1 = dc.index('</sc-for>', _m0)
_seg = dc[_m0:_m1].replace('min-height:112px', 'min-height:84px;padding:10px 12px;gap:4px')
dc = dc[:_m0] + _seg + dc[_m1:]
# 더보기 상단: 오늘 날씨 + 이번 주 날씨 + 일출·일몰 요약 카드
_anchor = '<div style="display:flex;flex-direction:column;gap:12px;padding:0 16px;min-height:calc(100lvh - 197px)">\n'
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
  '<div style="display:flex;gap:8px;flex-wrap:wrap"><button onClick="{{ pl2.allWalk }}" style="flex:1;min-width:140px;height:46px;border-radius:14px;border:1.5px solid #C9D3FF;background:#fff;color:#3B5BDB;font:800 14px Pretendard Variable,Pretendard,sans-serif;cursor:pointer">교통 안 타기 (전부 걷기)</button><button onClick="{{ pl2.reset }}" style="flex:1;min-width:140px;height:46px;border-radius:14px;border:1.5px solid #F3C3CB;background:#fff;color:#B8364A;font:800 14px Pretendard Variable,Pretendard,sans-serif;cursor:pointer">모두 되돌리기</button><a href="{{ pl2.agoda }}" target="_blank" rel="noopener" style="flex:1 1 100%;height:46px;border-radius:14px;background:#EDF0FF;color:#3B5BDB;font:800 14px Pretendard Variable,Pretendard,sans-serif;display:flex;align-items:center;justify-content:center;text-decoration:none">이 날 도착지 숙소 찾기 (아고다) ↗</a></div>'
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

rep('<sc-if value="{{ sb2.plan }}" hint-placeholder-val="{{ false }}">', '<sc-if value="{{ sb2.glance }}" hint-placeholder-val="{{ false }}">\n<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px;padding:0 16px 96px"><sc-for list="{{ jn.all }}" as="g" hint-placeholder-count="6"><button onClick="{{ g.open }}" style="display:flex;align-items:center;gap:12px;text-align:left;padding:12px 14px;border-radius:20px;border:{{ g.bd }};background:#fff;box-shadow:0 6px 18px rgba(40,50,140,.08);cursor:pointer;font-family:inherit;color:#18324F;min-width:0"><span style="flex:none;width:52px;height:52px;border-radius:16px;background:{{ g.nb }};color:{{ g.nf }};display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1.05"><span style="font-size:11px;font-weight:800;letter-spacing:.06em">DAY</span><b style="font-size:20px;font-weight:800">{{ g.n }}</b></span><span style="flex:1;min-width:0;display:flex;flex-direction:column;gap:3px"><b style="font-size:16px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ g.path }}</b><span style="font-size:14px;font-weight:600;color:#6B7A90;white-space:nowrap">{{ g.date }} · {{ g.km }}</span></span><span style="flex:none;white-space:nowrap;font-size:13px;font-weight:800;padding:5px 10px;border-radius:99px;background:{{ g.sb }};color:{{ g.sf }}">{{ g.st }}</span></button></sc-for></div>\n</sc-if>\n' + '<sc-if value="{{ sb2.plan }}" hint-placeholder-val="{{ false }}">')
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

rep('<input value="{{ f.v }}" onChange="{{ f.on }}" placeholder="" style="height:46px;border-radius:14px;border:1px solid #DCE0F7;background:#F8F9FF;padding:0 12px;font:600 15px \'Pretendard Variable\',Pretendard,sans-serif;color:#18324F;outline:none;min-width:0;"></label>', '<span style="display:flex;gap:8px;align-items:center"><input value="{{ f.v }}" onChange="{{ f.on }}" placeholder="" style="flex:1;height:46px;border-radius:14px;border:1px solid #DCE0F7;background:#F8F9FF;padding:0 12px;font:600 15px \'Pretendard Variable\',Pretendard,sans-serif;color:#18324F;outline:none;min-width:0;"><sc-if value="{{ f.isNote }}" hint-placeholder-val="{{ false }}"><button onClick="{{ pl2.lsave }}" style="flex:none;white-space:nowrap;height:46px;padding:0 18px;border:0;border-radius:14px;background:{{ pl2.lsBtnBg }};color:{{ pl2.lsBtnFg }};font:800 15px \'Pretendard Variable\',Pretendard,sans-serif;cursor:pointer">{{ pl2.lsBtnT }}</button></sc-if></span></label>')
rep('{{ dd2.lodge }}</b></span>', '{{ dd2.lodge }}</b><sc-if value="{{ dd2.hasLodgeSub }}" hint-placeholder-val="{{ false }}"><span style="font-size:13px;font-weight:600;color:#6B7A90;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ dd2.lodgeSub }}</span></sc-if></span>')
rep('<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><sc-for list="{{ pl2.sum }}"', '<div style="background:{{ pl2.lw.bg }};border-radius:20px;padding:14px 16px;display:flex;flex-direction:column;gap:8px"><span style="display:flex;align-items:center;gap:8px;font-size:16px;font-weight:800;color:{{ pl2.lw.fg }}"><span style="@@IC@@font-size:24px;color:{{ pl2.lw.fg }}">{{ pl2.lw.icon }}</span>{{ pl2.lw.title }}</span><sc-for list="{{ pl2.lw.rows }}" as="r" hint-placeholder-count="3"><button onClick="{{ r.go }}" style="display:flex;align-items:center;gap:10px;height:44px;padding:0 12px;border:0;border-radius:14px;background:rgba(255,255,255,.75);cursor:pointer;font-family:inherit;color:#18324F;text-align:left"><b style="flex:none;font-size:14px;color:#5B32D6">DAY {{ r.n }}</b><span style="flex:1;min-width:0;font-size:15px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{{ r.name }} <span style="font-size:13px;font-weight:600;color:#6B7A90">{{ r.date }}</span></span><span style="flex:none;white-space:nowrap;font-size:13px;font-weight:800;padding:4px 10px;border-radius:99px;background:{{ r.sb }};color:{{ r.sf }}">{{ r.st }}</span></button></sc-for></div>\n'.replace('@@IC@@', _ic) + '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px"><sc-for list="{{ pl2.sum }}"')
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
OLD = rep(PERSIST_OLD, "'bodyLog', 'expLog', 'noteLog', 'walk', 'wsrc', 'wStart', 'wPauseAt', 'wPausedMs', 'wDay', 'stageDate', 'dark', 'nfxDir', 'jc', 'wNoAuto', 'ntab', 'sub', 'dayN', 'lo', 'pd', 'sf', 'trm', 'jpBig', 'cur', 'ji', ", src=OLD)
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
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(dc)
shutil.copy(os.path.join(ROOT, 'design', 'v9', 'support.js'), os.path.join(OUT, 'support.js'))
(os.path.abspath(OUT) != ROOT) and shutil.copy(os.path.join(ROOT, 'image-slot.js'), os.path.join(OUT, 'image-slot.js'))
print('wrote', os.path.relpath(OUT, ROOT) + '/index.html', len(dc))
