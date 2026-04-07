---
name: pytest-to-postman
description: >
  pytest API 테스트 코드를 Postman Collection으로 변환. 비개발자도 API 테스트 가능.
  트리거: (1) "pytest를 Postman으로 변환" (2) "테스트 코드로 Postman 만들어줘"
  (3) "Postman Collection 생성" (4) pytest 파일 업로드 후 Postman 요청.
  출력: Postman Collection v2.1.0 JSON (순차 실행, 변수 자동 관리, 테스트 스크립트 포함).
---

# pytest to Postman Converter

pytest로 작성된 API 테스트를 Postman Collection으로 변환하여 비개발자도 테스트할 수 있게 한다.

## 사용 목적

| 대상 | pytest | Postman |
|------|--------|---------|
| 개발자/QA엔지니어 | 익숙함 | 선택적 |
| 기획자/비개발자 | 어려움 | GUI로 쉬움 |

-> pytest 코드를 Postman으로 변환하면 **팀 전체가 API 테스트 가능**

## 변환 프로세스

```
[pytest 테스트 파일] -> [분석] -> [Postman Collection JSON]
```

### 1단계: pytest 코드 분석

pytest 파일에서 추출하는 정보:

| 추출 항목 | pytest 코드 예시 | Postman 변환 |
|----------|-----------------|--------------|
| URL | `f"{BASE_URL}/api/users/{id}"` | `{{BASE_URL}}/api/users/{{USER_ID}}` |
| 메서드 | `requests.get(...)` | `"method": "GET"` |
| 헤더 | `headers=HEADERS` | `"header": [...]` |
| 본문 | `json=create_data` | `"body": {"raw": ...}` |
| 검증 | `assert response.status_code == 200` | `pm.test(...)` |

### 2단계: Collection 구조 생성

```json
{
  "info": {
    "name": "API 테스트 컬렉션",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [],
  "event": [],
  "item": []
}
```

## Collection Variables

pytest의 설정값을 Postman 변수로 변환:

```python
# pytest conftest.py
BASE_URL = "https://api.example.com"
API_TOKEN = "your-token"
```

```json
// Postman variables
[
  {"key": "BASE_URL", "value": "https://api.example.com"},
  {"key": "ACCESS_TOKEN", "value": ""},
  {"key": "timestamp", "value": ""}
]
```

**동적 변수 (자동 생성):**
- `timestamp`: 매 요청마다 자동 생성
- `[ENTITY]_ID`: POST 응답에서 자동 저장

## Pre-request Script (컬렉션 레벨)

```javascript
// 타임스탬프 자동 생성 (YYYYMMDDHHmmss)
const now = new Date();
const timestamp = now.getFullYear() +
    String(now.getMonth() + 1).padStart(2, '0') +
    String(now.getDate()).padStart(2, '0') +
    String(now.getHours()).padStart(2, '0') +
    String(now.getMinutes()).padStart(2, '0') +
    String(now.getSeconds()).padStart(2, '0');

pm.collectionVariables.set('timestamp', timestamp);
console.log('[Timestamp]', timestamp);
```

## Request 변환 패턴

### GET 요청

**pytest:**
```python
def test_사용자_조회():
    url = f"{BASE_URL}/api/users/{user_id}"
    response = requests.get(url, headers=HEADERS)
    assert response.status_code == 200
```

**Postman:**
```json
{
  "name": "GET 사용자 조회",
  "request": {
    "method": "GET",
    "header": [
      {"key": "Authorization", "value": "Bearer {{ACCESS_TOKEN}}"},
      {"key": "Content-Type", "value": "application/json"}
    ],
    "url": "{{BASE_URL}}/api/users/{{USER_ID}}"
  },
  "event": [{
    "listen": "test",
    "script": {
      "exec": [
        "pm.test('Status 200', function() {",
        "    pm.response.to.have.status(200);",
        "});",
        "",
        "pm.test('응답 데이터 존재', function() {",
        "    const data = pm.response.json();",
        "    pm.expect(data).to.have.property('id');",
        "});"
      ]
    }
  }]
}
```

### POST 요청 (ID 자동 저장)

**pytest:**
```python
def test_사용자_생성():
    create_data = {"name": f"테스트_{timestamp}"}
    response = requests.post(url, json=create_data, headers=HEADERS)
    assert response.status_code == 201
    created_id = response.json()["id"]
```

**Postman:**
```json
{
  "name": "POST 사용자 생성",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Authorization", "value": "Bearer {{ACCESS_TOKEN}}"},
      {"key": "Content-Type", "value": "application/json"}
    ],
    "body": {
      "mode": "raw",
      "raw": "{\n  \"name\": \"테스트_{{timestamp}}\"\n}",
      "options": {"raw": {"language": "json"}}
    },
    "url": "{{BASE_URL}}/api/users"
  },
  "event": [{
    "listen": "test",
    "script": {
      "exec": [
        "pm.test('Status 201', function() {",
        "    pm.response.to.have.status(201);",
        "});",
        "",
        "// 생성된 ID 자동 저장",
        "if (pm.response.code === 201) {",
        "    const data = pm.response.json();",
        "    pm.collectionVariables.set('USER_ID', data.id);",
        "    console.log('[저장] 생성된 ID:', data.id);",
        "}"
      ]
    }
  }]
}
```

### PUT 요청

**Postman:**
```json
{
  "name": "PUT 사용자 수정",
  "request": {
    "method": "PUT",
    "body": {
      "mode": "raw",
      "raw": "{\n  \"name\": \"수정된이름_{{timestamp}}\"\n}"
    },
    "url": "{{BASE_URL}}/api/users/{{USER_ID}}"
  },
  "event": [{
    "listen": "test",
    "script": {
      "exec": [
        "pm.test('Status 200', function() {",
        "    pm.response.to.have.status(200);",
        "});"
      ]
    }
  }]
}
```

### DELETE 요청

**Postman:**
```json
{
  "name": "DELETE 사용자 삭제",
  "request": {
    "method": "DELETE",
    "url": "{{BASE_URL}}/api/users/{{USER_ID}}"
  },
  "event": [{
    "listen": "test",
    "script": {
      "exec": [
        "pm.test('Status 200 or 204', function() {",
        "    pm.expect(pm.response.code).to.be.oneOf([200, 204]);",
        "});"
      ]
    }
  }]
}
```

## 폴더 구조

pytest 파일 구조를 Postman 폴더로 변환:

```
pytest 구조:
tests/
+-- user_api/
|   +-- test_get_사용자.py
|   +-- test_post_사용자.py
|   +-- test_delete_사용자.py
+-- order_api/
    +-- test_post_주문.py

  |  변환  |
  v        v

Postman 구조:
Collection
+-- User API
|   +-- GET 사용자 목록
|   +-- GET 사용자 조회
|   +-- POST 사용자 생성
|   +-- DELETE 사용자 삭제
+-- Order API
    +-- POST 주문 생성
```

## 순차 실행 지원

CRUD 순서로 자동 정렬:

```
1. POST (생성) -> ID 저장
2. GET (목록 조회)
3. GET (단건 조회) -> 저장된 ID 사용
4. PUT (수정) -> 저장된 ID 사용
5. DELETE (삭제) -> 저장된 ID 사용
```

## 변환 규칙 요약

| pytest | Postman |
|--------|---------|
| `BASE_URL` | `{{BASE_URL}}` |
| `HEADERS["Authorization"]` | `Bearer {{ACCESS_TOKEN}}` |
| `f".../{resource_id}"` | `{{RESOURCE_ID}}` |
| `datetime.now().strftime(...)` | `{{timestamp}}` |
| `assert status_code == 200` | `pm.response.to.have.status(200)` |
| `assert "field" in data` | `pm.expect(data).to.have.property('field')` |
| `assert data["name"] == "값"` | `pm.expect(data.name).to.eql('값')` |

## 출력 파일

```
collection/
+-- postman/
    +-- [프로젝트명]_Collection.json   # Postman Import용
    +-- README.md                      # 사용 가이드
```

## Postman 사용 가이드 (README.md 포함)

생성된 컬렉션과 함께 제공:

```markdown
# [프로젝트명] Postman Collection

## 설정 방법

1. Postman에서 Import -> 파일 선택
2. Collection Variables 설정:
   - BASE_URL: API 서버 주소
   - ACCESS_TOKEN: 인증 토큰

## 실행 방법

### 개별 실행
- 원하는 요청 선택 -> Send

### 전체 순차 실행
- Collection Runner 실행
- Run 클릭

## 변수 설명

| 변수 | 설명 | 설정 방법 |
|------|------|----------|
| BASE_URL | API 서버 주소 | 수동 입력 |
| ACCESS_TOKEN | 인증 토큰 | 수동 입력 |
| timestamp | 타임스탬프 | 자동 생성 |
| [ENTITY]_ID | 생성된 리소스 ID | POST 후 자동 저장 |
```

## 체크리스트

변환 완료 후 확인:

- [ ] Collection Variables에 BASE_URL, ACCESS_TOKEN 있는가?
- [ ] Pre-request Script에 timestamp 생성 있는가?
- [ ] POST 요청에 ID 자동 저장 스크립트 있는가?
- [ ] 각 요청에 테스트 스크립트 있는가?
- [ ] CRUD 순서로 정렬되어 있는가?
- [ ] 한글이 깨지지 않는가? (ensure_ascii=False)
