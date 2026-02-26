from pathlib import Path
from app.core.database import init_db
from app.services.pipeline import register_directory, recommend_playlist


def test_full_pipeline():
    # 1. DB 초기화
    init_db()

    # 2. 샘플 디렉토리 일괄 등록
    print("\n" + "=" * 50)
    print("📥 STEP 1: 오디오 파일 등록")
    print("=" * 50)
    register_directory("data/samples", game="테스트")

    # 3. 다양한 쿼리로 플레이리스트 추천
    queries = [
        ("집중해서 코딩하고 싶어", None),
        ("잔잔하게 쉬고 싶어", "휴식"),
        ("신나게 운동하고 싶어", "운동"),
        ("감성적인 음악 듣고 싶어", "감상"),
    ]

    for query, situation in queries:
        print(f"\n{'=' * 50}")
        print(f"🔍 쿼리: '{query}'", end="")
        if situation:
            print(f"  (상황 필터: {situation})", end="")
        print()
        print("=" * 50)

        playlist = recommend_playlist(query, top_k=3, situation_filter=situation)

        if not playlist:
            print("  결과 없음")
            continue

        for item in playlist:
            print(f"  {item['rank']}. {item['title']}", end="")
            if item['game']:
                print(f" [{item['game']}]", end="")
            print()
            print(f"     🏷️  무드: {item['mood']}  상황: {item['situation']}")
            print(f"     🥁 BPM: {item['bpm']} ({item['bpm_category']})  "
                  f"⚡ 에너지: {item['energy']} ({item['energy_level']})")
            print(f"     📊 유사도: {item['similarity']}")


if __name__ == "__main__":
    test_full_pipeline()