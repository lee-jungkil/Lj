#!/usr/bin/env python3
"""
배치 파일 버전 자동 업데이트 스크립트
모든 .bat 파일의 버전 번호를 현재 버전으로 업데이트합니다.
"""

import re
import os
from pathlib import Path

# 현재 버전 읽기
version_file = Path('/home/user/webapp/VERSION.txt')
with open(version_file, 'r', encoding='utf-8') as f:
    first_line = f.readline().strip()
    # v6.30.28-PROFIT-SELL-EXECUTION-FIX 형식에서 v6.30.28 추출
    current_version = first_line.split('-')[0]  # v6.30.28

print(f"📌 현재 버전: {current_version}")
print("=" * 80)

# 배치 파일 목록
batch_files = [
    'RUN_PAPER_CLEAN.bat',
    'RUN_LIVE_CLEAN.bat',
    'setup.bat',
    'DOWNLOAD_ALL_FILES.bat',
    'QUICK_UPDATE.bat',
    'RUN.bat',
    'UPDATE.bat',
]

# 버전 패턴 (v5.x, v6.30.x 등)
version_pattern = re.compile(r'v\d+\.\d+(?:\.\d+)?')

updated_files = []
not_found_files = []

for bat_file in batch_files:
    file_path = Path('/home/user/webapp') / bat_file
    
    if not file_path.exists():
        not_found_files.append(bat_file)
        print(f"⚠️  {bat_file}: 파일 없음 (스킵)")
        continue
    
    # 파일 읽기
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 버전 번호 찾기
    old_versions = version_pattern.findall(content)
    
    if not old_versions:
        print(f"ℹ️  {bat_file}: 버전 번호 없음 (스킵)")
        continue
    
    # 이전 버전 목록 (중복 제거)
    unique_old_versions = list(set(old_versions))
    
    # 모든 버전 번호를 현재 버전으로 교체
    new_content = version_pattern.sub(current_version, content)
    
    # 변경 사항이 있는지 확인
    if new_content != content:
        # 파일 쓰기
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        updated_files.append(bat_file)
        print(f"✅ {bat_file}:")
        for old_ver in unique_old_versions:
            print(f"    {old_ver} → {current_version}")
    else:
        print(f"✓  {bat_file}: 이미 최신 버전")

print("\n" + "=" * 80)
print("📊 업데이트 결과 요약")
print("=" * 80)
print(f"✅ 업데이트 완료: {len(updated_files)}개")
for f in updated_files:
    print(f"   - {f}")

if not_found_files:
    print(f"\n⚠️  파일 없음: {len(not_found_files)}개")
    for f in not_found_files:
        print(f"   - {f}")

print(f"\n현재 버전: {current_version}")
print("=" * 80)
