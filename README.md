# QA Testcase Writer 4file v3

> 리스크 분석까지 포함한 테스트 케이스 생성 스킬

---

## 이 스킬은 무엇을 하나요?

요구사항 문서를 분석하여 **4개 파일**을 생성합니다.
테스트케이스 외에 리스크 분석 문서를 함께 작성하여 위험도 기반의 테스트 우선순위 결정이 가능합니다.

---

## 출력 파일 (4개)

| 번호 | 파일명 | 용도 | TestRail 업로드 |
|------|--------|------|----------------|
| 1 | `[기능명]_테스트케이스.csv` | UI/UX 테스트케이스 | 가능 |
| 2 | `[기능명]_리스크분석.md` | 위험 항목, 발생 가능성, 영향도, 완화 전략 | — |
| 3 | `[기능명]_질문.md` | 불명확한 요구사항 질문 목록 | — |
| 4 | `[기능명]_체크리스트.md` | 커버리지 검증 체크리스트 | — |

---

## 어떤 상황에서 쓰나요?

- 위험도 분석 기반으로 테스트 우선순위를 결정해야 할 때
- 금융, 의료, 결제 등 리스크 관리가 중요한 도메인
- QA 계획서에 리스크 분석 섹션이 필요할 때
- 보안 테스트 CSV는 불필요하고 리스크 문서만 필요할 때

---

## 사용 방법

### 1단계: 스킬 설치

```bash
# 이 브랜치를 클론
git clone -b skill/qa-testcase-writer-4file-v3 https://github.com/taejin0618/skill.git

# Claude Code 스킬 디렉토리에 복사
cp SKILL.md ~/.claude/skills/qa-testcase-writer.md
```

### 2단계: Claude Code에서 요청

```
이 Figma 디자인으로 테스트 케이스 만들어줘
https://www.figma.com/file/abc123/login-page
```

### 3단계: 출력 파일 확인

`[기능명]_테스트케이스/` 폴더에 4개 파일이 생성됩니다.

---

## 리스크 분석 파일 구성

리스크분석.md에 포함되는 항목:

| 항목 | 내용 |
|------|------|
| 위험 항목 | 잠재적인 버그, 취약점, 비즈니스 리스크 |
| 발생 가능성 | 낮음 / 중간 / 높음 |
| 영향도 | 낮음 / 중간 / 높음 / 매우 높음 |
| 완화 전략 | 구체적인 대응 방안 |

---

## 자동으로 체크되는 커버리지 항목

- 모든 UI 요소의 기능 동작
- 입력값 검증 (빈 값, 경계값, 특수문자)
- 날짜 입력 오류 케이스
- 더블클릭, 타임아웃, 대용량 데이터 처리
- 불명확한 요구사항 질문 정리
- 커버리지 체크리스트 검증

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
skill/qa-testcase-writer-4file-v3/
├── SKILL.md                  # 스킬 정의 파일
├── scripts/
│   ├── validate_csv.py
│   ├── quality_check.py
│   └── testrail_upload_check.py
└── references/
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
