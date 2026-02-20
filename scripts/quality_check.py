#!/usr/bin/env python3
"""
테스트 케이스 품질 체크 스크립트
작성된 테스트 케이스의 품질을 평가합니다.
"""

import csv
import sys
import re
from pathlib import Path


class QualityChecker:
    def __init__(self):
        self.issues = []
        self.suggestions = []
        self.stats = {
            'total_cases': 0,
            'with_preconditions': 0,
            'with_steps': 0,
            'with_expected': 0,
            'priority_highest': 0,
            'priority_high': 0,
            'priority_medium': 0,
            'priority_low': 0,
        }
    
    def check_title_quality(self, row_num, title):
        """Title 품질 검증"""
        if not title:
            return
        
        # 너무 짧은 제목
        if len(title) < 10:
            self.suggestions.append(f"행 {row_num}: Title이 너무 짧습니다 ({len(title)}자). 더 구체적으로 작성하세요.")
        
        # 모호한 표현 체크
        vague_words = ['테스트', '확인', '검증', '체크']
        if any(word in title for word in vague_words) and len(title.split()) < 4:
            self.suggestions.append(f"행 {row_num}: Title이 모호합니다. 구체적인 조건과 결과를 포함하세요.")
    
    def check_steps_quality(self, row_num, steps):
        """Steps 품질 검증"""
        if not steps:
            return
        
        # 숫자 순서 확인
        if not re.search(r'^\d+\.', steps.strip()):
            self.suggestions.append(f"행 {row_num}: Steps가 숫자 순서로 시작하지 않습니다 (예: 1. 2. 3.)")
        
        # 구체적인 값 확인
        step_lines = [line.strip() for line in steps.split('\n') if line.strip()]
        for step in step_lines:
            # '입력'이라는 단어가 있지만 구체적인 값이 없는 경우
            if '입력' in step and not ("'" in step or '"' in step or '예:' in step):
                self.suggestions.append(f"행 {row_num}: Steps에 구체적인 입력 값을 명시하세요. 현재: '{step[:50]}...'")
                break
    
    def check_expected_quality(self, row_num, expected):
        """Expected Result 품질 검증"""
        if not expected:
            return
        
        # 측정 가능한 기준 확인
        vague_phrases = ['정상', '성공', '처리', '완료']
        if any(phrase in expected for phrase in vague_phrases) and len(expected) < 30:
            self.suggestions.append(f"행 {row_num}: Expected Result가 모호합니다. 측정 가능한 구체적 기준을 명시하세요.")
    
    def check_priority_distribution(self):
        """우선순위 분포 확인"""
        total = self.stats['total_cases']
        if total == 0:
            return
        
        highest_ratio = self.stats['priority_highest'] / total
        if highest_ratio > 0.3:
            self.suggestions.append(f"Highest Priority가 {highest_ratio*100:.1f}%로 너무 많습니다. 우선순위를 재검토하세요.")
    
    def analyze_csv(self, filepath):
        """CSV 파일 분석"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for idx, row in enumerate(reader, start=2):
                    title = row.get('Title', '').strip()
                    steps = row.get('Steps', '').strip()
                    expected = row.get('Expected Result', '').strip()
                    priority = row.get('Priority', '').strip()
                    preconditions = row.get('Preconditions', '').strip()
                    
                    # 통계 수집
                    if title:  # Section 행이 아닌 실제 테스트 케이스만
                        self.stats['total_cases'] += 1
                        
                        if preconditions:
                            self.stats['with_preconditions'] += 1
                        if steps:
                            self.stats['with_steps'] += 1
                        if expected:
                            self.stats['with_expected'] += 1
                        
                        if priority == 'Highest':
                            self.stats['priority_highest'] += 1
                        elif priority == 'High':
                            self.stats['priority_high'] += 1
                        elif priority == 'Medium':
                            self.stats['priority_medium'] += 1
                        elif priority == 'Low':
                            self.stats['priority_low'] += 1
                        
                        # 품질 체크
                        self.check_title_quality(idx, title)
                        self.check_steps_quality(idx, steps)
                        self.check_expected_quality(idx, expected)
                
                # 우선순위 분포 체크
                self.check_priority_distribution()
                
        except Exception as e:
            self.issues.append(f"분석 중 오류 발생: {str(e)}")
    
    def print_report(self):
        """품질 리포트 출력"""
        print("\n" + "=" * 60)
        print("📊 테스트 케이스 품질 리포트")
        print("=" * 60)
        
        # 통계
        print(f"\n총 테스트 케이스: {self.stats['total_cases']}개")
        
        if self.stats['total_cases'] > 0:
            print(f"\n✓ Preconditions 작성률: {self.stats['with_preconditions']/self.stats['total_cases']*100:.1f}%")
            print(f"✓ Steps 작성률: {self.stats['with_steps']/self.stats['total_cases']*100:.1f}%")
            print(f"✓ Expected Result 작성률: {self.stats['with_expected']/self.stats['total_cases']*100:.1f}%")
            
            print(f"\n우선순위 분포:")
            print(f"  • Highest: {self.stats['priority_highest']}개 ({self.stats['priority_highest']/self.stats['total_cases']*100:.1f}%)")
            print(f"  • High: {self.stats['priority_high']}개 ({self.stats['priority_high']/self.stats['total_cases']*100:.1f}%)")
            print(f"  • Medium: {self.stats['priority_medium']}개 ({self.stats['priority_medium']/self.stats['total_cases']*100:.1f}%)")
            print(f"  • Low: {self.stats['priority_low']}개 ({self.stats['priority_low']/self.stats['total_cases']*100:.1f}%)")
        
        # 이슈
        if self.issues:
            print("\n❌ 발견된 이슈:")
            for issue in self.issues:
                print(f"  • {issue}")
        
        # 개선 제안
        if self.suggestions:
            print("\n💡 개선 제안:")
            for suggestion in self.suggestions[:10]:  # 최대 10개만 표시
                print(f"  • {suggestion}")
            
            if len(self.suggestions) > 10:
                print(f"\n  ... 외 {len(self.suggestions) - 10}개의 제안이 더 있습니다.")
        
        # 종합 점수
        score = self.calculate_score()
        print(f"\n{'='*60}")
        print(f"종합 품질 점수: {score}/100")
        
        if score >= 90:
            print("✅ 우수한 품질입니다!")
        elif score >= 70:
            print("⚠️  양호한 품질이지만 개선이 필요합니다.")
        else:
            print("❌ 품질 개선이 필요합니다.")
        
        print("=" * 60)
    
    def calculate_score(self):
        """품질 점수 계산"""
        if self.stats['total_cases'] == 0:
            return 0
        
        score = 100
        
        # 작성률 점수 (50점)
        precond_rate = self.stats['with_preconditions'] / self.stats['total_cases']
        steps_rate = self.stats['with_steps'] / self.stats['total_cases']
        expected_rate = self.stats['with_expected'] / self.stats['total_cases']
        
        score -= (1 - steps_rate) * 25  # Steps 미작성 페널티
        score -= (1 - expected_rate) * 25  # Expected Result 미작성 페널티
        
        # 제안사항 페널티 (50점)
        penalty = min(len(self.suggestions) * 2, 50)
        score -= penalty
        
        return max(0, int(score))


def main():
    if len(sys.argv) < 2:
        print("사용법: python quality_check.py <csv_파일_경로>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not Path(filepath).exists():
        print(f"❌ 파일을 찾을 수 없습니다: {filepath}")
        sys.exit(1)
    
    print(f"🔍 테스트 케이스 품질 분석 중: {filepath}")
    
    checker = QualityChecker()
    checker.analyze_csv(filepath)
    checker.print_report()


if __name__ == "__main__":
    main()
