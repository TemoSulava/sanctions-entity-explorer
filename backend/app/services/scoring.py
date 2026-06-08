"""Fuzzy match scoring.

Pure functions over a single entity — no repository, no I/O — so the ranking
logic is unit-testable in isolation.

rapidfuzz's `WRatio` is a weighted blend of several ratios that tolerates word
reordering, partial matches, and length differences — the realistic shape of an
investigator typing a partial or variant-spelled name. `default_process`
lowercases and strips punctuation so "al madar" matches "Al-Madar". Scores are
normalised from rapidfuzz's 0–100 to 0–1.
"""

from rapidfuzz import fuzz, utils

from app.schemas import Entity, MatchedOn


def score(query: str, entity: Entity) -> tuple[float, MatchedOn]:
    """Best fuzzy score of `query` against the entity's name and aliases.

    Returns the 0–1 score and which field produced it ("name" or "alias").
    """
    if not query.strip():
        return 0.0, "name"

    best_score = fuzz.WRatio(query, entity.name, processor=utils.default_process) / 100.0
    best_matched_on: MatchedOn = "name"

    for alias in entity.aliases:
        alias_score = fuzz.WRatio(query, alias, processor=utils.default_process) / 100.0
        if alias_score > best_score:
            best_score = alias_score
            best_matched_on = "alias"

    return best_score, best_matched_on
