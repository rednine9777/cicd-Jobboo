import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import sys
import os

# app 디렉토리의 경로를 Python 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
print("Current sys.path:", sys.path)  # 추가된 경로 출력

# models 파일에서 Base를 가져옵니다.
from app.models import Base

# 환경 변수 로드
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '../../../config/.env')
load_dotenv(dotenv_path=dotenv_path)

# async_session fixture 정의
@pytest.fixture
async def async_session_maker():
    db_url = f"mysql+aiomysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
    engine = create_async_engine(db_url, echo=True)
    async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # async_session_maker를 반환
    yield async_session_maker

    # 엔진 종료
    await engine.dispose()
