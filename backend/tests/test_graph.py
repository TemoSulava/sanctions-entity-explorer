import pytest

from app.repository import EntityNotFound, EntityRepository
from app.schemas import Relation
from app.services.graph import build_graph


def test_neighbors_for_known_entity(repo):
    graph = build_graph(repo, "SDN-10001")
    assert graph.center.id == "SDN-10001"
    neighbor_ids = {node.id for node in graph.nodes if not node.is_center}
    assert neighbor_ids == {"SDN-10002", "SDN-10031"}
    assert sum(1 for node in graph.nodes if node.is_center) == 1


def test_center_summary_has_primary_country(repo):
    graph = build_graph(repo, "SDN-10001")
    assert graph.center.primary_country == "AE"


def test_edges_emitted_from_center_and_endpoints_are_nodes(repo):
    graph = build_graph(repo, "SDN-10001")
    node_ids = {node.id for node in graph.nodes}
    assert all(edge.source == "SDN-10001" for edge in graph.edges)
    assert all(edge.source in node_ids and edge.target in node_ids for edge in graph.edges)


def test_edge_carries_relation_type_and_note(repo):
    graph = build_graph(repo, "SDN-10001")
    edge = next(edge for edge in graph.edges if edge.target == "SDN-10002")
    assert edge.type == "shared_directors"
    assert edge.note is not None


def test_edge_note_can_be_null(repo):
    # SDN-10002 -> SDN-10001 has a null note in the fixture.
    graph = build_graph(repo, "SDN-10002")
    edge = next(edge for edge in graph.edges if edge.target == "SDN-10001")
    assert edge.note is None


def test_missing_entity_raises(repo):
    with pytest.raises(EntityNotFound):
        build_graph(repo, "SDN-99999")


def test_duplicate_target_dedups_node_but_keeps_each_edge(make_entity):
    center = make_entity(
        "Center Co",
        entity_id="SDN-00001",
        relations=[
            Relation(target_id="SDN-00002", type="operates", note=None),
            Relation(target_id="SDN-00002", type="shared_directors", note="second tie"),
        ],
    )
    neighbor = make_entity("Neighbor Co", entity_id="SDN-00002")
    repo = EntityRepository([center, neighbor])

    graph = build_graph(repo, "SDN-00001")

    assert len(graph.nodes) == 2  # center + one deduped neighbor
    assert sum(1 for node in graph.nodes if not node.is_center) == 1
    assert len(graph.edges) == 2  # one edge per relation


def test_entity_without_relations_returns_only_center(make_entity):
    center = make_entity("Lonely Co", entity_id="SDN-00001")
    repo = EntityRepository([center])

    graph = build_graph(repo, "SDN-00001")

    assert len(graph.nodes) == 1
    assert graph.nodes[0].is_center
    assert graph.edges == []


def test_dangling_target_is_silently_skipped(make_entity):
    # The fixture has no dangling targets, but build_graph skips them defensively
    # rather than crashing if a target id can't be resolved.
    center = make_entity(
        "Center Co",
        entity_id="SDN-00001",
        relations=[Relation(target_id="SDN-GHOST", type="operates", note=None)],
    )
    repo = EntityRepository([center])

    graph = build_graph(repo, "SDN-00001")

    assert len(graph.nodes) == 1
    assert graph.edges == []
