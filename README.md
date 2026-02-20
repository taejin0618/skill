# Happy Case Filter

> AI + 강화 키워드 이중 검증으로 순수 Happy Case만 필터링하는 스킬

---

## 이 스킬은 무엇을 하나요?

이미 작성된 TestRail 호환 CSV 파일을 분석하여 **순수 Happy Case만 필터링**해 새 CSV 파일을 생성합니다.
AI(Claude) 분류 후 강화 키워드 스크립트로 이중 검증하여, Extractor보다 더 엄격하게 비-Happy 케이스를 제거합니다.
원본 파일은 절대 수정하지 않습니다.

---

## 출력 파일 (1개)

| 파일명 | 용도 | TestRail 업로드 |
|--------|------|----------------|
| `[원본파일명]_happy.csv` | 순수 Happy Case만 필터링한 CSV | 가능 |

**파일명 예시**:
- 원본: `로그인_테스트케이스.csv` → 출력: `로그인_테스트케이스_happy.csv`
- 원본: `회원관리_testcase.csv` → 출력: `회원관리_testcase_happy.csv`

---

## 어떤 상황에서 쓰나요?

- Happy Case Extractor보다 더 엄격하게 필터링해야 할 때
- 오류/엣지 케이스가 조금이라도 혼입되면 안 되는 경우
- 최고의 순수성이 필요한 스모크 테스트 세트 구성 시
- 보안/품질 기준이 엄격한 프로젝트의 Happy Path 테스트

---

## Extractor와의 차이점

| 항목 | Happy Case Extractor | Happy Case Filter |
|------|---------------------|-------------------|
| 분류 방법 | AI 분류만 | AI 분류 + 강화 키워드 이중 검증 |
| 필터 강도 | 일반 | 강화 (더 엄격) |
| 검증 필드 | Title, Steps, Expected | Section, Section Hierarchy, Title, Steps, Expected 전체 |
| 순수성 | 높음 | 매우 높음 |

---

## 사용 방법

### 1단계: 스킬 설치

```bash
# 이 브랜치를 클론
git clone -b skill/happy-case-filter https://github.com/taejin0618/skill.git

# Claude Code 스킬 디렉토리에 복사
cp SKILL.md ~/.claude/skills/happy-case-filter.md
```

### 2단계: Claude Code에서 요청

CSV 파일을 업로드하거나 경로를 지정한 후:

```
이 CSV에서 Happy Case만 필터링해줘
```

또는:

```
비-Happy 케이스 제거하고 순수 Happy Case만 남겨줘
```

### 3단계: 출력 파일 확인

원본 파일과 같은 위치에 `_happy.csv` 파일이 생성됩니다.

---

## 이중 검증 시스템

### 1단계: AI 분류
Claude가 Section, Title, Steps, Expected Result를 읽고 Happy/비-Happy를 직접 판단합니다.

### 2단계: 강화 키워드 검증

| 검증 대상 | 금지 키워드 수 |
|----------|--------------|
| Title 금지 키워드 | 약 39개 |
| Expected Result 금지 키워드 | 약 20개 |
| Edge Case 키워드 (전체 필드 적용) | 약 31개 + 정규식 5개 |
| Steps 금지 패턴 | 12가지 패턴 |

Edge Case 키워드는 Section, Section Hierarchy, Title, Steps, Expected Result 전체 필드에 적용하여 완전 차단합니다.

---

## 중요 사항

- **원본 파일 보존**: 원본 CSV는 절대 수정하지 않습니다
- **형식 완전 보존**: 7컬럼 구조, 셀 값, 줄바꿈 방식 원본 그대로 유지
- **Section 구조 유지**: Happy Case가 속한 상위 Section 행도 함께 포함
- **TestRail 호환**: 출력 파일은 TestRail에 바로 업로드 가능

---

## 파일 구조

```
skill/happy-case-filter/
├── SKILL.md                  # 스킬 정의 파일
├── scripts/
│   ├── validate_csv.py
│   ├── quality_check.py
│   └── testrail_upload_check.py
└── references/
    └── happy-case-criteria.md  # Happy Case 판단 기준 및 금지 키워드 목록
```
