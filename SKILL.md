---
name: api-test-generator
description: >
  초보자 친화적 API 테스트 코드 생성기. Swagger/OpenAPI 또는 수동 입력으로 pytest 테스트 생성.
  트리거: (1) "API 테스트 코드 만들어줘" (2) "Swagger로 pytest 생성" (3) "API 테스트 작성해줘"
  (4) swagger.json 업로드 후 테스트 요청 (5) "엔드포인트 테스트 코드" (6) "requests로 API 테스트"
  (7) "generate API test" (8) "create pytest from Swagger" (9) "API test code".
  출력: Python requests 기반 pytest 테스트 코드. 초보자 1-2주 학습으로 작성 가능.
---

# API Test Generator

Swagger/OpenAPI 명세 또는 수동 입력으로 초보자 친화적인 pytest 테스트 코드를 생성한다.

## 핵심 철학: 극단적 단순화

```
목표: QA 초보자도 1-2주 학습으로 API 테스트 작성 가능
초보자 친화도: 5/5
필요 지식: Python 기초 + requests + pytest assert만
```

## 입력 방식

### 방식 1: Swagger/OpenAPI 자동 분석

Swagger 파일 업로드 시 자동으로:
1. 모든 엔드포인트 추출
2. 각 엔드포인트별 테스트 코드 생성
3. 스키마 기반 검증 코드 포함

### 방식 2: 수동 정보 입력

Swagger 없을 때 사용자가 제공:
- API 기본 URL
- 엔드포인트 경로
- HTTP 메서드
- 요청/응답 구조

## 절대 원칙 (Always Do)

1. **requests 라이브러리** 사용
2. **Given-When-Then** 구조로 테스트 작성
3. **print() 로깅** (요청/응답/데이터 출력)
4. **직접 assert** 사용 (검증 함수 만들지 않음)
5. **f-string으로 URL** 직접 생성
6. **친절한 에러 메시지** 포함
7. **상세한 주석** 달기

## 엄격한 금지 (Never Do)

1. pytest fixtures 사용 금지
2. helper 함수 생성 금지
3. logging 모듈 사용 금지
4. 별도 검증 함수 생성 금지

## 프로젝트 구조

```
project/
├── tests/
│   ├── conftest.py              # 설정값만
│   ├── [api_group]/
│   │   ├── test_get_[기능].py
│   │   ├── test_post_[기능].py
│   │   ├── test_put_[기능].py
│   │   └── test_delete_[기능].py
├── pytest.ini
└── requirements.txt
```

## conftest.py 템플릿

```python
"""
[설정] 공통 설정값
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

수정할 곳: 아래 인증 방식 중 하나를 선택하고 값을 입력하세요!

사용법:
    from tests.conftest import BASE_URL, HEADERS
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# [수정] 여기만 수정하세요!
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# (1) API 서버 주소
BASE_URL = "https://api.example.com"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# (2) 인증 방식 선택 (하나만 사용하세요)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# -- 방식 A: Bearer 토큰 (가장 일반적) --
API_TOKEN = "your-token-here"
HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# -- 방식 B: API Key 헤더 (주석 해제 후 사용) --
# HEADERS = {
#     "Accept": "application/json",
#     "X-API-Key": "your-api-key-here",
#     "Content-Type": "application/json"
# }

# -- 방식 C: 인증 없음 (공개 API) --
# HEADERS = {
#     "Accept": "application/json",
#     "Content-Type": "application/json"
# }
```

## 테스트 파일 템플릿 (복사-붙여넣기용)

### GET - 단건 조회

```python
"""
[기능명] 조회 테스트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
엔드포인트: GET /api/v1/[경로]
설명: [리소스]를 ID로 조회합니다

실행: pytest tests/[폴더]/test_get_[기능].py -v
"""

import json
import requests
from tests.conftest import BASE_URL, HEADERS


def test_조회_성공():
    """
    정상 케이스: ID로 조회 성공
    """
    print("\n" + "="*60)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # [수정] 수정할 부분 (2곳)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    resource_id = 1                           # <-- (1) 조회할 ID
    url = f"{BASE_URL}/api/v1/resources/{resource_id}"  # <-- (2) API 경로
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    # Given: 테스트 준비 완료
    print(f"[조회] 테스트 대상 ID: {resource_id}")

    # When: API 호출
    print(f"[요청] GET {url}")
    response = requests.get(url, headers=HEADERS)

    # Then: 응답 검증
    print(f"[응답] 응답 코드: {response.status_code}")

    # 응답 코드 확인 (200 = 성공)
    assert response.status_code == 200, \
        f"[FAIL] 실패! 예상: 200, 실제: {response.status_code}\n" \
        f"힌트: 401=토큰만료, 404=ID없음, 500=서버오류"

    # 응답 데이터 확인
    data = response.json()
    print("[데이터] 응답 데이터:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # [수정] 필드 검증 (필요한 필드로 수정)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    assert "id" in data, "[FAIL] id 필드가 없습니다"
    assert "name" in data, "[FAIL] name 필드가 없습니다"

    print(f"[PASS] 테스트 통과!")
    print("="*60)


def test_조회_존재하지않는ID():
    """
    에러 케이스: 없는 ID로 조회 시 404
    """
    print("\n" + "="*60)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # [수정] 수정할 부분
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    url = f"{BASE_URL}/api/v1/resources/99999999"  # <- 없는 ID
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    # When: API 호출
    print(f"[요청] GET {url}")
    response = requests.get(url, headers=HEADERS)

    # Then: 404 확인
    print(f"[응답] 응답 코드: {response.status_code}")
    assert response.status_code == 404, \
        f"[FAIL] 실패! 예상: 404, 실제: {response.status_code}"

    print(f"[PASS] 테스트 통과! (404 정상 반환)")
    print("="*60)
```

### GET - 목록 조회 (페이징)

```python
"""
[기능명] 목록 조회 테스트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
엔드포인트: GET /api/v1/[경로]
설명: [리소스] 목록을 페이징으로 조회합니다
"""

import json
import requests
from tests.conftest import BASE_URL, HEADERS


def test_목록조회_성공():
    """
    정상 케이스: 목록 조회 성공
    """
    print("\n" + "="*60)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # [수정] 수정할 부분
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    url = f"{BASE_URL}/api/v1/resources"  # <- API 경로
    params = {"page": 0, "size": 10}      # <- 페이징 파라미터
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    # When: API 호출
    print(f"[요청] GET {url}")
    print(f"[파라미터] {params}")
    response = requests.get(url, headers=HEADERS, params=params)

    # Then: 응답 검증
    print(f"[응답] 응답 코드: {response.status_code}")
    assert response.status_code == 200, \
        f"[FAIL] 실패! 예상: 200, 실제: {response.status_code}"

    data = response.json()

    # 페이징 응답 구조 확인 (API에 따라 다를 수 있음)
    if "content" in data:
        # Spring 스타일 페이징
        print(f"[결과] 조회 건수: {len(data['content'])}건")
        assert isinstance(data["content"], list), "[FAIL] content가 배열이 아닙니다"
    elif isinstance(data, list):
        # 단순 배열 응답
        print(f"[결과] 조회 건수: {len(data)}건")
    else:
        print(f"[데이터] 응답: {json.dumps(data, indent=2, ensure_ascii=False)}")

    print(f"[PASS] 테스트 통과!")
    print("="*60)
```

### POST - 생성

```python
"""
[기능명] 생성 테스트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
엔드포인트: POST /api/v1/[경로]
설명: 새 [리소스]를 생성합니다
"""

import json
import datetime
import requests
from tests.conftest import BASE_URL, HEADERS


def test_생성_성공():
    """
    정상 케이스: 새 리소스 생성 성공
    """
    print("\n" + "="*60)

    # 타임스탬프로 유니크한 테스트 데이터 생성
    # (같은 테스트 여러 번 실행해도 중복 안 됨)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # [수정] 수정할 부분
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    url = f"{BASE_URL}/api/v1/resources"  # <- API 경로

    # 생성할 데이터 (API 스펙에 맞게 수정)
    create_data = {
        "name": f"테스트_{timestamp}",
        "description": "자동 생성된 테스트 데이터"
    }
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    # When: API 호출
    print(f"[요청] POST {url}")
    print(f"[데이터] 요청 데이터:")
    print(json.dumps(create_data, indent=2, ensure_ascii=False))

    response = requests.post(url, headers=HEADERS, json=create_data)

    # Then: 응답 검증
    print(f"[응답] 응답 코드: {response.status_code}")

    # 생성 성공은 보통 200 또는 201
    assert response.status_code in [200, 201], \
        f"[FAIL] 실패! 예상: 200 또는 201, 실제: {response.status_code}\n" \
        f"응답: {response.text[:200]}"

    data = response.json()
    print(f"[데이터] 응답 데이터:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # 생성된 ID 확인 (필드명은 API에 따라 다름: id, seq, idx 등)
    assert "id" in data or "seq" in data, \
        "[FAIL] 생성된 ID가 응답에 없습니다"

    created_id = data.get("id") or data.get("seq")
    print(f"[PASS] 테스트 통과! 생성된 ID: {created_id}")
    print("="*60)


def test_생성_필수필드누락():
    """
    에러 케이스: 필수 필드 누락 시 400
    """
    print("\n" + "="*60)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # [수정] 수정할 부분
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    url = f"{BASE_URL}/api/v1/resources"  # <- API 경로
    # 의도적으로 빈 데이터 또는 필수 필드 누락
    invalid_data = {}
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    # When: 잘못된 데이터로 API 호출
    print(f"[요청] POST {url} (필수 필드 누락)")
    response = requests.post(url, headers=HEADERS, json=invalid_data)

    # Then: 400 Bad Request 확인
    print(f"[응답] 응답 코드: {response.status_code}")
    assert response.status_code == 400, \
        f"[FAIL] 실패! 예상: 400, 실제: {response.status_code}\n" \
        f"힌트: 필수 필드 누락 시 400이 반환되어야 합니다"

    print(f"[PASS] 테스트 통과! (400 정상 반환)")
    print("="*60)
```

### PUT - 수정

```python
"""
[기능명] 수정 테스트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
엔드포인트: PUT /api/v1/[경로]/{id}
설명: 기존 [리소스]를 수정합니다
"""

import json
import datetime
import requests
from tests.conftest import BASE_URL, HEADERS


def test_수정_성공():
    """
    정상 케이스: 리소스 수정 성공
    """
    print("\n" + "="*60)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # [수정] 수정할 부분
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    resource_id = 1  # <- 수정할 리소스 ID
    url = f"{BASE_URL}/api/v1/resources/{resource_id}"

    # 수정할 데이터
    update_data = {
        "name": f"수정됨_{timestamp}"
    }
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    # When: API 호출
    print(f"[요청] PUT {url}")
    print(f"[데이터] 수정 데이터:")
    print(json.dumps(update_data, indent=2, ensure_ascii=False))

    response = requests.put(url, headers=HEADERS, json=update_data)

    # Then: 응답 검증
    print(f"[응답] 응답 코드: {response.status_code}")
    assert response.status_code == 200, \
        f"[FAIL] 실패! 예상: 200, 실제: {response.status_code}"

    data = response.json()

    # 수정된 값 확인
    if "name" in data:
        assert data["name"] == update_data["name"], \
            f"[FAIL] 수정이 반영되지 않음. 예상: {update_data['name']}, 실제: {data['name']}"

    print(f"[PASS] 테스트 통과!")
    print("="*60)
```

### DELETE - 삭제

```python
"""
[기능명] 삭제 테스트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
엔드포인트: DELETE /api/v1/[경로]/{id}
설명: [리소스]를 삭제합니다

주의: 실제 데이터가 삭제됩니다!
"""

import requests
from tests.conftest import BASE_URL, HEADERS


def test_삭제_성공():
    """
    정상 케이스: 리소스 삭제 성공
    """
    print("\n" + "="*60)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # [수정] 수정할 부분
    # 삭제해도 되는 테스트용 ID를 사용하세요!
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    resource_id = 999  # <- 삭제할 ID (테스트용)
    url = f"{BASE_URL}/api/v1/resources/{resource_id}"
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    # When: API 호출
    print(f"[요청] DELETE {url}")
    response = requests.delete(url, headers=HEADERS)

    # Then: 응답 검증
    print(f"[응답] 응답 코드: {response.status_code}")

    # 삭제 성공은 보통 200 또는 204 (No Content)
    assert response.status_code in [200, 204], \
        f"[FAIL] 실패! 예상: 200 또는 204, 실제: {response.status_code}"

    print(f"[PASS] 테스트 통과! 삭제 완료")
    print("="*60)
```

## Swagger 분석 시 추출 항목

| Swagger 필드 | 추출 정보 | 테스트 코드 활용 |
|-------------|----------|----------------|
| paths | 엔드포인트 목록 | URL 생성 |
| methods | HTTP 메서드 | requests.get/post/put/delete |
| parameters | 경로/쿼리 파라미터 | Given 섹션 |
| requestBody | 요청 본문 구조 | json= 파라미터 |
| responses | 응답 코드/구조 | assert 검증 |
| schemas | DTO 필드 정보 | 필드 검증 |

## 실행 방법 (단계별 가이드)

### 1단계: 터미널 열기

```
Mac: Cmd + Space -> "터미널" 검색 -> Enter
Windows: Win + R -> "cmd" 입력 -> Enter
```

### 2단계: 프로젝트 폴더로 이동

```bash
cd /path/to/your/project
```

### 3단계: 패키지 설치 (최초 1회)

```bash
pip install pytest requests
```

### 4단계: 테스트 실행

```bash
# 전체 테스트
pytest tests/ -v

# 특정 파일만
pytest tests/user_api/test_get_사용자.py -v

# print 출력 보기 (디버깅용)
pytest tests/ -vvs
```

### 결과 읽는 법

```
PASSED  = 성공 (초록색)
FAILED  = 실패 (빨간색) - 아래에 원인 표시됨
SKIPPED = 건너뜀
```

## 트러블슈팅 가이드

### "ModuleNotFoundError: No module named 'requests'"

```bash
# 해결: requests 설치
pip install requests
```

### "ModuleNotFoundError: No module named 'tests'"

```bash
# 해결: 프로젝트 루트 폴더에서 실행하세요
cd /path/to/project  # tests/ 폴더가 있는 곳
pytest tests/ -v
```

### "connection refused" 또는 "timeout"

```
확인사항:
1. BASE_URL이 올바른가? (conftest.py 확인)
2. 서버가 실행 중인가?
3. VPN 연결이 필요한가?
4. 방화벽이 막고 있나?
```

### "401 Unauthorized"

```
해결:
1. conftest.py의 API_TOKEN이 만료됨
2. 새 토큰을 발급받아 교체하세요
```

### "404 Not Found"

```
확인사항:
1. URL 경로가 올바른가?
2. resource_id가 실제로 존재하는가?
3. API 버전(v1, v2)이 맞는가?
```

### "assert 200 == 500"

```
서버 오류:
1. 요청 데이터 형식이 올바른가?
2. 필수 필드가 누락되지 않았나?
3. 서버 로그 확인 필요
```

## 자주 묻는 질문

### "fixture 쓰면 안 되나요?"
-> 사용하지 마세요. 코드가 복잡해지고 초보자가 이해하기 어렵습니다.

### "URL 함수 만들면 편하지 않나요?"
-> 만들지 마세요. f-string 복사/붙여넣기가 더 명확합니다.

### "검증 코드가 반복되는데요?"
-> 괜찮습니다. 반복이 추상화보다 이해하기 쉽습니다.

### "한글 함수명 써도 되나요?"
-> 네! `def test_사용자_조회_성공():` 가독성이 더 좋습니다.

## 체크리스트

테스트 작성 후 확인:

- [ ] conftest.py에 BASE_URL, API_TOKEN 설정했는가?
- [ ] `from tests.conftest import BASE_URL, HEADERS` 있는가?
- [ ] Given-When-Then 구조인가?
- [ ] f-string으로 URL 직접 생성했는가?
- [ ] print() 로깅을 추가했는가?
- [ ] 응답 코드 검증에 힌트 메시지 있는가?
- [ ] fixture나 helper 함수 없는가?
