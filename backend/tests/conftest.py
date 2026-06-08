from collections.abc import Callable, Iterator

import pytest
from fastapi.testclient import TestClient

from app.config import DATA_PATH
from app.main import app
from app.repository import EntityRepository
from app.schemas import Entity, Relation


@pytest.fixture(scope="session")
def repo() -> EntityRepository:
    """The real fixture-backed repository, loaded once for the test session."""
    return EntityRepository.load_from_file(DATA_PATH)


@pytest.fixture
def client() -> Iterator[TestClient]:
    """TestClient inside a context so the lifespan loads the repository."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def make_entity() -> Callable[..., Entity]:
    """Factory for synthetic entities, so unit tests don't lean on fixture data."""

    def _make(
        name: str,
        *,
        aliases: list[str] | None = None,
        countries: list[str] | None = None,
        relations: list[Relation] | None = None,
        entity_id: str = "SDN-00000",
    ) -> Entity:
        return Entity(
            id=entity_id,
            name=name,
            aliases=aliases or [],
            type="organization",
            countries=countries or [],
            programs=[],
            list_date="2020-01-01",
            relations=relations or [],
        )

    return _make
