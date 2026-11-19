# Starlit Camp - https://starlitcamp.github.io

- 한국어는 루트, 영어/일본어/스페인어는 `en/`, `ja/`, `es/` 폴더에 있습니다.
- 페이지는 `python3 _src/build.py` 로 생성합니다. 문구: `_src/strings.py`, 약관·방침 본문: `_src/legal/`.
- 게임 상태는 `games.js` 에서 플랫폼마다 한 줄로 바꿉니다 — `status`(Android·Google Play: soon / recruiting / testing / released),
  `ios`(iPhone·iPad: soon / testing + `testFlight` 공개 링크 / released + `appStore` 주소), `steam`(PC: dev / soon / wishlist / demo / released + `steamAppId`).
  그 플랫폼으로 내지 않는 게임은 `""`. 홈 카드의 플랫폼 태그, 게임 페이지의 버튼과 Android·iOS·Steam 안내가 따라 바뀝니다.
  사이트가 실행 중에 games.js 를 읽으므로 다시 빌드하지 않아도 바로 반영됩니다.
- 게임 안 '스탈릿캠프 게임' 목록은 `games.json`(빌드가 strings.py·games.js 로 만든다)을 읽습니다. 게임을 추가하거나 상태를 바꾸면 `python3 _src/build.py` 로 다시 만들어 올려 주세요.
- 친구 초대 링크(`invite/?g=<게임 id>&c=<코드>`)는 `invite/index.html` 한 장입니다(빌드가 만들지 않는 손으로 쓴 페이지, 4개 언어 문구가 안에 있음). 게임 이름·아이콘은 `games.json`, 스토어 주소·상태는 `games.js` 를 읽습니다. Android 는 Play 로 보내며 코드를 설치 참조로 넘기고, iOS 는 `appStore` 주소가 있을 때 코드 복사 뒤 App Store 를 엽니다.
- **사이트 규칙 — 마켓은 아이콘으로 표기**: 상태 태그와 안내 제목은 마켓 아이콘(`_src/market_icons.json`, Simple Icons CC0)으로,
  Google Play·App Store 링크는 공식 배지(`img/badges/googleplay_<언어>.png`, `appstore_<언어>.svg` — Google·Apple 배지 그대로, 색·글자 수정 금지)로,
  Steam 링크는 Steam 아이콘 + 글자 버튼으로. 배지·아이콘을 쓰는 페이지 아래에는 상표 고지(`.tm`)를 둡니다. 새 페이지도 `build.py` 의 `icon()` · `badge()` 를 쓰세요.
