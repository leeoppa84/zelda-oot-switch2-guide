# 시간의 오카리나 공략 유지보수

- 이 폴더는 독립 Git 저장소임. 상위 `게임공략 만들기` 저장소에 파일을 추가하지 말 것.
- 원격: `https://github.com/leeoppa84/zelda-oot-switch2-guide.git`, 기본 브랜치 `main`.
- 대상은 2026년 Nintendo Switch 2 리메이크판임. N64·3DS·마스터 퀘스트 조건을 섞지 말 것.
- 작업 전 `README.md`, `docs/검증메모.md`, `git status --short`, 원격 변경을 확인하고 사용자 변경을 보존할 것.
- 본문·출처·메타데이터는 `src/content.py`, 기능은 `src/app.js`, 스타일은 `src/style.css`를 수정함. 생성물은 직접 수정하지 말 것.
- 출처는 별도 탭에 사이트별 접이식 목록으로 모음. 각 장 아래 출처·검증 문구를 반복하지 말 것. 항목별 근거는 원본과 `docs/sources.json`에 유지함.
- 기존 장·단계 ID와 저장 키 `zelda-oot-switch2:progress:v1`을 유지할 것.
- 수정 후 `python build.py`, `python verify.py`, `node --check dist/app.js` 실행함. 화면·기능 변경 시 해당 브라우저 동작과 모바일 폭도 확인함.
- 버전·수정일·변경 기록·QA를 일치시키고 생성된 `dist/`와 검토용 문서도 함께 커밋함.
- 커밋 전 `git diff --check`, `git diff --stat`, 스테이징 목록을 확인함. 비밀정보·무관한 파일·다운로드용 HTML을 포함하지 말 것.
- 저장소는 비공개로 생성함. GitHub Pages·블로그 게시·공개 전환은 별도 요청 범위를 확인할 것. 푸시 성공을 배포 완료로 표현하지 말 것.
