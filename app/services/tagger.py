from dataclasses import dataclass
from app.services.audio_analyzer import AudioFeatures


# 무드 태그
MOOD_TAGS = [
    "밝음", "어두움", "잔잔함", "웅장함", "긴장감", "감성적", "신나는", "몽환적"
]

# 상황 태그
SITUATION_TAGS = [
    "코딩", "집중", "휴식", "수면", "운동", "전투", "탐험", "감상"
]


@dataclass
class TrackTags:
    """곡에 붙은 태그 결과"""
    mood: list[str]         # 무드 태그 (복수 가능)
    situation: list[str]    # 상황 태그 (복수 가능)
    bpm_category: str       # "느림" / "보통" / "빠름"
    energy_level: str       # "저에너지" / "중에너지" / "고에너지"


def _bpm_category(bpm: float) -> str:
    if bpm < 80:
        return "느림"
    elif bpm < 130:
        return "보통"
    else:
        return "빠름"


def _energy_level(energy: float) -> str:
    if energy < 0.3:
        return "저에너지"
    elif energy < 0.65:
        return "중에너지"
    else:
        return "고에너지"


def auto_tag(features: AudioFeatures) -> TrackTags:
    """
    오디오 특징값을 기반으로 무드/상황 태그를 자동 부여합니다.
    규칙 기반 휴리스틱 방식.
    """
    mood = []
    situation = []
    
    bpm = features.bpm
    energy = features.energy
    valence = features.valence
    zcr = features.zero_crossing_rate
    
    # ── 무드 태깅 ──────────────────────────────
    if valence > 0.6:
        mood.append("밝음")
    if valence < 0.4:
        mood.append("어두움")
    if energy < 0.3 and bpm < 90:
        mood.append("잔잔함")
    if energy > 0.65 and bpm > 120:
        mood.append('웅장함')
    if zcr > 0.08 and energy > 0.5:
        mood.append("긴장감")
    if valence < 0.5 and energy < 0.5 and bpm < 100:
        mood.append("감성적")
    if bpm > 130 and energy > 0.6 and valence > 0.5:
        mood.append("신나는")
    if energy < 0.4 and valence > 0.4 and bpm < 100:
        mood.append("몽환적")
    
    # 태그 없으면 기본값
    if not mood:
        mood.append("잔잔함")
    
    # ── 상황 태깅 ──────────────────────────────
    if 80 <= bpm <= 130 and 0.3 <= energy <= 0.65:
        situation.append("코딩")
    if energy < 0.5 and bpm < 110:
        situation.append("집중")
    if energy < 0.35 and bpm < 90:
        situation.append("휴식")
    if energy < 0.25 and bpm < 75:
        situation.append("수면")
    if energy > 0.6 and bpm > 120:
        situation.append("운동")
    if energy > 0.65 and zcr > 0.07:
        situation.append("전투")
    if 0.4 <= energy <= 0.7 and 90 <= bpm <= 140:
        situation.append("탐험")
    if valence < 0.5 and energy < 0.5:
        situation.append("감상")

    # 태그 없으면 기본값
    if not situation:
        situation.append("집중")
    
    return TrackTags(
        mood=mood,
        situation=situation,
        bpm_category=_bpm_category(bpm),
        energy_level=_energy_level(energy),
    )


def tag_from_features(features: AudioFeatures) -> dict:
    """
    AudioFeatures → 저장 가능한 dict 형태로 반환
    """
    tags = auto_tag(features)
    return {
        "mood": tags.mood,
        "situation": tags.situation,
        "bpm_category": tags.bpm_category,
        "energy_level": tags.energy_level,
    }