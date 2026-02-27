"""
DB를 완전히 초기화합니다. (전체 삭제 후 재생성)
주의: 등록된 모든 곡 데이터가 삭제됩니다.

사용법:
    python scripts/reset_db.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.core.database import init_db
from app.models.track import Base
from sqlalchemy import create_engine


def main():
    confirm = input("⚠️  DB를 초기화하면 모든 데이터가 삭제됩니다. 계속할까요? (yes/no): ")
    if confirm.strip().lower() != "yes":
        print("취소되었습니다.")
        return

    db_path = Path(settings.db_url.replace("sqlite:///", ""))
    if db_path.exists():
        db_path.unlink()
        print(f"🗑️  기존 DB 삭제: {db_path}")

    init_db()
    print("✅ DB 초기화 완료. scripts/init_db.py 로 곡을 다시 등록하세요.")


if __name__ == "__main__":
    main()