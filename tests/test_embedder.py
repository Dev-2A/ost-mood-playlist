from pathlib import Path
from app.services.audio_analyzer import extract_features
from app.services.embedder import (
    embed_track,
    embed_query,
    features_to_text,
    find_similar_tracks,
)


def test_embedding():
    sample_dir = Path("data/samples")
    files = list(sample_dir.glob("*"))

    if not files:
        print("⚠️ data/samples/ 에 오디오 파일을 넣어주세요.")
        return

    # 곡 임베딩
    track_vectors = []
    for file in files:
        try:
            features = extract_features(file)
            text = features_to_text(features)
            vector = embed_track(features)
            track_vectors.append((file.name, vector))
            print(f"\n🎵 {file.name}")
            print(f"   텍스트: {text}")
            print(f"   벡터 shape: {vector.shape}")
        except Exception as e:
            print(f"⚠️ 오류 ({file.name}): {e}")

    if len(track_vectors) < 2:
        print("\n⚠️ 유사도 검색 테스트는 파일 2개 이상 필요합니다.")
        return

    # 쿼리로 유사 곡 검색
    query = "집중해서 코딩하고 싶어"
    print(f"\n🔍 쿼리: '{query}'")
    query_vec = embed_query(query)
    results = find_similar_tracks(query_vec, track_vectors, top_k=3)

    print("📋 추천 결과:")
    for rank, (track_id, score) in enumerate(results, 1):
        print(f"   {rank}. {track_id}  (유사도: {score:.4f})")


if __name__ == "__main__":
    test_embedding()