# Аксиомы и ограничения онтологии

Эти аксиомы реализуются в ноутбуке через owlready2 и сохраняются в `artifacts/university.owl`.

## Иерархия классов (subClassOf)

```
Thing
├── Person
│   ├── Student
│   │   ├── UndergraduateStudent
│   │   └── GraduateStudent
│   │       ├── MasterStudent
│   │       └── PhDStudent
│   ├── AcademicStaff
│   │   ├── Professor
│   │   └── Lecturer
│   └── AdministrativeStaff
├── AcademicUnit
│   ├── Department
│   └── Faculty
├── Course
│   ├── UndergraduateCourse
│   └── GraduateCourse
├── Publication
│   ├── Article
│   └── Book
├── Project
└── Room
    ├── Classroom
    └── Lab
```

## Ограничения (≥5)

| # | Аксиома | Тип | Смысл |
|---|---|---|---|
| C1 | `teaches` domain=AcademicStaff, range=Course | Domain/Range | Только преподаватель может «teaches», объект — курс. |
| C2 | `enrolledIn` domain=Student, range=Course | Domain/Range | Записаться может только студент. |
| C3 | `supervises` domain=Professor, range=PhDStudent | Domain/Range | Научное руководство — только профессор → аспирант. |
| C4 | `Student` disjoint with `AcademicStaff` | Disjoint | Студент и преподаватель — разные сущности. |
| C5 | `hasEmail` Functional | Functional DataProperty | У одного человека ровно один email. |
| C6 | `taughtBy` inverse of `teaches` | InverseProperty | Если X teaches Y, то Y taughtBy X. |
| C7 | `Course` ⊑ ∃ `taughtBy` AcademicStaff (min 1) | Cardinality | У каждого курса ≥1 преподаватель. |

В сумме это покрывает четыре из пяти типичных вариантов ограничений OWL DL:
**domain**, **range**, **cardinality**, **disjoint**, **functional**, **inverse**.
