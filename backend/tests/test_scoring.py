import pytest

from app.schemas import Entity
from app.services.scoring import score


def make_entity(name: str, aliases: list[str]) -> Entity:
    return Entity(
        id="SDN-00000",
        name=name,
        aliases=aliases,
        type="organization",
        countries=[],
        programs=[],
        list_date="2020-01-01",
        relations=[],
    )


def test_exact_name_scores_one():
    entity = make_entity("Al-Madar Holdings Ltd", [])
    result, matched_on = score("Al-Madar Holdings Ltd", entity)
    assert result == pytest.approx(1.0)
    assert matched_on == "name"


def test_case_insensitive():
    entity = make_entity("Al-Madar Holdings Ltd", [])
    result, _ = score("al-madar holdings ltd", entity)
    assert result == pytest.approx(1.0)


def test_alias_hit_sets_matched_on_alias():
    entity = make_entity("Al-Madar Holdings Ltd", ["AMH Group"])
    result, matched_on = score("AMH Group", entity)
    assert result == pytest.approx(1.0)
    assert matched_on == "alias"


def test_partial_name_still_scores_high():
    entity = make_entity("Al-Madar Holdings Ltd", [])
    result, matched_on = score("al madar", entity)
    assert result > 0.7
    assert matched_on == "name"


def test_name_beats_weaker_alias():
    # Query matches the name strongly and the alias not at all; name should win.
    entity = make_entity("Northbridge Maritime LLC", ["Zenith Trading"])
    result, matched_on = score("northbridge maritime", entity)
    assert matched_on == "name"
    assert result > 0.7


def test_unrelated_scores_low():
    entity = make_entity("Al-Madar Holdings Ltd", ["AMH Group"])
    result, _ = score("zzzzz qqqqq", entity)
    assert result < 0.5


def test_relevant_outranks_irrelevant():
    relevant = make_entity("Northbridge Maritime LLC", [])
    irrelevant = make_entity("Banco del Sur Internacional", [])
    query = "northbridge maritime"
    assert score(query, relevant)[0] > score(query, irrelevant)[0]


def test_empty_query_is_zero_without_crashing():
    # An empty/whitespace query is short-circuited by score() to a hard 0.0.
    entity = make_entity("Al-Madar Holdings Ltd", ["AMH Group"])
    assert score("", entity) == (0.0, "name")
    assert score("   ", entity) == (0.0, "name")


def test_empty_aliases_does_not_crash():
    entity = make_entity("Al-Madar Holdings Ltd", [])
    result, matched_on = score("al madar", entity)
    assert matched_on == "name"
    assert result > 0.5


def test_tie_prefers_name_over_alias():
    # Name and alias score identically; strictly-greater comparison keeps "name".
    entity = make_entity("Foo", ["Foo"])
    result, matched_on = score("Foo", entity)
    assert result == pytest.approx(1.0)
    assert matched_on == "name"
