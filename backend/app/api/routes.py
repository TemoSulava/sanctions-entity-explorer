"""HTTP routes. Thin layer: validate inputs, delegate to services, shape the
response envelope. All business logic lives in `app.services`.
"""

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_repository
from app.repository import EntityNotFound, EntityRepository
from app.schemas import EntitySummary, GraphResponse, SearchResponse
from app.services.graph import build_graph
from app.services.search import search

router = APIRouter(prefix="/api")


@router.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/search", tags=["search"])
def search_entities(
    q: str = Query("", description="Name or alias to search for."),
    limit: int = Query(10, ge=1, le=25, description="Max results to return."),
    repo: EntityRepository = Depends(get_repository),
) -> SearchResponse:
    # An empty/whitespace q yields no results (handled in search), not a 422.
    return SearchResponse(query=q, results=search(repo, q, limit))


@router.get("/entities/{entity_id}", tags=["entities"])
def get_entity(
    entity_id: str,
    repo: EntityRepository = Depends(get_repository),
) -> EntitySummary:
    entity = repo.get(entity_id)
    if entity is None:
        raise EntityNotFound(entity_id)
    return EntitySummary.from_entity(entity)


@router.get("/entities/{entity_id}/graph", tags=["graph"])
def get_entity_graph(
    entity_id: str,
    repo: EntityRepository = Depends(get_repository),
) -> GraphResponse:
    # build_graph raises EntityNotFound -> 404 via the app exception handler.
    return build_graph(repo, entity_id)
