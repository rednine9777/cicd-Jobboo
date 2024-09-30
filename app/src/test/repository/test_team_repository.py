import pytest
from sqlalchemy.ext.asyncio import AsyncSession
import sys
import os

# Python 경로 설정 후 출력
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
print("Current sys.path:", sys.path)  # 경로 출력

from app.models import Team  # models 경로 수정
from app.src.main.goo.repository.TeamRepository import TeamRepository

# pytest-asyncio 명시적으로 적용
@pytest.mark.asyncio
async def test_create_and_get_team_by_name(async_session: AsyncSession):
    async with async_session() as session:
        team_repo = TeamRepository(session)

        # 팀 생성
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

        # 팀 조회
        fetched_team = await team_repo.get_team_by_name("Test Team")
        assert fetched_team is not None
        assert fetched_team.t_name == "Test Team"
        assert fetched_team.t_intro == "This is a test team"

    await session.rollback()
