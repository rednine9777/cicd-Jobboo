# conftest.py

import pytest
import asyncio
import logging
from rich.logging import RichHandler
from rich.console import Console
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal  # Import AsyncSessionLocal for database connection management

# ---------------------- 로그 설정 섹션 시작 ----------------------
# RichHandler를 통해 콘솔에 출력되는 로그의 형식과 수준을 설정
# 로그 출력 형식을 지정하고, rich_tracebacks를 통해 상세 오류 정보를 콘솔에 표시
console = Console()
logging.basicConfig(
    level="INFO",
    format="\n%(asctime)s [%(levelname)s] %(message)s\n",  # 로그에 시간과 로그 레벨, 메시지를 포함하여 출력
    handlers=[RichHandler(console=console, rich_tracebacks=True)]
)
# ---------------------- 로그 설정 섹션 끝 ----------------------


# ---------------------- 테스트 종료 후 요약 출력 섹션 시작 ----------------------
# pytest의 훅 기능을 활용하여 테스트가 종료된 후 성공, 실패, 스킵된 테스트에 대한 요약 정보를 출력
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))

    console.print(f"\n\n[bold]=== Test Summary ===[/bold]")
    console.print(f"[green]Passed tests: {passed}[/green]")
    console.print(f"[red]Failed tests: {failed}[/red]")
    console.print(f"[yellow]Skipped tests: {skipped}[/yellow]\n")
    
    if failed > 0:
        console.print("[red]Failed tests details:[/red]")
        for report in terminalreporter.stats.get('failed', []):
            console.print(f" - {report.nodeid}")
# ---------------------- 테스트 종료 후 요약 출력 섹션 끝 ----------------------





# ---------------------- 비동기 이벤트 루프 섹션 시작 ----------------------
# pytest에서 비동기 테스트를 위한 이벤트 루프를 설정
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
# ---------------------- 비동기 이벤트 루프 섹션 끝 ----------------------

# ---------------------- SQLAlchemy 비동기 세션 관리 섹션 시작 ----------------------
# SQLAlchemy의 비동기 세션을 생성하고 테스트에서 사용할 수 있도록 설정
@pytest.fixture(scope="function")
async def async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            if session.in_transaction():
                await session.rollback()
            await session.close()
# ---------------------- SQLAlchemy 비동기 세션 관리 섹션 끝 ----------------------
