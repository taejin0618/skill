# QA TestCase Writer 스킬 모음

> Claude Code용 QA 테스트 케이스 자동 생성 스킬 모음 저장소

Figma, Jira, Confluence, PDF, 웹사이트 URL 등 다양한 입력에서 TestRail 호환 CSV 테스트 케이스를 자동으로 생성합니다.

---

## 스킬 목록

각 스킬은 독립 브랜치로 관리됩니다. 상황에 맞는 스킬을 선택해 사용하세요.

### 테스트 케이스 생성 스킬

| 스킬 | 버전 | 출력 | 목적/적합한 상황 | 브랜치 |
|------|------|------|----------------|--------|
| QA Testcase Writer - Full | v1 | 5개 파일 | 보안 테스트 분리 + 리스크 분석이 필요한 완전한 QA | `skill/qa-testcase-full` |
| QA Testcase Writer - Standard | v1 | 4개 파일 | 리스크 분석 포함 표준 QA 테스트케이스 | `skill/qa-testcase-standard` |
| QA Testcase Writer - Lite | v1 | 3개 파일 | 커버리지 검증 체크리스트 포함 (기본 추천) | `skill/qa-testcase-lite` |
| QA Testcase Writer - Minimal | v1 | 2개 파일 | 빠른 테스트케이스 작성 (간소화 버전) | `skill/qa-testcase-minimal` |
| Happy Testcase Writer | v1 | 1개 파일 | 정상 플로우만 포함하는 Happy Path 전용 | `skill/happy-testcase-writer` |

### Happy Case 처리 스킬

| 스킬 | 버전 | 입력 | 목적/적합한 상황 | 브랜치 |
|------|------|------|----------------|--------|
| Happy Case Extractor | v1 | 기존 CSV | AI 분류로 Happy Case만 추출 | `skill/happy-case-extractor` |
| Happy Case Filter | v1 | 기존 CSV | AI + 강화 키워드 이중 검증으로 순수 필터링 | `skill/happy-case-filter` |

---

## 어떤 스킬을 선택할까?

```
보안 테스트 분리 필요? → QA Testcase Full
리스크 분석 필요?       → QA Testcase Standard
커버리지 검증 필요?     → QA Testcase Lite (기본 추천)
빠른 작성 필요?         → QA Testcase Minimal
정상 플로우만?          → Happy Testcase Writer
기존 CSV에서 추출?      → Happy Case Extractor
기존 CSV 엄격히 필터?   → Happy Case Filter
```

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
