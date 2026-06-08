import pytest

from app.services.scoring import score


def test_exact_name_scores_one(make_entity):
    entity = make_entity("Al-Madar Holdings Ltd")
    result, matched_on = score("Al-Madar Holdings Ltd", entity)
    assert result == pytest.approx(1.0)
    assert matched_on == "name"


def test_case_insensitive(make_entity):
    entity = make_entity("Al-Madar Holdings Ltd")
    result, _ = score("al-madar holdings ltd", entity)
    assert result == pytest.approx(1.0)


def test_alias_hit_sets_matched_on_alias(make_entity):
    entity = make_entity("Al-Madar Holdings Ltd", aliases=["AMH Group"])
    result, matched_on = score("AMH Group", entity)
    assert result == pytest.approx(1.0)
    assert matched_on == "alias"


def test_partial_name_still_scores_high(make_entity):
    entity = make_entity("Al-Madar Holdings Ltd")
    result, matched_on = score("al madar", entity)
    assert result > 0.7
    assert matched_on == "name"


def test_name_beats_weaker_alias(make_entity):
    # Query matches the name strongly and the alias not at all; name should win.
    entity = make_entity("Northbridge Maritime LLC", aliases=["Zenith Trading"])
    result, matched_on = score("northbridge maritime", entity)
    assert matched_on == "name"
    assert result > 0.7


def test_unrelated_scores_low(make_entity):
    entity = make_entity("Al-Madar Holdings Ltd", aliases=["AMH Group"])
    result, _ = score("zzzzz qqqqq", entity)
    assert result < 0.5


def test_relevant_outranks_irrelevant(make_entity):
    relevant = make_entity("Northbridge Maritime LLC")
    irrelevant = make_entity("Banco del Sur Internacional")
    query = "northbridge maritime"
    assert score(query, relevant)[0] > score(query, irrelevant)[0]


def test_empty_query_is_zero_without_crashing(make_entity):
    # An empty/whitespace query is short-circuited by score() to a hard 0.0.
    entity = make_entity("Al-Madar Holdings Ltd", aliases=["AMH Group"])
    assert score("", entity) == (0.0, "name")
    assert score("   ", entity) == (0.0, "name")


def test_empty_aliases_does_not_crash(make_entity):
    entity = make_entity("Al-Madar Holdings Ltd")
    result, matched_on = score("al madar", entity)
    assert matched_on == "name"
    assert result > 0.7


def test_tie_prefers_name_over_alias(make_entity):
    # Name and alias score identically; strictly-greater comparison keeps "name".
    entity = make_entity("Foo", aliases=["Foo"])
    result, matched_on = score("Foo", entity)
    assert result == pytest.approx(1.0)
    assert matched_on == "name"
