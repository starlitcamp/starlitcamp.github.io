# Starlit Camp - https://starlitcamp.github.io

- 한국어는 루트, 영어/일본어/스페인어는 `en/`, `ja/`, `es/` 폴더에 있습니다.
- 페이지는 `python3 _src/build.py` 로 생성합니다. 문구: `_src/strings.py`, 약관·방침 본문: `_src/legal/`.
- 게임 상태(출시 준비 중 / 테스터 모집 / 비공개 테스트 / 출시)는 `games.js` 의 `status` 한 줄로 바꿉니다.
  사이트가 실행 중에 games.js 를 읽으므로 다시 빌드하지 않아도 바로 반영됩니다.
- 게임 안 '스탈릿캠프 게임' 목록은 `games.json`(빌드가 strings.py·games.js 로 만든다)을 읽습니다. 게임을 추가하거나 상태를 바꾸면 `python3 _src/build.py` 로 다시 만들어 올려 주세요.
- 친구 초대 링크(`invite/?g=<게임 id>&c=<코드>`)는 `invite/index.html` 한 장입니다(빌드가 만들지 않는 손으로 쓴 페이지, 4개 언어 문구가 안에 있음). 게임 이름·아이콘은 `games.json`, 스토어 주소·상태는 `games.js` 를 읽습니다. Android 는 Play 로 보내며 코드를 설치 참조로 넘기고, iOS 는 `appStore` 주소가 있을 때 코드 복사 뒤 App Store 를 엽니다.
