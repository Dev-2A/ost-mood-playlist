"""
현재 DB에 등록된 곡 목록과 태그 현황을 출력합니다.

사용법:
    python scripts/show_db.py
"""
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal
from app.services.track_service import get_all_tracks


def main():
    db = SessionLocal()
    try:
        tracks = get_all_tracks(db)

        if not tracks:
            print("⚠️ 등록된 곡이 없습니다.")
            return

        print(f"🎵 총 {len(tracks)}개 곡 등록됨\n")
        print(f"{'ID':<5} {'제목':<30} {'게임':<20} {'BPM':<8} {'에너지':<10} {'무드'}")
        print("-" * 90)

        mood_counter = Counter()
        situation_counter = Counter()

        for t in tracks:
            title = t.title[:28] + ".." if len(t.title) > 28 else t.title
            game = (t.game or "-")[:18]
            print(
                f"{t.id:<5} {title:<30} {game:<20} "
                f"{t.bpm:<8.1f} {t.energy:<10.3f} "
                f"{', '.join(t.mood)}"
            )
            mood_counter.update(t.mood)
            situation_counter.update(t.situation)

        print("\n📊 무드 태그 분포:")
        for tag, count in mood_counter.most_common():
            bar = "█" * count
            print(f"  {tag:<10} {bar} ({count})")

        print("\n📊 상황 태그 분포:")
        for tag, count in situation_counter.most_common():
            bar = "█" * count
            print(f"  {tag:<10} {bar} ({count})")

    finally:
        db.close()


if __name__ == "__main__":
    main()