"""Pydantic models.

`Relation` and `Entity` mirror the fixture exactly and are used to parse
`data/sdn_sample.json` on startup. `extra="forbid"` makes shape drift fail loud
rather than silently dropping unexpected fields. Response/DTO models for the
search and graph endpoints are added alongside their endpoints.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict

EntityType = Literal["organization", "person", "vessel"]


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
