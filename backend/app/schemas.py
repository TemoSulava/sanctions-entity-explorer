"""Pydantic models.

`Relation` and `Entity` mirror the fixture exactly and are used to parse
`data/sdn_sample.json` on startup. `extra="forbid"` makes shape drift fail loud
rather than silently dropping unexpected fields. Response/DTO models for the
search and graph endpoints are added alongside their endpoints.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict

EntityType = Literal["organization", "person", "vessel"]
MatchedOn = Literal["name", "alias"]


class Relation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_id: str
    type: str
    note: str | None = None


class Entity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    aliases: list[str]
    type: EntityType
    countries: list[str]
    programs: list[str]
    list_date: str
    remarks: str | None = None
    relations: list[Relation]

    @property
    def primary_country(self) -> str | None:
        """First listed country (ISO2), or None when none are recorded."""
        return self.countries[0] if self.countries else None


# --- Search API DTOs ---


class SearchResult(BaseModel):
    id: str
    name: str
    type: EntityType
    primary_country: str | None
    programs: list[str]
    score: float
    matched_on: MatchedOn


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]


# --- Graph API DTOs ---


class EntitySummary(BaseModel):
    id: str
    name: str
    type: EntityType
    primary_country: str | None


class GraphNode(BaseModel):
    id: str
    name: str
    type: EntityType
    is_center: bool


class GraphEdge(BaseModel):
    source: str
    target: str
    type: str
    note: str | None = None


class GraphResponse(BaseModel):
    center: EntitySummary
    nodes: list[GraphNode]
    edges: list[GraphEdge]
