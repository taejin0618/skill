# E2E 교차 시스템 검증 템플릿

App에서 작업 수행 후 Admin에서 결과를 확인하는 패턴.
두 시스템 간 데이터 동기화가 올바르게 동작하는지 검증한다.

## 기본 템플릿: App 작업 → Admin 확인

```python
"""
[기능명] App → Admin 교차 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
시나리오:
  1. App 로그인 → 작업 수행 (생성/수정 등)
  2. Admin 로그인 → 목록에서 해당 항목 존재 확인
  3. Admin 상세 조회 → App 데이터와 필드별 비교

실행: pytest tests/[폴더]/test_[기능]_cross.py -v
"""

import json
import requests
from conftest import (
    APP_BASE_URL, ADMIN_BASE_URL,
    COMMON_HEADERS
)


def test_기능_App_Admin_교차검증(app_token, admin_cookies):
    """App에서 작업 후 Admin에서 데이터 동기화 확인"""
    print("\n" + "=" * 60)
    print("[기능명] App → Admin 교차 검증")

    app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 1: App에서 작업 수행
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print("\n Step1: App에서 작업 수행")
    # [수정] App API 경로와 요청 데이터
    print(f"[REQUEST] POST {APP_BASE_URL}/resources")
    res_action = requests.post(
        f"{APP_BASE_URL}/resources",
        json={"requestUrl": "https://test.example.com/resource"},
        headers=app_headers
    )
    print(f"[RESPONSE] {res_action.status_code}")
    print(f"[BODY]\n{json.dumps(res_action.json(), indent=2, ensure_ascii=False)}")
    assert res_action.status_code in [200, 201], \
        f"App 작업 실패: {res_action.status_code}"
    resource_id = res_action.json().get("id")
    print(f"생성된 ID: {resource_id}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 2: Admin 목록에서 존재 확인
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print("\n Step2: Admin 목록에서 확인")
    # [수정] Admin 목록 API 경로
    print(f"[REQUEST] GET {ADMIN_BASE_URL}/admin/resources")
    res_admin_list = requests.get(
        f"{ADMIN_BASE_URL}/admin/resources",
        params={"size": 100},
        cookies=admin_cookies,
        headers=COMMON_HEADERS
    )
    assert res_admin_list.status_code == 200, \
        f"Admin 목록 조회 실패: {res_admin_list.status_code}"

    admin_data = res_admin_list.json()
    admin_items = admin_data.get("data", admin_data) if isinstance(admin_data, dict) else admin_data
    admin_ids = [item.get("id") for item in admin_items]
    assert resource_id in admin_ids, \
        f"Admin 목록에 ID:{resource_id} 없음!"
    print("Admin 목록 확인 완료")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 3: Admin 상세 조회 → 필드별 비교
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(f"\n Step3: Admin 상세 조회 (ID:{resource_id})")
    # [수정] Admin 상세 API 경로
    print(f"[REQUEST] GET {ADMIN_BASE_URL}/admin/resources/{resource_id}")
    res_detail = requests.get(
        f"{ADMIN_BASE_URL}/admin/resources/{resource_id}",
        cookies=admin_cookies,
        headers=COMMON_HEADERS
    )
    assert res_detail.status_code == 200, \
        f"Admin 상세 조회 실패: {res_detail.status_code}"

    admin_detail = res_detail.json()
    print(f"[DATA]\n{json.dumps(admin_detail, indent=2, ensure_ascii=False)}")

    # [수정] App 데이터와 Admin 데이터 필드별 비교
    # App에서 보낸 데이터가 Admin에서도 동일한지 확인
    assert admin_detail.get("id") == resource_id, "ID 불일치!"
    # 추가 필드 비교 (프로젝트에 맞게 수정)
    # assert admin_detail.get("email") == app_data.get("email"), \
    #     f"이메일 불일치! App: {app_data.get('email')}, Admin: {admin_detail.get('email')}"

    print(f"\n 교차 검증 통과! ID: {resource_id}")
    print("=" * 60)
```

## 변형: App 유저 정보 → Admin 유저 상세 비교

```python
def test_유저정보_App_Admin_교차검증(app_token, admin_cookies):
    """App 유저 정보와 Admin 유저 상세가 일치하는지 확인"""
    app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}

    # Step 1: App에서 내 정보 조회
    res_user = requests.get(f"{APP_BASE_URL}/users", headers=app_headers)
    assert res_user.status_code == 200
    app_user = res_user.json()
    user_id = app_user.get("id")

    # Step 2: Admin에서 유저 목록 → 존재 확인
    res_admin_users = requests.get(
        f"{ADMIN_BASE_URL}/admin/users",
        params={"withDeleted": "false", "start": 0, "perPage": 100,
                "sort": "createdAt", "order": "DESC"},
        cookies=admin_cookies,
        headers=COMMON_HEADERS
    )
    user_list = res_admin_users.json().get("data", [])
    user_ids = [u.get("id") for u in user_list]
    assert user_id in user_ids, f"Admin 목록에 유저(ID:{user_id}) 없음!"

    # Step 3: Admin 상세 → 필드별 비교
    res_detail = requests.get(
        f"{ADMIN_BASE_URL}/admin/users/{user_id}",
        cookies=admin_cookies,
        headers=COMMON_HEADERS
    )
    admin_user = res_detail.json()

    assert admin_user.get("email") == app_user.get("email"), \
        f"이메일 불일치! App: {app_user.get('email')}, Admin: {admin_user.get('email')}"
    assert admin_user.get("nickname") == app_user.get("nickname"), \
        f"닉네임 불일치! App: {app_user.get('nickname')}, Admin: {admin_user.get('nickname')}"
```

## 핵심 포인트

1. **이중 인증**: App은 Bearer 토큰, Admin은 Cookie로 각각 인증
2. **3단계 검증**: App 작업 → Admin 목록 존재 → Admin 상세 필드 비교
3. **ID 추적**: App에서 생성된 ID를 Admin에서 추적
4. **유연한 파싱**: Admin 응답도 `data.get("data", data)` 패턴 적용
