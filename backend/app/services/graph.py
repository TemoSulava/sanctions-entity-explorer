"""Graph service: build the one-hop relations graph for an entity.

Shapes the payload exactly for the renderer: a `center` summary, a deduped list
of `nodes` (center + direct neighbors), and `edges` emitted center -> neighbor.
`source`/`target` match node ids (the d3 / React-Flow convention) so the
frontend can render without remapping. Directionality lives in the relation
`type` (e.g. `operates` vs `operated_by`), so no separate direction field.
"""

from app.repository import EntityNotFound, EntityRepository
from app.schemas import EntitySummary, GraphEdge, GraphNode, GraphResponse


def build_graph(repo: EntityRepository, entity_id: str) -> GraphResponse:
    center = repo.get(entity_id)
    if center is None:
        raise EntityNotFound(entity_id)

    nodes = [GraphNode(id=center.id, name=center.name, type=center.type, is_center=True)]
    edges: list[GraphEdge] = []
    seen = {center.id}  # dedup neighbor nodes; one node per target, one edge per relation

    for relation in center.relations:
        neighbor = repo.get(relation.target_id)
        if neighbor is None:
            # Fixture has no dangling targets; skip defensively rather than crash.
            continue

        edges.append(
            GraphEdge(
                source=center.id,
                target=neighbor.id,
                type=relation.type,
                note=relation.note,
            )
        )

        if neighbor.id not in seen:
            seen.add(neighbor.id)
            nodes.append(
                GraphNode(
                    id=neighbor.id,
                    name=neighbor.name,
                    type=neighbor.type,
                    is_center=False,
                )
            )

    return GraphResponse(
        center=EntitySummary.from_entity(center),
        nodes=nodes,
        edges=edges,
    )
