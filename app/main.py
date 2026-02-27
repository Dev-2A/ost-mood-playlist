from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import init_db
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 DB 초기화
    init_db()
    yield


app = FastAPI(
    title="🎵 OST Mood Playlist",
    description="게임 OST를 기분·상황별로 태깅하고 맞춤 플레이리스트를 생성합니다.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS 설정 (프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {"message": "🎵 OST Mood Playlist API", "docs": "/docs"}