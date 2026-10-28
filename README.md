# tokaido-walk
## 수정하는 법
- 일정 원본: `data/schedule.xlsx`
- 사이트 다시 만들기: `python3 build/build.py data/schedule.xlsx index.html` (openpyxl 필요)
- `index.html`을 main에 올리면 Vercel이 자동 배포합니다.

## 삼성 헬스 연동 (HC Webhook → Supabase → 사이트)
- 받는 주소: `https://jmfvsusybouibqmdvtmy.supabase.co/functions/v1/hc-webhook` (헤더 `x-api-key`)
- 읽는 주소: `.../functions/v1/hc-read?from=YYYY-MM-DD&to=YYYY-MM-DD` (헤더 `x-read-key`)
- 열쇠 값은 Supabase `hc_config` 표에만 있음(저장소에 없음). 사이트는 `/#k=읽기열쇠`로 한 번 열면 폰에 기억.
- 함수 코드: `supabase/functions/`
