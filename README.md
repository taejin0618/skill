# QA Testcase Writer 3file v6

> 커버리지 검증 체크리스트까지 포함한 테스트 케이스 생성 스킬

---

## 이 스킬은 무엇을 하나요?

요구사항 문서를 분석하여 **3개 파일**을 생성합니다.
테스트케이스 작성 후 커버리지 체크리스트 파일로 누락된 항목을 즉시 확인할 수 있습니다.
커버율 80% 이상을 목표로 합니다.

---

## 출력 파일 (3개)

| 번호 | 파일명 | 용도 | TestRail 업로드 |
|------|--------|------|----------------|
| 1 | `[기능명]_테스트케이스.csv` | 테스트케이스 전체 | 가능 |
| 2 | `[기능명]_질문.md` | 불명확한 요구사항 질문 목록 | — |
| 3 | `[기능명]_체크리스트.md` | 테스트 커버리지 검증 체크리스트 | — |

---

## 어떤 상황에서 쓰나요?

- 테스트 케이스 완성도를 문서로 증명해야 할 때
- 커버리지 검토가 필요한 공식 QA 릴리즈 시
- 팀 리뷰 때 커버리지 근거 자료가 필요할 때

---

## 사용 방법

### 1단계: 스킬 설치

```bash
# 이 브랜치를 클론
git clone -b skill/qa-testcase-writer-3file-v6 https://github.com/taejin0618/skill.git

# Claude Code 스킬 디렉토리에 복사
cp SKILL.md ~/.claude/skills/qa-testcase-writer.md
```

### 2단계: Claude Code에서 요청

```
이 Figma 디자인으로 테스트 케이스 만들어줘
https://www.figma.com/file/abc123/login-page
```

### 3단계: 출력 파일 확인

`[기능명]_테스트케이스/` 폴더에 3개 파일이 생성됩니다.

---

## 자동으로 체크되는 커버리지 항목

- 기능 커버리지 (모든 버튼, 입력란, 드롭다운, 체크박스 등)
- 입력값 검증 (빈 값, 경계값, 특수문자, 이모지, 한글/영문/숫자 혼합)
- 날짜 입력 (역순, 잘못된 형식, 미래/과거 날짜, 오늘 날짜)
- 동작/상호작용 (더블클릭, 새로고침, 뒤로가기, 필수 입력 누락 제출)
- UX 피드백 (로딩 인디케이터, 성공 메시지, 확인 다이얼로그)
- 접근성 (키보드 탭 이동, 포커스, 스크린리더)
- 데이터 상태 (0건, 1건, 다건, 대용량)

체크리스트.md에서 각 항목의 커버 여부를 확인하고 누락된 테스트케이스를 즉시 파악할 수 있습니다.

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
skill/qa-testcase-writer-3file-v6/
├── SKILL.md                  # 스킬 정의 파일
├── scripts/
│   ├── validate_csv.py
│   ├── quality_check.py
│   └── testrail_upload_check.py
└── references/
    └── templates/
        ├── questions-template.md
        └── checklist-template.md
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
