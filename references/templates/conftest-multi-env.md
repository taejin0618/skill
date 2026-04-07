# conftest.py 템플릿: 멀티 환경

## 기본 템플릿 (이중 서버: App + Admin)

```python
"""
공통 설정값
---
수정할 곳: 아래 환경별 URL과 인증 정보를 프로젝트에 맞게 수정하세요.

사용법:
    ENV=dev pytest tests/ -v
    ENV=stg pytest tests/ -v

임포트:
    from conftest import (
        APP_BASE_URL, ADMIN_BASE_URL,
        APP_EMAIL, APP_PASSWORD,
        ADMIN_USERNAME, ADMIN_PASSWORD,
        COMMON_HEADERS
    )
"""

import os
import datetime
import pytest
import requests

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 환경 선택 (ENV 환경변수로 전환)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ENV = os.environ.get("ENV", "dev")  # dev 또는 stg

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [수정] 환경별 설정값
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if ENV == "stg":
    # 스테이징 환경
    APP_BASE_URL    = "https://stg-api.example.com"
    ADMIN_BASE_URL  = "https://stg-admin-api.example.com"
    APP_EMAIL       = "test@example.com"
    APP_PASSWORD    = "TestPassword123!"
    ADMIN_USERNAME  = "admin"
    ADMIN_PASSWORD  = "AdminPassword123!"
else:
    # 개발 환경 (기본값)
    APP_BASE_URL    = "https://dev-api.example.com"
    ADMIN_BASE_URL  = "https://dev-admin-api.example.com"
    APP_EMAIL       = "dev-test@example.com"
    APP_PASSWORD    = "DevPassword123!"
    ADMIN_USERNAME  = "dev_admin"
    ADMIN_PASSWORD  = "DevAdminPass123!"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 공통 헤더 (수정 불필요)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMMON_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 리포트 파일명에 타임스탬프 (실행마다 누적 보존)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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

## 간소화 변형 (단일 서버)

App/Admin 구분이 필요 없는 단순 프로젝트용.

```python
"""
공통 설정값 (단일 서버)
---
사용법: ENV=dev pytest tests/ -v
임포트: from conftest import BASE_URL, HEADERS
"""

import os

ENV = os.environ.get("ENV", "dev")

if ENV == "stg":
    BASE_URL  = "https://stg-api.example.com"
    API_TOKEN = "stg-token-here"
else:
    BASE_URL  = "https://dev-api.example.com"
    API_TOKEN = "dev-token-here"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_TOKEN}"
}
```

## pytest.ini 템플릿

```ini
[pytest]
testpaths = tests/e2e
addopts = -v -s --tb=short
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

## requirements.txt 템플릿

```
pytest==8.3.5
requests==2.32.3
pytest-html==4.1.1
python-dotenv==1.0.1
```
