# Assert 패턴 카탈로그

E2E API 테스트에서 자주 사용하는 검증 패턴 모음.
모든 assert에는 실패 시 원인 파악이 쉽도록 힌트 메시지를 포함한다.

## 1. 상태 코드 검증

```python
# 기본: 단일 상태 코드
assert res.status_code == 200, \
    f"실패! 예상: 200, 실제: {res.status_code}\n힌트: 401=토큰만료, 404=없음, 500=서버오류"

# 복수 허용 (생성은 200 또는 201)
assert res.status_code in [200, 201], \
    f"실패! 예상: 200/201, 실제: {res.status_code}"

# 알려진 버그 대응 (서버가 500을 반환하지만 실제로는 생성됨)
assert res.status_code in [201, 500], \
    f"실패! 상태코드: {res.status_code}\n참고: 현재 버그로 500 반환하지만 실제 생성됨"
```

## 2. 목록 포함 확인 (ID가 목록에 있는지)

```python
# 신규 항목이 목록에 존재하는지
ids = [item.get("id") for item in items]
assert target_id in ids, \
    f"목록에 ID:{target_id} 없음! 전체: {ids[:5]}..."

# 문자열 변환 후 비교 (타입 불일치 방지)
ids = [str(item.get("id")) for item in items]
assert str(target_id) in ids, \
    f"목록에 ID:{target_id} 없음!"
```

## 3. 목록 부재 확인 (삭제 후 없는지)

```python
# 삭제된 항목이 목록에 없는지
ids = [item.get("id") for item in items]
assert target_id not in ids, \
    f"삭제 후에도 ID:{target_id} 존재!"
```

## 4. 교차 API 필드 비교

```python
# App 데이터와 Admin 데이터의 필드별 일치 확인
assert admin_data.get("email") == app_data.get("email"), \
    f"이메일 불일치! App: {app_data.get('email')}, Admin: {admin_data.get('email')}"

assert admin_data.get("nickname") == app_data.get("nickname"), \
    f"닉네임 불일치! App: {app_data.get('nickname')}, Admin: {admin_data.get('nickname')}"
```

## 5. 데이터 존재 확인

```python
# 필드 존재 여부
assert "id" in data, "응답에 id 필드 없음"
assert data.get("id") is not None, "id 값이 null"

# 리스트가 비어있지 않은지
assert len(items) > 0, "목록이 비어있음"

# next()로 찾은 항목 존재 확인
found = next((i for i in items if i.get("id") == target_id), None)
assert found is not None, f"항목(ID:{target_id}) 없음!"
```

## 6. 값 일치 확인

```python
# 수량/숫자 일치
assert item.get("quantity") == 6, \
    f"수량 불일치! 기대: 6, 실제: {item.get('quantity')}"

# Boolean 상태 확인
assert data.get("enabled") == False, \
    f"비활성화 후에도 enabled={data.get('enabled')}"

# 빈 결과 확인 (검색 결과 없음 등)
assert len(items) == 0, \
    f"결과가 있으면 안 됨! 실제: {len(items)}건"

total = data.get("total", -1)
assert total == 0, f"예상 total=0, 실제: {total}"
```

## 7. 집합 관계 확인

```python
# 정확 검색 결과가 부분 검색 결과의 서브셋인지
exact_ids = {r.get("id") for r in exact_results}
partial_ids = {r.get("id") for r in partial_results}
assert exact_ids.issubset(partial_ids), \
    f"정확 검색이 부분 검색의 서브셋 아님!\n정확: {exact_ids}\n부분: {partial_ids}"
```

## 8. 응답 본문 포함 로깅

assert만으로 원인 파악이 어려울 때, 실패 메시지에 응답 본문 일부를 포함한다.

```python
assert res.status_code == 201, \
    f"생성 실패! 상태: {res.status_code}\n응답: {res.text[:200]}"
```
