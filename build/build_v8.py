# 새 디자인(클로드 디자인 v8: design/v8/Tokaido Walk App.dc.html)을 기존 데이터·기능에 연결해 내보냄.
#  - 화면(마크업)은 디자인 파일 그대로. 시안용 요소(가짜 상태바·홈 바·가짜 지도)만 실제 것으로 교체.
#  - 데이터·기능은 기존 앱(build.py 결과 index.html)의 로직을 그대로 가져와 씀:
#    일정(엑셀)·위치/GPS·건강 동기화·날씨·저장/클라우드 백업·당겨서 새로고침 등.
#  - 사용: python3 build/build.py data/schedule.xlsx _  →  python3 build/build_v8.py [출력폴더(기본 new)]
import os, sys, re, shutil, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'design', 'v8', 'Tokaido Walk App.dc.html')
OUT = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else 'new')
dc = open(SRC, encoding='utf-8').read()
old = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()


def rep(a, b, cnt=1, src=None):
    global dc
    s = dc if src is None else src
    assert s.count(a) == cnt, (s.count(a), a[:120])
    s = s.replace(a, b)
    if src is None:
        dc = s
    return s


# ───────────────────────── 1. 화면 틀 ─────────────────────────
rep("box-shadow:0 30px 60px rgba(40,40,100,.18),0 0 0 10px #1B1C22", "")
rep("w:'760px', h:'860px', r:'28px'", "w:'100%', h:'100lvh', r:'0'")
rep("w:'390px', h:'844px', r:'44px'", "w:'100%', h:'100lvh', r:'0'")
WIDE = "(typeof window !== 'undefined' && window.innerWidth >= 640)"
rep("const F = !!this.props.fold || this.props.go==='flex'", "const F = " + WIDE)
rep("this.props.fold", WIDE, cnt=3)

# 시안용 가짜 상태바(14:20·신호·배터리) 제거 → 실제 폰 상태바 사용, 위쪽은 안전 영역만큼 띄움
i = dc.index('<b style="font-size:15px">14:20</b>')
a0 = dc.rindex('<div style="position:absolute;left:0;right:0;top:0;height:50px;', 0, i)
depth, k = 0, a0
while True:
    o, c = dc.find('<div', k), dc.find('</div>', k)
    if o != -1 and o < c:
        depth += 1; k = o + 4
    else:
        depth -= 1; k = c + 6
        if depth == 0:
            break
dc = dc[:a0] + dc[k:]
rep('padding:58px 20px 14px', 'padding:calc(env(safe-area-inset-top) + 18px) 20px 14px')
rep('height:98px;padding-top:52px;z-index:8;', 'height:calc(env(safe-area-inset-top) + 52px);padding-top:env(safe-area-inset-top);z-index:8;')

# 시안용 홈 바(화면 아래 검은 줄) 제거, 하단 메뉴는 기기 안전 영역 위로
rep('<i style="position:absolute;left:50%;bottom:8px;transform:translateX(-50%);width:134px;height:5px;border-radius:3px;background:#18324F;opacity:.85;z-index:11"></i>', '')
rep('width:{{ fr.navW }};bottom:22px;z-index:10;', 'width:{{ fr.navW }};bottom:calc(env(safe-area-inset-bottom) + 14px);z-index:10;')
# 머리글 문구·날씨를 실제 값으로
rep('<span style="font-size:13px;color:#4A5D78">도카이도 종주 · {{ todayN }}일째</span>', '<span style="font-size:13px;color:#4A5D78">{{ headSub }}</span>')
rep("font-size:18px;color:#E0861A;\">sunny</span>18°</span>", "font-size:18px;color:{{ wxNow.c }};\">{{ wxNow.icon }}</span>{{ wxNow.t }}</span>")

# 가짜 지도(타일 그림 + 그린 선 + 가짜 핀) → 실제 지도(Leaflet) 자리
def swap_maps():
    global dc
    n = 0
    while True:
        t = dc.find('<img src="https://tile.openstreetmap.org/')
        if t < 0:
            break
        a = dc.rindex('<span', 0, t)
        m = dc.index('<sc-for list="{{ mp.mk }}"', t)
        e = dc.index('</sc-for>', m) + len('</sc-for>')
        kind = ['home', 'sheet', 'tab'][n] if n < 3 else 'x'
        dc = dc[:a] + '<div data-v8map="' + kind + '" data-k="{{ mapKey }}" style="position:absolute;inset:0;z-index:0"></div>' + dc[e:]
        n += 1
    return n
print('maps swapped:', swap_maps())

# ───────────────────────── 2. 문서 머리 ─────────────────────────
head_shim = old[old.index('<script>(function(){var F=\'.image-slots.state.json\''):]
head_shim = head_shim[:head_shim.index('</script>') + 9]
rep('<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>도카이도 53의 쉼표</title>'
    '<meta name="theme-color" content="#DCE2FF"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes">'
    '<meta name="apple-mobile-web-app-status-bar-style" content="default">'
    '<link rel="manifest" href="/manifest.json"><link rel="icon" href="/icon-192.png"><link rel="apple-touch-icon" href="/icon-180.png">'
    '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'
    '<style>html,body{overscroll-behavior:none;-webkit-text-size-adjust:100%;overflow-x:hidden;touch-action:pan-y}[data-v8map] .leaflet-control-attribution{display:none}</style>'
    + head_shim)

# ───────────────────────── 3. 로직: 기존 앱 로직 + 새 화면 값 ─────────────────────────
oa = old.index('<script type="text/x-dc"'); ob = old.index('>', oa) + 1; oe = old.index('</script>', ob)
OLD = old[ob:oe]
# 기존 화면값 계산은 oldVals 로 이름만 바꿔 그대로 쓰고, 필요한 중간값을 밖으로 꺼냄
OLD = rep('  renderVals() {', '  oldVals() {', src=OLD)
OLD = rep('\n    return {\n      morePlaces:', '\n    return { _x: { dd, n, stage, reached, done, isToday, isPast, walked, remain, steps, mins, hcT, stationsDone, posKmF, eta, today, view, places },\n      morePlaces:', src=OLD)

na = dc.index('<script type="text/x-dc"'); nb = dc.index('>', na) + 1; ne = dc.index('</script>', nb)
NEW = dc[nb:ne]
ci = NEW.index('class Component extends DCLogic {')
NEWC = NEW[ci + len('class Component extends DCLogic {'):NEW.rindex('}')]

# 새 화면 상태: 기존 상태와 이름이 겹치는 것은 n 접두로 분리 (기존 저장값을 덮지 않도록)
s0 = NEWC.index('  state = (() => {'); s1 = NEWC.index('})();', s0) + len('})();')
st = NEWC[s0:s1]
st = st.replace('  state = (() => {', '  nInit() {', 1)[:-len('})();')] + '}'
for a, b in [("amt:'', cat:'식비'", "amt:'', ncat:'식비'"), ("exp:[{cat:'식비'", "nexp:[{cat:'식비'"), ("note:'', noteSaved", "nnote:'', noteSaved"),
             ("fxDir:'jk'", "nfxDir:'jk'"), ("view:11, ", ""), ("...(g==='past'?{view:8}:{}), ...(g==='future'?{view:13}:{}), ", ""), ("arr:2, ", ""), ("...(g==='done'?{arr:4}:{}), ", "")]:
    st = rep(a, b, src=st)
rv = NEWC[NEWC.index('  renderVals() {'):]
rv = rv.replace('  renderVals() {', '  renderVals() {\n    const O = this.oldVals(), X = O._x;', 1)

R = [
    # 역참 이름·거리: 기존 데이터(ST)
    (re.search(r"    const KO = \[.*?\];\n    const JP = \[.*?\];\n    const KM = \[.*?\];\n", rv, re.S).group(0),
     "    const KO = ST.map(t => t.ko.replace(/\\(.*\\)/, '')), JP = ST.map(t => t.jp), KM = ST.map(t => t.km);\n"),
    (re.search(r"    const E = \[.*?\];\n", rv).group(0), ""),
    ("const WD = ['일','월','화','수','목','금','토'], TODAY = 11, TR = {17:5.7, 24:27.3};",
     "const WD = ['일','월','화','수','목','금','토'], TODAY = X.today - 1, VW = X.view - 1, DIST = X.dd.dist, HT = window.TK_HOTELS || {};"),
    # 날짜별 구간: 기존 일정(PLAN·dayData)
    (re.search(r"    const day = i => \{.*?\n.*?\n", rv).group(0),
     "    const day = i => { const P = PLAN[i+1], s = P[0]+1, e = P[1]+1, d = new Date(2026,11,4+i), q = dayData(i+1), dist = q.dist, rest = s===e;\n"
     "      return { i, n:i+1, s, e, dist, rest, tr:q.trKm||0, date:(d.getMonth()+1)+'.'+d.getDate()+' ('+WD[d.getDay()]+')', path: rest ? KO[s-1]+' · 휴식' : KO[s-1]+' → '+KO[e-1], jp: rest ? JP[s-1] : JP[s-1]+' → '+JP[e-1] }; };\n"),
    ("const D = day(S.view), isT = S.view === TODAY;", "const D = day(VW), _df = this.dayInfo().diff, isT = VW === TODAY && X.isToday && _df >= 0 && _df <= 30;"),
    # 오늘 구간의 지점과 진행: 기존 단계(stage)·걸은 거리
    ("const STOPS = [19,20,21,22].map(n => ({ n, ko:KO[n-1], jp:JP[n-1], rel:+(KM[n-1]-KM[18]).toFixed(1) }));",
     "const STOPS = X.dd.stops.map((t,k) => ({ n:k, ko:t.ko.replace(/\\(.*\\)/, ''), jp:t.jp, rel:t.rel }));"),
    ("const arr = S.arr, done = arr >= 4, nxt = done ? null : STOPS[arr], pos = Math.max(12.4, STOPS[Math.min(arr,4)-1].rel), walked = done ? 20.2 : pos;",
     "const arr = Math.max(0, X.stage), done = X.done && X.stage > 0, nxt = done ? null : STOPS[Math.min(arr, STOPS.length-1)], walked = X.walked;"),
]
for a, b in R:
    rv = rep(a, b, src=rv)
# 20.2km(시안 숫자) → 실제 오늘 거리
rv = rep("name:'후지에다', jp:'藤枝', sub:'도착 · 20.2km 걸었어요'", "name:STOPS[STOPS.length-1].ko, jp:STOPS[STOPS.length-1].jp, sub:'도착 · '+DIST+'km 걸었어요'", src=rv)
rv = rep("walked:'20.2km'", "walked:DIST+'km'", src=rv)
rv = rv.replace('20.2', 'DIST')
R2 = [
    ("const past = k < arr, cur = k === arr, last = k === 3;", "const past = k < arr, cur = k === arr && !done, last = k === STOPS.length-1;"),
    ("note: past ? (k===0?'08:02 출발':k===1?'09:31 도착':k===2?'11:40 도착':'도착') : cur",
     "note: past ? (k===0?'출발':'지나옴'+(((S.passed||{})[X.iso]||{})[s.ko] ? ' · '+((S.passed||{})[X.iso]||{})[s.ko] : '')) : cur"),
    ("const past = S.view < TODAY, ids = [];", "const past = X.isPast, ids = [];"),
    ("const N = S.view < 30 ? day(S.view+1) : null;", "const N = VW < 30 ? day(VW+1) : null;"),
    ("const past = S.view < TODAY;", "const past = X.isPast;"),
]
for a, b in R2:
    rv = rep(a, b, src=rv)
# 지나는 곳: 기존 명소 데이터
SPm = re.search(r"    const SP = \[\n.*?\n    \];\n", rv, re.S).group(0)
rv = rep(SPm, "    const CI = { '역사유적':'museum', '신사·사찰':'temple_buddhist', '명물 음식':'restaurant', '자연·전망':'landscape', '공예·특산':'storefront' };\n"
         "    const SP = (X.places || []).map(p => { const c = (p.desc || '').split(' · ')[0]; return { ko:p.name, jp:p.q || '', at:p.km, icon: CI[c] || 'location_on', short:(p.desc || '').split(' · ').slice(1).join(' · ') || p.desc, desc:(p.long || p.desc || ''), ll:p.ll }; });\n", src=rv)
rv = rep("map: 'https://www.google.com/maps/dir/?api=1&travelmode=walking&destination='+encodeURIComponent(p.jp), open:",
         "map: 'https://www.google.com/maps/dir/?api=1&travelmode=walking&destination='+(p.ll ? p.ll[0]+','+p.ll[1] : encodeURIComponent(p.jp || p.ko)), open:", src=rv)
rv = rep("const passed = p.at <= walked, d = Math.abs(p.at - walked);", "const passed = X.isPast || (isT && p.at <= walked), d = Math.abs(p.at - (isT ? walked : 0));", src=rv)
rv = rep("const spI = S.sheet && S.sheet.type==='spot' ? S.sheet.i : 0, spN = SP.length;", "const spI = S.sheet && S.sheet.type==='spot' ? S.sheet.i : 0, spN = Math.max(1, SP.length);", src=rv)
rv = rep("const passedN = SP.filter(p => p.at <= walked).length;", "const passedN = SP.filter(p => X.isPast || (isT && p.at <= walked)).length;", src=rv)
# 숙소: 기존 숙소 목록(HOTELS)
LOm = re.search(r"    const lodgeOf = d => \{.*?\};\n", rv, re.S).group(0)
rv = rep(LOm, "    const lodgeOf = d => { const h = HT[d.n] || HT[String(d.n)] || null, conf = !!(h && h.ko), q = h && h.ll && !/^35\\.0,138\\.5$/.test(h.ll) ? h.ll : (h && (h.ja || h.en || h.ko)) || (JP[d.e-1]+'駅 ホテル');\n"
         "      return { when: (d.i===TODAY?'오늘':d.n+'일차')+' 숙소 · '+KO[d.e-1], name: conf ? h.ko : KO[d.e-1]+' · 숙소 미정', chip: conf?'예약 확정':'미정', chipBg: conf?'#E4F8EC':'#FFF3D8', chipFg: conf?'#16804A':'#8A5A0E',\n"
         "      facts:[{k:'도착 지점',v:KO[d.e-1]},{k:'지역',v:(h && h.town) || JP[d.e-1]},{k:'예약',v:conf?'확정':'미정'}], map:'https://www.google.com/maps/dir/?api=1&travelmode=walking&destination='+encodeURIComponent(q) }; };\n", src=rv)
# 지난 날 기록: 실제 건강 기록
rv = rep("facts: past ? [{k:'걸은 거리',v:(D.rest?0:D.dist-D.tr).toFixed(1)+'km'},{k:'걸음',v:D.rest?'—':f1(Math.round((D.dist-D.tr)*1330))},{k:'걸은 시간',v:D.rest?'—':Math.floor((D.dist-D.tr)/4.3)+':'+String(Math.round(((D.dist-D.tr)/4.3%1)*60)).padStart(2,'0')}]",
         "facts: past ? [{k:'걸은 거리',v:X.hcT ? (+X.hcT.km||0).toFixed(1)+'km' : '—'},{k:'걸음',v:X.hcT && X.hcT.steps ? f1(X.hcT.steps) : '—'},{k:'걸은 시간',v:X.hcT && X.hcT.min != null ? Math.floor(X.hcT.min/60)+':'+String(X.hcT.min%60).padStart(2,'0') : '—'}]", src=rv)
# 시간대별 걸음(7시~18시): 실제 기록
rv = rep("const hrs = [0,1820,2950,3100,2400,1200,3200,3150,0,0,0,0], mx = 3200;",
         "const hrs = Array.from({length:12},(x,k) => +((((X.hcT||{}).hourly)||{})[7+k] || 0)), mx = Math.max(1, ...hrs);", src=rv)
# 걸음·걸은 시간·누적
rv = rep("tiles: [{k:'걸음',v:'17,820',u:'걸음',icon:'steps',grad:'linear-gradient(135deg,#1C7ED6,#4DABF7)'},{k:'걸은 시간',v:'3:12',u:'시간',icon:'schedule',grad:'linear-gradient(135deg,#7048E8,#9775FA)'}],",
         "tiles: [{k:'걸음',v:f1(X.steps||0),u:'걸음',icon:'steps',grad:'linear-gradient(135deg,#1C7ED6,#4DABF7)'},{k:'걸은 시간',v:Math.floor((X.mins||0)/60)+':'+String((X.mins||0)%60).padStart(2,'0'),u:'시간',icon:'schedule',grad:'linear-gradient(135deg,#7048E8,#9775FA)'}],", src=rv)
rv = rep("const km = isT ? 167.8+walked : KM[D.e-1]; const stN = KO.slice(0,53).filter((x,k) => KM[k] <= km).length;",
         "const km = isT ? X.posKmF : X.isPast ? KM[D.e-1] : KM[D.s-1]; const stN = KO.slice(0,53).filter((x,k) => KM[k] <= km + .01).length;", src=rv)
rv = rep("const km = isT ? 167.8+walked : 167.8;", "const km = X.posKmF;", src=rv)
rv = rep("health: [{k:'평균 심박',v:'112bpm'},{k:'소모',v:'1,240kcal'},{k:'페이스',v:\"15'28\\\"/km\"}]",
         "health: (() => { const h = X.hcT || {}, pace = h.km > .3 && h.min ? h.min / h.km : 0; return [{k:'평균 심박',v:h.hr ? h.hr+'bpm' : '—'},{k:'소모',v:h.kcal ? f1(h.kcal)+'kcal' : '—'},{k:'페이스',v:pace ? Math.floor(pace)+\"'\"+String(Math.round(pace%1*60)).padStart(2,'0')+'\"/km' : '—'}]; })()", src=rv)
# 날짜 이동·도착 체크: 기존 동작
R3 = [
    ("prevO: S.view === 0 ? '.35' : '1', nextO: S.view === 30 ? '.35' : '1',", "prevO: VW === 0 ? '.35' : '1', nextO: VW === 30 ? '.35' : '1',"),
    ("prev: () => S.view > 0 && set({ view:S.view-1, sheet:null }), next: () => S.view < 30 && set({ view:S.view+1, sheet:null }), goToday: () => set({ view:TODAY, sheet:null }),",
     "prev: () => { O.prevDay(); set({ sheet:null }); }, next: () => { O.nextDayFn(); set({ sheet:null }); }, goToday: () => { O.goToday(); set({ sheet:null }); },"),
    ("check: () => S.arr < 4 && set({ arr:S.arr+1 }), undo: () => S.arr > 2 && set({ arr:S.arr-1 }), undoO: S.arr > 2 ? '1' : '.4',",
     "check: () => { if (isT && !done) O.advance(); }, undo: () => { if (isT && X.stage > 1) this.setState(s => ({ stage: Math.max(1, Math.min(s.stage, STOPS.length) - 1) })); }, undoO: isT && X.stage > 1 ? '1' : '.4',"),
    ("todayN: TODAY+1,", "todayN: TODAY+1, headSub: (() => { const df = this.dayInfo().diff; return df < 0 ? '도카이도 종주 · 출발까지 D-'+(-df) : df > 30 ? '도카이도 종주 · 완주' : '도카이도 종주 · '+(df+1)+'일째'; })(), wxNow: (() => { const w = S.wlive; if (!w || w.now == null) return { icon:'partly_cloudy_day', t:'—', c:'#8C96C2' }; const c = w.code, ic = c <= 1 ? 'sunny' : c <= 3 ? 'partly_cloudy_day' : c >= 51 && c <= 82 ? 'rainy' : 'cloud'; return { icon: ic, t: Math.round(w.now)+'°', c: ic==='sunny' ? '#E0861A' : ic==='rainy' ? '#1C7ED6' : '#8C96C2' }; })(), mapKey: VW+'|'+arr+'|'+((this.routeCache||{})[VW+1] ? 1 : 0),"),
    ("onScroll: e => { const c = e.currentTarget.scrollTop > 60;", "onScroll: e => { const c = e.currentTarget.scrollTop > 56;"),
]
for a, b in R3:
    rv = rep(a, b, src=rv)
rv = rep("    const F = " + WIDE, """    try { const q = dayData(VW+1), rc = (this.routeCache||{})[VW+1], iso = X.iso, tk = isT ? (((S.track||{})[iso])||[]).concat((((S.hc||{}).locs||{})[iso])||[]).sort((a,b) => a[2]-b[2]) : [];
      window.__v8 = { route: rc && rc.pts ? rc.pts : q.route, stops: q.stops.map((t,k) => ({ ll:t.ll, past: X.isPast || (isT && k < arr) })), trk: tk, me: isT && tk.length ? [tk[tk.length-1][0], tk[tk.length-1][1]] : null }; } catch (e) {}
    const F = """ + WIDE, src=rv)
rv = rep("q: QS[S.view % 3]", "q: QS[(VW+3) % 3]", src=rv)
rv = rep("when:(S.view+1===TODAY+1?'내일'", "when:(VW+1===TODAY+1?'내일'", src=rv)
assert 'S.view' not in rv, rv[rv.index('S.view') - 200:rv.index('S.view') + 100]
assert 'S.arr' not in rv, rv[rv.index('S.arr') - 200:rv.index('S.arr') + 100]
# 이름이 겹치는 상태(지출·메모·환율·카테고리)는 새 화면 전용 이름으로 (다음 단계에서 실제 기록과 연결)
for a, b in [("S.cat", "S.ncat"), ("set({ cat:c })", "set({ ncat:c })"), ("S.exp", "S.nexp"), ("exp:[...S.nexp", "nexp:[...S.nexp"),
             ("S.note", "S.nnote"), ("set({ note:e.target.value", "set({ nnote:e.target.value"), ("S.fxDir", "S.nfxDir"), ("set({ fxDir:", "set({ nfxDir:")]:
    rv = rv.replace(a, b)
# 마지막으로 보던 화면 전환(t, sheet 등)은 기존 상태와 겹치지 않음. 오늘 날짜(ISO)도 꺼내 줌
OLD = rep("today, view, places },", "today, view, places, iso: (() => { const q = new Date(); return q.getFullYear()+'-'+String(q.getMonth()+1).padStart(2,'0')+'-'+String(q.getDate()).padStart(2,'0'); })() },", src=OLD)
OLD = rep("  state = { theme: null,", "  state = { ...this.nInit(), theme: null,", src=OLD)
# 기존 클래스 끝에 새 메서드 추가
ce = OLD.rindex('}')
OLD = OLD[:ce] + '\n' + st + '\n' + rv.rstrip() + '\n' + OLD[ce:]

# 숙소 목록(HOTELS)을 전역으로
_hi = old.index('var HOTELS = ') + len('var HOTELS = ')
_ho, _hend = json.JSONDecoder().raw_decode(old[_hi:])
HOTELS = json.dumps(_ho, ensure_ascii=False)
dc = dc[:nb] + '\nwindow.TK_HOTELS = ' + HOTELS + ';\n' + OLD + dc[ne:]

# ───────────────────────── 4. 지도(Leaflet) + 기존 보조 기능 ─────────────────────────
MAP_JS = r"""<script>(function () {
  var TILE = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
  function pin(t, bg, fg, bd, s) { return '<div style="transform:translate(-50%,-100%);display:grid;place-items:center;width:' + s + 'px;height:' + s + 'px;border-radius:50% 50% 50% 0;rotate:-45deg;background:' + bg + ';border:2px solid ' + bd + ';box-shadow:0 4px 10px rgba(24,50,79,.3)"><b style="rotate:45deg;font:800 12px Pretendard,sans-serif;color:' + fg + '">' + t + '</b></div>'; }
  setInterval(function () {
    if (!window.L || !window.__v8) return;
    document.querySelectorAll('[data-v8map]').forEach(function (el) {
      var D = window.__v8, k = el.getAttribute('data-k') + '|' + (D.trk || '').length;
      if (!el._map) { try { el._map = L.map(el, { zoomControl: false, attributionControl: false, scrollWheelZoom: false }); L.tileLayer(TILE, { maxZoom: 18 }).addTo(el._map); el._lay = L.layerGroup().addTo(el._map); } catch (e) { return; } }
      if (el._k === k && el._w === el.clientWidth) return; el._k = k; el._w = el.clientWidth; el._lay.clearLayers();
      try { el._map.invalidateSize(); } catch (e) {}
      var pts = D.route || []; if (pts.length > 1) { L.polyline(pts, { color: '#fff', weight: 10, opacity: .9 }).addTo(el._lay); L.polyline(pts, { color: '#3B5BDB', weight: 6, opacity: .95 }).addTo(el._lay); }
      var tr = D.trk || []; if (tr.length > 1 && window.tkSeg) window.tkSeg(tr).forEach(function (r) { L.polyline(r.pts, r.m === 'v' ? { color: '#F08A24', weight: 5, dashArray: '2 9', lineCap: 'round' } : { color: '#7048E8', weight: 5 }).addTo(el._lay); });
      (D.stops || []).forEach(function (s, i, a) { var st = i === 0, en = i === a.length - 1; L.marker(s.ll, { icon: L.divIcon({ className: '', iconSize: [0, 0], html: pin(st ? 'A' : en ? 'B' : String(i), st ? '#18324F' : en ? '#7048E8' : s.past ? '#3B5BDB' : '#fff', st || en || s.past ? '#fff' : '#3B5BDB', st || en ? '#fff' : '#3B5BDB', st || en ? 30 : 24) }), zIndexOffset: st || en ? 300 : 200 }).addTo(el._lay); });
      if (D.me) L.circleMarker(D.me, { radius: 8, color: '#fff', weight: 3, fillColor: '#2F7CF6', fillOpacity: 1 }).addTo(el._lay);
      var b = (D.stops || []).map(function (s) { return s.ll; }).concat(pts); if (b.length) try { el._map.fitBounds(L.latLngBounds(b), { padding: [24, 24], maxZoom: 15 }); } catch (e) {}
    });
  }, 600);
})();</script>"""

# 기존 보조 스크립트 중 데이터·기능에 해당하는 것만 가져옴
def old_script(marker):
    i = old.index(marker); a = old.rindex('<script>', 0, i); e = old.index('</script>', i) + 9
    return old[a:e]
KEEP = [
    old_script("var URL_ = 'https://jmfvsusybouibqmdvtmy.supabase.co/functions/v1/tk-sync'"),  # 저장값 클라우드 백업/복원
    old_script('/* 위에서 아래로 당기면 새로고침'),                                             # 당겨서 새로고침
    old_script('window.tkSeg = function (pts)'),                                                   # 걸음/차량 구간 나누기
]
dc = dc.replace('</body>', MAP_JS + ''.join(KEEP) + '</body>', 1)

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(dc)
for f in ('support.js',):
    shutil.copy(os.path.join(ROOT, 'design', 'v8', f), os.path.join(OUT, f))
shutil.copy(os.path.join(ROOT, 'image-slot.js'), os.path.join(OUT, 'image-slot.js'))
print('wrote', os.path.relpath(OUT, ROOT) + '/index.html', len(dc))
