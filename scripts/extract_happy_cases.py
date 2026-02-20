#!/usr/bin/env python3
"""
Happy Case 추출 스크립트
기존 테스트케이스 CSV에서 Happy Case만 추출하여 새 CSV 파일을 생성합니다.

사용법:
  python extract_happy_cases.py <입력_CSV_파일_경로>

예:
  python extract_happy_cases.py 로그인_테스트케이스.csv
  → 출력: 로그인_테스트케이스_happy.csv

동작 방식:
  AI(Claude)가 분류한 결과를 키워드 기반으로 자동 필터링합니다.
  Section 구조를 보존하며, Happy Case가 있는 Section만 포함합니다.
  출력 파일은 원본과 동일한 7컬럼 TestRail 호환 CSV 형식입니다.
"""

import csv
import sys
import re
from pathlib import Path


# ================================================================
# 분류 기준 키워드 정의
# (references/happy-case-criteria.md 기준과 동일)
# ================================================================

# Title 제외 키워드 - 있으면 EXCLUDE
EXCLUDE_TITLE_KEYWORDS = [
    '오류', '에러', '실패', 'error', 'fail',
    '잘못된', '유효하지 않은', '올바르지 않은', '틀린',
    '빈 값', '빈칸', '미입력', '입력하지 않', '입력 없이', '미선택',
    '접근 거부', '권한 없음', '권한없음', '차단', '금지',
    '중복', '이미 사용 중', '이미 존재', '재시도',
    '최댓값', '최솟값', '경계값', '경계', '경계',
    '불일치',
]

# Expected Result 제외 키워드 - 있으면 EXCLUDE
EXCLUDE_EXPECTED_KEYWORDS = [
    '올바르지 않습니다', '오류 메시지', '에러 메시지', '오류가 발생',
    '다시 시도', '재입력', '필수 입력', '입력해주세요', '필수 항목',
    '빨간색 테두리', '붉은 테두리', '경고 아이콘', '오류 아이콘',
    '403', '404', '500', '접근 불가', '페이지를 찾을 수 없습니다',
]

# Edge Case 제외 키워드 - Title 또는 Steps에 있으면 EXCLUDE
EXCLUDE_EDGE_KEYWORDS = [
    '특수문자', '이모지', '공백만', '줄바꿈만',
    '데이터 없음', '0건', '빈 목록', '연결 끊김',
    '동시에', '중복 요청', '연속 클릭', '이중 제출',
    '뒤로가기', '새로고침 후', '브라우저 닫기', '탭 전환',
    '세션 만료', '타임아웃', '토큰 만료',
    '최대 글자수', '자 초과', '자 미만',
]

# Steps 제외 정규식 패턴
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
            return 'EXCLUDE', f"Expected Result: '{keyword}'"

    # 2순위: Title 오류 키워드
    for keyword in EXCLUDE_TITLE_KEYWORDS:
        if keyword in title:
            return 'EXCLUDE', f"Title: '{keyword}'"

    # 3순위: Steps 비정상 패턴
    for pattern in EXCLUDE_STEPS_PATTERNS:
        if re.search(pattern, steps):
            return 'EXCLUDE', f"Steps 제외 패턴 감지"

    # 4순위: Edge Case 키워드 (Title + Steps)
    combined = title + ' ' + steps
    for keyword in EXCLUDE_EDGE_KEYWORDS:
        if keyword in combined:
            return 'EXCLUDE', f"Edge Case 키워드: '{keyword}'"

    return 'HAPPY', '제외 키워드 없음 → Happy Case'


# ================================================================
# 메인 추출 로직
# ================================================================

def extract_happy_cases(input_filepath):
    """
    입력 CSV에서 Happy Case만 추출하여 새 파일을 생성한다.
    반환: (출력_파일_경로, 통계_딕셔너리)
    """
    input_path = Path(input_filepath)

    if not input_path.exists():
        print(f"오류: 파일을 찾을 수 없습니다: {input_filepath}")
        sys.exit(1)

    # 출력 파일명: [원본]_happy.csv
    output_path = input_path.parent / f"{input_path.stem}_happy{input_path.suffix}"

    print("=" * 70)
    print("Happy Case 추출 스크립트")
    print("=" * 70)
    print(f"입력 파일: {input_path.name}")
    print(f"출력 파일: {output_path.name}")
    print()

    # CSV 읽기 (UTF-8)
    all_rows = []
    fieldnames = None
    try:
        with open(input_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames

            if not fieldnames:
                print("오류: CSV 헤더가 없습니다.")
                sys.exit(1)

            required_cols = [
                'Section', 'Section Hierarchy', 'Title',
                'Preconditions', 'Steps', 'Expected Result', 'Priority'
            ]
            missing = set(required_cols) - set(fieldnames)
            if missing:
                print(f"오류: 필수 컬럼 누락: {', '.join(missing)}")
                sys.exit(1)

            for row in reader:
                all_rows.append(dict(row))

    except UnicodeDecodeError:
        print("오류: UTF-8 인코딩이 아닙니다. UTF-8로 저장 후 다시 시도하세요.")
        sys.exit(1)
    except Exception as e:
        print(f"오류: 파일 읽기 실패 - {e}")
        sys.exit(1)

    print(f"전체 행 수 (헤더 제외): {len(all_rows)}개")
    print()

    # ----------------------------------------------------------------
    # 분류 수행
    # ----------------------------------------------------------------
    print("분류 결과:")
    print("-" * 70)
    print(f"{'행':>4} | {'분류':^7} | {'Title (최대 28자)':<30} | 근거")
    print("-" * 70)

    classification = []  # (row, label, reason)
    stats = {'total': 0, 'happy': 0, 'exclude': 0, 'section': 0}

    for idx, row in enumerate(all_rows, start=2):
        if is_section_row(row):
            classification.append((row, 'SECTION', ''))
            stats['section'] += 1
            name = (row.get('Section', '') or '(Section 행)')[:30]
            print(f"{idx:>4} | {'SECTION':^7} | {name:<30} | Section 헤더")
        else:
            label, reason = classify_row(row)
            classification.append((row, label, reason))
            stats['total'] += 1
            if label == 'HAPPY':
                stats['happy'] += 1
            else:
                stats['exclude'] += 1
            title_preview = row.get('Title', '')[:28]
            print(f"{idx:>4} | {label:^7} | {title_preview:<30} | {reason}")

    print("-" * 70)
    print()

    # ----------------------------------------------------------------
    # Section 행 포함 여부 결정
    # ----------------------------------------------------------------
    # 각 Section 내 Happy Case 존재 여부 파악
    section_has_happy = {}
    current_section = None

    for row, label, _ in classification:
        if label == 'SECTION':
            current_section = row.get('Section', '')
            if current_section not in section_has_happy:
                section_has_happy[current_section] = False
        elif label == 'HAPPY' and current_section is not None:
            section_has_happy[current_section] = True

    # ----------------------------------------------------------------
    # 출력 행 목록 구성 (원본 데이터 그대로 사용)
    # ----------------------------------------------------------------
    output_rows = []
    current_section = None

    for row, label, _ in classification:
        if label == 'SECTION':
            current_section = row.get('Section', '')
            if section_has_happy.get(current_section, False):
                output_rows.append(row)
        elif label == 'HAPPY':
            output_rows.append(row)
        # EXCLUDE는 건너뜀

    # ----------------------------------------------------------------
    # 출력 파일 저장 (기존과 동일한 7컬럼 형식, 원본 값 그대로)
    # ----------------------------------------------------------------
    output_cols = [
        'Section', 'Section Hierarchy', 'Title',
        'Preconditions', 'Steps', 'Expected Result', 'Priority'
    ]

    try:
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=output_cols,
                quoting=csv.QUOTE_ALL,
                extrasaction='ignore'
            )
            writer.writeheader()
            writer.writerows(output_rows)
    except Exception as e:
        print(f"오류: 파일 저장 실패 - {e}")
        sys.exit(1)

    # ----------------------------------------------------------------
    # 결과 요약 출력
    # ----------------------------------------------------------------
    print("=" * 70)
    print("추출 완료 요약")
    print("=" * 70)
    print(f"입력 파일        : {input_path.name}")
    print(f"출력 파일        : {output_path.name}")
    print(f"전체 테스트케이스 : {stats['total']}개")
    print(f"Happy Case 추출  : {stats['happy']}개")
    print(f"제외된 케이스    : {stats['exclude']}개")

    if stats['total'] > 0:
        rate = stats['happy'] / stats['total'] * 100
        print(f"추출률           : {rate:.1f}%")

    print()
    print(f"출력 파일 위치: {output_path}")
    print()
    print("다음 단계 (검증):")
    print(f"  python scripts/validate_csv.py \"{output_path}\"")
    print(f"  python scripts/testrail_upload_check.py \"{output_path}\"")
    print("=" * 70)

    return str(output_path), stats


def main():
    if len(sys.argv) < 2:
        print("사용법: python extract_happy_cases.py <입력_CSV_파일_경로>")
        print()
        print("예:")
        print("  python extract_happy_cases.py 로그인_테스트케이스.csv")
        print("  python extract_happy_cases.py /path/to/회원관리_testcase.csv")
        sys.exit(1)

    extract_happy_cases(sys.argv[1])


if __name__ == "__main__":
    main()
