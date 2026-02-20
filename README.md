# QA Testcase Writer 2file v6

> 7가지 커버리지를 자동 체크하는 빠른 테스트 케이스 생성 스킬

---

## 이 스킬은 무엇을 하나요?

요구사항 문서를 분석하여 **2개 파일**을 생성합니다.
7가지 커버리지 항목을 체크리스트로 검증하며, 빠르게 테스트 케이스를 작성해야 할 때 적합합니다.

---

## 출력 파일 (2개)

| 번호 | 파일명 | 용도 | TestRail 업로드 |
|------|--------|------|----------------|
| 1 | `[기능명]_테스트케이스.csv` | 테스트케이스 전체 | 가능 |
| 2 | `[기능명]_질문.md` | 불명확한 요구사항 질문 목록 | — |

---

## 어떤 상황에서 쓰나요?

- 빠르게 테스트 케이스 초안이 필요할 때
- 테스트 케이스 + 질문 목록만 있으면 충분할 때
- 반복적으로 많은 기능의 테스트 케이스를 작성해야 할 때

---

## 사용 방법

### 1단계: 스킬 설치

```bash
# 이 브랜치를 클론
git clone -b skill/qa-testcase-writer-2file-v6 https://github.com/taejin0618/skill.git

# Claude Code 스킬 디렉토리에 복사
cp SKILL.md ~/.claude/skills/qa-testcase-writer.md
```

### 2단계: Claude Code에서 요청

```
이 Figma 디자인으로 테스트 케이스 만들어줘
https://www.figma.com/file/abc123/login-page
```

### 3단계: 출력 파일 확인

`[기능명]_테스트케이스/` 폴더에 2개 파일이 생성됩니다.

---

## 자동으로 체크되는 7가지 커버리지

| 번호 | 커버리지 항목 |
|------|--------------|
| 1 | 기능 커버리지 (모든 UI 요소 동작) |
| 2 | 입력값 검증 (빈 값, 경계값, 특수문자, 이모지 등) |
| 3 | 날짜 입력 (역순, 잘못된 형식, 미래/과거 날짜) |
| 4 | 동작/상호작용 (더블클릭, 새로고침, 뒤로가기) |
| 5 | UX 피드백 (로딩, 성공 메시지, 다이얼로그) |
| 6 | 접근성 (키보드 탭 이동, 포커스, 스크린리더) |
| 7 | 데이터 상태 (0건, 1건, 다건, 대용량) |

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
skill/qa-testcase-writer-2file-v6/
├── SKILL.md                  # 스킬 정의 파일
├── scripts/
│   ├── validate_csv.py
│   ├── quality_check.py
│   └── testrail_upload_check.py
└── references/
    ├── input-validation-examples.md
    └── templates/
        └── questions-template.md
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
