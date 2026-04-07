# 응답 파싱 패턴 카탈로그

API 응답 구조가 일관되지 않을 때 유연하게 데이터를 추출하는 패턴 모음.

## 패턴 1: 유연한 리스트 추출

API마다 응답 구조가 다르다. `{"data": [...]}` 형태일 수도 있고, 바로 `[...]`일 수도 있다.
이 패턴 하나로 둘 다 처리한다.

```python
data = res.json()
items = data.get("data", data) if isinstance(data, dict) else data

# 사용 예시
print(f"조회 건수: {len(items)}건")
```

## 패턴 2: ID 리스트 추출

목록에서 특정 ID 존재 여부를 확인할 때 먼저 ID 리스트를 만든다.

```python
# 기본: id 필드 추출
ids = [item.get("id") for item in items]

# 문자열 변환 필요 시 (비교 타입 맞추기)
ids = [str(item.get("id")) for item in items]

# 중첩된 ID 추출 (예: 카트의 프레임 ID)
frame_ids = [
    str(item.get("frame", {}).get("id", item.get("frameId", "")))
    for item in cart_items
]
```

## 패턴 3: next()로 특정 항목 찾기

목록에서 조건에 맞는 항목 하나를 찾을 때 사용. 없으면 None 반환.

```python
# ID로 특정 항목 찾기
found = next((i for i in items if i.get("id") == target_id), None)
assert found is not None, f"항목(ID:{target_id}) 없음!"

# 조건으로 항목 찾기
ko_detail = next(
    (d for d in details if d.get("languageCode", "").upper() == "KO"),
    details[0] if details else None
)
```

## 패턴 4: 중첩 필드 안전 접근

깊은 구조의 데이터를 안전하게 접근할 때 `.get()` 체이닝 사용.

```python
# 1단계 중첩
frame_id = item.get("frame", {}).get("id")

# 2단계 이상
value = data.get("result", {}).get("detail", {}).get("name", "기본값")

# 배열의 첫 번째 항목 안전 접근
first = items[0] if items else {}
name = first.get("name", "")
```

## 패턴 5: Fallback 데이터 추출

API 응답 필드명이 불확실할 때 여러 필드를 순차적으로 시도.

```python
# 필드명이 API마다 다를 때
search_keyword = (
    item.get("name")
    or item.get("title")
    or item.get("keyword")
    or "기본검색어"
)

# 생성된 ID 추출 (id 또는 seq)
created_id = data.get("id") or data.get("seq") or data.get("idx")
```

## 패턴 6: 페이징 응답 처리

페이징 응답의 구조가 다양할 때 대응하는 패턴.

```python
data = res.json()

# Spring 스타일 페이징
if "content" in data:
    items = data["content"]
    total = data.get("totalElements", len(items))
# Photoism 스타일 페이징
elif "data" in data:
    items = data["data"]
    total = data.get("total", len(items))
# 단순 배열
elif isinstance(data, list):
    items = data
    total = len(items)
else:
    items = []
    total = 0
```
