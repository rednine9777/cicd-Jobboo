# import sys
# import os
# import pytest
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv

# # 환경 변수 로드
# dotenv_path = os.getenv('DOTENV_PATH')
# load_dotenv(dotenv_path=dotenv_path)

# # 프로젝트 루트 경로 명시적으로 추가
# current_path = os.path.dirname(os.path.abspath(__file__))
# root_path = os.path.abspath(os.path.join(current_path, "../../../"))
# sys.path.append(root_path)

# # 디버그 출력 추가
# print(f"Current path: {current_path}")
# print(f"Root path added to sys.path: {root_path}")
# print(f"sys.path: {sys.path}")
# print(f"Current working directory: {os.getcwd()}")

# # 올바른 임포트 방식
# from models import Team
# from src.main.goo.repository import TeamRepository

# # pytest fixture로 세션 설정
# @pytest.fixture
# async def get_async_session():
#     db_url = f"mysql+aiomysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
#     print("DB URL:", db_url)  # 디버깅을 위해 DB URL 출력
#     engine = create_async_engine(db_url, echo=True)
#     async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

#     async with async_session_maker() as session:
#         yield session

#     # 세션 종료 후 리소스 정리
#     await engine.dispose()

# # pytest-asyncio를 사용한 비동기 테스트 함수
# @pytest.mark.asyncio
# async def test_create_and_get_team_by_name(get_async_session):
#     print("세션 시작")
#     # get_async_session을 호출하여 실제 세션 객체 가져오기
#     async for session in get_async_session:
#         team_repo = TeamRepository(session)

#         new_team = Team(
#             t_name="Test Team",
#             t_intro="This is a test team",
#             t_descript="Test description",
#             t_logo="logo.png",
#             t_git="https://github.com/testteam"
#         )
#         created_team = await team_repo.create_team(new_team)

#         # 팀 생성 확인
#         assert created_team.t_name == "Test Team"
#         assert created_team.t_intro == "This is a test team"

#         # 팀 조회 확인
#         fetched_team = await team_repo.get_team_by_name("Test Team")
#         assert fetched_team is not None
#         assert fetched_team.t_name == "Test Team"
#         assert fetched_team.t_intro == "This is a test team"

#         await session.rollback()
