/*
  Starlit Camp — 게임 상태 설정 / Game status config
  ---------------------------------------------------
  status 한 줄만 바꾸면 사이트 전체(홈 카드 태그, 게임 페이지의 참여/다운로드 영역)가 바뀝니다.
    "soon"       출시 준비 중 (모집 안내 없음)
    "recruiting" 테스터 모집 중 (그룹 가입만 안내, 테스트 링크는 아직 없음)
    "testing"    비공개 테스트 중 (그룹 가입 → 참여 링크 → 설치 → 14일 유지)
    "released"   출시됨 (Google Play 스토어 버튼만 표시)
  appStore: iOS 출시 후 App Store 주소를 넣으면 App Store 버튼이 함께 표시됩니다.
  아래 { ... } 부분은 JSON 형식을 지켜 주세요 (_src/build.py 가 읽습니다).
*/
window.STARLIT_GAMES = /*CONFIG*/{
  "stellarbloom": {
    "status": "testing",
    "package": "com.quasarlab.stellarbloom",
    "group": "starlitcamp-testers",
    "appStore": ""
  },
  "wizardtower": {
    "status": "recruiting",
    "package": "com.starlitcamp.wizardtower",
    "group": "starlitcamp-testers",
    "appStore": ""
  }
}/*END*/;
