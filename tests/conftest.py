import pytest 
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import DATABASE_URL, get_session
from app.main import app
from app.models import Base

TEST_DATABASE_URL = (
    DATABASE_URL.rsplit("/", 1)[0]
    + "/gigkit_test"
)

assert TEST_DATABASE_URL != DATABASE_URL
assert TEST_DATABASE_URL.endswith("/gigkit_test") 


test_engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(test_engine)

def get_test_session():
    with TestSessionLocal() as session:
        yield session



@pytest.fixture
def client():

    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)

    app.dependency_overrides[get_session] = get_test_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()