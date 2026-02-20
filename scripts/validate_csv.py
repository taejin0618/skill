#!/usr/bin/env python3
"""
TestRail CSV 포맷 검증 스크립트
TestRail 업로드 가능한 CSV 형식인지 검증합니다.
"""

import csv
import sys
from pathlib import Path


def validate_csv_format(filepath):
    """CSV 파일의 TestRail 호환성을 검증합니다."""
    
    errors = []
    warnings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # 필수 컬럼 확인
            required_columns = ['Section', 'Section Hierarchy', 'Title', 'Preconditions', 'Steps', 'Expected Result', 'Priority']
            
            if not reader.fieldnames:
                errors.append("CSV 파일에 헤더가 없습니다.")
                return errors, warnings
            
            missing_columns = set(required_columns) - set(reader.fieldnames)
            if missing_columns:
                errors.append(f"필수 컬럼이 누락되었습니다: {', '.join(missing_columns)}")
                return errors, warnings
            
            # 각 행 검증
            for idx, row in enumerate(reader, start=2):  # 헤더 다음부터 2행
                # Title 검증
                title = row.get('Title', '').strip()
                if title and len(title) > 250:
                    warnings.append(f"행 {idx}: Title이 250자를 초과합니다 ({len(title)}자)")
                
                # Priority 검증
                priority = row.get('Priority', '').strip()
                valid_priorities = ['Highest', 'High', 'Medium', 'Low', 'Lowest', '']
                if priority and priority not in valid_priorities:
                    errors.append(f"행 {idx}: 유효하지 않은 Priority '{priority}'. 가능한 값: {', '.join(valid_priorities[:-1])}")
                
                # Steps와 Expected Result가 함께 있는지 확인
                steps = row.get('Steps', '').strip()
                expected = row.get('Expected Result', '').strip()
                
                if steps and not expected:
                    warnings.append(f"행 {idx}: Steps는 있지만 Expected Result가 없습니다")
                if expected and not steps:
                    warnings.append(f"행 {idx}: Expected Result는 있지만 Steps가 없습니다")
                
                # Section Hierarchy 깊이 체크
                hierarchy = row.get('Section Hierarchy', '').strip()
                if hierarchy:
                    depth = hierarchy.count('>') + 1
                    if depth > 4:
                        warnings.append(f"행 {idx}: Section Hierarchy 깊이가 4를 초과합니다 (권장: 최대 4 depth)")
        
        return errors, warnings
        
    except FileNotFoundError:
        errors.append(f"파일을 찾을 수 없습니다: {filepath}")
        return errors, warnings
    except Exception as e:
        errors.append(f"검증 중 오류 발생: {str(e)}")
        return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("사용법: python validate_csv.py <csv_파일_경로>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    print(f"📋 CSV 파일 검증 중: {filepath}")
    print("=" * 60)
    
    errors, warnings = validate_csv_format(filepath)
    
    # 결과 출력
    if errors:
        print("\n❌ 오류 발견:")
        for error in errors:
            print(f"  • {error}")
    
    if warnings:
        print("\n⚠️  경고:")
        for warning in warnings:
            print(f"  • {warning}")
    
    if not errors and not warnings:
        print("\n✅ 검증 통과! TestRail 업로드 가능한 형식입니다.")
        sys.exit(0)
    elif errors:
        print("\n💥 검증 실패! 오류를 수정해주세요.")
        sys.exit(1)
    else:
        print("\n⚠️  경고가 있지만 업로드는 가능합니다.")
        sys.exit(0)


if __name__ == "__main__":
    main()
