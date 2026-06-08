from app.repository import EntityRepository
from app.services.search import search


def test_empty_query_returns_nothing(repo):
    assert search(repo, "", 10) == []
    assert search(repo, "   ", 10) == []


def test_results_sorted_by_score_desc(repo):
    results = search(repo, "al madar", 25)
    scores = [result.score for result in results]
    assert scores == sorted(scores, reverse=True)


def test_equal_scores_tie_break_by_name_asc(make_entity):
    # Two entities match the same alias exactly -> identical scores; the only
    # discriminator is name, which must order ascending.
    bravo = make_entity("Bravo Corp", aliases=["Acme Identifier"], entity_id="SDN-00001")
    alpha = make_entity("Alpha Corp", aliases=["Acme Identifier"], entity_id="SDN-00002")
    repo = EntityRepository([bravo, alpha])

    results = search(repo, "Acme Identifier", 5)

    assert results[0].score == results[1].score  # genuinely a tie
    assert [result.name for result in results] == ["Alpha Corp", "Bravo Corp"]


def test_top_result_is_relevant(repo):
    results = search(repo, "al madar", 5)
    assert results
    assert "Madar" in results[0].name or "Mader" in results[0].name


def test_limit_caps_results(repo):
    assert len(search(repo, "al", 3)) == 3
    assert len(search(repo, "al", 1)) == 1


def test_scores_within_unit_range(repo):
    for result in search(repo, "al madar", 25):
        assert 0.0 <= result.score <= 1.0


def test_primary_country_null_when_no_countries(make_entity):
    entity = make_entity("Ghost Holdings", countries=[])
    repo = EntityRepository([entity])
    results = search(repo, "ghost holdings", 5)
    assert results
    assert results[0].primary_country is None


def test_primary_country_is_first_country(make_entity):
    entity = make_entity("Ghost Holdings", countries=["DE", "FR"])
    repo = EntityRepository([entity])
    results = search(repo, "ghost holdings", 5)
    assert results[0].primary_country == "DE"


def test_alias_match_surfaces_matched_on_alias(make_entity):
    entity = make_entity("Obscure Legal Name", aliases=["Findme Trading"])
    repo = EntityRepository([entity])
    results = search(repo, "Findme Trading", 5)
    assert results[0].matched_on == "alias"
