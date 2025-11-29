import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from app.main import app as fastapi_app

# Real app for full e2e workflows.
@pytest.fixture(scope="session")
def e2e_app() -> FastAPI:
    return fastapi_app