# 도카이도 모바일 앱 — 초기 개발

## 포함 기능
- 기존 루트 HTML/manifest/아이콘을 복사해 기존 웹 화면을 유지
- Capacitor 7 기반 Android 앱 설정
- 백그라운드 위치 플러그인 연결
- 네이티브 앱에서 걷기 기록 시작/일시정지/종료, 거리/시간/GPS 점 수 표시
- 위치 좌표를 기기 localStorage에 저장하고 JSON으로 내보내기/삭제

## 로컬 빌드
필요: Node.js 22+, Android Studio 및 Android SDK.
1. 저장소를 내려받고 `cd mobile`
2. `npm install`
3. 최초 1회 `npm run cap:add:android`
4. `npm run android` 후 Android Studio에서 실제 Galaxy 기기에 설치

## 주의사항
- 이 브랜치에는 아직 생성된 Android Gradle 프로젝트나 APK가 포함되지 않았습니다.
- 위치 권한, GPS, Android 13+ 알림 권한을 허용해야 백그라운드 기록이 작동할 수 있습니다.
- 화면 잠금 상태에서 30~60분 테스트가 필요합니다. 제조사 절전 정책, GPS 환경, OS 버전에 따라 중단되거나 정확도가 낮아질 수 있습니다.
- 현재 좌표 저장은 웹뷰 localStorage 기반입니다. 프로세스 강제 종료 후에도 확실하게 기록을 복구하는 기능은 보장하지 않습니다. 이를 위해서는 네이티브 서비스/로컬 DB로 저장 기능을 옮기는 후속 작업이 필요합니다.
- 경로 지도 렌더링은 아직 미구현이며, 현재는 JSON 내보내기를 지원합니다.
- Galaxy Watch9/Samsung Health 연동은 아직 포함되지 않았습니다.
- Google Maps 키나 외부 지도 API는 추가하지 않았습니다.
