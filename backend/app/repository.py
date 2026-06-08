"""In-memory, read-only store over the fixture.

Loaded once on startup (see `app.main` lifespan) and shared via dependency
injection. Holds the parsed entities plus an id index for O(1) lookup.
"""

import json
from pathlib import Path

from app.schemas import Entity


class EntityRepository:
    def __init__(self, entities: list[Entity]) -> None:
        self._entities = entities
        self._by_id: dict[str, Entity] = {entity.id: entity for entity in entities}
        # Fail loud on duplicate ids rather than silently clobbering an entity.
        if len(self._by_id) != len(entities):
            raise ValueError("Fixture contains duplicate entity ids")

    @classmethod
    def load_from_file(cls, path: Path) -> EntityRepository:
        """Parse the whole fixture through `Entity` so shape drift fails loud."""
        records = json.loads(path.read_text(encoding="utf-8"))
        entities = [Entity.model_validate(record) for record in records]
        return cls(entities)

    def all(self) -> list[Entity]:
        return self._entities

    def get(self, entity_id: str) -> Entity | None:
        return self._by_id.get(entity_id)
