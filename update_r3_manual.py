"""
v6.31.8-R3 수동 업데이트 스크립트
배치 파일이 작동하지 않을 때 사용
"""

import os
import sys
import shutil
from pathlib import Path
import urllib.request

def download_file(url, destination):
    """파일 다운로드"""
    try:
        print(f"다운로드 중: {url}")
        urllib.request.urlretrieve(url, destination)
        print(f"✅ 완료: {destination}")
        return True
    except Exception as e:
        print(f"❌ 에러: {e}")
        return False

def main():
    print("="*60)
    print("  v6.31.8-R3 수동 업데이트 스크립트")
    print("="*60)
    print()
    
    # 현재 디렉토리
    bot_dir = Path.cwd()
    print(f"봇 디렉토리: {bot_dir}")
    print()
    
    # 1. 백업
    print("[1/6] 백업 생성...")
    backup_dir = bot_dir / "backup"
    backup_dir.mkdir(exist_ok=True)
    
    config_path = bot_dir / "src" / "config.py"
    if config_path.exists():
        shutil.copy(config_path, backup_dir / "config_manual.py")
        print("✅ config.py 백업 완료")
    
    version_path = bot_dir / "VERSION.txt"
    if version_path.exists():
        shutil.copy(version_path, backup_dir / "VERSION_manual.txt")
        print("✅ VERSION.txt 백업 완료")
    print()
    
    # 2. 파일 다운로드
    files = {
        "src/config.py": "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/config.py",
        "src/utils/smart_investment_manager.py": "https://raw.githubusercontent.com/lee-jungkil/Lj/main/src/utils/smart_investment_manager.py",
        "VERSION.txt": "https://raw.githubusercontent.com/lee-jungkil/Lj/main/VERSION.txt",
        "test_smart_investment.py": "https://raw.githubusercontent.com/lee-jungkil/Lj/main/test_smart_investment.py"
    }
    
    print("[2/6] 파일 다운로드...")
    success_count = 0
    for file_path, url in files.items():
        dest = bot_dir / file_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        if download_file(url, str(dest)):
            success_count += 1
    
    print(f"\n다운로드 완료: {success_count}/{len(files)}")
    print()
    
    # 3. 캐시 삭제
    print("[3/6] 캐시 삭제...")
    cache_dirs = [
        bot_dir / "__pycache__",
        bot_dir / "src" / "__pycache__",
        bot_dir / "src" / "utils" / "__pycache__"
    ]
    
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            shutil.rmtree(cache_dir, ignore_errors=True)
            print(f"✅ {cache_dir.name} 삭제")
    print()
    
    # 4. 버전 확인
    print("[4/6] 버전 확인...")
    if version_path.exists():
        with open(version_path, 'r', encoding='utf-8') as f:
            version = f.read().strip()
        print(f"✅ 현재 버전: {version}")
        
        if version == "v6.31.8-R3-SMART-INVESTMENT":
            print("✅ 버전 업데이트 성공!")
        else:
            print(f"⚠️ 예상 버전: v6.31.8-R3-SMART-INVESTMENT")
            print(f"   실제 버전: {version}")
    else:
        print("❌ VERSION.txt 없음")
    print()
    
    # 5. 테스트
    print("[5/6] 시스템 테스트...")
    test_file = bot_dir / "test_smart_investment.py"
    if test_file.exists():
        print("테스트 실행 중...")
        os.system(f"python {test_file}")
    else:
        print("⚠️ 테스트 파일 없음")
    print()
    
    # 6. 완료
    print("[6/6] 완료!")
    print("="*60)
    print()
    print("다음 단계:")
    print("1. 봇 재시작: python -B -u -m src.main --mode paper")
    print("2. 콘솔에서 투자 금액 확인")
    print("3. 첫 10~20건 거래 모니터링")
    print()
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n중단됨")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
