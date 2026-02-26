from pathlib import Path
from sqlalchemy.orm import Session

from app.core.database import init_db, SessionLocal
from app.services.track_service import register_track, get_all_tracks, get_track_vectors
from app.services.embedder import embed_query, find_similar_tracks
from app.models.track import Track


AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}


def register_directory(
    audio_dir: str | Path,
    game: str = None,
    db: Session = None,
) -> list[Track]:
    """
    디렉토리 내 오디오 파일을 전부 DB에 등록합니다.
    game 인자로 게임명을 일괄 지정할 수 있습니다.
    """
    audio_dir = Path(audio_dir)
    if not audio_dir.exists():
        raise FileNotFoundError(f"디렉토리를 찾을 수 없습니다: {audio_dir}")
    
    files = [
        f for f in audio_dir.rglob("*")
        if f.suffix.lower() in AUDIO_EXTENSIONS
    ]
    
    if not files:
        print(f"⚠️ {audio_dir} 에 오디오 파일이 없습니다.")
        return []

    print(f"🎵 총 {len(files)}개 파일 발견 → 등록 시작\n")
    
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
    
    registered = []
    try:
        for i, file in enumerate(files, 1):
            print(f"[{i}/{len(files)}]", end=" ")
            track = register_track(file, db, game=game)
            registered.append(track)
    finally:
        if close_db:
            db.close()
    
    print(f"\n✅ 등록 완료: {len(registered)}개")
    return registered


def recommend_playlist(
    mood_query: str,
    top_k: int = 10,
    situation_filter: str = None,
    db: Session = None,
) -> list[dict]:
    """
    기분/상황 텍스트를 입력받아 맞춤 플레이리스트를 반환합니다.
    
    Args:
        mood_query: 자연어 기분 입력 ("집중해서 코딩하고 싶어" 등)
        top_k: 추천 곡 수
        situation_filter: 상황 태그로 사전 필터링 ("코딩", "휴식" 등)
        db: DB 세션
    
    Returns:
        [{"rank": 1, "id": 1, "title": "...", "game": "...", ...}, ...]
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
    
    try:
        # 상황 필터링
        if situation_filter:
            all_tracks = (
                db.query(Track)
                .filter(Track.embedding_json.isnot(None))
                .all()
            )
            tracks = [t for t in all_tracks if situation_filter in t.situation]
        else:
            tracks = db.query(Track).filter(Track.embedding_json.isnot(None)).all()
        
        if not tracks:
            print("⚠️ 조건에 맞는 곡이 없습니다.")
            return []
        
        # 쿼리 임베딩
        query_vec = embed_query(mood_query)
        
        # 유사도 계산
        track_vectors = [(t.id, t.embedding) for t in tracks]
        results = find_similar_tracks(query_vec, track_vectors, top_k=top_k)
        
        # 결과 조립
        id_to_track = {t.id: t for t in tracks}
        playlist = []
        for rank, (track_id, score) in enumerate(results, 1):
            t = id_to_track[track_id]
            playlist.append({
                "rank": rank,
                "id": t.id,
                "title": t.title,
                "game": t.game,
                "bpm": round(t.bpm, 1),
                "energy": round(t.energy, 3),
                "mood": t.mood,
                "situation": t.situation,
                "bpm_category": t.bpm_category,
                "energy_level": t.energy_level,
                "similarity": round(score, 4),
                "file_path": t.file_path,
            })
        
        return playlist
    
    finally:
        if close_db:
            db.close()