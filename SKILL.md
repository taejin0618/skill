---
name: happy-case-filter
description: >
  기존 CSV 테스트케이스에서 순수 Happy Case만 필터링하는 스킬.
  AI 분류 + 강화 키워드 자동 필터링을 병행하여 100% 순수 Happy Case만 남긴다.
  트리거: (1) "Happy Case만 필터링" (2) "순수 해피케이스만 남겨줘"
  (3) "테스트케이스 필터링" (4) "비-Happy 케이스 제거"
  (5) "CSV에서 오류/엣지 케이스 걸러줘"
  입력: 기존 테스트케이스 CSV 파일 (TestRail 호환 7컬럼 형식)
  출력: [원본파일명]_happy.csv 파일 (순수 Happy Case만 포함, 동일 7컬럼 형식)
---

# Happy Case 필터링 스킬

기존 TestRail 호환 CSV 파일을 분석하여 **순수 Happy Case(정상 성공 시나리오)만 필터링**해
새 CSV 파일을 생성하는 후처리(filtering) 스킬이다.

AI(Claude)가 각 행의 Section, Section Hierarchy, Title, Steps, Expected Result를 직접 읽고 분류한 후,
강화된 키워드 Python 스크립트로 이중 검증하여 원본 파일은 보존하고 새 파일로 저장한다.

## 핵심 원칙

1. **비파괴적 처리**: 원본 CSV 파일은 절대 수정하지 않는다. 항상 새 `_happy.csv` 파일 생성.
2. **AI 주도 분류**: Claude가 각 행의 Section, Section Hierarchy, Title, Steps, Expected Result를 읽고 직접 판단한다.
3. **형식 완전 보존**: 필터링된 케이스는 원본과 동일한 CSV 형식(7컬럼)을 유지하며, 셀 값을 수정하지 않는다.
4. **Section 구조 유지**: Happy Case가 속한 상위 Section 행도 함께 포함한다.
5. **TestRail 호환성**: 출력 파일은 TestRail에 바로 업로드 가능한 형식이어야 한다.
6. **순수성 보장**: 강화된 키워드 필터(Title 약 39개, Expected 약 20개, Edge 약 31개+5정규식, Steps 12패턴)로
   AI 분류 후에도 혼입될 수 있는 비-Happy 케이스를 이중 검증한다.
   Edge Case 키워드는 Section, Section Hierarchy, Title, Steps, Expected Result 전체 필드에 적용하여 완전 차단한다.

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

## ⛔ 절대 제외 체크리스트

### Title 금지 키워드

| 카테고리         | 금지 키워드                                                        |
| ---------------- | ------------------------------------------------------------------ |
| 오류/실패 명시   | 오류, 에러, 실패, error, fail                                      |
| 부정 입력 수식어 | 잘못된, 유효하지 않은, 올바르지 않은, 틀린                         |
| 빈 값            | 빈 값, 빈칸, 미입력, 입력하지 않, 입력 없이, 미선택                |
| 거부/차단        | 접근 거부, 권한 없음, 권한없음, 차단, 금지                         |
| 중복             | 중복, 이미 사용 중, 이미 존재, 재시도                              |
| 경계값           | 최댓값, 최솟값, 경계값, 경계                                       |
| 비정상 상태      | 불일치, 초과, 미만, 부족, 만료, 타임아웃, 비정상, 예외, 누락, 위반 |

### Expected Result 금지 키워드

| 금지 키워드                                              |
| -------------------------------------------------------- |
| 올바르지 않습니다, 오류 메시지, 에러 메시지, 오류가 발생 |
| 다시 시도, 재입력, 필수 입력, 입력해주세요, 필수 항목    |
| 빨간색 테두리, 붉은 테두리, 경고 아이콘, 오류 아이콘     |
| 403, 404, 500, 접근 불가, 페이지를 찾을 수 없습니다      |
| 실패, 거부, 유효하지 않, 경고 메시지                     |

### Steps 금지 패턴

| 패턴                    | 예시                               |
| ----------------------- | ---------------------------------- |
| 비워두고                | "이메일 입력란을 비워두고"         |
| 아무것도 입력하지 않    | "아무것도 입력하지 않고 버튼 클릭" |
| 잘못된 형식/값/데이터   | "잘못된 이메일 형식으로 입력"      |
| 허용되지 않는           | "허용되지 않는 특수문자 입력"      |
| 권한 없는 상태          | "권한 없는 상태로 메뉴 접근"       |
| 로그아웃 상태           | "로그아웃 상태에서 URL 직접 접속"  |
| `<script`               | "`<script>alert(1)</script>` 입력" |
| `' OR '`                | "`' OR '1'='1` 입력"               |
| 이모지                  | "이모지 문자 입력"                 |
| 존재하지 않는           | "존재하지 않는 계정으로 로그인"    |
| 만료된 토큰/세션/링크   | "만료된 토큰으로 API 호출"         |
| 삭제된 계정/데이터/파일 | "삭제된 계정으로 접근"             |

### Edge Case 금지 키워드

| 카테고리         | 금지 키워드                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| 특수 데이터      | 특수문자, 이모지, 공백만, 줄바꿈만, 한자, 아랍어                         |
| 비정상 상태      | 데이터 없음, 0건, 빈 목록, 연결 끊김                                     |
| 동시성           | 동시에, 중복 요청, 연속 클릭, 이중 제출                                  |
| 브라우저 동작    | 뒤로가기, 새로고침 후, 브라우저 닫기, 탭 전환                            |
| 세션/타임아웃    | 세션 만료, 타임아웃, 토큰 만료                                           |
| 글자수           | 최대 글자수, 자 초과, 자 미만                                            |
| 경계값 숫자 패턴 | N자 초과/미만/이상/이하, 딱 N자, 최대 N자, 최소 N자, N건/개/회 초과/미만 |
| 네트워크         | 네트워크 끊김, 오프라인                                                  |
| 보안             | XSS, SQL, 인젝션, 스크립트                                               |

---

## Happy Case 분류 기준

### 판단 우선순위 (이 순서대로 체크)

```
1순위: Expected Result에 오류/에러/실패 패턴 있음? → EXCLUDE
2순위: Title + Section + Section Hierarchy에 오류/에러/실패/잘못된 키워드 있음? → EXCLUDE
3순위: Steps에 빈 값/잘못된 값/특수 입력 패턴 있음? → EXCLUDE
4순위: 전체 필드(Title + Steps + Expected + Section + Section Hierarchy)에 Edge Case 키워드 있음? → EXCLUDE
5순위: 전체 필드에 경계값 숫자 패턴(N자 초과/미만 등) 있음? → EXCLUDE
6순위: 위 5가지 해당 없음 → HAPPY
```

### Happy Case 시그널 (포함)

| 필드            | Happy 시그널                                                 | 예시                          |
| --------------- | ------------------------------------------------------------ | ----------------------------- |
| Title           | 유효한, 정상, 성공, 완료, 조회, 저장, 등록, 수정, 삭제, 이동 | "유효한 계정으로 로그인 성공" |
| Steps           | 구체적 유효값 사용, 표준 사용 흐름                           | `'test@example.com'` 입력     |
| Expected Result | 성공 메시지, 페이지 이동, 데이터 정상 표시, 로딩 완료        | "저장되었습니다 메시지 표시"  |

### 특수 케이스 처리

| 케이스 유형          | 처리 방법                       |
| -------------------- | ------------------------------- |
| 삭제 확인 다이얼로그 | **HAPPY 포함** (정상 UX 플로우) |
| 취소 버튼 정상 이동  | **HAPPY 포함** (정상 사용 행동) |
| 관리자 권한으로 접근 | **HAPPY 포함** (유효 권한 사용) |
| 0건 조회 결과        | **EXCLUDE** (경계 상황)         |
| 빈 목록 표시         | **EXCLUDE** (예외 상태)         |
| 경계값(최대/최솟값)  | **EXCLUDE** (Edge Case)         |

> 💡 상세 기준: `references/happy-case-criteria.md` 참조
> 💡 분류 예시: `references/classification-examples.md` 참조

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
   a. references/happy-case-criteria.md 기준 적용 (강화 키워드 포함)
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

### 4단계: 필터 스크립트 실행

```bash
python scripts/filter_happy_cases.py [입력_CSV_파일_경로]
```

스크립트 동작:

- 강화된 키워드로 Happy/EXCLUDE 재분류 (Title 약 39개, Expected 약 20개, Edge 약 31개+5정규식, Steps 12패턴)
- **Edge Case 키워드는 Section + Section Hierarchy + Title + Steps + Expected Result 전체 필드를 대상으로 검사**
- **경계값 정규식 패턴으로 "N자 초과/미만/이상/이하", "딱 N자", "최대/최소 N자" 등 자동 감지**
- Section 행 처리 (Happy Case 있는 Section만 포함)
- `[원본파일명]_happy.csv` 신규 생성 (원본 보존)

### 5단계: 순수성 재확인

```
□ 스크립트 출력에서 제거된 케이스 목록 확인
□ 제거된 케이스가 모두 비-Happy인지 검토
□ AI 분류 결과와 스크립트 필터 결과 비교
□ 불일치 케이스가 있으면 사용자에게 보고
```

### 6단계: 검증 수행

```bash
# CSV 포맷 검증
python scripts/validate_csv.py [출력_파일_경로]

# TestRail 업로드 호환성 검증
python scripts/testrail_upload_check.py [출력_파일_경로]
```

### 7단계: 완료 보고

```
필터링 완료:
- 입력: [원본파일명].csv (전체 N개)
- 출력: [원본파일명]_happy.csv (순수 Happy Case N개)
- 제거된 비-Happy 케이스: N개
- 필터율: N%
- TestRail 업로드 가능: O
```

---

## 레퍼런스

| 파일                                    | 용도                                               | 참조 시점                  |
| --------------------------------------- | -------------------------------------------------- | -------------------------- |
| `references/happy-case-criteria.md`     | Happy/Error/Edge 분류 기준 상세 (강화 키워드 포함) | 2단계 AI 분류 수행 시      |
| `references/classification-examples.md` | 실제 분류 예시 모음                                | 판단 어려운 케이스 처리 시 |

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
□ filter_happy_cases.py 실행 후 제거된 케이스가 모두 비-Happy인지 확인?
□ AI 분류 결과와 스크립트 필터 결과가 일치하는지 확인?
```
