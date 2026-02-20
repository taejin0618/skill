#!/usr/bin/env python3
"""
TestRail 업로드 전 최종 검증 스크립트
CSV 포맷 + 품질 체크를 모두 수행합니다.
"""

import csv
import sys
from pathlib import Path


def validate_testrail_upload(filepath):
    """TestRail 업로드 가능 여부 최종 검증"""

    errors = []
    warnings = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

            # BOM 체크
            if content.startswith('\ufeff'):
                warnings.append("파일에 BOM이 포함되어 있습니다. TestRail 업로드 시 문제가 될 수 있습니다.")

            # CSV 파싱
            f.seek(0)
            reader = csv.DictReader(f)

            # 필수 컬럼 확인
            required_columns = ['Section', 'Section Hierarchy', 'Title', 'Preconditions', 'Steps', 'Expected Result', 'Priority']

            if not reader.fieldnames:
                errors.append("CSV 파일에 헤더가 없습니다.")
                return errors, warnings

            missing_columns = set(required_columns) - set(reader.fieldnames)
            if missing_columns:
                errors.append(f"필수 컬럼 누락: {', '.join(missing_columns)}")
                return errors, warnings

            # 데이터 검증
            has_content = False
            section_count = 0
            testcase_count = 0

            for idx, row in enumerate(reader, start=2):
                title = row.get('Title', '').strip()
                section = row.get('Section', '').strip()

                if section:
                    section_count += 1

                if title:
                    has_content = True
                    testcase_count += 1

                    # 필수 필드 체크 (테스트 케이스만)
                    steps = row.get('Steps', '').strip()
                    expected = row.get('Expected Result', '').strip()

                    if not steps:
                        errors.append(f"행 {idx}: Title은 있지만 Steps가 비어있습니다")

                    if not expected:
                        errors.append(f"행 {idx}: Title은 있지만 Expected Result가 비어있습니다")

                    # Priority 검증
                    priority = row.get('Priority', '').strip()
                    valid_priorities = ['Highest', 'High', 'Medium', 'Low', 'Lowest']
                    if priority not in valid_priorities:
                        errors.append(f"행 {idx}: 유효하지 않은 Priority '{priority}'")

            if not has_content:
                errors.append("테스트 케이스가 하나도 없습니다.")

            if section_count == 0:
                warnings.append("Section이 정의되지 않았습니다. TestRail에서 폴더 구조가 없을 수 있습니다.")

            # 통계 정보
            if testcase_count > 0:
                warnings.append(f"총 {section_count}개 섹션, {testcase_count}개 테스트 케이스 발견")

        return errors, warnings

    except FileNotFoundError:
        errors.append(f"파일을 찾을 수 없습니다: {filepath}")
        return errors, warnings
    except UnicodeDecodeError:
        errors.append("파일 인코딩 오류. UTF-8 인코딩으로 저장해주세요.")
        return errors, warnings
    except Exception as e:
        errors.append(f"검증 중 오류 발생: {str(e)}")
        return errors, warnings


def check_file_size(filepath):
    """파일 크기 확인"""
    size_mb = Path(filepath).stat().st_size / (1024 * 1024)
    if size_mb > 10:
        return f"⚠️  파일 크기가 큽니다 ({size_mb:.2f}MB). TestRail 업로드에 시간이 걸릴 수 있습니다."
    return None


def main():
    if len(sys.argv) < 2:
        print("사용법: python testrail_upload_check.py <csv_파일_경로>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not Path(filepath).exists():
        print(f"❌ 파일을 찾을 수 없습니다: {filepath}")
        sys.exit(1)

    print("=" * 70)
    print("🚀 TestRail 업로드 최종 검증")
    print("=" * 70)
    print(f"\n📁 파일: {filepath}")

    # 파일 크기 체크
    size_warning = check_file_size(filepath)
    if size_warning:
        print(size_warning)

    # 검증 수행
    errors, warnings = validate_testrail_upload(filepath)

    # 결과 출력
    print("\n" + "=" * 70)

    if errors:
        print("❌ 오류 발견 - 업로드 불가:")
        for error in errors:
            print(f"  • {error}")

    if warnings:
        print("\n⚠️  경고:")
        for warning in warnings:
            print(f"  • {warning}")

    print("\n" + "=" * 70)

    if not errors and not warnings:
        print("✅ 검증 완료! TestRail에 바로 업로드 가능합니다.")
        print("\n📤 TestRail 업로드 방법:")
        print("  1. TestRail 프로젝트 > Test Cases 섹션 이동")
        print("  2. 우측 상단 'Import' 버튼 클릭")
        print("  3. CSV 파일 선택 및 업로드")
        sys.exit(0)
    elif errors:
        print("💥 오류를 수정한 후 다시 시도해주세요.")
        sys.exit(1)
    else:
        print("⚠️  경고가 있지만 업로드는 가능합니다.")
        print("    문제가 없다면 TestRail에 업로드하세요.")
        sys.exit(0)


if __name__ == "__main__":
    main()
