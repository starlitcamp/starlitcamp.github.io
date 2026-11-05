# Starlit Camp - https://starlitcamp.github.io

- 한국어는 루트, 영어/일본어/스페인어는 `en/`, `ja/`, `es/` 폴더에 있습니다.
- 페이지는 `python3 _src/build.py` 로 생성합니다. 문구: `_src/strings.py`, 약관·방침 본문: `_src/legal/`.
- 게임 상태(출시 준비 중 / 테스터 모집 / 비공개 테스트 / 출시)는 `games.js` 의 `status` 한 줄로 바꿉니다.
  사이트가 실행 중에 games.js 를 읽으므로 다시 빌드하지 않아도 바로 반영됩니다.
