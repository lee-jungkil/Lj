#!/usr/bin/env python3
"""
디버그 출력 완전 제거 스크립트 v6.30.71
모든 DEBUG, CHECK, 체크, 확인 관련 출력 제거
"""
import os
import re

def remove_debug_outputs(file_path):
    """모든 디버그 관련 출력 제거"""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    original_count = len(lines)
    new_lines = []
    removed_count = 0
    
    # 제거할 패턴들
    remove_patterns = [
        r'_original_print\(.*?\[DEBUG.*?\)',  # [DEBUG-*] 메시지
        r'_original_print\(.*?체크.*?\)',      # 체크 관련
        r'_original_print\(.*?확인.*?\)',      # 확인 관련
        r'_original_print\(.*?CHECK.*?\)',     # CHECK 관련
        r'_original_print\(.*?포지션.*?체크.*?\)',  # 포지션 체크
        r'_original_print\(.*?청산.*?체크.*?\)',    # 청산 체크
        r'self\.logger\.log_info\(.*?체크.*?\)',    # logger 체크
        r'self\.logger\.log_info\(.*?확인.*?\)',    # logger 확인
        r'print\(.*?체크.*?\)',                     # print 체크
        r'print\(.*?확인.*?\)',                     # print 확인
    ]
    
    skip_next_line = False
    
    for i, line in enumerate(lines):
        # 이전 줄에서 skip 플래그가 설정된 경우
        if skip_next_line:
            skip_next_line = False
            removed_count += 1
            continue
        
        # 패턴 매칭
        should_remove = False
        for pattern in remove_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                should_remove = True
                removed_count += 1
                
                # 여러 줄에 걸친 함수 호출 처리
                if line.rstrip().endswith('('):
                    skip_next_line = True
                break
        
        if not should_remove:
            new_lines.append(line)
    
    # 파일 쓰기
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    new_count = len(new_lines)
    
    return {
        'original': original_count,
        'new': new_count,
        'removed': removed_count
    }

def main():
    print("=" * 60)
    print("디버그 출력 완전 제거 도구 v6.30.71")
    print("=" * 60)
    
    files_to_process = [
        'src/main.py',
        'src/utils/fixed_screen_display.py'
    ]
    
    total_removed = 0
    
    for file_path in files_to_process:
        if not os.path.exists(file_path):
            print(f"⚠️ 파일 없음: {file_path}")
            continue
        
        result = remove_debug_outputs(file_path)
        total_removed += result['removed']
        
        print(f"✅ {file_path}")
        print(f"   원본: {result['original']}줄")
        print(f"   제거: {result['removed']}줄")
        print(f"   결과: {result['new']}줄")
        print()
    
    print("=" * 60)
    print(f"✅ 총 {total_removed}개 디버그 출력 제거 완료!")
    print("=" * 60)
    print()
    print("다음 단계:")
    print("1. 봇 중지: Ctrl+C")
    print("2. 캐시 정리: del /s /q *.pyc")
    print("3. 재시작: python -B -u -m src.main --mode paper")

if __name__ == '__main__':
    main()
