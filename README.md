# Happy Case Extractor

> 기존 CSV 테스트케이스에서 Happy Case만 AI가 분류하여 추출하는 스킬

---

## 이 스킬은 무엇을 하나요?

이미 작성된 TestRail 호환 CSV 파일을 분석하여 **Happy Case(정상 성공 시나리오)만 추출**해 새 CSV 파일을 생성합니다.
AI(Claude)가 각 행의 Title, Steps, Expected Result를 직접 읽고 분류합니다.
원본 파일은 절대 수정하지 않습니다.

---

## 출력 파일 (1개)

| 파일명 | 용도 | TestRail 업로드 |
|--------|------|----------------|
| `[원본파일명]_happy.csv` | Happy Case만 추출한 CSV | 가능 |

**파일명 예시**:
- 원본: `로그인_테스트케이스.csv` → 출력: `로그인_테스트케이스_happy.csv`
- 원본: `order-payment_tc.csv` → 출력: `order-payment_tc_happy.csv`

---

## 어떤 상황에서 쓰나요?

- 기존 전체 테스트케이스 CSV에서 스모크 테스트용 Happy Case만 빠르게 추출할 때
- 정상 플로우만 대상으로 회귀 테스트를 실행해야 할 때
- 오류/엣지 케이스를 제외하고 긍정 경로만 공유해야 할 때

---

## 사용 방법

### 1단계: 스킬 설치

```bash
# 이 브랜치를 클론
git clone -b skill/happy-case-extractor https://github.com/taejin0618/skill.git

# Claude Code 스킬 디렉토리에 복사
cp SKILL.md ~/.claude/skills/happy-case-extractor.md
```

### 2단계: Claude Code에서 요청

CSV 파일을 업로드하거나 경로를 지정한 후:

```
이 CSV에서 Happy Case만 추출해줘
```

또는:

```
로그인_테스트케이스.csv에서 Happy Path 케이스만 분리해줘
```

### 3단계: 출력 파일 확인

원본 파일과 같은 위치에 `_happy.csv` 파일이 생성됩니다.

---

## Happy Case 분류 기준

AI가 다음 우선순위로 각 케이스를 분류합니다:

| 우선순위 | 판단 기준 | 결과 |
|---------|----------|------|
| 1순위 | Expected Result에 오류/에러/실패 패턴 | 제외 |
| 2순위 | Title에 오류/실패/잘못된 키워드 | 제외 |
| 3순위 | Steps에 빈 값/잘못된 값/특수 입력 패턴 | 제외 |
| 4순위 | 위 3가지에 해당 없음 | 포함 (Happy) |

### 특수 케이스 처리

| 케이스 | 처리 |
|--------|------|
| 삭제 확인 다이얼로그 | 포함 (정상 UX 플로우) |
| 취소 버튼 정상 이동 | 포함 (정상 사용 행동) |
| 관리자 권한으로 접근 | 포함 (유효 권한 사용) |
| 0건 조회 결과 | 제외 (경계 상황) |
| 경계값 테스트 | 제외 (Edge Case) |

---

## 중요 사항

- **원본 파일 보존**: 원본 CSV는 절대 수정하지 않습니다
- **형식 완전 보존**: 7컬럼 구조, 셀 값, 줄바꿈 방식 원본 그대로 유지
- **Section 구조 유지**: Happy Case가 속한 상위 Section 행도 함께 포함
- **TestRail 호환**: 출력 파일은 TestRail에 바로 업로드 가능

---

## 파일 구조

```
skill/happy-case-extractor/
├── SKILL.md                  # 스킬 정의 파일
├── scripts/
│   ├── validate_csv.py
│   ├── quality_check.py
│   └── testrail_upload_check.py
└── references/
    ├── happy-case-criteria.md     # Happy Case 판단 기준
    └── classification-examples.md # 분류 예시
```
