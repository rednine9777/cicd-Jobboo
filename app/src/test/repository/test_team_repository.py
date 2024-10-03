import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
import sys
import os

# 프로젝트 루트 경로 설정
current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_path, "../../../"))
sys.path.append(root_path)

# 필요한 모듈 임포트
from database import AsyncSessionLocal  # AsyncSessionLocal 임포트
from src.main.goo.repository.TeamRepository import TeamRepository
from models import Team

# pytest에서 사용할 event loop를 수동으로 설정
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# AsyncSession을 제공하는 피처 정의
@pytest.fixture(scope="function")
async def async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            if session.in_transaction():
                await session.rollback()
            await session.close()

# Team 모델 임포트 테스트
def test_import_team():
    assert Team is not None
    print("Team model import 성공!")

# TeamRepository 임포트 테스트
def test_import_team_repository():
    assert isinstance(TeamRepository, type), "TeamRepository is not a class!"
    print("TeamRepository import 성공!")

# 환경 변수 확인 테스트
def test_env_variables():
    db_user = os.getenv('MYSQL_USER')
    db_password = os.getenv('MYSQL_PASSWORD')
    db_host = os.getenv('MYSQL_HOST')
    db_name = os.getenv('MYSQL_DATABASE')

    assert db_user is not None, "MYSQL_USER 환경 변수가 설정되지 않았습니다."
    assert db_password is not None, "MYSQL_PASSWORD 환경 변수가 설정되지 않았습니다."
    assert db_host is not None, "MYSQL_HOST 환경 변수가 설정되지 않았습니다."
    assert db_name is not None, "MYSQL_DATABASE 환경 변수가 설정되지 않았습니다."
    print(f"환경 변수 설정 성공: {db_user}, {db_password}, {db_host}, {db_name}")

# 데이터베이스 연결 테스트
@pytest.mark.asyncio
async def test_database_connection(async_session: AsyncSession):
    assert async_session is not None
    print("Database connection 성공!")

# Team 생성 및 조회 테스트
@pytest.mark.asyncio
async def test_create_and_get_team_by_name(async_session: AsyncSession):
    team_repository = TeamRepository(async_session)

    new_team = Team(
        t_name="Test Team",
        t_intro="This is a test team",
        t_descript="Test description",
        t_logo="logo.png",
        t_git="https://github.com/testteam"
    )

    # 팀 생성
    await team_repository.create_team(new_team)
    print(f"팀 생성됨: {new_team.t_name}, {new_team.t_intro}")

    # 팀 이름으로 팀 조회
    created_team_by_name = await team_repository.get_team_by_name("Test Team")
    print(f"이름으로 조회된 팀: {created_team_by_name.t_name}, {created_team_by_name.t_intro}")

    # 조회된 팀 정보가 맞는지 검증
    assert created_team_by_name is not None, "Team not found"
    assert created_team_by_name.t_name == "Test Team"
    assert created_team_by_name.t_intro == "This is a test team"
    
# 팀 리스트 조회 테스트 (데이터 없으면 생략)
@pytest.mark.asyncio
async def test_list_team_if_data_exists(async_session: AsyncSession):
    team_repository = TeamRepository(async_session)

    # 팀 리스트 조회
    team_list = await team_repository.list_team()

    if len(team_list) == 0:
        pytest.skip("데이터베이스에 팀 데이터가 없어서 테스트를 생략합니다.")

    print("팀 리스트 조회 결과:")
    for team in team_list:
        print(f"팀 이름: {team.t_name}, 팀 소개: {team.t_intro}")

    assert len(team_list) > 0, "팀 리스트가 비어있습니다."
