"""
Pydantic-схемы для CSV starter-pack.
Используются ноутбуком для валидации входных данных перед построением онтологии.
"""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


VALID_CLASSES = {
    "Person", "Student", "UndergraduateStudent", "GraduateStudent",
    "MasterStudent", "PhDStudent", "AcademicStaff", "Professor", "Lecturer",
    "AdministrativeStaff", "AcademicUnit", "Department", "Faculty",
    "Course", "UndergraduateCourse", "GraduateCourse",
    "Publication", "Article", "Book",
    "Project", "Room", "Classroom", "Lab",
}

VALID_PROPERTIES = {
    "memberOf", "partOf", "teaches", "taughtBy", "enrolledIn",
    "supervises", "offeredBy", "hasAuthor", "worksOnProject", "heldIn",
}


class IndividualRow(BaseModel):
    id: str = Field(..., min_length=1)
    cls: str = Field(..., alias="class")
    name: str
    email: Optional[str] = None
    age: Optional[int] = None
    extra: Optional[str] = None

    model_config = {"populate_by_name": True}

    @field_validator("cls")
    @classmethod
    def class_must_be_valid(cls, v: str) -> str:
        if v not in VALID_CLASSES:
            raise ValueError(f"Unknown class: {v}")
        return v


class RelationshipRow(BaseModel):
    subject: str
    property: str
    object: str

    @field_validator("property")
    @classmethod
    def property_must_be_valid(cls, v: str) -> str:
        if v not in VALID_PROPERTIES:
            raise ValueError(f"Unknown property: {v}")
        return v


class KPIRow(BaseModel):
    kpi: str
    target: str
    actual: str
    pass_: bool = Field(..., alias="pass")
    notes: str = ""

    model_config = {"populate_by_name": True}
