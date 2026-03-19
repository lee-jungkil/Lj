"""
AI 학습 데이터 보존 + GitHub에서 전체 새로 설치
현재 경로: C:\Users\admin\Downloads\Lj-main\Lj-main
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
import urllib.request
import json

def backup_ai_data(old_dir):
    """AI 학습 데이터 백업"""
    print("\n" + "="*70)
    print("  Step 1: AI 학습 데이터 백업")
    print("="*70)
    print()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = old_dir / f"AI_BACKUP_{timestamp}"
    backup_dir.mkdir(exist_ok=True)
    
    # 백업할 항목들
    backup_items = {
        'ai_learning_data.json': 'AI 학습 데이터',
        'trade_history.json': '거래 기록',
        'ai_learning.db': 'AI 데이터베이스',
        '.env': '환경 설정',
        'logs': '로그 폴더',
        'data': '데이터 폴더'
    }
    
    backed_up = []
    
    for item, desc in backup_items.items():
        source = old_dir / item
        if source.exists():
            dest = backup_dir / item
            try:
                if source.is_file():
                    shutil.copy2(source, dest)
                    size = source.stat().st_size
                    print(f"✅ {item:30s} ({size:>10,} bytes) - {desc}")
                elif source.is_dir():
                    shutil.copytree(source, dest)
                    print(f"✅ {item:30s} (폴더) - {desc}")
                backed_up.append(item)
            except Exception as e:
                print(f"⚠️ {item:30s} - 백업 실패: {e}")
        else:
            print(f"⏭️ {item:30s} - 파일 없음 (건너뜀)")
    
    # 백업 정보 저장
    backup_info = {
        'timestamp': timestamp,
        'original_path': str(old_dir),
        'backed_up_items': backed_up,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(backup_dir / 'backup_info.json', 'w', encoding='utf-8') as f:
        json.dump(backup_info, f, indent=2, ensure_ascii=False)
    
    print()
    print(f"✅ 백업 완료: {len(backed_up)}개 항목")
    print(f"📁 백업 위치: {backup_dir}")
    print()
    
    return backup_dir, backed_up

def download_latest_release(download_dir):
    """최신 릴리즈 다운로드"""
    print("\n" + "="*70)
    print("  Step 2: GitHub에서 최신 코드 다운로드")
    print("="*70)
    print()
    
    zip_url = "https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip"
    zip_path = download_dir / "Lj-main.zip"
    
    print(f"다운로드 중: {zip_url}")
    print("(파일 크기에 따라 30초~1분 소요)")
    print()
    
    try:
        urllib.request.urlretrieve(zip_url, zip_path)
        size = zip_path.stat().st_size
        print(f"✅ 다운로드 완료: {size:,} bytes")
        return zip_path
    except Exception as e:
        print(f"❌ 다운로드 실패: {e}")
        return None

def extract_zip(zip_path, extract_dir):
    """ZIP 압축 해제"""
    print("\n" + "="*70)
    print("  Step 3: 압축 해제")
    print("="*70)
    print()
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # GitHub에서 다운로드한 ZIP은 Lj-main/ 폴더 안에 있음
        extracted_folder = extract_dir / "Lj-main"
        
        if extracted_folder.exists():
            print(f"✅ 압축 해제 완료: {extracted_folder}")
            return extracted_folder
        else:
            print("❌ 압축 해제 후 폴더를 찾을 수 없습니다")
            return None
    except Exception as e:
        print(f"❌ 압축 해제 실패: {e}")
        return None

def restore_ai_data(new_dir, backup_dir, backed_up_items):
    """AI 데이터 복원"""
    print("\n" + "="*70)
    print("  Step 4: AI 학습 데이터 복원")
    print("="*70)
    print()
    
    restored = 0
    
    for item in backed_up_items:
        source = backup_dir / item
        dest = new_dir / item
        
        try:
            if source.is_file():
                shutil.copy2(source, dest)
                print(f"✅ {item:30s} 복원 완료")
                restored += 1
            elif source.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(source, dest)
                print(f"✅ {item:30s} 복원 완료 (폴더)")
                restored += 1
        except Exception as e:
            print(f"⚠️ {item:30s} 복원 실패: {e}")
    
    print()
    print(f"✅ 복원 완료: {restored}/{len(backed_up_items)}개 항목")
    print()

def clear_cache(bot_dir):
    """캐시 삭제"""
    print("\n" + "="*70)
    print("  Step 5: 캐시 삭제")
    print("="*70)
    print()
    
    cache_patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo"
    ]
    
    deleted = 0
    for pattern in cache_patterns:
        for cache_path in bot_dir.rglob(pattern.replace("**", "*")):
            try:
                if cache_path.is_file():
                    cache_path.unlink()
                    deleted += 1
                elif cache_path.is_dir():
                    shutil.rmtree(cache_path)
                    deleted += 1
            except:
                pass
    
    print(f"✅ 캐시 삭제 완료: {deleted}개 항목")
    print()

def verify_installation(bot_dir):
    """설치 검증"""
    print("\n" + "="*70)
    print("  Step 6: 설치 검증")
    print("="*70)
    print()
    
    # VERSION 확인
    version_file = bot_dir / "VERSION.txt"
    if version_file.exists():
        version = version_file.read_text(encoding='utf-8').strip()
        print(f"✅ 버전: {version}")
    else:
        print("⚠️ VERSION.txt 없음")
        version = "Unknown"
    
    # 필수 파일 확인
    required_files = [
        "src/config.py",
        "src/main.py",
        "src/utils/smart_investment_manager.py",
        "src/api/upbit_api.py",
        "src/strategies/conservative_scalping.py",
        "src/ai/learning_engine.py"
    ]
    
    print()
    print("필수 파일 확인:")
    all_exist = True
    for file in required_files:
        file_path = bot_dir / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✅ {file:45s} ({size:>8,} bytes)")
        else:
            print(f"  ❌ {file:45s} 없음")
            all_exist = False
    
    # AI 데이터 확인
    print()
    print("AI 학습 데이터 확인:")
    ai_files = [
        "ai_learning_data.json",
        "trade_history.json",
        ".env"
    ]
    
    for file in ai_files:
        file_path = bot_dir / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✅ {file:30s} ({size:>10,} bytes)")
        else:
            print(f"  ⚠️ {file:30s} 없음 (새로 생성됨)")
    
    print()
    return all_exist, version

def main():
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "AI 학습 데이터 보존 + 전체 새로 설치" + " "*17 + "║")
    print("╚" + "="*68 + "╝")
    print()
    print("현재 경로: C:\\Users\\admin\\Downloads\\Lj-main\\Lj-main")
    print()
    print("⚠️ 주의: 이 스크립트는 다음을 수행합니다:")
    print("  1. 현재 AI 학습 데이터 백업")
    print("  2. GitHub에서 최신 코드 다운로드")
    print("  3. 새 폴더에 압축 해제")
    print("  4. AI 학습 데이터 복원")
    print("  5. 캐시 삭제 및 검증")
    print()
    
    input("Enter를 눌러 계속...")
    print()
    
    try:
        # 현재 디렉토리 (기존 봇)
        old_dir = Path.cwd()
        print(f"📁 현재 디렉토리: {old_dir}")
        
        # 부모 디렉토리 (다운로드 폴더)
        parent_dir = old_dir.parent.parent  # Lj-main의 부모의 부모
        print(f"📁 다운로드 위치: {parent_dir}")
        print()
        
        # 1. AI 데이터 백업
        backup_dir, backed_up_items = backup_ai_data(old_dir)
        
        input("\nEnter를 눌러 다운로드 시작...")
        
        # 2. 최신 코드 다운로드
        zip_path = download_latest_release(parent_dir)
        if not zip_path:
            print("\n❌ 다운로드 실패. 수동으로 다운로드하세요:")
            print("   https://github.com/lee-jungkil/Lj/archive/refs/heads/main.zip")
            return
        
        # 3. 압축 해제
        new_dir = extract_zip(zip_path, parent_dir)
        if not new_dir:
            print("\n❌ 압축 해제 실패")
            return
        
        # 4. AI 데이터 복원
        restore_ai_data(new_dir, backup_dir, backed_up_items)
        
        # 5. 캐시 삭제
        clear_cache(new_dir)
        
        # 6. 검증
        all_exist, version = verify_installation(new_dir)
        
        # 7. 완료
        print("="*70)
        print("  ✅ 전체 새로 설치 완료!")
        print("="*70)
        print()
        print(f"📁 새 봇 위치: {new_dir}")
        print(f"📦 버전: {version}")
        print(f"💾 백업 위치: {backup_dir}")
        print()
        print("="*70)
        print()
        print("📋 다음 단계:")
        print()
        print("1. 새 폴더로 이동:")
        print(f"   cd {new_dir}")
        print()
        print("2. 테스트 실행:")
        print("   python test_smart_investment.py")
        print()
        print("3. 봇 시작:")
        print("   python -B -u -m src.main --mode paper")
        print()
        print("="*70)
        print()
        print("⚠️ 주의:")
        print(f"  - 기존 폴더: {old_dir}")
        print(f"  - 새 폴더: {new_dir}")
        print("  - 새 폴더에서 봇을 실행하세요!")
        print("  - 기존 폴더는 삭제해도 됩니다 (백업 완료)")
        print()
        
        # ZIP 파일 삭제
        if zip_path.exists():
            zip_path.unlink()
            print(f"🗑️ ZIP 파일 삭제: {zip_path.name}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자가 중단했습니다")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
