# 클로드 디자인 v2(design/v9/app.dc.html)를 기존 데이터·기능에 연결해 내보냄.
#  - 화면(마크업)은 디자인 파일 그대로. 시안용 요소(가짜 상태바·가짜 지도·예시 숫자)만 실제 것으로 교체.
#  - 데이터·기능은 기존 앱(index.html)의 로직을 그대로 가져와 씀.
#  - 사용: python3 build/build_v9.py [출력폴더(기본 new)]
import os, sys, re, shutil, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'design', 'v9', 'app.dc.html')
OUT = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else 'new')
dc = open(SRC, encoding='utf-8').read()
old = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
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
rep('padding:52px 0 200px', 'padding:calc(%s + 12px) 0 calc(%s + 200px)' % (SAT, SAB))
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
names = set(m.group(1).split(',')) | {'local_fire_department', 'thermostat', 'partly_cloudy_day', 'foggy', 'thunderstorm', 'umbrella', 'wb_twilight', 'delete', 'edit', 'close'}
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
         '<iframe src="{{ gmSrc }}" title="구글 지도" style="position:absolute;inset:0;width:100%;height:100%;border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>',
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
_compact = ('<sc-if value="{{ ctl.compact }}" hint-placeholder-val="{{ true }}">'
  '<div style="display:flex;align-items:center;gap:8px">'
  '<button onClick="{{ ctl.tog }}" style="flex:1;min-width:0;height:54px;display:flex;align-items:center;gap:10px;padding:0 14px 0 10px;border-radius:27px;border:1px solid rgba(255,255,255,.95);background:#fff;box-shadow:0 8px 20px rgba(40,50,140,.14);cursor:pointer;font-family:inherit;color:#18324F;text-align:left">'
  '<span style="flex:none;position:relative;width:34px;height:34px;border-radius:12px;background:#EDF0FF;display:grid;place-items:center"><span style="'+_ico+'font-size:20px;color:#3B5BDB">watch</span><i style="position:absolute;right:-3px;top:-3px;width:10px;height:10px;border-radius:50%;background:#2F9E44;border:2px solid #fff;animation:wpulse 1.6s ease-in-out infinite"></i></span>'
  '<span style="flex:1;min-width:0;font-size:14px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">와치 시작 대기</span>'
  '<span style="'+_ico+'font-size:22px;color:#8C96B0">expand_less</span></button>'
  '<button onClick="{{ start }}" style="flex:none;height:54px;padding:0 20px 0 14px;border:0;border-radius:27px;background:linear-gradient(135deg,#3B5BDB,#6C7FE8);color:#fff;font-size:16px;font-weight:800;display:flex;align-items:center;gap:6px;box-shadow:0 10px 22px rgba(59,91,219,.36);cursor:pointer;font-family:inherit"><span style="'+_ico+'font-size:24px;color:#fff">directions_walk</span>폰에서 시작</button>'
  '</div></sc-if>')
_full = _inner.replace('<div style="display:flex;align-items:center;gap:12px;padding:12px 14px', '<div onClick="{{ ctl.tog }}" style="cursor:pointer;display:flex;align-items:center;gap:12px;padding:12px 14px', 1)
_full = _full.replace('<button onClick="{{ watchStart }}"', '<button onClick="{{ ctl.demo }}"', 1)
dc = dc.replace(_m.group(0), '<sc-if value="{{ ctl.ready }}" hint-placeholder-val="{{ false }}">' + _compact + '<sc-if value="{{ ctl.open }}" hint-placeholder-val="{{ false }}">' + _full + '</sc-if></sc-if>')
rep('<span style="flex:none;height:46px;min-width:46px;padding:0 10px;border-radius:14px;background:{{ dn2.chipBg }}', '<span onClick="{{ dn2.goToday }}" style="cursor:pointer;flex:none;height:46px;min-width:46px;padding:0 10px;border-radius:14px;background:{{ dn2.chipBg }}')
# 일정 변경 시트: 누르면 실제 동작
_pi = dc.index('{{ p.bg }}'); _pb = dc.rindex('<button style="', 0, _pi)
dc = dc[:_pb] + '<button onClick="{{ p.run }}" style="' + dc[_pb + len('<button style="'):]

# ───────────────────────── 5. 로직: 기존 앱 로직 + 새 화면 값 ─────────────────────────
oa = old.index('<script type="text/x-dc"'); ob = old.index('>', oa) + 1; oe = old.index('</script>', ob)
OLD = old[ob:oe]
OLD = rep('  renderVals() {', '  oldVals() {', src=OLD)
OLD = rep('\n    return {\n      morePlaces:', '\n    return { _x: { dd, n, stage, reached, done, isToday, isPast, walked, remain, steps, mins, hcT, stationsDone, posKmF, eta, today, view, places, hcH, hcR, recLabel, recIso, iso: (() => { const q = new Date(); return q.getFullYear()+"-"+String(q.getMonth()+1).padStart(2,"0")+"-"+String(q.getDate()).padStart(2,"0"); })() },\n      morePlaces:', src=OLD)
OLD = rep("synced: v.synced || '' };", "synced: v.synced || '', sleep: v.sleepMin == null ? null : v.sleepMin, weight: v.weight == null ? null : v.weight };", src=OLD)
PERSIST_OLD = "'bodyLog', "
OLD = rep("if (this.dayInfo().diff < 0) return 0; ", "", src=OLD)  # 출발 전에도 걷기 상태(테스트) 허용
OLD = rep(PERSIST_OLD, "'bodyLog', 'expLog', 'noteLog', 'walk', 'wsrc', 'wStart', 'wPauseAt', 'wPausedMs', 'wDay', 'stageDate', 'dark', 'nfxDir', 'jc', 'wNoAuto', 'ntab', 'sub', 'dayN', 'lo', 'pd', 'sf', 'trm', 'jpBig', 'cur', 'ji', ", src=OLD)
na = dc.index('<script type="text/x-dc"'); nb = dc.index('>', na) + 1; ne = dc.index('</script>', nb)
NEWJS = open(os.path.join(HERE, 'v9_logic.js'), encoding='utf-8').read()
HEROS = sorted(os.listdir(os.path.join(ROOT, 'assets', 'hero')))
NEWJS = NEWJS.replace('__WIDE__', WIDE).replace('__HEROS__', json.dumps(HEROS))
i0 = NEWJS.index('  renderVals() {')
NINIT = NEWJS[:i0]
RV = NEWJS[i0:]
OLD = rep("  state = { theme: null,", "  state = { ...this.nInit(), theme: null,", src=OLD)
OLD = rep("  componentDidMount() {", "  componentDidMount() { try { window.addEventListener('popstate', () => this.hwBack()); } catch (e) {} try { if (this.state.stageDate !== this.todayIso()) this.setState({ stage: this.dayInfo().diff < 0 ? 0 : 0, stageDate: this.todayIso(), walk: null }); } catch (e) {} try { this._tk = setInterval(() => { if (this.state.walk === 'walking') { this._c = (this._c || 0) + 1; if (this.state.mode || this._c % 15 === 0) this.setState({ tick: Date.now() }); } if (this.state.walk !== 'walking' && this.state.walk !== 'paused' && (this._ac = (this._ac || 0) + 1) % 10 === 0) this.autoWatch(); }, 1000); setTimeout(() => this.autoWatch(), 4000); } catch (e) {}", src=OLD)
METH = '''
  autoWatch() { try {
    const S = this.state, iso = this.todayIso(); if (S.wNoAuto === iso) return;
    if (S.stageDate === iso && S.stage > 0) return;
    const h = S.hc && S.hc.days && S.hc.days[iso]; if (!h || !h.hourly || !S.hc.at || Date.now() - S.hc.at > 30 * 6e4) return;
    const n = new Date(), hr = n.getHours(), hv = h.hourly, cur = +hv[hr] || 0, prev = n.getMinutes() < 25 ? (+hv[hr - 1] || 0) : 0;
    if (cur + prev < 500) return;
    this.setState({ walk: 'walking', wsrc: 'watch', wStart: Date.now() - 5 * 6e4, wPausedMs: 0, wPauseAt: null, wDay: iso, stageDate: iso, stage: Math.max(1, S.stage || 0), toast: { a: '와치 걷기 감지', b: '기록을 시작했어요' } }); setTimeout(() => this.setState({ toast: null }), 4000);
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
MAP_JS = MAP_JS.replace("(D.me || (D.stops && D.stops[0] && D.stops[0].ll) || [35.62, 139.74])", "(D.logC || D.me || (D.stops && D.stops[0] && D.stops[0].ll) || [35.62, 139.74])")
ns = {'old': old}
ks = v8src.index('def old_script(marker):')
ke = v8src.index("KEEP.append(FS)") + len("KEEP.append(FS)")
exec(v8src[ks:ke], ns)
KEEP, FS = ns['KEEP'], ns['FS']
dc = dc.replace('</body>', MAP_JS + ''.join(KEEP) + '</body>', 1)

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(dc)
shutil.copy(os.path.join(ROOT, 'design', 'v9', 'support.js'), os.path.join(OUT, 'support.js'))
shutil.copy(os.path.join(ROOT, 'image-slot.js'), os.path.join(OUT, 'image-slot.js'))
print('wrote', os.path.relpath(OUT, ROOT) + '/index.html', len(dc))
