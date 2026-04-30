"""Схемы данных для Темы 13. Используются ноутбуком для валидации входов и артефактов."""
from __future__ import annotations
from enum import Enum
from typing import List, Literal, Optional

try:
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover
    raise ImportError("Установите pydantic: pip install pydantic")


class PersonClass(str, Enum):
    male = "Male"
    female = "Female"


class Predicate(str, Enum):
    has_parent = "hasParent"
    has_child = "hasChild"
    has_ancestor = "hasAncestor"
    has_sibling = "hasSibling"


class Individual(BaseModel):
    id: str = Field(..., min_length=1)
    cls: PersonClass = Field(..., alias="class")
    label: str = ""
    note: str = ""

    class Config:
        populate_by_name = True


class Relationship(BaseModel):
    subject: str
    predicate: Predicate
    object: str
    note: str = ""


class QueryResult(BaseModel):
    id: str
    type: str
    query: str
    before: List[str]
    after: List[str]
    interpretation: str


class InferredFact(BaseModel):
    subject: str
    predicate: Predicate
    object: str
    rule: Literal["inverse_property", "symmetric", "transitive", "subPropertyOf", "chain"]


class KPIRow(BaseModel):
    kpi: str
    target: str
    actual: str
    passed: bool
    notes: Optional[str] = None
