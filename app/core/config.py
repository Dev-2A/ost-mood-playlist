from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    app_name: str = "OST Mood Playlist"
    debug: bool = True
    
    db_url: str = f"sqlite:///{BASE_DIR}/data/ost_playlist.db"
    audio_dir: Path = BASE_DIR / "data" / "audio"
    sample_dir: Path = BASE_DIR / "data" / "samples"
    
    embedding_model: str = "snunlp/KR-SBERT-V40K-KlueNLI-augSTS"
    
    class Config:
        env_file = ".env"

settings = Settings()