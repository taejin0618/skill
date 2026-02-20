#!/usr/bin/env python3
"""
Happy Case 순수성 필터링 스크립트
생성된 테스트케이스 CSV에서 엣지케이스를 자동 감지하고 제거합니다.

사용법:
  python scripts/happy_case_filter.py <csv_파일_경로>

예:
  python scripts/happy_case_filter.py 로그인_테스트케이스.csv

동작 방식:
  CSV를 읽어 행별로 Happy/EXCLUDE 분류 후 EXCLUDE 행을 자동 제거합니다.
  원본 파일을 덮어씁니다. Section 구조(Happy Case가 있는 Section만)를 보존합니다.
"""

import csv
import sys
import re
from pathlib import Path


# ================================================================
# 분류 기준 키워드 정의
# (happy-case-extractor 기반 + 추가 강화)
# ================================================================

# Title 제외 키워드 (~45개)
EXCLUDE_TITLE_KEYWORDS = [
    '오류', '에러', '실패', 'error', 'fail',
    '잘못된', '유효하지 않은', '올바르지 않은', '틀린',
    '빈 값', '빈칸', '미입력', '입력하지 않', '입력 없이', '미선택',
    '접근 거부', '권한 없음', '권한없음', '차단', '금지',
    '중복', '이미 사용 중', '이미 존재', '재시도',
    '최댓값', '최솟값', '경계값', '경계',
    '불일치',
    # 추가 강화
    '초과', '미만', '부족', '만료', '타임아웃', '비정상', '예외', '누락', '위반',
]

# Expected Result 제외 키워드 (~20개)
EXCLUDE_EXPECTED_KEYWORDS = [
    '올바르지 않습니다', '오류 메시지', '에러 메시지', '오류가 발생',
    '다시 시도', '재입력', '필수 입력', '입력해주세요', '필수 항목',
    '빨간색 테두리', '붉은 테두리', '경고 아이콘', '오류 아이콘',
    '403', '404', '500', '접근 불가', '페이지를 찾을 수 없습니다',
    # 추가 강화
    '거부', '유효하지 않', '경고 메시지',
]

# Edge Case 제외 키워드 (~23개)
EXCLUDE_EDGE_KEYWORDS = [
    '특수문자', '이모지', '공백만', '줄바꿈만',
    '데이터 없음', '0건', '빈 목록', '연결 끊김',
    '동시에', '중복 요청', '연속 클릭', '이중 제출',
    '뒤로가기', '새로고침 후', '브라우저 닫기', '브라우저 탭 전환',
    '세션 만료', '타임아웃', '토큰 만료',
    '최대 글자수', '자 초과', '자 미만',
    # 추가 강화
    'XSS', 'SQL', '인젝션', '스크립트', '네트워크 끊김', '오프라인',
]

# Steps 제외 정규식 패턴 (~12개)
EXCLUDE_STEPS_PATTERNS = [
    r'비워\s*두고',
    r'아무것도\s*입력하지\s*않',
    r'잘못된\s*.+\s*(형식|값|데이터)',
    r'허용되지\s*않는',
    r'권한\s*없는\s*상태',
    r'로그아웃\s*상태',
    r'<script',
    r"'\s*OR\s*'",
    r'이모지',
    # 추가 강화
    r'존재하지\s*않는',
    r'만료된\s*(토큰|세션|링크)',
    r'삭제된\s*(계정|데이터|파일)',
]


# ================================================================
# 분류 함수
# ================================================================

def is_section_row(row):
    """Section 헤더 행인지 확인 (Title이 비어있는 행)"""
    return not row.get('Title', '').strip()


def classify_row(row):
    """
    단일 행을 분류한다.
    반환: ('HAPPY' | 'EXCLUDE', 판단_근거)
    """
    title = row.get('Title', '').strip()
    steps = row.get('Steps', '').strip()
    expected = row.get('Expected Result', '').strip()

    # 1순위: Expected Result 오류 패턴
    for keyword in EXCLUDE_EXPECTED_KEYWORDS:
        if keyword in expected:
            return 'EXCLUDE', f"Expected Result에 '{keyword}' 포함"

    # 2순위: Title 오류 키워드
    for keyword in EXCLUDE_TITLE_KEYWORDS:
        if keyword in title:
            return 'EXCLUDE', f"Title에 '{keyword}' 포함"

    # 3순위: Steps 비정상 패턴
    for pattern in EXCLUDE_STEPS_PATTERNS:
        if re.search(pattern, steps):
            return 'EXCLUDE', f"Steps 패턴 감지"

    # 4순위: Edge Case 키워드 (Title + Steps + Expected Result)
    combined = title + ' ' + steps + ' ' + expected
    for keyword in EXCLUDE_EDGE_KEYWORDS:
        if keyword in combined:
            return 'EXCLUDE', f"Edge 키워드 '{keyword}' 감지"

    return 'HAPPY', ''


# ================================================================
# 메인 필터링 로직
# ================================================================

def filter_happy_cases(csv_filepath):
    """
    CSV에서 엣지케이스를 제거하고 원본 파일을 덮어쓴다.
    반환: 종료 코드 (0: 정상, 2: 파일 오류)
    """
    input_path = Path(csv_filepath)

    if not input_path.exists():
        print(f"오류: 파일을 찾을 수 없습니다: {csv_filepath}", file=sys.stderr)
        return 2

    print("🔍 Happy Case 순수성 검증 및 필터링")
    print()

    # CSV 읽기
    all_rows = []
    fieldnames = None
    try:
        with open(input_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames

            if not fieldnames:
                print("오류: CSV 헤더가 없습니다.", file=sys.stderr)
                return 2

            required_cols = [
                'Section', 'Section Hierarchy', 'Title',
                'Preconditions', 'Steps', 'Expected Result', 'Priority'
            ]
            missing = set(required_cols) - set(fieldnames)
            if missing:
                print(f"오류: 필수 컬럼 누락: {', '.join(missing)}", file=sys.stderr)
                return 2

            for row in reader:
                all_rows.append(dict(row))

    except UnicodeDecodeError:
        print("오류: UTF-8 인코딩이 아닙니다.", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"오류: 파일 읽기 실패 - {e}", file=sys.stderr)
        return 2

    # 분류 수행
    classification = []  # (row, label, reason, original_row_num)
    stats = {'total': 0, 'happy': 0, 'exclude': 0}
    excluded_details = []

    for idx, row in enumerate(all_rows, start=2):  # start=2: 헤더가 1행
        if is_section_row(row):
            classification.append((row, 'SECTION', '', idx))
        else:
            label, reason = classify_row(row)
            classification.append((row, label, reason, idx))
            stats['total'] += 1
            if label == 'HAPPY':
                stats['happy'] += 1
            else:
                stats['exclude'] += 1
                title_preview = row.get('Title', '')[:40]
                excluded_details.append((idx, title_preview, reason))

    # Section 행 포함 여부 결정 (Happy Case가 있는 Section만 유지)
    # 키: (Section, Section Hierarchy) 튜플 — 동일 Section명이 다른 Hierarchy에 존재해도 구분
    section_has_happy = {}
    current_section_key = None

    for row, label, _, *_ in classification:
        if label == 'SECTION':
            current_section_key = (row.get('Section', ''), row.get('Section Hierarchy', ''))
            if current_section_key not in section_has_happy:
                section_has_happy[current_section_key] = False
        elif label == 'HAPPY' and current_section_key is not None:
            section_has_happy[current_section_key] = True

    # 출력 행 목록 구성
    output_rows = []
    current_section_key = None

    for row, label, _, *_ in classification:
        if label == 'SECTION':
            current_section_key = (row.get('Section', ''), row.get('Section Hierarchy', ''))
            if section_has_happy.get(current_section_key, False):
                output_rows.append(row)
        elif label == 'HAPPY':
            output_rows.append(row)
        # EXCLUDE는 건너뜀

    # 통계 출력
    print(f"- 전체 테스트케이스: {stats['total']}개")
    print(f"- Happy Case: {stats['happy']}개 (유지)")
    print(f"- 제거된 비-Happy 케이스: {stats['exclude']}개")

    if excluded_details:
        for row_num, title, reason in excluded_details:
            print(f"  행 {row_num}: \"{title}\" → {reason}")

    print()

    # 원본 파일 덮어쓰기
    output_cols = [
        'Section', 'Section Hierarchy', 'Title',
        'Preconditions', 'Steps', 'Expected Result', 'Priority'
    ]
    try:
        with open(input_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=output_cols,
                quoting=csv.QUOTE_ALL,
                extrasaction='ignore'
            )
            writer.writeheader()
            writer.writerows(output_rows)
    except Exception as e:
        print(f"오류: 파일 저장 실패 - {e}", file=sys.stderr)
        return 2

    print(f"✅ 필터링 완료: {stats['happy']}개 순수 Happy Case만 남았습니다.")
    return 0


def main():
    if len(sys.argv) < 2:
        print("사용법: python scripts/happy_case_filter.py <csv_파일_경로>")
        print()
        print("예:")
        print("  python scripts/happy_case_filter.py 로그인_테스트케이스.csv")
        sys.exit(1)

    exit_code = filter_happy_cases(sys.argv[1])
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
