from sqlalchemy import Column, String, Float, Text, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import json


class Base(DeclarativeBase):
    pass


class Track(Base):
    """곡 메타데이터 + 오디오 특징 + 태그 + 임베딩 벡터"""
    __tablename__ = "tracks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String(512), unique=True, nullable=False)
    title = Column(String(256), nullable=False)         # 파일명에서 추출
    game = Column(String(128), nullable=True)           # 게임명 (선택)
    
    # 오디오 특징
    duration = Column(Float, nullable=False)
    bpm = Column(Float, nullable=False)
    energy = Column(Float, nullable=False)
    valence = Column(Float, nullable=False)
    spectral_centroid = Column(Float, nullable=False)
    zero_crossing_rate = Column(Float, nullable=False)
    mfcc_json = Column(Text, nullable=False)            # JSON 직렬화
    
    # 태그
    mood_json = Column(Text, nullable=False)            # JSON 직렬화
    situation_json = Column(Text, nullable=False)       # JSON 직렬화
    bpm_category = Column(String(16), nullable=False)
    energy_level = Column(String(16), nullable=False)
    
    # 임베딩 벡터 (numpy array -> JSON 직렬화)
    embedding_json = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # ── 헬퍼 프로퍼티 ──────────────────────────
    
    @property
    def mood(self) -> list[str]:
        return json.loads(self.mood_json)
    
    @property
    def situation(self) -> list[str]:
        return json.loads(self.situation_json)
    
    @property
    def mfcc(self) -> list[float]:
        return json.loads(self.mfcc_json)
    
    @property
    def embedding(self):
        import numpy as np
        if self.embedding_json:
            return np.array(json.loads(self.embedding_json))
        return None
    
    def __repr__(self):
        return f"<Track id={self.id} title={self.title}>"