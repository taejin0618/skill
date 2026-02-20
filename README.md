# Full QA Testcase Writer

> 가장 완전한 QA 테스트 케이스 자동 생성 스킬 — UI/UX + 보안 테스트를 한 번에

---

## 이 스킬은 무엇을 하나요?

Figma, Jira, Confluence, PDF, 웹사이트 URL 등 다양한 요구사항 문서를 분석하여 **5개의 산출물**을 자동으로 생성합니다.
UI/UX 테스트케이스와 보안 테스트케이스를 별도 CSV로 분리하는 가장 포괄적인 버전입니다.

---

## 출력 파일 (5개)

| 번호 | 파일명 | 용도 | TestRail 업로드 |
|------|--------|------|----------------|
| 1 | `[기능명]_테스트케이스.csv` | UI/UX 테스트케이스 | 가능 |
| 2 | `[기능명]_보안테스트케이스.csv` | 보안 테스트케이스 (SQL Injection, XSS 등) | 가능 |
| 3 | `[기능명]_리스크분석.md` | 위험 항목, 발생 가능성, 영향도, 완화 전략 | — |
| 4 | `[기능명]_질문.md` | 불명확한 요구사항 질문 목록 | — |
| 5 | `[기능명]_체크리스트.md` | 커버리지 검증 체크리스트 | — |

---

## 어떤 상황에서 쓰나요?

- 새 기능을 처음 테스트할 때 (전체 커버리지 확보)
- 보안 테스트까지 함께 설계해야 할 때
- 리스크 분석 문서가 별도로 필요할 때
- QA 팀 전체가 공유하는 공식 테스트 케이스 작성 시

---

## 사용 방법

### 1단계: 스킬 설치

```bash
# 이 브랜치를 클론
git clone -b skill/full-qa-testcase-writer https://github.com/taejin0618/skill.git

# Claude Code 스킬 디렉토리에 복사
cp SKILL.md ~/.claude/skills/qa-testcase-writer.md
```

### 2단계: Claude Code에서 요청

```
이 Figma 디자인으로 테스트 케이스 만들어줘
https://www.figma.com/file/abc123/login-page
```

또는 파일 업로드 후:

```
이 기획서로 TestRail CSV 생성해줘
```

### 3단계: 출력 파일 확인

`[기능명]_테스트케이스/` 폴더에 5개 파일이 생성됩니다.

---

## 자동으로 커버되는 항목

- 모든 UI 요소의 정상/오류 동작
- SQL Injection, XSS, 비인증 접근, 권한 없는 접근 등 보안 테스트
- 입력값 경계값 테스트 (빈 값, 최대/최솟값, 특수문자)
- 날짜 역순, 잘못된 형식 등 날짜 입력 오류
- 더블클릭, 타임아웃, 대용량 데이터 등 네트워크/성능 케이스
- 리스크 항목 및 완화 전략
- 불명확한 요구사항 질문 목록

---

## 검증 스크립트

```bash
# CSV 포맷 검증
python scripts/validate_csv.py [파일명].csv

# 품질 체크 (커버리지, 우선순위 등)
python scripts/quality_check.py [파일명].csv

# TestRail 업로드 전 최종 검증
python scripts/testrail_upload_check.py [파일명].csv
```

---

## 파일 구조

```
skill/full-qa-testcase-writer/
├── SKILL.md                  # 스킬 정의 파일 (Claude Code에서 읽음)
├── scripts/
│   ├── validate_csv.py       # CSV 포맷 검증
│   ├── quality_check.py      # 품질 체크
│   └── testrail_upload_check.py  # TestRail 호환성 확인
└── references/
    ├── security-testcases.csv    # 보안 테스트 템플릿
    ├── edge-cases.md             # 엣지케이스 체크리스트
    ├── test-techniques.md        # 테스트 기법 가이드
    └── templates/
        ├── risk-analysis-template.md
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
