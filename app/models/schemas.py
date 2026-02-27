from pydantic import BaseModel
from typing import Optional


# ── 요청 스키마 ──────────────────────────────

class PlaylistRequest(BaseModel):
    query: str                  # 기분/상황 자연어 입력
    top_k: int = 10             # 추천 곡 수
    situation_filter: Optional[str] = None  # 상황 태그 필터 (선택)


class RegisterRequest(BaseModel):
    audio_dir: str              # 등록할 디렉토리 경로
    game: Optional[str] = None  # 게임명 (선택)


# ── 응답 스키마 ──────────────────────────────

class TrackResponse(BaseModel):
    rank: int
    id: int
    title: str
    game: Optional[str]
    bpm: float
    energy: float
    mood: list[str]
    situation: list[str]
    bpm_category: str
    energy_level: str
    similarity: float
    file_path: str


class PlaylistResponse(BaseModel):
    query: str
    situation_filter: Optional[str]
    total: int
    tracks: list[TrackResponse]


class RegisterResponse(BaseModel):
    message: str
    registered: int


class TrackDetailResponse(BaseModel):
    id: int
    title: str
    game: Optional[str]
    duration: float
    bpm: float
    energy: float
    valence: float
    mood: list[str]
    situation: list[str]
    bpm_category: str
    energy_level: str