import numpy as np
from sentence_transformers import SentenceTransformer
from app.services.audio_analyzer import AudioFeatures
from app.services.tagger import auto_tag
from app.core.config import settings


# 모델은 최초 1회만 로드
_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"📦 임베딩 모델 로드 중: {settings.embedding_model}")
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def features_to_text(features: AudioFeatures) -> str:
    """
    AudioFeatures → 자연어 문장으로 변환 (임베딩 입력용)
    예: "BPM 128, 에너지 높음, 밝은 분위기, 무드: 신나는, 상황: 코딩 탐험"
    """
    tags = auto_tag(features)
    
    energy_desc = tags.energy_level
    bpm_desc = tags.bpm_category
    mood_str = " ".join(tags.mood)
    situation_str = " ".join(tags.situation)
    
    text = (
        f"BPM {features.bpm:.0f} {bpm_desc}, "
        f"에너지 {energy_desc}, "
        f"밝기 {features.valence:.2f}, "
        f"무드 {mood_str}, "
        f"상황 {situation_str}"
    )
    return text


def embed_track(features: AudioFeatures) -> np.ndarray:
    """
    단일 곡의 특징을 임베딩 벡터로 변환합니다.
    반환: shape (embedding_dim,) numpy array
    """
    model = _get_model()
    text = features_to_text(features)
    vector = model.encode(text, normalize_embeddings=True)
    return vector


def embed_query(mood_query: str) -> np.ndarray:
    """
    사용자가 입력한 기분/상황 텍스트를 임베딩 벡터로 변환합니다.
    예: "집중해서 코딩하고 싶어", "잔잔하게 쉬고 싶어"
    """
    model = _get_model()
    vector = model.encode(mood_query, normalize_embeddings=True)
    return vector


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """두 벡터의 코사인 유사도를 계산합니다. (정규화된 벡터라면 내적과 동일)"""
    return float(np.dot(vec_a, vec_b))


def find_similar_tracks(
    query_vector: np.ndarray,
    track_vectors: list[tuple[str, np.ndarray]],    # [(track_id, vector), ...]
    top_k: int = 10
) -> list[tuple[str, float]]:
    """
    쿼리 벡터와 가장 유사한 곡 top_k개를 반환합니다.
    반환: [(track_id, similarity_score), ...] 내림차순 정렬
    """
    scored = [
        (track_id, cosine_similarity(query_vector, vec))
        for track_id, vec in track_vectors
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]