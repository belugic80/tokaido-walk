# 새 디자인(클로드 디자인 v8, design/v8/Tokaido Walk App.dc.html)을 /new/ 에 내보냄.
# 원본은 손대지 않고 아래 치환만 적용. 실제 데이터 연결은 이 파일에 단계별로 추가.
import os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'design', 'v8', 'Tokaido Walk App.dc.html')
OUT = os.path.join(ROOT, 'new')
dc = open(SRC, encoding='utf-8').read()

def rep(a, b, cnt=1):
    global dc
    assert dc.count(a) == cnt, (dc.count(a), a[:90])
    dc = dc.replace(a, b)

# 1) 폰/폴드 모형 테두리 제거 → 화면 가득
rep("box-shadow:0 30px 60px rgba(40,40,100,.18),0 0 0 10px #1B1C22", "")
rep("w:'760px', h:'860px', r:'28px'", "w:'100%', h:'100lvh', r:'0'")
rep("w:'390px', h:'844px', r:'44px'", "w:'100%', h:'100lvh', r:'0'")
# 2) 접힘 여부는 화면 폭으로 판단 (펼친 폴드 ≈ 820px, 일반 폰 ≈ 400px)
rep("const F = !!this.props.fold || this.props.go==='flex'", "const F = (typeof window !== 'undefined' && window.innerWidth >= 640)")
rep("this.props.fold", "(typeof window !== 'undefined' && window.innerWidth >= 640)", cnt=3)
# 3) 문서 머리: 앱 설정
rep('<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>도카이도 53의 쉼표</title><meta name="theme-color" content="#DCE2FF"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><link rel="manifest" href="/manifest.json"><link rel="icon" href="/icon-192.png"><link rel="apple-touch-icon" href="/icon-180.png"><script>window.addEventListener("resize",function(){})</script>')

os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(dc)
shutil.copy(os.path.join(ROOT, 'design', 'v8', 'support.js'), os.path.join(OUT, 'support.js'))
print('wrote new/index.html', len(dc))
