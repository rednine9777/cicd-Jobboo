# import pytest
# from sqlalchemy.ext.asyncio import AsyncSession
# import os
# from dotenv import load_dotenv

# # 환경에 따라 .env 파일 경로를 동적으로 설정
# dotenv_path = os.getenv('DOTENV_PATH')
# load_dotenv(dotenv_path=dotenv_path)

# # models와 repository 경로를 정확히 지정
# from models import Team
# from src.main.goo.repository.TeamRepository import TeamRepository

# import sys
# print(sys.path)

# import os
# print(os.getcwd())


# # pytest-asyncio 명시적으로 적용
# @pytest.mark.asyncio
# async def test_create_and_get_team_by_name(async_session: AsyncSession):
#     print("세션 시작")
#     async with async_session as session:
#         print("세션 실행 중...")

#         team_repo = TeamRepository(session)

#         # 팀 생성
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

#         # 팀 조회
#         fetched_team = await team_repo.get_team_by_name("Test Team")
#         assert fetched_team is not None
#         assert fetched_team.t_name == "Test Team"
#         assert fetched_team.t_intro == "This is a test team"

#     print("세션 종료")
#     await session.rollback()
