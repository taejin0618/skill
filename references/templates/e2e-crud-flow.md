# E2E CRUD 플로우 템플릿

하나의 테스트 함수에서 Create → Read → Update → Delete 전체 라이프사이클을 검증한다.
각 단계에서 이전 단계의 결과를 확인하여 데이터 무결성을 보장한다.

## 전체 템플릿

```python
"""
[기능명] CRUD 플로우 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
시나리오:
  1. [리소스] 목록 조회 → 대상 ID 획득
  2. [리소스] 추가 → 목록에서 존재 확인
  3. [리소스] 수정 → 수정 내용 확인
  4. [리소스] 삭제 → 목록에서 부재 확인

실행: pytest tests/[폴더]/test_[기능]_crud.py -v
"""

import json
import requests
from conftest import (
    APP_BASE_URL,
    COMMON_HEADERS
)


def test_리소스_CRUD_플로우(app_token):
    """리소스 추가/조회/수정/삭제 E2E 플로우"""
    print("\n" + "=" * 60)
    print("[기능명] CRUD 플로우 검증")

    app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 1: 목록 조회 → 대상 ID 획득
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print("\n Step1: 목록 조회")
    # [수정] API 경로
    print(f"[REQUEST] GET {APP_BASE_URL}/resources")
    res_list = requests.get(
        f"{APP_BASE_URL}/resources",
        params={"sort": "createdAt", "order": "DESC"},
        headers=app_headers
    )
    assert res_list.status_code == 200, f"목록 조회 실패: {res_list.status_code}"
    list_data = res_list.json()
    items = list_data.get("data", list_data) if isinstance(list_data, dict) else list_data
    assert len(items) > 0, "목록이 비어있음"
    target_id = str(items[0].get("id"))
    print(f"대상 ID: {target_id}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 2: 추가 → 목록에서 존재 확인
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(f"\n Step2: 추가 (target_id: {target_id})")
    # [수정] 추가 API 경로와 요청 데이터
    print(f"[REQUEST] POST {APP_BASE_URL}/favorites/{target_id}")
    res_add = requests.post(
        f"{APP_BASE_URL}/favorites/{target_id}",
        headers=app_headers
    )
    assert res_add.status_code in [200, 201], \
        f"추가 실패: {res_add.status_code}"

    # 추가 후 목록에서 확인
    # [수정] 목록 조회 API 경로
    res_check = requests.get(
        f"{APP_BASE_URL}/favorites",
        params={"size": 100},
        headers=app_headers
    )
    assert res_check.status_code == 200
    check_data = res_check.json()
    check_items = check_data.get("data", check_data) if isinstance(check_data, dict) else check_data
    check_ids = [str(item.get("id")) for item in check_items]
    assert target_id in check_ids, \
        f"추가 후 목록에 ID:{target_id} 없음!"
    print("추가 확인 완료")

    # 추가된 항목의 내부 ID 획득 (수정/삭제용)
    added_item = next((i for i in check_items if str(i.get("id")) == target_id), None)
    item_id = added_item.get("id") if added_item else None

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 3: 수정 → 수정 내용 확인
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(f"\n Step3: 수정 (item_id: {item_id})")
    # [수정] 수정 API 경로와 데이터
    print(f"[REQUEST] PUT {APP_BASE_URL}/favorites/{item_id}")
    res_edit = requests.put(
        f"{APP_BASE_URL}/favorites/{item_id}",
        json={"quantity": 6},  # [수정] 수정할 데이터
        headers=app_headers
    )
    assert res_edit.status_code == 200, \
        f"수정 실패: {res_edit.status_code}"

    # 수정 결과 확인
    res_after_edit = requests.get(
        f"{APP_BASE_URL}/favorites",
        headers=app_headers
    )
    edit_data = res_after_edit.json()
    edit_items = edit_data.get("data", edit_data) if isinstance(edit_data, dict) else edit_data
    edited = next((i for i in edit_items if i.get("id") == item_id), None)
    assert edited is not None, f"수정 후 항목(ID:{item_id}) 없음!"
    # [수정] 수정된 필드 검증
    assert edited.get("quantity") == 6, \
        f"수량 불일치! 기대: 6, 실제: {edited.get('quantity')}"
    print("수정 확인 완료")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Step 4: 삭제 → 목록에서 부재 확인
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print(f"\n Step4: 삭제 (item_id: {item_id})")
    # [수정] 삭제 API 경로
    print(f"[REQUEST] DELETE {APP_BASE_URL}/favorites/{item_id}")
    res_delete = requests.delete(
        f"{APP_BASE_URL}/favorites/{item_id}",
        headers=app_headers
    )
    assert res_delete.status_code in [200, 204], \
        f"삭제 실패: {res_delete.status_code}"

    # 삭제 후 부재 확인
    res_final = requests.get(f"{APP_BASE_URL}/favorites", headers=app_headers)
    final_data = res_final.json()
    final_items = final_data.get("data", final_data) if isinstance(final_data, dict) else final_data
    final_ids = [item.get("id") for item in final_items]
    assert item_id not in final_ids, \
        f"삭제 후에도 항목(ID:{item_id}) 존재!"
    print("삭제 확인 완료")

    print(f"\n CRUD 플로우 통과! 대상 ID: {target_id}")
    print("=" * 60)
```

## 핵심 포인트

1. **각 단계 후 반드시 검증**: 추가 후 목록에서 확인, 수정 후 값 확인, 삭제 후 부재 확인
2. **ID 전달**: Step 2에서 획득한 ID를 Step 3, 4에서 재사용
3. **유연한 응답 파싱**: `data.get("data", data)` 패턴 일관 적용
4. **next() 활용**: 목록에서 특정 항목을 찾을 때 `next()` 사용
