import json
import numpy as np
from pathlib import Path
from sqlalchemy.orm import Session

from app.models.track import Track
from app.services.audio_analyzer import extract_features
from app.services.tagger import auto_tag
from app.services.embedder import embed_track


def register_track(file_path: str | Path, db: Session, game: str = None) -> Track:
    """
    오디오 파일을 분석하고 DB에 등록합니다.
    이미 등록된 파일이라면 기존 레코드를 반환합니다.
    """
    file_path = str(Path(file_path).resolve())
    
    # 중복 체크
    existing = db.query(Track).filter(Track.file_path == file_path).first()
    if existing:
        print(f"  ⏭️  이미 등록됨: {Path(file_path).name}")
        return existing
    
    print(f"  🔍 분석 중: {Path(file_path).name}")
    
    # 오디오 특징 추출
    features = extract_features(file_path)
    
    # 태그 생성
    tags = auto_tag(features)
    
    # 임베딩 생성
    vector = embed_track(features)
    
    # Track 객체 생성
    track = Track(
        file_path=file_path,
        title=Path(file_path).stem,
        game=game,
        duration=features.duration,
        bpm=features.bpm,
        energy=features.energy,
        valence=features.valence,
        spectral_centroid=features.spectral_centroid,
        zero_crossing_rate=features.zero_crossing_rate,
        mfcc_json=json.dumps(features.mfcc),
        mood_json=json.dumps(tags.mood),
        situation_json=json.dumps(tags.situation),
        bpm_category=tags.bpm_category,
        energy_level=tags.energy_level,
        embedding_json=json.dumps(vector.tolist()),
    )
    
    db.add(track)
    db.commit()
    db.refresh(track)
    print(f"  ✅ 등록 완료: {track.title} (id={track.id})")
    return track


def get_all_tracks(db: Session) -> list[Track]:
    return db.query(Track).all()


def get_track_vectors(db: Session) -> list[tuple[int, np.ndarray]]:
    """모든 곡의 (id, embedding) 리스트 반환"""
    tracks = db.query(Track).filter(Track.embedding_json.isnot(None)).all()
    return [(t.id, t.embedding) for t in tracks]