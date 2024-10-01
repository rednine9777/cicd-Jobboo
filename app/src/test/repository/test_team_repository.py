import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import sys

# 경로 설정
current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_path, "../../../"))
sys.path.append(root_path)

# 환경 변수 로드
dotenv_path = os.getenv('DOTENV_PATH')
load_dotenv(dotenv_path=dotenv_path)

# 데이터베이스 URL 설정
db_url = f"mysql+aiomysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
engine = create_async_engine(db_url, echo=True)

# Async 세션을 생성하는 세션메이커
async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Team 모델 임포트 테스트
def test_import_team():
    try:
        from models import Team  # models.py에서 Team 클래스 가져오기
        assert Team is not None
        print("Team model import 성공!")
    except ImportError as e:
        pytest.fail(f"Team model import 실패: {e}")
        
def test_import_team_repository():
    try:
        # TeamRepository 임포트 시 경로 수정
        from src.main.goo.repository.TeamRepository import TeamRepository
        assert isinstance(TeamRepository, type), "TeamRepository is not a class!"
        print("TeamRepository import 성공!")
    except ImportError as e:
        pytest.fail(f"TeamRepository import 실패: {e}")
        
# pytest fixture로 세션 설정
@pytest.fixture
async def async_session():
    # 세션 생성 및 제공
    async with async_session_maker() as session:
        yield session
    await engine.dispose()

# 환경 변수 확인 테스트
def test_env_variables():
    try:
        db_user = os.getenv('MYSQL_USER')
        db_password = os.getenv('MYSQL_PASSWORD')
        db_host = os.getenv('MYSQL_HOST')
        db_name = os.getenv('MYSQL_DATABASE')

        assert db_user is not None, "MYSQL_USER 환경 변수가 설정되지 않았습니다."
        assert db_password is not None, "MYSQL_PASSWORD 환경 변수가 설정되지 않았습니다."
        assert db_host is not None, "MYSQL_HOST 환경 변수가 설정되지 않았습니다."
        assert db_name is not None, "MYSQL_DATABASE 환경 변수가 설정되지 않았습니다."
        print(f"환경 변수 설정 성공: {db_user}, {db_password}, {db_host}, {db_name}")
    except AssertionError as e:
        pytest.fail(f"환경 변수 로드 실패: {e}")

# 데이터베이스 연결 테스트
@pytest.mark.asyncio
async def test_database_connection(async_session):
    try:
        # 세션이 생성되었는지 확인
        assert async_session is not None
        print("Database connection 성공!")
    except Exception as e:
        pytest.fail(f"Database connection 실패: {e}")

# Team 생성 및 조회 테스트
@pytest.mark.asyncio
async def test_create_and_get_team_by_name(async_session: AsyncSession):
    from models import Team  # 팀 모델 임포트
    from src.main.goo.repository.TeamRepository import TeamRepository  # TeamRepository 임포트
    
    print("세션 시작")
    
    # TeamRepository 인스턴스 생성
    team_repo = TeamRepository(async_session)

    # 새로운 팀 객체 생성
    new_team = Team(
        t_name="Test Team",
        t_intro="This is a test team",
        t_descript="Test description",
        t_logo="logo.png",
        t_git="https://github.com/testteam"
    )

    # 팀 생성
    created_team = await team_repo.create_team(new_team)

    # 팀 생성 확인
    assert created_team.t_name == "Test Team"
    assert created_team.t_intro == "This is a test team"

    # 팀 조회 확인
    fetched_team = await team_repo.get_team_by_name("Test Team")
    assert fetched_team is not None
    assert fetched_team.t_name == "Test Team"
    assert fetched_team.t_intro == "This is a test team"

    # 롤백 처리
    await async_session.rollback()
