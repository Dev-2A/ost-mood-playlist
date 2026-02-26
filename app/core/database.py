from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.models.track import Base


engine = create_engine(
    settings.db_url,
    connect_args={"check_same_thread": False},  # SQLite 전용
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    """테이블 생성 (없으면 새로 만듦)"""
    Base.metadata.create_all(bind=engine)
    print("✅ DB 초기화 완료")


def get_db() -> Session:
    """FastAPI 의존성 주입용 세션 생성기"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()