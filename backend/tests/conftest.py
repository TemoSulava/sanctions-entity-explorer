import pytest

from app.config import DATA_PATH
from app.repository import EntityRepository


@pytest.fixture(scope="session")
def repo() -> EntityRepository:
    """The real fixture-backed repository, loaded once for the test session."""
    return EntityRepository.load_from_file(DATA_PATH)
