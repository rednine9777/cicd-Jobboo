import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import sys
import os

# app 디렉토리의 경로를 Python 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
print("Current sys.path:", sys.path)  # 추가된 경로 출력

# models 파일에서 Base를 가져옵니다.
from app.models import Base

# 환경 변수 로드
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '../../../config/.env')
load_dotenv(dotenv_path=dotenv_path)

# async_session fixture 정의
@pytest.fixture
async def async_session():
    db_url = f"mysql+aiomysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
    print("DB URL:", db_url)  # 디버깅을 위해 DB URL 출력
    engine = create_async_engine(db_url, echo=True)
    async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # 세션 확인
    print("세션 생성 시도 중...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("테이블 생성 완료")
    
    async with async_session_maker() as session:
        print("세션이 생성되었습니다:", session)
        yield session

    await engine.dispose()
