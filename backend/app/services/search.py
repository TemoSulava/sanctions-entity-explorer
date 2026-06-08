"""Search service: rank entities against a query.

Scores every entity (32 records — a linear scan is proportionate; a real index
would matter at scale), sorts by score descending with name as a stable
tie-break, and maps the top `limit` to response DTOs. An empty/whitespace query
returns no results rather than a 422 — investigators clearing the box is normal.
"""

from app.repository import EntityRepository
from app.schemas import SearchResult
from app.services.scoring import score


def search(repo: EntityRepository, query: str, limit: int) -> list[SearchResult]:
    cleaned = query.strip()
    if not cleaned:
        return []

    scored = [(score(cleaned, entity), entity) for entity in repo.all()]
    # Score descending, then name ascending so equal scores are ordered stably.
    scored.sort(key=lambda item: (-item[0][0], item[1].name))

    # Sorted on the raw score above; rounding here only cleans up the payload.
    return [
        SearchResult(
            id=entity.id,
            name=entity.name,
            type=entity.type,
            primary_country=entity.primary_country,
            programs=entity.programs,
            score=round(entity_score, 4),
            matched_on=matched_on,
        )
        for (entity_score, matched_on), entity in scored[:limit]
    ]
