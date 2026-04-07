# 단일 엔드포인트 테스트 템플릿

개별 API 엔드포인트를 검증하는 템플릿. 로그인 기반 인증 + 유연한 응답 파싱 적용.

## GET - 단건 조회

```python
"""
[기능명] 조회 테스트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
엔드포인트: GET /api/v1/[경로]/{id}
실행: pytest tests/[폴더]/test_get_[기능].py -v
"""

import json
import requests
from conftest import APP_BASE_URL, COMMON_HEADERS


def test_조회_성공(app_token):
    """정상 케이스: ID로 리소스 조회"""
    print("\n" + "=" * 60)

    app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}

    # [수정] 조회할 리소스 ID와 API 경로
    resource_id = 1
    url = f"{APP_BASE_URL}/api/v1/resources/{resource_id}"

    # Step 1: API 호출
    print(f"[REQUEST] GET {url}")
    res = requests.get(url, headers=app_headers)
    print(f"[RESPONSE] {res.status_code}")
    assert res.status_code == 200, \
        f"실패! 예상: 200, 실제: {res.status_code}\n힌트: 401=토큰만료, 404=ID없음"

    data = res.json()
    print(f"[DATA]\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    assert data.get("id") is not None, "응답에 id 없음"

    print(f"[PASS] 조회 성공! ID: {data.get('id')}")
    print("=" * 60)
```

## GET - 목록 조회 (페이징)

```python
def test_목록조회_성공(app_token):
    """정상 케이스: 목록 페이징 조회"""
    print("\n" + "=" * 60)

    app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}

    # [수정] API 경로와 페이징 파라미터
    url = f"{APP_BASE_URL}/api/v1/resources"
    params = {"start": 0, "perPage": 10, "sort": "createdAt", "order": "DESC"}

    # Step 1: 목록 조회
    print(f"[REQUEST] GET {url}")
    res = requests.get(url, headers=app_headers, params=params)
    assert res.status_code == 200, f"실패: {res.status_code}"

    data = res.json()
    # 유연한 리스트 추출 ({"data":[...]} 또는 [...] 모두 대응)
    items = data.get("data", data) if isinstance(data, dict) else data
    print(f"[RESULT] 조회 건수: {len(items)}건")
    assert len(items) > 0, "목록이 비어있음"

    print("[PASS] 목록 조회 성공!")
    print("=" * 60)
```

## POST - 생성

```python
import datetime

def test_생성_성공(app_token):
    """정상 케이스: 리소스 생성"""
    print("\n" + "=" * 60)

    app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # [수정] API 경로와 생성 데이터
    url = f"{APP_BASE_URL}/api/v1/resources"
    create_data = {
        "name": f"테스트_{ts}",
        "description": "자동 생성된 테스트 데이터"
    }

    # Step 1: 리소스 생성
    print(f"[REQUEST] POST {url}")
    print(f"[BODY]\n{json.dumps(create_data, indent=2, ensure_ascii=False)}")
    res = requests.post(url, headers=app_headers, json=create_data)
    print(f"[RESPONSE] {res.status_code}")
    assert res.status_code in [200, 201], \
        f"실패! 예상: 200/201, 실제: {res.status_code}\n응답: {res.text[:200]}"

    data = res.json()
    created_id = data.get("id") or data.get("seq")
    assert created_id is not None, "생성된 ID가 응답에 없음"
    print(f"[PASS] 생성 성공! ID: {created_id}")
    print("=" * 60)
```

## PUT - 수정

```python
def test_수정_성공(app_token):
    """정상 케이스: 리소스 수정"""
    print("\n" + "=" * 60)

    app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # [수정] 수정 대상 ID, 경로, 데이터
    resource_id = 1
    url = f"{APP_BASE_URL}/api/v1/resources/{resource_id}"
    update_data = {"name": f"수정됨_{ts}"}

    # Step 1: 수정 요청
    print(f"[REQUEST] PUT {url}")
    res = requests.put(url, headers=app_headers, json=update_data)
    print(f"[RESPONSE] {res.status_code}")
    assert res.status_code == 200, f"실패: {res.status_code}"

    data = res.json()
    if "name" in data:
        assert data["name"] == update_data["name"], \
            f"수정 미반영! 기대: {update_data['name']}, 실제: {data['name']}"

    print("[PASS] 수정 성공!")
    print("=" * 60)
```

## DELETE - 삭제

```python
def test_삭제_성공(app_token):
    """정상 케이스: 리소스 삭제"""
    print("\n" + "=" * 60)

    app_headers = {**COMMON_HEADERS, "Authorization": f"Bearer {app_token}"}

    # [수정] 삭제할 리소스 ID (테스트용 데이터만!)
    resource_id = 999
    url = f"{APP_BASE_URL}/api/v1/resources/{resource_id}"

    # Step 1: 삭제 요청
    print(f"[REQUEST] DELETE {url}")
    res = requests.delete(url, headers=app_headers)
    print(f"[RESPONSE] {res.status_code}")
    assert res.status_code in [200, 204], \
        f"실패! 예상: 200/204, 실제: {res.status_code}"

    print("[PASS] 삭제 성공!")
    print("=" * 60)
```
