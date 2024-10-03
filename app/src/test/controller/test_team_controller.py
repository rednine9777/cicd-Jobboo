# import asyncio
# from sqlalchemy.ext.asyncio import AsyncSession
# from database import AsyncSessionLocal  # AsyncSessionLocal 임포트
# import pytest
# import logging
# from rich.logging import RichHandler
# from rich.console import Console
# from httpx import AsyncClient  # FastAPI API 테스트를 위한 httpx.AsyncClient 사용
# from main import app  # FastAPI 앱 임포트

# # Rich 콘솔 설정
# console = Console()
# logging.basicConfig(level="INFO", format="%(message)s", handlers=[RichHandler(console=console, rich_tracebacks=True)])

# # AsyncSession을 제공하는 피처 정의
# @pytest.fixture(scope="function")
# async def async_session() -> AsyncSession:
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         finally:
#             if session.in_transaction():
#                 await session.rollback()
#             await session.close()

# # 팀 리스트 API 테스트 (httpx.AsyncClient 사용)
# @pytest.mark.asyncio
# async def test_list_team_api():
#     async with AsyncClient(app=app, base_url="http://testserver") as client:
#         response = await client.get("/list_team")

#         # 로그 출력
#         logging.info(f"API 응답 상태 코드: {response.status_code}")

#         # 응답 검증
#         assert response.status_code == 200
#         assert "teams" in response.json()
#         logging.info(f"팀 리스트: {response.json()['teams']}")
