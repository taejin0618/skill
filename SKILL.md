---
name: happy-case-extractor
description: >
  기존 CSV 테스트케이스 파일에서 Happy Case만 AI가 분류하여 추출하는 스킬.
  트리거: (1) "Happy Case만 추출해줘" (2) "Happy Path 케이스만 분리해줘"
  (3) "정상 케이스만 뽑아줘" (4) "CSV에서 Happy Case 추출"
  (5) "기존 테스트케이스에서 성공 케이스만" (6) "테스트케이스에서 오류 케이스 제거"
  입력: 기존 테스트케이스 CSV 파일 (TestRail 호환 7컬럼 형식)
  출력: [원본파일명]_happy.csv 파일 (Happy Case만 포함, 동일 7컬럼 형식)
---

# Happy Case 추출 스킬

기존 TestRail 호환 CSV 파일을 분석하여 **Happy Case(정상 성공 시나리오)만 추출**해
새 CSV 파일을 생성하는 후처리(extraction) 스킬이다.

AI(Claude)가 각 행의 Title, Steps, Expected Result를 직접 읽고 분류한 후,
Python 스크립트로 파일을 저장하고 검증한다.

## 핵심 원칙

1. **비파괴적 처리**: 원본 CSV 파일은 절대 수정하지 않는다.
2. **AI 주도 분류**: Claude가 각 행의 Title, Steps, Expected Result를 읽고 직접 판단한다.
3. **형식 완전 보존**: 추출된 케이스는 원본과 동일한 CSV 형식(7컬럼)을 유지하며, 셀 값을 수정하지 않는다.
4. **Section 구조 유지**: Happy Case가 속한 상위 Section 행도 함께 추출한다.
5. **TestRail 호환성**: 출력 파일은 TestRail에 바로 업로드 가능한 형식이어야 한다.

---

## 출력 파일 형식

### 형식: 기존과 동일한 7컬럼 TestRail 호환 CSV

```csv
"Section","Section Hierarchy","Title","Preconditions","Steps","Expected Result","Priority"
```

- 컬럼 구조: 원본과 동일 (추가/삭제 없음)
- 셀 값: 원본 그대로 (Preconditions, Steps, Expected Result 수정 없음)
- Priority: 원본 값 그대로 유지 (재분류 없음)
- 줄바꿈: 물리적 줄바꿈 방식 그대로 유지 (\n 이스케이프 변환 없음)
- 인코딩: UTF-8

### 파일명 규칙

**형식**: `[원본파일명]_happy.csv`

```
✅ 올바른 예:
- 원본: 로그인_테스트케이스.csv    → 출력: 로그인_테스트케이스_happy.csv
- 원본: 회원관리_testcase.csv     → 출력: 회원관리_testcase_happy.csv
- 원본: order-payment_tc.csv     → 출력: order-payment_tc_happy.csv
```

---

## Happy Case 분류 기준

### 판단 우선순위 (이 순서대로 체크)

```
1순위: Expected Result에 오류/에러/실패 패턴 있음? → EXCLUDE
2순위: Title에 오류/에러/실패/잘못된 키워드 있음? → EXCLUDE
3순위: Steps에 빈 값/잘못된 값/특수 입력 패턴 있음? → EXCLUDE
4순위: 위 3가지 해당 없음 → HAPPY
```

### Happy Case 시그널 (포함)

| 필드 | Happy 시그널 | 예시 |
|------|------------|------|
| Title | 유효한, 정상, 성공, 완료, 조회, 저장, 등록, 수정, 삭제, 이동 | "유효한 계정으로 로그인 성공" |
| Steps | 구체적 유효값 사용, 표준 사용 흐름 | `'test@example.com'` 입력 |
| Expected Result | 성공 메시지, 페이지 이동, 데이터 정상 표시, 로딩 완료 | "저장되었습니다 메시지 표시" |

### Error/Edge Case 시그널 (제외)

| 필드 | 제외 시그널 | 예시 |
|------|-----------|------|
| Title | 오류, 에러, 실패, 잘못된, 빈 값, 중복, 경계 | "잘못된 비밀번호로 로그인 실패" |
| Steps | 비워두고, 잘못된 형식, 허용되지 않는 값, 특수문자 | "이메일 입력란을 비워두고" |
| Expected Result | 오류 메시지, 에러 아이콘, 빨간 테두리, 접근 불가 | "올바르지 않습니다 메시지" |

> 💡 상세 기준: `references/happy-case-criteria.md` 참조
> 💡 분류 예시: `references/classification-examples.md` 참조

### 특수 케이스 처리

| 케이스 유형 | 처리 방법 |
|------------|---------|
| 삭제 확인 다이얼로그 | **HAPPY 포함** (정상 UX 플로우) |
| 취소 버튼 정상 이동 | **HAPPY 포함** (정상 사용 행동) |
| 관리자 권한으로 접근 | **HAPPY 포함** (유효 권한 사용) |
| 0건 조회 결과 | **EXCLUDE** (경계 상황) |
| 빈 목록 표시 | **EXCLUDE** (예외 상태) |
| 경계값(최대/최솟값) | **EXCLUDE** (Edge Case) |

---

## 작업 프로세스

### 1단계: 입력 파일 확인

```
사용자가 제공한 CSV 파일 경로를 확인한다.
□ 파일 존재 여부
□ 인코딩 확인 (UTF-8 필수)
□ 헤더 7컬럼 확인:
  "Section","Section Hierarchy","Title","Preconditions","Steps","Expected Result","Priority"
```

### 2단계: AI 분류 수행

CSV의 모든 행을 순서대로 읽으며 분류한다.

```
각 행에 대해:
1. Title이 비어있으면 → Section 행으로 표시 (분류 보류)
2. Title이 있으면:
   a. references/happy-case-criteria.md 기준 적용
   b. references/classification-examples.md 예시 참조
   c. HAPPY / EXCLUDE 판정 + 근거 메모
```

### 3단계: 분류 결과 요약 출력

```markdown
분류 결과:
| 행 번호 | Title (요약) | 분류 | 판단 근거 |
|---------|-------------|------|-----------|
| 3 | 유효한 계정으로 로그인 | HAPPY | Expected Result 성공 메시지 |
| 5 | 잘못된 비밀번호 입력 | EXCLUDE | Title 오류 키워드 |

요약:
- 전체 테스트케이스: N개
- Happy Case: N개
- 제외된 케이스: N개
```

### 4단계: 추출 스크립트 실행

```bash
python scripts/extract_happy_cases.py [입력_CSV_파일_경로]
```

스크립트 동작:
- Happy Case 행만 추출
- Section 행 처리 (Happy Case 있는 Section만 포함)
- `[원본파일명]_happy.csv` 생성

### 5단계: 검증 수행

```bash
# CSV 포맷 검증
python scripts/validate_csv.py [출력_파일_경로]

# TestRail 업로드 호환성 검증
python scripts/testrail_upload_check.py [출력_파일_경로]
```

### 6단계: 완료 보고

```
추출 완료:
- 입력: [원본파일명].csv (전체 N개)
- 출력: [원본파일명]_happy.csv (Happy Case N개)
- 추출률: N%
- TestRail 업로드 가능: O
```

---

## 레퍼런스

| 파일 | 용도 | 참조 시점 |
|------|------|-----------|
| `references/happy-case-criteria.md` | Happy/Error/Edge 분류 기준 상세 | 2단계 AI 분류 수행 시 |
| `references/classification-examples.md` | 실제 분류 예시 모음 | 판단 어려운 케이스 처리 시 |

---

## 최종 검증 체크리스트

```
□ 원본 파일이 수정되지 않았는가?
□ 출력 파일명이 [원본]_happy.csv 형식인가?
□ 출력 CSV가 동일한 7컬럼 구조인가?
□ 셀 값이 원본 그대로 유지되었는가? (수정/가공 없음)
□ Error/Edge Case가 포함되지 않았는가?
□ Happy Case가 속한 Section 구조가 올바르게 유지되었는가?
□ validate_csv.py 검증 통과?
□ testrail_upload_check.py 검증 통과?
```
