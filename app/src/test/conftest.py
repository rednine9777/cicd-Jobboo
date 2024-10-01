# import pytest
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# import os
# from dotenv import load_dotenv

# dotenv_path = os.getenv('DOTENV_PATH')
# load_dotenv(dotenv_path=dotenv_path)

# @pytest.fixture
# async def async_session():
#     db_url = f"mysql+aiomysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
#     print("DB URL:", db_url)  # 디버깅을 위해 DB URL 출력
#     engine = create_async_engine(db_url, echo=True)
#     async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

#     # 세션 생성 및 제공
#     print("세션 생성 시도 중...")
#     async with async_session_maker() as session:
#         print("세션이 생성되었습니다:", session)
#         yield session

#     # 세션 종료 후 리소스 정리
#     await engine.dispose()
