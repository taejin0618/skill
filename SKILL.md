---
name: swagger-to-postman
description: >
  Swagger/OpenAPI 명세를 Postman Collection으로 직접 변환. 코드 작성 없이 바로 테스트 가능.
  트리거: (1) "Swagger를 Postman으로 변환" (2) "OpenAPI로 Postman 컬렉션 만들어줘"
  (3) "swagger.json을 Postman으로" (4) swagger/openapi 파일 업로드 후 Postman 요청.
  출력: Postman Collection v2.1.0 JSON (바로 Import 가능).
---

# Swagger to Postman Converter

Swagger/OpenAPI 명세를 Postman Collection으로 직접 변환한다. pytest 코드 없이 바로 API 테스트 가능.

## 사용 시나리오

```
[기존 방식]
Swagger → pytest 코드 작성 → Postman 변환
         (개발 필요)

[이 스킬]
Swagger → Postman Collection
         (바로 변환!)
```

**적합한 상황:**
- 빠르게 API 테스트하고 싶을 때
- 코드 작성 없이 테스트하고 싶을 때
- 비개발자가 API 테스트할 때
- API 문서를 팀에 공유할 때

## 지원 형식

| 형식 | 버전 | 확장자 |
|------|------|--------|
| OpenAPI | 3.0.x, 3.1.x | .json, .yaml |
| Swagger | 2.0 | .json, .yaml |

## 변환 프로세스

### 1단계: Swagger 분석

```python
# 버전 감지
if 'openapi' in doc:
    version = 'openapi-3.x'
    schemas = doc.get('components', {}).get('schemas', {})
elif 'swagger' in doc:
    version = 'swagger-2.0'
    schemas = doc.get('definitions', {})
```

### 2단계: 정보 추출

| Swagger | 추출 | Postman |
|---------|------|---------|
| info.title | API 이름 | Collection 이름 |
| servers[0].url | 서버 주소 | {{BASE_URL}} |
| paths | 엔드포인트 | Request 목록 |
| tags | 그룹 | Folder 구조 |
| components/schemas | DTO 정의 | 검증 스크립트 |

### 3단계: Postman Collection 생성

## Collection 구조

```json
{
  "info": {
    "name": "[API명] Collection",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {"key": "BASE_URL", "value": "https://api.example.com"},
    {"key": "ACCESS_TOKEN", "value": ""},
    {"key": "timestamp", "value": ""}
  ],
  "event": [
    {"listen": "prerequest", "script": {...}},
    {"listen": "test", "script": {...}}
  ],
  "item": [
    {"name": "Users API", "item": [...]},
    {"name": "Orders API", "item": [...]}
  ]
}
```

## Collection Variables

Swagger에서 자동 추출:

```json
[
  {"key": "BASE_URL", "value": "[servers[0].url에서 추출]"},
  {"key": "ACCESS_TOKEN", "value": "", "description": "Bearer 토큰"},
  {"key": "timestamp", "value": "", "description": "자동 생성"}
]
```

**동적 ID 변수** (엔티티별 자동 생성):
```json
{"key": "USER_ID", "value": "", "description": "POST /users 응답에서 자동 저장"}
{"key": "ORDER_ID", "value": "", "description": "POST /orders 응답에서 자동 저장"}
```

## Pre-request Script (컬렉션 레벨)

```javascript
// 타임스탬프 자동 생성
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

## Test Script (컬렉션 레벨)

```javascript
// 공통 응답 검증
pm.test('Status code is successful', function() {
    pm.expect(pm.response.code).to.be.oneOf([200, 201, 204]);
});

// 응답 시간 검증
pm.test('Response time < 5s', function() {
    pm.expect(pm.response.responseTime).to.be.below(5000);
});
```

## Folder 구조 생성

Swagger tags 기반으로 폴더 구성:

```
Collection
+-- Users API (tag: user)
|   +-- POST 사용자 생성
|   +-- GET 사용자 목록
|   +-- GET 사용자 조회
|   +-- PUT 사용자 수정
|   +-- DELETE 사용자 삭제
+-- Orders API (tag: order)
|   +-- POST 주문 생성
|   +-- GET 주문 조회
+-- Others (태그 없는 것들)
```

## Request 변환 규칙

### Path Parameters

```yaml
# Swagger
/users/{userId}:
  get:
    parameters:
      - name: userId
        in: path
```

```json
// Postman
"url": "{{BASE_URL}}/users/{{USER_ID}}"
```

### Query Parameters

```yaml
# Swagger
/users:
  get:
    parameters:
      - name: page
        in: query
        schema:
          default: 0
      - name: size
        in: query
        schema:
          default: 10
```

```json
// Postman
"url": {
  "raw": "{{BASE_URL}}/users?page=0&size=10",
  "query": [
    {"key": "page", "value": "0"},
    {"key": "size", "value": "10"}
  ]
}
```

### Request Body

```yaml
# Swagger
/users:
  post:
    requestBody:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CreateUserDto'
```

```json
// Postman - 스키마 기반 예시 데이터 생성
"body": {
  "mode": "raw",
  "raw": "{\n  \"name\": \"테스트_{{timestamp}}\",\n  \"email\": \"test_{{timestamp}}@example.com\"\n}",
  "options": {"raw": {"language": "json"}}
}
```

## HTTP Method별 Request 템플릿

### POST (생성)

```json
{
  "name": "POST [리소스] 생성",
  "request": {
    "method": "POST",
    "header": [
      {"key": "Content-Type", "value": "application/json"},
      {"key": "Authorization", "value": "Bearer {{ACCESS_TOKEN}}"}
    ],
    "body": {
      "mode": "raw",
      "raw": "[스키마 기반 예시 데이터]"
    },
    "url": "{{BASE_URL}}[path]"
  },
  "event": [{
    "listen": "test",
    "script": {
      "exec": [
        "// 생성된 ID 자동 저장",
        "if (pm.response.code === 200 || pm.response.code === 201) {",
        "    const data = pm.response.json();",
        "    const id = data.id || data.seq || data.payload?.id || data.payload?.seq;",
        "    if (id) {",
        "        pm.collectionVariables.set('[ENTITY]_ID', id);",
        "        console.log('[저장] ID:', id);",
        "    }",
        "}"
      ]
    }
  }]
}
```

### GET (조회)

```json
{
  "name": "GET [리소스] 조회",
  "request": {
    "method": "GET",
    "header": [
      {"key": "Authorization", "value": "Bearer {{ACCESS_TOKEN}}"}
    ],
    "url": "{{BASE_URL}}[path]/{{[ENTITY]_ID}}"
  },
  "event": [{
    "listen": "test",
    "script": {
      "exec": [
        "pm.test('Status 200', function() {",
        "    pm.response.to.have.status(200);",
        "});",
        "",
        "pm.test('Response has data', function() {",
        "    const data = pm.response.json();",
        "    pm.expect(data).to.not.be.empty;",
        "});"
      ]
    }
  }]
}
```

### PUT (수정)

```json
{
  "name": "PUT [리소스] 수정",
  "request": {
    "method": "PUT",
    "header": [
      {"key": "Content-Type", "value": "application/json"},
      {"key": "Authorization", "value": "Bearer {{ACCESS_TOKEN}}"}
    ],
    "body": {
      "mode": "raw",
      "raw": "[스키마 기반 수정 데이터]"
    },
    "url": "{{BASE_URL}}[path]/{{[ENTITY]_ID}}"
  }
}
```

### DELETE (삭제)

```json
{
  "name": "DELETE [리소스] 삭제",
  "request": {
    "method": "DELETE",
    "header": [
      {"key": "Authorization", "value": "Bearer {{ACCESS_TOKEN}}"}
    ],
    "url": "{{BASE_URL}}[path]/{{[ENTITY]_ID}}"
  },
  "event": [{
    "listen": "test",
    "script": {
      "exec": [
        "pm.test('Delete successful', function() {",
        "    pm.expect(pm.response.code).to.be.oneOf([200, 204]);",
        "});"
      ]
    }
  }]
}
```

## 스키마 -> 예시 데이터 변환

```yaml
# Swagger Schema
CreateUserDto:
  type: object
  properties:
    name:
      type: string
      example: "홍길동"
    email:
      type: string
      format: email
    age:
      type: integer
      minimum: 0
```

```json
// Postman Body (자동 생성)
{
  "name": "테스트_{{timestamp}}",
  "email": "test_{{timestamp}}@example.com",
  "age": 25
}
```

**타입별 기본값:**

| Schema Type | 기본 예시값 |
|-------------|------------|
| string | `"테스트_{{timestamp}}"` |
| string (email) | `"test_{{timestamp}}@example.com"` |
| string (date) | `"2024-01-01"` |
| integer | `1` |
| number | `1.0` |
| boolean | `true` |
| array | `[]` |

## 순차 실행 순서

CRUD 순서로 자동 정렬:

```
1. POST (생성) -> ID 자동 저장
2. GET (목록)
3. GET (단건) -> 저장된 ID 사용
4. PUT (수정) -> 저장된 ID 사용
5. PATCH (부분수정) -> 저장된 ID 사용
6. DELETE (삭제) -> 저장된 ID 사용
```

## 출력 파일

```
collection/
+-- postman/
    +-- [API명]_Collection.json    # Postman Import용
    +-- README.md                  # 사용 가이드
```

## README.md (함께 생성)

```markdown
# [API명] Postman Collection

## Import 방법

1. Postman 실행
2. Import 버튼 클릭
3. 파일 선택: `[API명]_Collection.json`
4. Import 클릭

## 설정 방법

Collection Variables에서 설정:

| 변수 | 설명 | 예시 |
|------|------|------|
| BASE_URL | API 서버 주소 | https://api.example.com |
| ACCESS_TOKEN | 인증 토큰 | eyJhbGc... |

## 실행 방법

### 개별 실행
1. 원하는 요청 선택
2. Send 클릭

### 전체 순차 실행
1. Collection 우클릭 -> Run collection
2. Run 클릭

## 변수 설명

| 변수 | 자동/수동 | 설명 |
|------|----------|------|
| BASE_URL | 수동 | API 서버 주소 |
| ACCESS_TOKEN | 수동 | 인증 토큰 |
| timestamp | 자동 | 매 요청마다 생성 |
| [ENTITY]_ID | 자동 | POST 응답에서 저장 |
```

## 체크리스트

변환 완료 후 확인:

- [ ] Collection Variables에 BASE_URL 있는가?
- [ ] Pre-request Script에 timestamp 생성 있는가?
- [ ] POST 요청에 ID 자동 저장 있는가?
- [ ] 태그별로 Folder 구성되었는가?
- [ ] CRUD 순서로 정렬되었는가?
- [ ] 스키마 기반 예시 데이터 생성되었는가?
- [ ] README.md 함께 생성되었는가?
