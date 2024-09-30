import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Base  # 정확한 경로로 수정

# DB URL 설정
@pytest.fixture
async def async_session():
    engine = create_async_engine("mysql+aiomysql://user:password@localhost/test_db", echo=True)
    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        yield session

    await engine.dispose()
