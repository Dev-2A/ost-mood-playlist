"""
초기 DB 구축 스크립트.
dasta/audio/ 하위의 게임별 폴더를 순서대로 등록합니다.

사용법:
    python scripts/init_db.py
"""
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import init_db
from app.services.pipeline import register_directory


GAME_DIRS = {
    "data/audio/ffxiv": "FINAL FANTASY XIV",
    "data/audio/stardew": "Stardew Valley",
    "data/audio/undertale": "UNDERTALE",
    "data/audio/etc": None,
}


def main():
    print("🎵 OST Mood Playlist — 초기 DB 구축")
    print("=" * 50)
    
    init_db()
    
    total = 0
    for dir_path, game_name in GAME_DIRS.items():
        path = Path(dir_path)
        if not path.exists():
            print(f"⚠️  폴더 없음, 건너뜀: {dir_path}")
            continue
        
        label = game_name if game_name else "기타"
        print(f"\n📁 [{label}] {dir_path}")
        print("-" * 40)
        
        tracks = register_directory(dir_path, game=game_name)
        total += len(tracks)
    
    print("\n" + "=" * 50)
    print(f"🏁 전체 등록 완료: {total}개")


if __name__ == "__main__":
    main()