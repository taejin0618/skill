# 인증 패턴 카탈로그

E2E API 테스트에서 사용하는 인증 패턴 모음.

## 패턴 1: App Bearer 토큰 인증

로그인 API를 호출하여 accessToken을 받고, 이후 요청의 Authorization 헤더에 포함한다.

```python
# App 로그인 → Bearer 토큰 획득
res_login = requests.post(
    f"{APP_BASE_URL}/auth",
    json={"email": APP_EMAIL, "password": APP_PASSWORD, "remember": True},
    headers=COMMON_HEADERS
)
assert res_login.status_code == 200, \
    f"App 로그인 실패: {res_login.status_code}\n힌트: 401=인증실패, 500=서버오류"
app_token = res_login.json()["accessToken"]

# 인증 헤더 생성 (스프레드 연산자로 기존 헤더 + Authorization 추가)
app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}

# 이후 요청에서 사용
res = requests.get(f"{APP_BASE_URL}/users", headers=app_headers)
```

## 패턴 2: Admin Cookie 인증

Admin 로그인 시 응답의 쿠키를 추출하여, 이후 요청에 cookies 파라미터로 전달한다.

```python
# Admin 로그인 → 쿠키 획득
res_admin_login = requests.post(
    f"{ADMIN_BASE_URL}/admin/auth",
    json={"name": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
    headers=COMMON_HEADERS
)
assert res_admin_login.status_code == 200, \
    f"Admin 로그인 실패: {res_admin_login.status_code}"
admin_cookies = res_admin_login.cookies.get_dict()

# 이후 요청에서 cookies= 파라미터로 전달
res = requests.get(
    f"{ADMIN_BASE_URL}/admin/users",
    params={"start": 0, "perPage": 100},
    cookies=admin_cookies,
    headers=COMMON_HEADERS
)
```

## 패턴 3: 신규 계정 로그인

회원가입 직후 신규 계정으로 재로그인하여 새 토큰을 획득하는 패턴.

```python
# 회원가입 후 신규 계정으로 로그인
new_login_res = requests.post(
    f"{APP_BASE_URL}/auth",
    json={"email": test_email, "password": test_password, "remember": True},
    headers=COMMON_HEADERS
)
assert new_login_res.status_code == 200, \
    f"신규 계정 로그인 실패: {new_login_res.status_code}"
new_token = new_login_res.json()["accessToken"]
new_app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {new_token}"}
```

## 패턴 4: 이중 인증 (App + Admin 동시)

교차 검증 테스트에서 App과 Admin 모두 로그인이 필요할 때 사용.

```python
# App 로그인
app_login_res = requests.post(
    f"{APP_BASE_URL}/auth",
    json={"email": APP_EMAIL, "password": APP_PASSWORD, "remember": True},
    headers=COMMON_HEADERS
)
assert app_login_res.status_code == 200
app_token = app_login_res.json()["accessToken"]
app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}

# Admin 로그인
admin_login_res = requests.post(
    f"{ADMIN_BASE_URL}/admin/auth",
    json={"name": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
    headers=COMMON_HEADERS
)
assert admin_login_res.status_code == 200
admin_cookies = admin_login_res.cookies.get_dict()
```

## 패턴 5: Fixture 기반 인증 (권장 — conftest.py 재사용)

conftest.py에 정의된 fixture를 함수 파라미터로 받아 자동 주입한다.
파일당 1번만 로그인 API를 호출하므로 50개 파일이 있어도 로그인은 50번뿐.

```python
# conftest.py에 이미 정의됨 (conftest-multi-env.md 참고)
# @pytest.fixture(scope="module") def app_token(): ...
# @pytest.fixture(scope="module") def admin_cookies(): ...

# test_tc_N.py에서 파라미터로 받아 사용
def test_유저_정보_조회(app_token, admin_cookies):
    # App 헤더 구성
    app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}

    # Step 1: App에서 유저 정보 조회
    res = requests.get(f"{APP_BASE_URL}/users", headers=app_headers)
    assert res.status_code == 200

    # Admin 쿠키는 cookies= 파라미터로 바로 전달
    res2 = requests.get(
        f"{ADMIN_BASE_URL}/admin/users",
        cookies=admin_cookies,
        headers=COMMON_HEADERS
    )
    assert res2.status_code == 200
```

패턴 1-4 (인라인 방식)는 회원가입 후 신규 계정 로그인처럼
fixture로 분리할 수 없는 경우에만 사용한다.

## 언제 어떤 패턴을 쓸까?

| 상황 | 패턴 |
|------|------|
| App/Admin 일반 API 테스트 | 패턴 5 (fixture — 권장) |
| App API만 테스트 | 패턴 5 또는 패턴 1 (Bearer) |
| Admin API만 테스트 | 패턴 5 또는 패턴 2 (Cookie) |
| App→Admin 교차 검증 | 패턴 5 (app_token + admin_cookies 동시) |
| 회원가입 후 신규 계정 로그인 | 패턴 3 (인라인 — fixture 불가) |
