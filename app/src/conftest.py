# app/src/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base  # models 파일에서 Base를 가져옵니다.

# 환경 변수 로드
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '../../../config/.env')
load_dotenv(dotenv_path=dotenv_path)

# async_session fixture 정의
@pytest.fixture
async def async_session():
    db_url = f"mysql+aiomysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"

    # SQLAlchemy 엔진 및 세션 설정
    engine = create_async_engine(db_url, echo=True)
    async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 세션 반환
    async with async_session_maker() as session:
        yield session

    # 엔진 종료
    await engine.dispose()
