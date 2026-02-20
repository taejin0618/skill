# Happy Testcase Writer

> 정상 플로우만 포함하는 Happy Path 테스트 케이스 생성 스킬

---

## 이 스킬은 무엇을 하나요?

요구사항 문서를 분석하여 **정상 동작만 포함**하는 테스트 케이스 CSV 1개를 생성합니다.
39개의 금지 키워드 필터로 오류/엣지 케이스를 자동 제거하여 순수한 Happy Path 테스트 케이스만 작성합니다.

---

## 출력 파일 (1개)

| 번호 | 파일명 | 용도 | TestRail 업로드 |
|------|--------|------|----------------|
| 1 | `[기능명]_테스트케이스.csv` | Happy Path 테스트케이스 | 가능 |

질문.md 파일은 생성하지 않습니다. 정상 플로우에 집중하기 때문에 불명확한 요구사항 질문이 필요 없습니다.

---

## 어떤 상황에서 쓰나요?

- 스모크 테스트 (릴리즈 전 빠른 기능 확인)
- 긍정 경로만 검증하면 되는 회귀 테스트
- 데모나 시연을 위한 시나리오 검증
- 오류 케이스 없이 정상 흐름만 확인하고 싶을 때

---

## 사용 방법

### 1단계: 스킬 설치

```bash
# 이 브랜치를 클론
git clone -b skill/happy-testcase-writer https://github.com/taejin0618/skill.git

# Claude Code 스킬 디렉토리에 복사
cp SKILL.md ~/.claude/skills/happy-testcase-writer.md
```

### 2단계: Claude Code에서 요청

```
Happy Path 테스트 케이스 만들어줘
https://www.figma.com/file/abc123/login-page
```

또는:

```
정상 케이스만 테스트 케이스 작성해줘
```

### 3단계: 출력 파일 확인

`[기능명]_테스트케이스/` 폴더에 CSV 1개 파일이 생성됩니다.

---

## 자동 포함 (Happy Path)

| 항목 | 예시 |
|------|------|
| 모든 버튼 정상 동작 | 검색, 저장, 수정, 이동 |
| 유효한 입력값 입력 | 정상 이메일, 정상 비밀번호 |
| 페이지 정상 이동 | 로그인 성공 후 대시보드 이동 |
| 성공 메시지 표시 | "저장되었습니다" 토스트 |
| 데이터 정상 조회 | 목록 정상 표시 |

## 자동 제외 (39개 금지 키워드)

오류, 에러, 실패, 잘못된, 빈 값, 빈칸, 미입력, 접근 거부, 권한 없음, 중복, 경계값, 초과, 만료, 타임아웃 등

오류/엣지 케이스에 해당하는 테스트 케이스는 자동으로 제외됩니다.

---

## 커버리지 (자동으로 체크되는 항목)

- 기능 커버리지: 모든 UI 요소의 정상 동작
- UX 피드백: 로딩 인디케이터, 성공 메시지, 확인 다이얼로그
- 데이터 상태: 1건, 다건 데이터에서 정상 동작

---

## 검증 스크립트

```bash
# CSV 포맷 검증
python scripts/validate_csv.py [파일명].csv

# 품질 체크
python scripts/quality_check.py [파일명].csv

# TestRail 업로드 전 최종 검증
python scripts/testrail_upload_check.py [파일명].csv
```

---

## 파일 구조

```
skill/happy-testcase-writer/
├── SKILL.md                  # 스킬 정의 파일
├── scripts/
│   ├── validate_csv.py
│   ├── quality_check.py
│   └── testrail_upload_check.py
└── references/
    └── happy-case-criteria.md  # Happy Case 판단 기준
```

---

## 지원 입력 형식

| 형식 | 지원 여부 |
|------|----------|
| Figma URL | 지원 |
| Axure URL | 지원 |
| Jira / Confluence | 지원 |
| 웹사이트 URL | 지원 |
| PDF / PPT / 스크린샷 | 지원 |
