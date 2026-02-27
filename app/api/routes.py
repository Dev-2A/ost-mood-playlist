from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse as FastFileResponse
from sqlalchemy.orm import Session
import os

from app.core.database import get_db
from app.models.schemas import (
    PlaylistRequest, PlaylistResponse, TrackResponse,
    RegisterRequest, RegisterResponse,
    TrackDetailResponse,
)
from app.services.pipeline import recommend_playlist, register_directory
from app.services.track_service import get_all_tracks
from app.models.track import Track

router = APIRouter()


@router.post("/playlist", response_model=PlaylistResponse)
def get_playlist(req: PlaylistRequest, db: Session = Depends(get_db)):
    """
    기분/상황 텍스트를 입력받아 맞춤 플레이리스트를 반환합니다.
    """
    results = recommend_playlist(
        mood_query=req.query,
        top_k=req.top_k,
        situation_filter=req.situation_filter,
        db=db,
    )
    
    if not results:
        raise HTTPException(status_code=404, detail="조건에 맞는 곡이 없습니다.")
    
    return PlaylistResponse(
        query=req.query,
        situation_filter=req.situation_filter,
        total=len(results),
        tracks=[TrackResponse(**item) for item in results],
    )


@router.post("/register", response_model=RegisterResponse)
def register_tracks(req: RegisterRequest, db: Session = Depends(get_db)):
    """
    디렉토리 내 오디오 파일을 일괄 분석/등록 합니다.
    """
    try:
        tracks = register_directory(
            audio_dir=req.audio_dir,
            game=req.game,
            db=db,
        )
        return RegisterResponse(
            message="등록 완료",
            registered=len(tracks),
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/tracks", response_model=list[TrackDetailResponse])
def list_tracks(db: Session = Depends(get_db)):
    """
    등록된 모든 곡 목록을 반환합니다.
    """
    tracks = get_all_tracks(db)
    return [
        TrackDetailResponse(
            id=t.id,
            title=t.title,
            game=t.game,
            duration=t.duration,
            bpm=t.bpm,
            energy=t.energy,
            valence=t.valence,
            mood=t.mood,
            situation=t.situation,
            bpm_category=t.bpm_category,
            energy_level=t.energy_level,
        )
        for t in tracks
    ]


@router.get("/tracks/{track_id}", response_model=TrackDetailResponse)
def get_track(track_id: int, db: Session = Depends(get_db)):
    """
    특정 곡의 상세 정보를 반환합니다.
    """
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="곡을 찾을 수 없습니다.")
    
    return TrackDetailResponse(
        id=track.id,
        title=track.title,
        game=track.game,
        duration=track.duration,
        bpm=track.bpm,
        energy=track.energy,
        valence=track.valence,
        mood=track.mood,
        situation=track.situation,
        bpm_category=track.bpm_category,
        energy_level=track.energy_level,
    )


@router.get("/tags/situations")
def list_situations():
    """사용 가능한 상황 태그 목록"""
    from app.services.tagger import SITUATION_TAGS
    return {"situations": SITUATION_TAGS}


@router.get("/tags/moods")
def list_moods():
    """사용 가능한 무드 태그 목록"""
    from app.services.tagger import MOOD_TAGS
    return {"moods": MOOD_TAGS}


@router.get("/audio/{track_id}")
def stream_audio(track_id: int, db: Session = Depends(get_db)):
    """오디오 파일을 스트리밍합니다."""
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="곡을 찾을 수 없습니다.")
    if not os.path.exists(track.file_path):
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    return FastFileResponse(track.file_path, media_type="audio/mpeg")