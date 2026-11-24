/*
  Starlit Camp — 게임 상태 설정 / Game status config
  ---------------------------------------------------
  플랫폼마다 상태 한 줄만 바꾸면 사이트 전체(홈 카드 태그, 게임 페이지의 버튼·참여/다운로드 안내)가 바뀝니다.
  그 플랫폼으로 내지 않는 게임은 "" 로 둡니다.

  status   Android (Google Play) — package: Play 패키지 이름, group: 테스터 Google 그룹
    "soon"       출시 준비 중 (모집 안내 없음)
    "recruiting" 테스터 모집 중 (그룹 가입만 안내, 테스트 링크는 아직 없음)
    "testing"    비공개 테스트 중 (그룹 가입 → 참여 링크 → 설치 → 14일 유지)
    "released"   출시됨 (Google Play 스토어 버튼)
  ios      iPhone·iPad (App Store)
    "soon"       출시 준비 중
    "testing"    TestFlight 공개 테스트 중 (testFlight 에 https://testflight.apple.com/join/... 공개 링크)
    "released"   출시됨 (appStore 에 App Store 주소)
  steam    PC (Steam) — steamAppId: Steam 앱 ID (스토어 페이지가 생기면 넣기)
    "dev"        개발 중
    "soon"       출시 준비 중
    "wishlist"   스토어 페이지 공개 (찜하기 버튼)
    "demo"       체험판 공개
    "released"   출시됨

  아래 { ... } 부분은 JSON 형식을 지켜 주세요 (_src/build.py 가 읽습니다).
*/
window.STARLIT_GAMES = /*CONFIG*/{
  "stellarbloom": {
    "status": "testing",
    "package": "com.quasarlab.stellarbloom",
    "group": "starlitcamp-testers",
    "ios": "soon",
    "appStore": "",
    "testFlight": "",
    "steam": "",
    "steamAppId": 0
  },
  "wizardtower": {
    "status": "released",
    "package": "com.starlitcamp.wizardtower",
    "group": "starlitcamp-testers",
    "ios": "soon",
    "appStore": "",
    "testFlight": "",
    "steam": "",
    "steamAppId": 0
  },
  "starspire": {
    "status": "",
    "package": "",
    "group": "",
    "ios": "",
    "appStore": "",
    "testFlight": "",
    "steam": "dev",
    "steamAppId": 0
  }
}/*END*/;
