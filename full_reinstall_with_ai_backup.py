"""
AI 학습 데이터 보존 + 전체 재설치 스크립트
현재 경로: C:\Users\admin\Downloads\Lj-main\Lj-main
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
import json

def backup_ai_data(bot_dir):
    """AI 학습 데이터 백업"""
    print("\n" + "="*60)
    print("  Step 1: AI 학습 데이터 백업")
    print("="*60)
    
    backup_dir = bot_dir / "AI_BACKUP"
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_items = []
    
    # 백업할 파일/폴더 목록
    ai_files = [
        "ai_learning_data.json",
        "trade_history.json",
        "ai_learning.db",
        "logs",
        "data",
        ".env"  # 환경 변수도 백업
    ]
    
    for item in ai_files:
        source = bot_dir / item
        if source.exists():
            if source.is_file():
                dest = backup_dir / f"{item}.{timestamp}"
                shutil.copy2(source, dest)
                print(f"✅ 백업: {item} → {dest.name}")
                backup_items.append(item)
            elif source.is_dir():
                dest = backup_dir / f"{item}_{timestamp}"
                shutil.copytree(source, dest, dirs_exist_ok=True)
                print(f"✅ 백업: {item}/ → {dest.name}/")
                backup_items.append(item)
    
    # 백업 정보 저장
    backup_info = {
        "timestamp": timestamp,
        "items": backup_items,
        "restore_command": f"python restore_ai_data.py {timestamp}"
    }
    
    with open(backup_dir / f"backup_info_{timestamp}.json", 'w', encoding='utf-8') as f:
        json.dump(backup_info, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 백업 완료: {len(backup_items)}개 항목")
    print(f"📁 백업 위치: {backup_dir}")
    print(f"🔄 복원 명령어: python restore_ai_data.py {timestamp}")
    
    return timestamp

def create_restore_script(bot_dir, timestamp):
    """복원 스크립트 생성"""
    restore_script = f'''"""
AI 학습 데이터 복원 스크립트
백업 타임스탬프: {timestamp}
"""

import shutil
from pathlib import Path
import json

bot_dir = Path(__file__).parent
backup_dir = bot_dir / "AI_BACKUP"

# 백업 정보 로드
with open(backup_dir / "backup_info_{timestamp}.json", 'r', encoding='utf-8') as f:
    backup_info = json.load(f)

print("="*60)
print("  AI 학습 데이터 복원")
print("="*60)
print(f"\\n백업 시간: {backup_info['timestamp']}")
print(f"복원 항목: {{len(backup_info['items'])}}개\\n")

for item in backup_info['items']:
    if item == ".env":
        source = backup_dir / f"{{item}}.{timestamp}"
        dest = bot_dir / item
    else:
        source_file = backup_dir / f"{{item}}.{timestamp}"
        source_dir = backup_dir / f"{{item}}_{timestamp}"
        dest = bot_dir / item
        
        if source_file.exists():
            source = source_file
        elif source_dir.exists():
            source = source_dir
        else:
            print(f"⚠️ 백업 없음: {{item}}")
            continue
    
    if source.is_file():
        shutil.copy2(source, dest)
        print(f"✅ 복원: {{item}}")
    elif source.is_dir():
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(source, dest)
        print(f"✅ 복원: {{item}}/")

print("\\n✅ 복원 완료!")
print("\\n다음 단계:")
print("  python -B -u -m src.main --mode paper")
'''
    
    with open(bot_dir / "restore_ai_data.py", 'w', encoding='utf-8') as f:
        f.write(restore_script)
    
    print(f"\n✅ 복원 스크립트 생성: restore_ai_data.py")

def download_latest_files(bot_dir):
    """최신 파일 다운로드"""
    print("\n" + "="*60)
    print("  Step 2: 최신 파일 다운로드")
    print("="*60)
    print()
    
    import urllib.request
    
    files = {
        "src/config.py": "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py",
        "src/main.py": "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/main.py",
        "src/utils/smart_investment_manager.py": "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/smart_investment_manager.py",
        "src/utils/surge_detector.py": "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/surge_detector.py",
        "VERSION.txt": "https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt",
        "test_smart_investment.py": "https://raw.githubusercontent.com/lee-jungkil/Lj/main/test_smart_investment.py"
    }
    
    success = 0
    for file_path, url in files.items():
        dest = bot_dir / file_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            print(f"다운로드: {file_path}... ", end="")
            urllib.request.urlretrieve(url, dest)
            print("✅")
            success += 1
        except Exception as e:
            print(f"❌ {e}")
    
    print(f"\n✅ 다운로드 완료: {success}/{len(files)}")
    return success == len(files)

def clear_cache(bot_dir):
    """캐시 삭제"""
    print("\n" + "="*60)
    print("  Step 3: 캐시 삭제")
    print("="*60)
    print()
    
    cache_dirs = [
        "__pycache__",
        "src/__pycache__",
        "src/utils/__pycache__",
        "src/api/__pycache__",
        "src/strategies/__pycache__",
        "src/ai/__pycache__"
    ]
    
    for cache_dir in cache_dirs:
        cache_path = bot_dir / cache_dir
        if cache_path.exists():
            shutil.rmtree(cache_path, ignore_errors=True)
            print(f"✅ 삭제: {cache_dir}")
    
    print("\n✅ 캐시 삭제 완료")

def verify_installation(bot_dir):
    """설치 검증"""
    print("\n" + "="*60)
    print("  Step 4: 설치 검증")
    print("="*60)
    print()
    
    # VERSION 확인
    version_file = bot_dir / "VERSION.txt"
    if version_file.exists():
        version = version_file.read_text(encoding='utf-8').strip()
        print(f"✅ 버전: {version}")
        
        if version == "v6.31.8-R3-SMART-INVESTMENT":
            print("✅ 최신 버전 확인!")
        else:
            print(f"⚠️ 예상 버전: v6.31.8-R3-SMART-INVESTMENT")
    else:
        print("❌ VERSION.txt 없음")
    
    # 필수 파일 확인
    required_files = [
        "src/config.py",
        "src/main.py",
        "src/utils/smart_investment_manager.py"
    ]
    
    all_exist = True
    for file in required_files:
        file_path = bot_dir / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {file} ({size:,} bytes)")
        else:
            print(f"❌ {file} 없음")
            all_exist = False
    
    return all_exist

def main():
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "AI 학습 데이터 보존 + 전체 재설치" + " "*14 + "║")
    print("╚" + "="*58 + "╝")
    print()
    print("현재 경로: C:\\Users\\admin\\Downloads\\Lj-main\\Lj-main")
    print()
    
    # 현재 디렉토리
    bot_dir = Path.cwd()
    print(f"작업 디렉토리: {bot_dir}")
    
    input("\nEnter를 눌러 시작...")
    
    try:
        # 1. AI 데이터 백업
        timestamp = backup_ai_data(bot_dir)
        
        # 2. 복원 스크립트 생성
        create_restore_script(bot_dir, timestamp)
        
        # 3. 최신 파일 다운로드
        if not download_latest_files(bot_dir):
            print("\n⚠️ 일부 파일 다운로드 실패")
            print("수동으로 다운로드하거나 재시도하세요")
            return
        
        # 4. 캐시 삭제
        clear_cache(bot_dir)
        
        # 5. 설치 검증
        if not verify_installation(bot_dir):
            print("\n⚠️ 일부 파일이 누락되었습니다")
            return
        
        # 6. 완료
        print("\n" + "="*60)
        print("  ✅ 전체 재설치 완료!")
        print("="*60)
        print()
        print("📋 다음 단계:")
        print()
        print("1. 테스트 실행:")
        print("   python test_smart_investment.py")
        print()
        print("2. 봇 시작:")
        print("   python -B -u -m src.main --mode paper")
        print()
        print("3. AI 데이터 복원 (필요 시):")
        print(f"   python restore_ai_data.py {timestamp}")
        print()
        print("📁 백업 위치: AI_BACKUP/")
        print(f"   - 백업 시간: {timestamp}")
        print("   - AI 학습 데이터 보존됨")
        print()
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
        print("\n백업 데이터는 AI_BACKUP/ 폴더에 안전하게 저장되었습니다")

if __name__ == "__main__":
    main()
