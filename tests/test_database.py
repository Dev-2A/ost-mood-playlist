from pathlib import Path
from app.core.database import init_db, SessionLocal
from app.services.track_service import register_track, get_all_tracks


def test_db():
    # DB 초기화
    init_db()

    db = SessionLocal()
    try:
        sample_dir = Path("data/samples")
        files = list(sample_dir.glob("*"))

        if not files:
            print("⚠️ data/samples/ 에 오디오 파일을 넣어주세요.")
            return

        # 등록
        print("\n📥 곡 등록 테스트:")
        for file in files:
            register_track(file, db, game="테스트")

        # 조회
        print("\n📋 등록된 곡 목록:")
        tracks = get_all_tracks(db)
        for t in tracks:
            print(f"  [{t.id}] {t.title}")
            print(f"       무드: {t.mood} | 상황: {t.situation}")
            print(f"       BPM: {t.bpm:.1f} | 에너지: {t.energy:.3f}")

    finally:
        db.close()


if __name__ == "__main__":
    test_db()