---
name: api-e2e-test-generator
description: >
  E2E API 테스트 코드 생성기. 다단계 시나리오, CRUD 플로우, 교차 시스템(App↔Admin) 검증, 멀티 환경 지원.
  초보자 친화적 pytest + requests 기반. Swagger/OpenAPI 또는 수동 입력으로 생성.
  트리거: (1) "E2E API 테스트 만들어줘" (2) "CRUD 테스트 코드 작성" (3) "App에서 Admin 교차 검증 테스트"
  (4) "회원가입 플로우 테스트" (5) "다단계 API 시나리오 테스트" (6) "멀티 환경 API 테스트"
  (7) "E2E test code" (8) "cross-system API test" (9) "API 시나리오 테스트 코드 만들어줘"
  (10) "App API 테스트" (11) "Admin API 검증". 단순 단일 엔드포인트 테스트는 api-test-generator 스킬 사용.
  이 스킬은 여러 API를 순차 호출하거나, 두 시스템 간 데이터 동기화를 검증하거나, CRUD 전체 흐름을
  테스트해야 할 때 사용한다. "API 테스트"라는 키워드가 나오면 단일 vs E2E 중 적절한 스킬을 판단하라.
---

# API E2E Test Generator

Swagger/OpenAPI 명세 또는 수동 입력으로 다단계 E2E API 테스트 코드를 생성한다.

## 핵심 철학: 극단적 단순화

```
목표: QA 초보자도 1-2주 학습으로 E2E API 테스트 작성 가능
초보자 친화도: 5/5
필요 지식: Python 기초 + requests + pytest assert만
```

## 입력 방식

### 방식 1: Swagger/OpenAPI 자동 분석
Swagger 파일 업로드 시 엔드포인트 추출 → 시나리오별 테스트 코드 생성.

### 방식 2: 수동 정보 입력
API 기본 URL, 엔드포인트, HTTP 메서드, 요청/응답 구조를 사용자가 제공.

### 방식 3: 기존 프로젝트 참고
기존 conftest.py나 테스트 코드가 있으면 해당 패턴에 맞춰 생성.

## 절대 원칙 (Always Do)

1. **requests 라이브러리** 사용
2. **Step 1/2/3 한글 주석**으로 단계 구분 — `# Step 1: 설명` + `print("\nStep1: 설명")` 형식
3. **print() 로깅** — 모든 요청/응답을 `[REQUEST]`, `[RESPONSE]`, `[BODY]` 태그로 출력
4. **직접 assert** 사용 — 검증 함수 만들지 않음
5. **f-string으로 URL** 직접 생성
6. **친절한 에러 메시지** — assert 실패 시 힌트 포함 (예: `힌트: 401=토큰만료`)
7. **상세한 주석** — 한국어 docstring + Step 주석

## 엄격한 금지 (Never Do)

1. conftest.py의 `app_token`, `admin_cookies` auth fixture 외 pytest fixtures 사용 금지
2. 별도 파일(utils.py, helpers.py) 생성 금지 — conftest.py 하나만 사용
3. logging 모듈 사용 금지
4. 별도 검증 함수 생성 금지
5. 클래스 기반 테스트 금지 — 함수만 사용

## 테스트 유형 판단 기준

사용자 요청에 따라 적절한 템플릿을 선택한다. 판단 불가 시 사용자에게 질문.

| 사용자 요청 키워드 | 테스트 유형 | 참조 템플릿 |
|-------------------|------------|------------|
| "단일 API 테스트", "GET/POST 테스트", "엔드포인트 테스트" | 단일 엔드포인트 | `references/templates/single-endpoint.md` |
| "CRUD 테스트", "추가/수정/삭제", "장바구니 플로우" | CRUD 라이프사이클 | `references/templates/e2e-crud-flow.md` |
| "App→Admin", "교차 검증", "동기화 확인" | 교차 시스템 검증 | `references/templates/e2e-cross-system.md` |
| "회원가입 플로우", "전체 시나리오", "다단계 테스트" | 전체 라이프사이클 | `references/templates/e2e-full-lifecycle.md` |

각 템플릿 파일을 읽고 프로젝트에 맞게 `[수정]` 표시된 부분을 변경하여 코드를 생성한다.

## 프로젝트 구조

```
project/
├── conftest.py              # 환경 설정 (URL, 인증, 헤더)
├── pytest.ini               # pytest 설정
├── requirements.txt         # 의존성
├── report/                  # HTML 리포트 (자동 생성)
└── tests/
    └── e2e/
        ├── [기능그룹_1]/
        │   ├── test_tc_1.py
        │   ├── test_tc_2.py
        │   └── ...
        └── [기능그룹_2]/
            ├── test_tc_26.py
            └── ...
```

conftest.py 템플릿은 `references/templates/conftest-multi-env.md` 참조.

## conftest.py 핵심 구조

```python
import os
import datetime
import pytest
import requests

ENV = os.environ.get("ENV", "dev")  # dev 또는 stg

if ENV == "stg":
    APP_BASE_URL    = "https://stg-api.example.com"
    ADMIN_BASE_URL  = "https://stg-admin-api.example.com"
    APP_EMAIL       = "test@example.com"
    APP_PASSWORD    = "Password123!"
    ADMIN_USERNAME  = "admin"
    ADMIN_PASSWORD  = "AdminPass123!"
else:  # dev (기본값)
    APP_BASE_URL    = "https://dev-api.example.com"
    ADMIN_BASE_URL  = "https://dev-admin-api.example.com"
    APP_EMAIL       = "dev@example.com"
    APP_PASSWORD    = "DevPass123!"
    ADMIN_USERNAME  = "dev_admin"
    ADMIN_PASSWORD  = "DevAdminPass123!"

COMMON_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 로그인 Fixture (파일당 1번만 실행 — scope=module)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@pytest.fixture(scope="module")
def app_token():
    """App 로그인 토큰 — 파일당 1번만 발급"""
    res = requests.post(
        f"{APP_BASE_URL}/auth",
        json={"email": APP_EMAIL, "password": APP_PASSWORD, "remember": True},
        headers=COMMON_HEADERS
    )
    assert res.status_code == 200, f"App 로그인 실패: {res.status_code}"
    return res.json()["accessToken"]

@pytest.fixture(scope="module")
def admin_cookies():
    """Admin 로그인 쿠키 — 파일당 1번만 발급"""
    res = requests.post(
        f"{ADMIN_BASE_URL}/admin/auth",
        json={"name": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
        headers=COMMON_HEADERS
    )
    assert res.status_code == 200, f"Admin 로그인 실패: {res.status_code}"
    return res.cookies.get_dict()

def pytest_configure(config):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    config.option.htmlpath = f"report/test_report_{ts}.html"
    config.option.self_contained_html = True
```

App/Admin 구분 없는 단일 서버 프로젝트는 `references/templates/conftest-multi-env.md`의 간소화 변형 참조.

## 인증 패턴 요약

상세 패턴은 `references/patterns/auth-patterns.md` 참조.

### Fixture 기반 인증 (권장)
conftest.py에 정의된 `app_token`, `admin_cookies` fixture를 함수 파라미터로 받는다.
```python
def test_기능명(app_token, admin_cookies):
    app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}
    # admin_cookies는 cookies= 파라미터로 바로 전달
```

### 인라인 인증 (신규 계정 등 fixture 불가 시)
회원가입 후 신규 계정 로그인처럼 매 실행마다 달라지는 경우에만 인라인 사용.
```python
# App 인증
app_token = requests.post(f"{APP_BASE_URL}/auth",
    json={"email": APP_EMAIL, "password": APP_PASSWORD, "remember": True},
    headers=COMMON_HEADERS).json()["accessToken"]
app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}

# Admin 인증
admin_cookies = requests.post(f"{ADMIN_BASE_URL}/admin/auth",
    json={"name": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
    headers=COMMON_HEADERS).cookies.get_dict()
```

## 핵심 패턴 요약

상세 패턴은 `references/patterns/response-parsing.md`, `references/patterns/assertion-patterns.md` 참조.

### 유연한 응답 파싱
```python
# API 응답이 {"data": [...]} 또는 [...] 둘 다 대응
data = res.json()
items = data.get("data", data) if isinstance(data, dict) else data
```

### ID 리스트 추출 및 존재 확인
```python
ids = [item.get("id") for item in items]
assert target_id in ids, f"목록에 ID:{target_id} 없음!"
```

### next()로 특정 항목 찾기
```python
found = next((i for i in items if i.get("id") == target_id), None)
assert found is not None, f"항목(ID:{target_id}) 없음!"
```

### 교차 API 필드 비교
```python
assert admin_data.get("email") == app_data.get("email"), \
    f"이메일 불일치! App: {app_data.get('email')}, Admin: {admin_data.get('email')}"
```

### 동적 테스트 데이터 생성
```python
ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
test_email = f"aqa_test_{ts}@test.com"
phone = f"010{ts[-8:]}"
nickname = f"AQA_{ts}"
```

### 알려진 버그 대응
```python
# 서버가 500을 반환하지만 실제로는 생성 성공하는 경우
assert res.status_code in [201, 500], \
    f"실패! {res.status_code}\n참고: 현재 버그로 500이지만 실제 생성됨"
```

## Swagger 분석 시 추출 항목

| Swagger 필드 | 추출 정보 | 테스트 코드 활용 |
|-------------|----------|----------------|
| paths | 엔드포인트 목록 | URL 생성, 시나리오 구성 |
| methods | HTTP 메서드 | requests.get/post/put/delete |
| parameters | 경로/쿼리 파라미터 | Given 섹션, params= |
| requestBody | 요청 본문 구조 | json= 파라미터 |
| responses | 응답 코드/구조 | assert 검증 |
| schemas | DTO 필드 정보 | 필드 검증, 교차 비교 |

시나리오 구성 시: 관련 엔드포인트를 묶어 CRUD 플로우나 교차 검증 시나리오로 자동 구성한다.

## 실행 방법

### 1단계: 패키지 설치 (최초 1회)
```bash
pip install pytest requests pytest-html
```

### 2단계: 테스트 실행
```bash
# 개발 환경 (기본)
pytest tests/e2e/ -v

# 스테이징 환경
ENV=stg pytest tests/e2e/ -v

# 특정 파일만
pytest tests/e2e/signup_home/test_tc_1.py -v

# 상세 출력 (print 로그 보기)
pytest tests/e2e/ -vvs
```

### 결과 읽는 법
```
PASSED  = 성공 (초록색)
FAILED  = 실패 (빨간색) — 아래에 assert 에러 메시지 표시
SKIPPED = 건너뜀
```

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `ModuleNotFoundError: requests` | 패키지 미설치 | `pip install requests` |
| `connection refused` / `timeout` | 서버 미실행 또는 URL 오류 | conftest.py의 BASE_URL 확인, VPN 확인 |
| `401 Unauthorized` | 토큰 만료 또는 인증 실패 | conftest.py의 인증 정보 확인 |
| `404 Not Found` | 경로 오류 또는 리소스 미존재 | URL 경로, API 버전, ID 확인 |
| `assert 200 == 500` | 서버 오류 | 요청 데이터 형식 확인, 서버 로그 확인 |

## 자주 묻는 질문

**"fixture 쓰면 안 되나요?"**
→ conftest.py의 `app_token`, `admin_cookies` auth fixture는 허용합니다. 파일당 1번만 로그인하므로 효율적입니다. 단, 별도 utils.py/helpers.py를 만들거나 비즈니스 로직을 fixture로 분리하지 마세요.

**"helper 함수로 로그인 코드를 분리하면 편하지 않나요?"**
→ conftest.py fixture로 충분합니다. 별도 파일(utils.py, helpers.py)은 만들지 마세요. fixture가 아닌 일반 helper 함수는 어디에 있는지 찾기 어려워집니다.

**"한글 함수명 써도 되나요?"**
→ 네! `def test_회원가입_로그인_이메일_플로우():` 가독성이 더 좋습니다.

**"ENV 환경변수 없이도 되나요?"**
→ 네. ENV를 설정하지 않으면 기본값(dev)이 사용됩니다.

**"App/Admin 구분이 없는 프로젝트는요?"**
→ conftest.py에서 `BASE_URL` 하나만 사용하세요. `references/templates/conftest-multi-env.md`의 간소화 변형을 참고하세요.

## 체크리스트

테스트 작성 후 확인:

- [ ] conftest.py에 ENV 기반 환경 전환 설정했는가?
- [ ] conftest.py에 `app_token`, `admin_cookies` fixture가 있는가?
- [ ] BASE_URL이 올바르게 설정되었는가?
- [ ] 인증 방식이 올바른가? (App=Bearer 토큰, Admin=Cookie)
- [ ] `from conftest import ...` 임포트가 맞는가?
- [ ] Step 1/2/3 한글 주석으로 단계를 구분했는가? (Given-When-Then 아님)
- [ ] f-string으로 URL을 직접 생성했는가?
- [ ] print() 로깅을 `[REQUEST]`, `[RESPONSE]` 형식으로 추가했는가?
- [ ] assert에 실패 힌트 메시지가 있는가?
- [ ] 응답 파싱이 유연한가? (`data.get("data", data)` 패턴)
- [ ] E2E 테스트에서 각 단계 후 검증이 있는가?
- [ ] utils.py, helpers.py 등 별도 파일이 없는가? (conftest.py auth fixture는 OK)
- [ ] 테스트 데이터가 유니크한가? (타임스탬프 등)
