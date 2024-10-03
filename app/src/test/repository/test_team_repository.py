# test_team_repository.py

import pytest
from httpx import AsyncClient  # AsyncClient for API testing
from database import AsyncSessionLocal  # Import AsyncSessionLocal for session handling
from src.main.goo.repository.TeamRepository import TeamRepository  # Import TeamRepository for testing
from models import Team

# Test to validate team model import
def test_import_team():
    assert Team is not None
    print("Team model import 성공!")

# Test to validate TeamRepository import
def test_import_team_repository():
    assert isinstance(TeamRepository, type), "TeamRepository is not a class!"
    print("TeamRepository import 성공!")

# Test database connection
@pytest.mark.asyncio
async def test_database_connection(async_session):
    assert async_session is not None
    print("Database connection 성공!")

# Test team creation and fetching by name
@pytest.mark.asyncio
async def test_create_and_get_team_by_name(async_session):
    team_repository = TeamRepository(async_session)

    new_team = Team(
        t_name="Test Team",
        t_intro="This is a test team",
        t_descript="Test description",
        t_logo="logo.png",
        t_git="https://github.com/testteam"
    )

    # Create a new team
    await team_repository.create_team(new_team)
    print(f"팀 생성됨: {new_team.t_name}, {new_team.t_intro}")

    # Fetch the team by name
    created_team = await team_repository.get_team_by_name("Test Team")
    print(f"조회된 팀 이름: {created_team.t_name}, 팀 소개: {created_team.t_intro}")

    # Validate fetched team information
    assert created_team is not None
    assert created_team.t_name == "Test Team"
    assert created_team.t_intro == "This is a test team"

# Test fetching team list if data exists
@pytest.mark.asyncio
async def test_list_team_if_data_exists(async_session):
    team_repository = TeamRepository(async_session)

    # Fetch list of teams
    team_list = await team_repository.list_team()

    if len(team_list) == 0:
        pytest.skip("데이터베이스에 팀 데이터가 없어서 테스트를 생략합니다.")

    print("팀 리스트 조회 결과:")
    for team in team_list:
        print(f"팀 이름: {team.t_name}, 팀 소개: {team.t_intro}")

    assert len(team_list) > 0, "팀 리스트가 비어있습니다."
