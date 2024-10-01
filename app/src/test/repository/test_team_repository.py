import sys
import os
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

# 프로젝트 루트 경로 명시적으로 추가
current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_path, "../../../"))
sys.path.append(root_path)  # /app 경로를 추가

# 디버그 출력 추가
print(f"Current path: {current_path}")
print(f"Root path added to sys.path: {root_path}")
print(f"sys.path: {sys.path}")
print(f"Current working directory: {os.getcwd()}")

# 올바른 임포트 방식
from models import Team
from src.main.goo.repository import TeamRepository

# pytest-asyncio를 사용한 비동기 테스트 함수
@pytest.mark.asyncio
async def test_create_and_get_team_by_name(async_session: AsyncSession):
    print("세션 시작")
    async with async_session as session:
        team_repo = TeamRepository(session)

        new_team = Team(
            t_name="Test Team",
            t_intro="This is a test team",
            t_descript="Test description",
            t_logo="logo.png",
            t_git="https://github.com/testteam"
        )
        created_team = await team_repo.create_team(new_team)

        # 팀 생성 확인
        assert created_team.t_name == "Test Team"
        assert created_team.t_intro == "This is a test team"

        # 팀 조회 확인
        fetched_team = await team_repo.get_team_by_name("Test Team")
        assert fetched_team is not None
        assert fetched_team.t_name == "Test Team"
        assert fetched_team.t_intro == "This is a test team"

    await session.rollback()
