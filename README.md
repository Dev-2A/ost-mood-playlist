# 🎵 OST Mood Playlist

> 게임 OST를 기분·상황별로 자동 태깅하고, 현재 기분을 입력하면 맞춤 플레이리스트를 생성하는 서비스

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)
![librosa](https://img.shields.io/badge/librosa-0.10-orange?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## 📌 주요 기능

- 🎼 **오디오 자동 분석** — librosa로 BPM·에너지·음색 등 특징 추출
- 🏷️ **자동 태깅** — 분석 결과를 무드(밝음·어두움·웅장함 등) / 상황(코딩·휴식·전투 등) 태그로 변환
- 🔍 **임베딩 기반 추천** — sentence-transformers로 기분 텍스트와 곡의 유사도 계산
- 🎮 **게임별 관리** — FFXIV·스타듀밸리 등 게임명으로 분류
- 🌐 **웹 UI** — 기분 입력 / 빠른 선택 버튼 / 하단 플레이어

---

## 🖥️ 스크린샷

> 기분을 입력하면 유사도 순으로 플레이리스트가 생성됩니다.

---

## 🛠️ 기술 스택

| 분류 | 기술 |
| ------ | ------ |
| Backend | Python 3.11, FastAPI, SQLAlchemy |
| 오디오 분석 | librosa, soundfile, numpy |
| 임베딩/ML | sentence-transformers, scikit-learn |
| 저장소 | SQLite |
| Frontend | HTML, CSS, JavaScript (바닐라) |

---

## 📁 프로젝트 구조

```text
ost-mood-playlist/
├── app/
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── api/
│   │   └── routes.py           # API 엔드포인트
│   ├── core/
│   │   ├── config.py           # 설정 모듈
│   │   └── database.py         # DB 세션 관리
│   ├── models/
│   │   ├── track.py            # SQLAlchemy 모델
│   │   └── schemas.py          # Pydantic 스키마
│   └── services/
│       ├── audio_analyzer.py   # librosa 특징 추출
│       ├── tagger.py           # 자동 태깅
│       ├── embedder.py         # 임베딩 및 유사도
│       ├── track_service.py    # 곡 CRUD
│       └── pipeline.py         # 통합 파이프라인
├── scripts/
│   ├── init_db.py              # 초기 DB 구축
│   ├── show_db.py              # DB 현황 조회
│   └── reset_db.py             # DB 초기화
├── static/
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
├── data/
│   └── audio/
│       ├── ffxiv/
│       ├── stardew/
│       └── etc/
├── tests/
│   ├── test_audio_analyzer.py
│   ├── test_tagger.py
│   ├── test_embedder.py
│   ├── test_database.py
│   └── test_pipeline.py
├── .env
├── .gitignore
├── LICENSE
├── pyproject.toml
└── requirements.txt
```

---

## 🚀 설치 및 실행

### 1. 레포지토리 클론

```bash
git clone https://github.com/Dev-2A/ost-mood-playlist.git
cd ost-mood-playlist
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. 오디오 파일 준비

```text
data/audio/ffxiv/     ← FFXIV OST mp3 파일
data/audio/stardew/   ← 스타듀밸리 OST mp3 파일
data/audio/etc/       ← 기타 게임 OST
```

### 5. 초기 DB 구축

```bash
python scripts/init_db.py
```

### 6. 서버 실행

```bash
uvicorn app.main:app --reload --port 8000
```

브라우저에서 `http://localhost:8000` 접속

---

## 📡 API 엔드포인트

| Method | URL | 설명 |
| -------- | ----- | ------ |
| POST | `/api/playlist` | 기분 입력 → 플레이리스트 생성 |
| GET | `/api/tracks` | 전체 곡 목록 조회 |
| GET | `/api/tracks/{id}` | 특정 곡 상세 정보 |
| GET | `/api/audio/{id}` | 오디오 스트리밍 |
| POST | `/api/register` | 디렉토리 일괄 등록 |
| POST | `/api/register/file` | 단일 파일 등록 |
| GET | `/api/tags/moods` | 무드 태그 목록 |
| GET | `/api/tags/situations` | 상황 태그 목록 |

Swagger UI: `http://localhost:8000/docs`

---

## 🏷️ 태그 목록

**무드** — 밝음, 어두움, 잔잔함, 웅장함, 긴장감, 감성적, 신나는, 몽환적

**상황** — 코딩, 집중, 휴식, 수면, 운동, 전투, 탐험, 감상

---

## 📝 유틸 스크립트

```bash
# DB 현황 확인
python scripts/show_db.py

# DB 전체 초기화 (주의: 데이터 전체 삭제)
python scripts/reset_db.py
```

---

## 📄 License

MIT License © 2026
