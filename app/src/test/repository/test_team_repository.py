import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from models import Team
from repository import TeamRepository

@pytest.mark.asyncio
async def test_create_and_get_team_by_name(async_session: AsyncSession):
    # TeamRepository 인스턴스 생성
    team_repo = TeamRepository(async_session)

    # 팀 생성
    new_team = Team(t_name="Test Team", t_intro="This is a test team", t_descript="Test description", t_logo="logo.png", t_git="https://github.com/testteam")
    created_team = await team_repo.create_team(new_team)

    # 팀 생성 확인
    assert created_team.t_name == "Test Team"
    assert created_team.t_intro == "This is a test team"

    # get_team_by_name으로 팀 조회
    fetched_team = await team_repo.get_team_by_name("Test Team")

    # 조회된 팀 확인
    assert fetched_team is not None
    assert fetched_team.t_name == "Test Team"
    assert fetched_team.t_intro == "This is a test team"
