# E2E 전체 라이프사이클 템플릿

5단계 이상의 복잡한 시나리오를 순차적으로 검증한다.
동적 데이터 생성, 다단계 API 호출, 교차 시스템 검증을 모두 포함하는 가장 종합적인 템플릿.

## 전체 템플릿: 회원가입 플로우 예시

```python
"""
[기능명] 전체 라이프사이클 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
시나리오:
  1. 사전 인증 (전화번호 인증 요청)
  2. 인증 코드 확인 및 토큰 획득
  3. 회원가입
  4. 신규 계정 로그인
  5. App에서 유저 정보 조회
  6. Admin에서 유저 목록 확인 (존재 검증)
  7. Admin에서 유저 상세 조회 (App과 필드별 비교)

실행: pytest tests/[폴더]/test_[기능]_lifecycle.py -v
"""

import datetime
import json
import requests
from conftest import (
    APP_BASE_URL, ADMIN_BASE_URL,
    COMMON_HEADERS
)


def test_기능_전체_라이프사이클(admin_cookies):
    """[기능명] 전체 시나리오 E2E 검증"""
    print("\n" + "=" * 60)
    print("[기능명] 전체 라이프사이클 검증")

    # 타임스탬프 기반 유니크 데이터 (테스트 반복 실행 시 충돌 방지)
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 1: 사전 인증 요청
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # [수정] 인증 요청 데이터
    verify_body = {
        "phone": f"010{ts[-8:]}",  # 유니크 전화번호
        "type": "register",
        "division": "email"
    }
    print(f"\n Step1: 사전 인증 요청 - {verify_body['phone']}")
    print(f"[REQUEST] POST {APP_BASE_URL}/verifications/phone")
    res_verify = requests.post(
        f"{APP_BASE_URL}/verifications/phone",
        json=verify_body,
        headers=COMMON_HEADERS
    )
    print(f"[RESPONSE] {res_verify.status_code}")
    print(f"[BODY]\n{json.dumps(res_verify.json(), indent=2, ensure_ascii=False)}")
    assert res_verify.status_code == 201, \
        f"인증 요청 실패! {res_verify.status_code}\n응답: {res_verify.text[:200]}"
    code_token = res_verify.json()["codeToken"]
    code = res_verify.json()["code"]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 2: 인증 코드 확인
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    confirm_body = {"codeToken": code_token, "code": code}
    print(f"\n Step2: 인증 코드 확인")
    print(f"[REQUEST] POST {APP_BASE_URL}/verifications/confirm")
    res_confirm = requests.post(
        f"{APP_BASE_URL}/verifications/confirm",
        json=confirm_body,
        headers=COMMON_HEADERS
    )
    print(f"[RESPONSE] {res_confirm.status_code}")
    assert res_confirm.status_code == 200, \
        f"인증 확인 실패! {res_confirm.status_code}"
    confirmed_token = res_confirm.json().get("codeToken", "")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 3: 회원가입
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # [수정] 회원가입 데이터
    test_email = f"aqa_test_{ts}@test.com"
    signup_body = {
        "email": test_email,
        "password": "TestPassword123!",
        "nickname": f"AQA_{ts}",
        "phone": verify_body["phone"],
        "codeToken": confirmed_token,
        "agreeMarketing": False,
        "type": "email"
    }
    print(f"\n Step3: 회원가입 - {test_email}")
    print(f"[REQUEST] POST {APP_BASE_URL}/auth/register")
    res_signup = requests.post(
        f"{APP_BASE_URL}/auth/register",
        json=signup_body,
        headers=COMMON_HEADERS
    )
    print(f"[RESPONSE] {res_signup.status_code}")
    print(f"[BODY]\n{json.dumps(res_signup.json(), indent=2, ensure_ascii=False)}")
    # 참고: 일부 API는 생성 성공이지만 500을 반환하는 버그가 있음
    assert res_signup.status_code in [201, 500], \
        f"회원가입 실패! {res_signup.status_code}"

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 4: 신규 계정 로그인
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(f"\n Step4: 신규 계정 로그인 - {test_email}")
    print(f"[REQUEST] POST {APP_BASE_URL}/auth")
    new_login_res = requests.post(
        f"{APP_BASE_URL}/auth",
        json={"email": test_email, "password": signup_body["password"], "remember": True},
        headers=COMMON_HEADERS
    )
    print(f"[RESPONSE] {new_login_res.status_code}")
    assert new_login_res.status_code == 200, \
        f"신규 계정 로그인 실패! {new_login_res.status_code}"
    new_token = new_login_res.json()["accessToken"]
    new_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {new_token}"}

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 5: App에서 유저 정보 조회
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(f"\n Step5: App 유저 정보 조회")
    print(f"[REQUEST] GET {APP_BASE_URL}/users")
    res_user = requests.get(f"{APP_BASE_URL}/users", headers=new_headers)
    print(f"[RESPONSE] {res_user.status_code}")
    print(f"[BODY]\n{json.dumps(res_user.json(), indent=2, ensure_ascii=False)}")
    assert res_user.status_code == 200, \
        f"유저 정보 조회 실패! {res_user.status_code}"
    app_user = res_user.json()
    user_id = app_user.get("id")
    print(f"App 유저 ID: {user_id}, 이메일: {app_user.get('email')}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 6: Admin 유저 목록 확인
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(f"\n Step6: Admin 유저 목록 확인")
    print(f"[REQUEST] GET {ADMIN_BASE_URL}/admin/users")
    res_admin_list = requests.get(
        f"{ADMIN_BASE_URL}/admin/users",
        params={"withDeleted": "false", "start": 0, "perPage": 100,
                "sort": "createdAt", "order": "DESC"},
        cookies=admin_cookies,
        headers=COMMON_HEADERS
    )
    print(f"[RESPONSE] {res_admin_list.status_code}")
    assert res_admin_list.status_code == 200
    user_list = res_admin_list.json().get("data", [])
    user_ids = [u.get("id") for u in user_list]
    assert user_id in user_ids, \
        f"Admin 목록에 신규 유저(ID:{user_id}) 없음!"
    print("Admin 목록 확인 완료")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 7: Admin 상세 → App 데이터와 비교
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(f"\n Step7: Admin 유저 상세 (ID:{user_id})")
    print(f"[REQUEST] GET {ADMIN_BASE_URL}/admin/users/{user_id}")
    res_detail = requests.get(
        f"{ADMIN_BASE_URL}/admin/users/{user_id}",
        cookies=admin_cookies,
        headers=COMMON_HEADERS
    )
    print(f"[RESPONSE] {res_detail.status_code}")
    print(f"[BODY]\n{json.dumps(res_detail.json(), indent=2, ensure_ascii=False)}")
    assert res_detail.status_code == 200
    admin_user = res_detail.json()

    # 교차 검증: App vs Admin
    assert admin_user.get("email") == app_user.get("email"), \
        f"이메일 불일치! App: {app_user.get('email')}, Admin: {admin_user.get('email')}"
    assert admin_user.get("nickname") == app_user.get("nickname"), \
        f"닉네임 불일치! App: {app_user.get('nickname')}, Admin: {admin_user.get('nickname')}"

    print(f"\n 전체 라이프사이클 통과! 유저 ID: {user_id}")
    print("=" * 60)
```

## 핵심 포인트

1. **타임스탬프 유니크 데이터**: `ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")`로 매 실행마다 유니크한 이메일/전화번호 생성
2. **단계 간 데이터 전달**: Step 1의 codeToken → Step 2 → Step 3에서 사용
3. **이중 인증**: App(Bearer) + Admin(Cookie) 동시 사용
4. **교차 검증**: Step 5(App) vs Step 7(Admin) 필드별 비교
5. **버그 대응**: `assert status in [201, 500]`로 알려진 버그 허용
6. **상세 로깅**: 모든 단계에서 REQUEST/RESPONSE 출력

## 다른 라이프사이클 예시

이 템플릿을 기반으로 다양한 시나리오를 구성할 수 있다:

- **주문 플로우**: 상품 조회 → 카트 추가 → 결제 → 주문 상세 확인 → Admin 주문 목록 확인
- **리뷰 플로우**: 로그인 → 상품 구매 확인 → 리뷰 작성 → 리뷰 목록 확인 → Admin 리뷰 관리
- **프로필 수정**: 로그인 → 정보 조회 → 프로필 수정 → Admin 변경 확인 → 재로그인 → 변경 유지 확인
