# QA TestCase Writer

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

TestRail 호환 CSV 테스트 케이스를 자동으로 생성하는 Claude Code 스킬입니다.

---

## 소개

QA 엔지니어는 테스트 케이스 작성에 많은 시간을 소비합니다. 수동으로 작성하다 보면 다음과 같은 문제가 발생합니다:

- ⏱️ **시간 소모**: 한 기능당 테스트 케이스 작성에 수 시간 소요
- 🔍 **커버리지 누락**: 보안 테스트, 엣지케이스 등 중요한 시나리오 누락
- 📋 **포맷 오류**: TestRail CSV 포맷을 수동으로 작성하면서 발생하는 실수
- 🔄 **반복 작업**: 비슷한 테스트 케이스를 매번 새로 작성

**QA TestCase Writer**는 이러한 문제를 해결합니다:

✅ Figma, Jira, PDF 등 다양한 입력 형식에서 테스트 케이스 자동 생성
✅ TestRail에 직접 업로드 가능한 CSV 파일 생성
✅ 보안 테스트(SQL Injection, XSS 등) 자동 포함
✅ 리스크 분석, 질문 목록, 커버리지 체크리스트 자동 생성
✅ 검증 스크립트로 품질 보증

---

## 주요 기능

- ✅ **다양한 입력 형식 지원**
  Figma, Axure, Jira, Confluence, PDF, PPT, 웹사이트 URL 모두 사용 가능

- ✅ **TestRail 호환 CSV 자동 생성**
  복잡한 CSV 포맷을 신경 쓸 필요 없이 바로 TestRail에 업로드

- ✅ **UI/UX + 보안 테스트 분리**
  UI/UX 테스트케이스와 보안 테스트케이스를 별도 CSV로 관리

- ✅ **5가지 출력 파일**
  테스트 케이스 외에도 리스크 분석, 질문 목록, 체크리스트 제공

- ✅ **품질 검증 자동화**
  검증 스크립트로 CSV 포맷과 테스트 케이스 품질 자동 체크

---

## 빠른 시작

### 전제조건

- Claude Code CLI가 설치되어 있어야 합니다
- Python 3.8 이상 (검증 스크립트 사용 시)

### 설치

1. **저장소 클론**

```bash
git clone https://github.com/[username]/qa-testcase-writer.git
cd qa-testcase-writer
```

2. **Claude Code 스킬 디렉토리에 복사**

```bash
cp -r full_qa-testcase-writer ~/.claude/skills/
```

3. **Claude Code 재시작**

```bash
claude restart
```

### 첫 테스트 케이스 생성

Claude Code에서 다음과 같이 요청:

```
Figma URL https://www.figma.com/file/example로 테스트 케이스 만들어줘
```

5분 안에 5개 파일이 생성됩니다:

- `[기능명]_테스트케이스.csv`
- `[기능명]_보안테스트케이스.csv`
- `[기능명]_리스크분석.md`
- `[기능명]_질문.md`
- `[기능명]_체크리스트.md`

---

## 사용 예제

### 예제 1: Figma 디자인에서 테스트 케이스 생성

**입력**:
```
이 Figma 디자인으로 테스트 케이스 만들어줘
https://www.figma.com/file/abc123/login-page
```

**출력**: `로그인_테스트케이스.csv` 등 5개 파일 생성

---

### 예제 2: 실제 웹사이트에서 테스트 케이스 생성

**입력**:
```
이 웹사이트로 테스트 케이스 작성해줘
https://example.com/login
```

**출력**: `웹사이트_테스트케이스.csv` 등 5개 파일 생성

---

### 예제 3: 기획서(PDF/PPT)에서 테스트 케이스 생성

**입력**: 기획서.pdf 업로드 후
```
이 기획서로 TestRail CSV 생성
```

**출력**: `기획서_테스트케이스.csv` 등 5개 파일 생성

---

## 출력 파일 상세

| 번호 | 파일명 | 용도 | TestRail 업로드 |
|------|--------|------|----------------|
| 1 | `[기능명]_테스트케이스.csv` | UI/UX 테스트케이스 | ✅ 가능 |
| 2 | `[기능명]_보안테스트케이스.csv` | 보안 테스트케이스 | ✅ 가능 |
| 3 | `[기능명]_리스크분석.md` | 위험 항목 및 완화 전략 | - |
| 4 | `[기능명]_질문.md` | 불명확한 요구사항 질문 | - |
| 5 | `[기능명]_체크리스트.md` | 커버리지 검증 체크리스트 | - |

### 1. UI/UX 테스트케이스.csv 예시

```csv
"Section","Section Hierarchy","Title","Preconditions","Steps","Expected Result","Priority"
"로그인","","","","","","Highest"
"정상 케이스","로그인 > 정상 케이스","유효한 계정으로 로그인","1. 로그인 권한: 일반 사용자
2. 접근 경로: 메인 > 로그인
3. 테스트 계정: test@example.com / Pass1234!","1. 로그인 페이지 접속 (URL: /login)
2. 이메일 입력란에 'test@example.com' 입력
3. 비밀번호 입력란에 'Pass1234!' 입력
4. '로그인' 버튼 클릭","1. 대시보드 페이지로 이동 (URL: /dashboard)
2. 우측 상단에 'test@example.com' 표시
3. '로그인 성공' 토스트 메시지 표시","High"
"오류 케이스","로그인 > 오류 케이스","잘못된 비밀번호 입력","1. 회원가입 완료된 계정 존재
2. 올바른 이메일: test@example.com","1. 로그인 페이지 접속
2. 이메일 입력란에 'test@example.com' 입력
3. 비밀번호 입력란에 'WrongPass123!' 입력
4. '로그인' 버튼 클릭","1. 로그인 실패
2. '비밀번호가 일치하지 않습니다' 에러 메시지 표시
3. 비밀번호 입력란 초기화","High"
```

### 2. 보안테스트케이스.csv 예시

```csv
"Section","Section Hierarchy","Title","Preconditions","Steps","Expected Result","Priority"
"보안 테스트","","","","","","Highest"
"입력값 공격","보안 테스트 > 입력값 공격","SQL Injection 공격 차단","1. 로그인 페이지 접속","1. 이메일 입력란에 '' OR '1'='1' 입력
2. 비밀번호 입력란에 'password' 입력
3. '로그인' 버튼 클릭","1. SQL Injection 공격 차단됨
2. 로그인 실패 처리
3. 에러 메시지 표시 (DB 정보 미노출)","Highest"
"입력값 공격","보안 테스트 > 입력값 공격","XSS 공격 차단 (Script 태그)","1. 로그인 페이지 접속","1. 이메일 입력란에 '<script>alert(1)</script>' 입력
2. '로그인' 버튼 클릭","1. 스크립트 실행되지 않음
2. 입력값 이스케이프 처리
3. 페이지 정상 동작","Highest"
"인증/인가","보안 테스트 > 인증/인가","비로그인 사용자 페이지 직접 접근 차단","1. 로그아웃 상태
2. 인증 필요 페이지 URL 확보 (예: /mypage)","1. 브라우저 주소창에 인증 필요 페이지 URL 직접 입력
2. Enter 키 입력","1. 로그인 페이지로 리다이렉트
2. '로그인이 필요합니다' 메시지 표시","High"
```

### 3. 리스크분석.md 예시

```markdown
# 리스크 분석

요청 URL: https://www.figma.com/file/abc123/login-page

| 위험 항목 | 발생 가능성 | 영향도 | 완화 전략 |
|-----------|------------|--------|----------|
| 세션 탈취 | 중간 | 높음 | HTTPS 강제, HttpOnly 쿠키 사용 |
| 무차별 대입 공격 | 높음 | 중간 | 로그인 실패 5회 시 계정 잠금, CAPTCHA 적용 |
| SQL Injection | 낮음 | 매우 높음 | Prepared Statement 사용, 입력값 검증 |
```

### 4. 질문.md 예시

```markdown
# 불명확한 요구사항 질문

요청 URL: https://www.figma.com/file/abc123/login-page

## 높은 우선순위

1. 비밀번호 재설정 이메일 발송 시간 제한이 있나요? (예: 1일 1회)
2. 자동 로그인 유지 기간은 얼마인가요? (예: 30일)
3. 로그인 실패 시 계정 잠금 정책이 있나요?

## 중간 우선순위

4. 소셜 로그인(Google, Kakao 등) 지원 여부는?
5. 비밀번호 최소 길이 및 복잡도 요구사항은?
```

### 5. 체크리스트.md 예시

```markdown
# 커버리지 검증 체크리스트

## 필수 기능

- [x] 로그인 정상 케이스
- [x] 로그인 오류 케이스
- [x] 비밀번호 찾기
- [ ] 소셜 로그인 (요구사항 확인 필요)

## 보안 테스트

- [x] SQL Injection 차단
- [x] XSS 공격 차단
- [x] 비로그인 접근 차단

## 엣지케이스

- [x] 빈 값 입력
- [x] 공백만 입력
- [x] 더블클릭 중복 요청 방지
```

---

## 기술 구현

본 스킬은 다음 기술을 활용합니다:

### MCP 통합

- **Figma MCP**: Figma 디자인에서 Component, Text, Input 속성, Interactive 흐름 자동 추출
- **Atlassian MCP**: Jira/Confluence에서 이슈 설명, Acceptance Criteria, 첨부파일, 연결 이슈 추출
- **Playwright/Chrome-in-Chrome MCP**: 웹사이트 크롤링 및 UI 구성요소 분석

### 테스트 설계 방법론

- **경계값 분석** (Boundary Value Analysis)
- **동등 분할** (Equivalence Partitioning)
- **상태 전환 테스트** (State Transition Testing)
- **Nielsen의 UX 사용성 원칙** 기반 검증

### 품질 보증

- CSV 포맷 검증 스크립트 (TestRail 호환성)
- 테스트 케이스 품질 체크 스크립트
- 커버리지 검증 체크리스트

### 레퍼런스 자료

- `references/edge-cases.md` - 엣지케이스 체크리스트
- `references/test-techniques.md` - 테스트 기법 가이드
- `references/nielsen-heuristics.md` - UX 사용성 원칙
- `references/security-testcases.csv` - 보안 테스트 템플릿

---

## 검증 스크립트

생성된 CSV 파일을 검증할 수 있습니다:

```bash
# CSV 포맷 검증
python scripts/validate_csv.py [파일명].csv

# 품질 체크 (커버리지, 우선순위 등)
python scripts/quality_check.py [파일명].csv

# TestRail 업로드 전 최종 검증
python scripts/testrail_upload_check.py [파일명].csv
```

모든 검증을 통과하면 TestRail에 안전하게 업로드할 수 있습니다.

---

## FAQ

### 설정 관련

**Q1. MCP 연결 오류가 발생합니다**

A: Claude Code에서 MCP 서버가 활성화되어 있는지 확인하세요. `claude mcp list` 명령어로 Figma MCP, Atlassian MCP 상태를 확인할 수 있습니다.

**Q2. Python 스크립트 실행 시 권한 오류가 발생합니다**

A: 스크립트에 실행 권한을 부여하세요: `chmod +x scripts/*.py`

### 사용법 관련

**Q3. 생성된 테스트 케이스가 너무 적습니다**

A: 요구사항 문서에 상세한 정보가 부족할 수 있습니다. Figma의 경우 Component 설명, Jira의 경우 Acceptance Criteria를 상세히 작성하면 더 많은 테스트 케이스가 생성됩니다.

**Q4. 보안 테스트 케이스가 생성되지 않았습니다**

A: 보안 테스트는 별도 CSV 파일(`[기능명]_보안테스트케이스.csv`)로 분리됩니다. 파일을 확인하세요. 최소 3개 이상의 보안 테스트가 자동 포함됩니다.

### 고급 사용

**Q5. 커스텀 테스트 기법을 추가할 수 있나요?**

A: `references/test-techniques.md`와 `references/edge-cases.md` 파일을 수정하여 프로젝트 특화 테스트 기법을 추가할 수 있습니다. SKILL.md에서 이 레퍼런스를 참조합니다.

---

## 라이센스

본 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

## 기여

Issue 및 Pull Request를 환영합니다. 기여하기 전에 다음을 확인해주세요:

1. 버그 리포트는 재현 단계를 포함해주세요
2. 기능 제안은 사용 사례를 설명해주세요
3. PR은 테스트와 함께 제출해주세요

---

## 문의

문제가 발생하거나 질문이 있으시면 GitHub Issues를 이용해주세요.

---

## 관련 문서

- [SKILL.md](full_qa-testcase-writer/SKILL.md) - 상세한 스킬 가이드 및 작성 규칙
- [테스트 기법 가이드](full_qa-testcase-writer/references/test-techniques.md)
- [엣지케이스 체크리스트](full_qa-testcase-writer/references/edge-cases.md)
- [보안 테스트 템플릿](full_qa-testcase-writer/references/security-testcases.csv)

---

## 요구사항

- Claude Code CLI (최신 버전 권장)
- Python 3.8 이상 (검증 스크립트 사용 시)
- 지원되는 MCP 서버: Figma, Atlassian, Playwright, Chrome-in-Chrome

---

## 지원되는 입력 형식

| 형식 | MCP/도구 | 추출 내용 |
|------|---------|----------|
| Figma URL | Figma MCP | Component, Text, Input 속성, Interactive 흐름 |
| Axure URL | Playwright/Chrome-in-Chrome MCP | Widget Notes, Interaction, Dynamic Panel |
| Jira/Confluence | Atlassian MCP | 이슈 설명, AC, 첨부파일, 연결 이슈 |
| 웹사이트 URL | Playwright/Chrome-in-Chrome MCP | UI 구성요소, 라벨, 화면 전환 경로 |
| PDF/PPT/스크린샷 | 이미지 분석 | UI 구성요소, 라벨, 화면 전환 경로 |
