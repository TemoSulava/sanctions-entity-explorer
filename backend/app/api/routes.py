"""HTTP routes. Thin layer: validate inputs, delegate to services, shape the
response envelope. All business logic lives in `app.services`.
"""

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_repository
from app.repository import EntityRepository
from app.schemas import SearchResponse
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
