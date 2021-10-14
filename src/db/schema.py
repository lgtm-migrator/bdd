from __future__ import annotations

from sqlmodel import Field, SQLModel, Relationship

# sqlalchemy debería ser evitado, pero la API de sqlmodel no es tan completa aún
from sqlalchemy.sql.sqltypes import Enum
from sqlalchemy import Column

from typing import Optional
import enum
from datetime import datetime


RequirementRelationEnum = enum.Enum("RequirementRelationEnum", ["and", "or", "null"])

class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    credits: int
    initials: str
    school_id: Optional[int] = Field(default=None, foreign_key="school.id", primary_key=True)
    school: Optional[School] = Relationship(back_populates="subjects")
    syllabus: str
    academic_level: str
    description: str
    restrictions: str
    prerequisites_raw: str
    requirements_relation: RequirementRelationEnum = Field(sa_column=Column(Enum(RequirementRelationEnum)))
    # _prerequisites: list["PrerequisitesOrGroup"] = Relationship(back_populates="subjects")
    equivalences: Subject = Relationship(
        back_populates="equivalences", link_model="SubjectEquivalencies"
    )

    # @property
    # def prerequisites(self):
    #     return [[C1 & C2] | [C1 & C3]]


class PrerequisitesOrGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="Subject.id", primary_key=True)
    subject: Subject = Relationship(back_populates="_prerequisites")


class PrerequisitesAndGroup(SQLModel, table=True):
    prerequisites_or_group_id: int = Field(foreign_key="RestrictionsOrGroup.id", primary_key=True)
    course_id: int = Field(foreign_key="Course.id", primary_key=True)
    course: Course = Relationship()


class RestrictionsOrGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="Subject.id", primary_key=True)


class RestrictionsAndGroup(SQLModel, table=True):
    restrictions_or_group_id: int = Field(foreign_key="RestrictionsOrGroup.id", primary_key=True)
    restriction: str


class SubjectEquivalencies(SQLModel, table=True):
    subject_id: int = Field(default=None, foreign_key="subject.id", primary_key=True)
    equivalence_id: int = Field(default=None, foreign_key="subject.id", primary_key=True)


PeriodEnum = enum.Enum("PeriodEnum", [1, 2, "TAV"])


class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject: Subject = Relationship()
    year: int
    period: PeriodEnum
    section: int
    nrc: str
    schedule_summary: str
    campus_id: int = Field(foreign_key="Campus.id")
    campus: Campus = Relationship(back_populates="courses")
    format: str
    category: str
    fg_area: str
    is_removable: bool
    is_english: bool
    need_special_aproval: bool
    available_quota: int
    total_quota: int


class Campus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


DayEnum = enum.Enum("DayEnum", ["L", "M", "W", "J", "V", "S"])


class ClassSchedule:
    day: DayEnum
    module: int = Field(gt=1, lt=7)  # [1, 2, 3, 4, 5, 6, 7, 8]
    classroom: str
    course_id: Optional[str] = Field(default=None, foreign_key="Course.id")
    course: Course = Relationship()


class Teacher(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    photo_url: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None


class CoursesTeachers(SQLModel, table=True):
    course_id: Optional[int] = Field(default=None, foreign_key="Course.id", primary_key=True)
    teacher_id: Optional[int] = Field(default=None, foreign_key="Teacher.id", primary_key=True)


class School(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    website: Optional[str] = None
    description: Optional[str] = None


class Faculty(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    website: str
    description: str
    campus_id: int = Field(default=None, foreign_key="Campus.id")
    campus: Campus = Relationship(back_populates="faculties")


class Place(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    #   latLng: point
    #   polygon: polygon?
    campus_id: int = Field(default=None, foreign_key="Campus.id")
    campus: Campus = Relationship(back_populates="places")
    name: str
    floor: int
    notes: Optional[str] = None
    description: str
    categories: list["PlaceCategory"] = Relationship(
        back_populates="places", link_model="CategoryOfPlace"
    )
    parent_id: Optional[int]
    parent: Place = Relationship(back_populates="child")


class CategoryOfPlace(SQLModel, table=True):
    course_id: Optional[int] = Field(default=None, foreign_key="Courses.id", primary_key=True)
    place_id: Optional[int] = Field(default=None, foreign_key="Places.id", primary_key=True)


class PlaceCategory(SQLModel, table=True):
    name: str
    id: Optional[int] = Field(default=None, primary_key=True)
    places: list[Place] = Relationship(back_populates="categories")


class UniversityEvents(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    start: datetime
    end: datetime
    tag: str
    description: str
    is_a_holiday: bool = False



if __name__ == "__main__":
    from sqlmodel import create_engine, SQLModel
    engine = create_engine("sqlite://", echo=True)  # in memory temp DB
    SQLModel.metadata.create_all(engine)