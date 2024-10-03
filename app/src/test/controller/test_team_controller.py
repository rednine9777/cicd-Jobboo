# test_team_controller.py

import pytest
from httpx import AsyncClient  # httpx.AsyncClient for FastAPI API testing
from main import app  # FastAPI app import

# Team list API test using httpx.AsyncClient
@pytest.mark.asyncio
async def test_list_team_api():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/list_team")

        # Log API response status code
        print(f"API 응답 상태 코드: {response.status_code}")

        # Validate response
        assert response.status_code == 200
        assert "teams" in response.json()
        print(f"팀 리스트: {response.json()['teams']}")
