# QA TestCase Writer 스킬 모음

> Claude Code용 QA 테스트 케이스 자동 생성 스킬 모음 저장소

Figma, Jira, Confluence, PDF, 웹사이트 URL 등 다양한 입력에서 TestRail 호환 CSV 테스트 케이스를 자동으로 생성합니다.

---

## 스킬 목록

각 스킬은 독립 브랜치로 관리됩니다. 상황에 맞는 스킬을 선택해 사용하세요.

### 테스트 케이스 생성 스킬

| 스킬 | 출력 파일 수 | 특징 | 브랜치 |
|------|------------|------|--------|
| Full QA Testcase Writer | 5개 | 가장 완전한 버전, 보안 테스트 CSV 분리 | `skill/full-qa-testcase-writer` |
| QA Testcase Writer 2file v6 | 2개 | 7가지 커버리지 체크, 빠른 작성 | `skill/qa-testcase-writer-2file-v6` |
| QA Testcase Writer 3file v6 | 3개 | 커버리지 검증 체크리스트 포함 | `skill/qa-testcase-writer-3file-v6` |
| QA Testcase Writer 4file v3 | 4개 | 리스크 분석 포함 | `skill/qa-testcase-writer-4file-v3` |
| Happy Testcase Writer | 1개 | 정상 플로우만, 39개 금지 키워드 자동 필터 | `skill/happy-testcase-writer` |

### Happy Case 처리 스킬

| 스킬 | 입력 | 특징 | 브랜치 |
|------|------|------|--------|
| Happy Case Extractor | 기존 CSV | AI 분류로 Happy Case만 추출 | `skill/happy-case-extractor` |
| Happy Case Filter | 기존 CSV | AI + 강화 키워드 이중 검증으로 필터링 | `skill/happy-case-filter` |

---

## 어떤 스킬을 선택할까?

- **처음 사용, 기능 전체 검증** → Full QA Testcase Writer
- **빠른 테스트 케이스 작성** → 2file v6
- **커버리지 문서도 필요** → 3file v6
- **위험도 분석까지 필요** → 4file v3
- **스모크 테스트 / 정상 경로만** → Happy Testcase Writer
- **기존 CSV에서 Happy Case 추출** → Happy Case Extractor
- **기존 CSV에서 엄격하게 필터링** → Happy Case Filter

---

## 스킬 설치 방법

각 브랜치의 README를 참고하세요.

---

## 공통 검증 스크립트

모든 스킬에는 다음 Python 검증 스크립트가 포함됩니다:

- `scripts/validate_csv.py` — CSV 포맷 검증
- `scripts/quality_check.py` — 품질 체크
- `scripts/testrail_upload_check.py` — TestRail 호환성 확인

---

## 라이센스

MIT License
