"""
거래 로그 파일 복구 도구
손상된 JSON 파일을 정리하고 복구합니다
"""
import json
from pathlib import Path
from datetime import datetime


def fix_log_files():
    """모든 거래 로그 파일 검증 및 복구"""
    log_dir = Path("trading_logs")
    
    if not log_dir.exists():
        print("❌ trading_logs 폴더가 없습니다")
        return
    
    print("=" * 60)
    print("거래 로그 파일 복구 도구")
    print("=" * 60)
    print()
    
    # JSON 파일 찾기
    json_files = list(log_dir.glob("trade_*.json"))
    
    if not json_files:
        print("✅ 거래 로그 파일이 없습니다 (정상)")
        return
    
    print(f"📂 발견된 파일: {len(json_files)}개")
    print()
    
    fixed_count = 0
    error_count = 0
    
    for json_file in json_files:
        print(f"검사 중: {json_file.name}")
        
        try:
            # 파일 읽기
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                print(f"  ⚠️  빈 파일 - 초기화")
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                fixed_count += 1
                continue
            
            # JSON 파싱 시도
            try:
                trades = json.loads(content)
                
                if not isinstance(trades, list):
                    print(f"  ⚠️  리스트가 아님 - 변환")
                    trades = []
                
                # 유효성 검증
                valid_trades = []
                for trade in trades:
                    if isinstance(trade, dict) and 'ticker' in trade:
                        valid_trades.append(trade)
                
                # 재저장
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(valid_trades, f, ensure_ascii=False, indent=2)
                
                print(f"  ✅ 정상 ({len(valid_trades)}건 거래)")
                
            except json.JSONDecodeError as e:
                print(f"  ❌ JSON 오류: {e}")
                
                # 백업
                backup_path = json_file.with_suffix('.json.backup')
                json_file.rename(backup_path)
                print(f"  💾 백업 생성: {backup_path.name}")
                
                # 새 파일 생성
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                print(f"  🔧 새 파일 생성")
                
                fixed_count += 1
                error_count += 1
        
        except Exception as e:
            print(f"  ❌ 처리 실패: {e}")
            error_count += 1
    
    print()
    print("=" * 60)
    print(f"완료: 수정 {fixed_count}개, 오류 {error_count}개")
    print("=" * 60)
    
    if error_count > 0:
        print()
        print("💡 TIP:")
        print("  - .backup 파일은 원본 백업입니다")
        print("  - 봇을 다시 실행하면 정상 작동합니다")


if __name__ == "__main__":
    fix_log_files()
    print()
    input("엔터를 눌러 종료...")
