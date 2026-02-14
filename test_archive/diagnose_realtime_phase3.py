#!/usr/bin/env python3
"""
실시간 Phase 3 실행 진단 스크립트
실제 봇 실행 중에 왜 Phase 3가 작동하지 않는지 진단
"""

import sys
import time
import importlib.util

def diagnose_python_cache():
    """Python 캐시 상태 진단"""
    
    print("=" * 80)
    print("🔍 Python 캐시 상태 진단")
    print("=" * 80)
    print()
    
    # main.py 파일 경로
    main_py = "/home/user/webapp/src/main.py"
    
    # 캐시 폴더 확인
    import os
    cache_dirs = []
    for root, dirs, files in os.walk("/home/user/webapp"):
        for d in dirs:
            if d == "__pycache__":
                cache_path = os.path.join(root, d)
                cache_dirs.append(cache_path)
                
                # .pyc 파일 찾기
                for pyc_file in os.listdir(cache_path):
                    if pyc_file.endswith(".pyc"):
                        pyc_path = os.path.join(cache_path, pyc_file)
                        pyc_stat = os.stat(pyc_path)
                        py_stat = os.stat(main_py) if os.path.exists(main_py) else None
                        
                        print(f"📁 {cache_path}")
                        print(f"   📄 {pyc_file}")
                        print(f"      수정 시간: {time.ctime(pyc_stat.st_mtime)}")
                        
                        if py_stat:
                            if pyc_stat.st_mtime < py_stat.st_mtime:
                                print(f"      ⚠️  .py 파일이 더 최신! (.pyc 오래됨)")
                            else:
                                print(f"      ✅ .pyc 파일이 최신 (또는 동일)")
                        print()
    
    if not cache_dirs:
        print("   ✅ __pycache__ 폴더 없음 (깨끗한 상태)")
    else:
        print(f"   총 {len(cache_dirs)}개의 __pycache__ 폴더 발견")
    
    print()

def check_main_py_version():
    """main.py 파일의 Phase 3 코드 확인"""
    
    print("=" * 80)
    print("🔍 main.py Phase 3 코드 버전 확인")
    print("=" * 80)
    print()
    
    with open("/home/user/webapp/src/main.py", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 라인 2143 확인
    line_2143 = lines[2142].strip() if len(lines) > 2142 else ""
    
    print(f"Line 2143: {line_2143}")
    print()
    
    if "current_time - self.last_position_check_time >= self.position_check_interval" in line_2143:
        print("   ✅ v6.30.29 코드 확인됨!")
        print("   ✅ Phase 3 시간 체크 로직 존재!")
        return True
    elif "if self.risk_manager.positions:" in line_2143:
        print("   ❌ v6.30.28 이전 코드!")
        print("   ❌ Phase 3 시간 체크 로직 없음!")
        return False
    else:
        print("   ⚠️  알 수 없는 코드 형식")
        print(f"   내용: {line_2143}")
        return False

def simulate_bot_import():
    """봇을 실제로 import했을 때의 코드 버전 확인"""
    
    print("=" * 80)
    print("🔍 실제 import 시 로드되는 코드 확인")
    print("=" * 80)
    print()
    
    try:
        # src.main import
        sys.path.insert(0, '/home/user/webapp')
        
        # 기존 모듈 제거 (캐시 무시)
        if 'src.main' in sys.modules:
            del sys.modules['src.main']
        if 'src' in sys.modules:
            del sys.modules['src']
        
        # 새로 import
        from src import main as bot_main
        
        # TradingBot 클래스 확인
        if hasattr(bot_main, 'TradingBot'):
            bot_class = bot_main.TradingBot
            
            # 소스 코드 확인
            import inspect
            source = inspect.getsource(bot_class)
            
            # Phase 3 코드 검색
            if "current_time - self.last_position_check_time >= self.position_check_interval" in source:
                print("   ✅ import된 코드는 v6.30.29!")
                print("   ✅ 최신 Phase 3 로직 포함!")
                return True
            elif "if self.risk_manager.positions:" in source:
                print("   ❌ import된 코드는 v6.30.28 이전!")
                print("   ❌ 구버전 Phase 3 로직!")
                return False
            else:
                print("   ⚠️  Phase 3 코드를 찾을 수 없음")
                return False
        else:
            print("   ❌ TradingBot 클래스를 찾을 수 없음")
            return False
            
    except Exception as e:
        print(f"   ❌ import 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_position_check_interval_init():
    """position_check_interval 초기화 확인"""
    
    print("=" * 80)
    print("🔍 position_check_interval 초기화 확인")
    print("=" * 80)
    print()
    
    with open("/home/user/webapp/src/main.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # self.position_check_interval 검색
    if "self.position_check_interval" in content:
        print("   ✅ position_check_interval 정의 존재")
        
        # 초기화 위치 찾기
        for i, line in enumerate(content.split("\n"), 1):
            if "self.position_check_interval" in line and "=" in line:
                print(f"   Line {i}: {line.strip()}")
        
        return True
    else:
        print("   ❌ position_check_interval 정의 없음!")
        return False

if __name__ == "__main__":
    print("\n" * 2)
    print("🏥 실시간 Phase 3 실행 진단")
    print("실제 봇이 왜 '⚡ 포지션 청산 체크' 로그를 출력하지 않는지 확인합니다")
    print()
    input("엔터를 눌러 진단 시작...")
    print("\n" * 2)
    
    # 1. Python 캐시 상태
    diagnose_python_cache()
    
    # 2. main.py 파일 버전
    file_ok = check_main_py_version()
    
    # 3. 실제 import 버전
    import_ok = simulate_bot_import()
    
    # 4. 초기화 확인
    init_ok = check_position_check_interval_init()
    
    # 최종 진단
    print("\n" * 2)
    print("=" * 80)
    print("📊 최종 진단 결과")
    print("=" * 80)
    print()
    
    print(f"   main.py 파일 버전: {'✅ v6.30.29' if file_ok else '❌ 구버전'}")
    print(f"   import 코드 버전: {'✅ v6.30.29' if import_ok else '❌ 구버전'}")
    print(f"   변수 초기화 확인: {'✅ 정상' if init_ok else '❌ 누락'}")
    print()
    
    if file_ok and import_ok and init_ok:
        print("   ✅ 모든 코드가 최신 버전입니다!")
        print("   ✅ Phase 3 로직이 정상적으로 로드됩니다!")
        print()
        print("   봇을 재시작하면 정상 작동할 것으로 예상됩니다.")
    elif file_ok and not import_ok:
        print("   ⚠️  main.py는 최신이지만 import 시 구버전 로드!")
        print("   ⚠️  Python 캐시 (.pyc) 문제 확실!")
        print()
        print("   🔧 해결 방법:")
        print("      1. 모든 python.exe 프로세스 종료")
        print("      2. __pycache__ 폴더 전체 삭제")
        print("      3. 봇 재시작")
        print()
        print("   또는:")
        print("      FIX_POSITION_CHECK_URGENT.bat 실행")
    elif not file_ok:
        print("   ❌ main.py 파일 자체가 구버전!")
        print("   ❌ git pull이 제대로 안 됐거나 파일이 되돌아갔습니다!")
        print()
        print("   🔧 해결 방법:")
        print("      git reset --hard HEAD")
        print("      git pull origin main --force")
    else:
        print("   ❌ 알 수 없는 문제!")
        print("   ❌ 수동 점검 필요!")
    
    print("=" * 80)
    print()
