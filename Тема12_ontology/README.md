# Тема 12. Разработка онтологии (OWL)

Учебная онтология **университетского академического домена**: люди, подразделения, курсы, публикации, проекты, помещения. Цель темы — создать формальную семантическую модель в OWL, задать иерархию классов, свойства и ограничения, добавить индивидов и программно проверить количественные/качественные требования.

## Структура

```
Тема12_ontology/
├── README.md                    # этот файл
├── requirements.txt
├── Тема12_ontology.ipynb        # основной ноутбук (12 секций по единому шаблону)
├── starter_pack/
│   ├── docs/domain_brief.md
│   ├── data/individuals.csv
│   ├── data/relationships.csv
│   ├── data/data_dictionary.md
│   ├── kb/ontology_seed_terms.csv
│   ├── kb/ontology_axioms.md
│   ├── kb/competency_questions.md
│   ├── tests/cases.csv
│   ├── tests/expected.json
│   ├── tests/queries.txt
│   ├── schemas/pydantic_models.py
│   └── prompts/                 # пусто (LLM не используется)
└── artifacts/                   # генерируется ноутбуком
```

## Как запустить

### Google Colab
1. Загрузите всю папку `Тема12_ontology/`.
2. Откройте `Тема12_ontology.ipynb`.
3. Runtime → Run all. Все артефакты будут в `artifacts/`.

### Локально
```bash
cd Тема12_ontology
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter
jupyter notebook Тема12_ontology.ipynb
```

Затем Cell → Run All.

## Что появится в `artifacts/`

| Файл | Описание |
|---|---|
| `university.owl` | Готовая онтология (RDF/XML, читается owlready2/Protégé). |
| `classes.csv` | Таблица классов и их супер-классов. |
| `properties.csv` | Таблица Object/Data-свойств с domain/range. |
| `individuals.csv` | Таблица индивидов и их типов. |
| `architecture.mmd` + `architecture.svg`/`.png` | Диаграмма иерархии классов. |
| `input_profile.json` | Паспорт входных данных. |
| `results.csv` | Сводный snapshot результатов CQ. |
| `kpi_report.csv` | Таблица KPI с PASS/FAIL. |
| `trace.jsonl` | Лог проверки competency questions (вход/выход каждого). |
| `validation_log.txt` | Лог сохранения/загрузки `.owl` и self-check. |
| `export_summary.txt` | Список всех артефактов. |

## KPI

| KPI | Порог | Где измеряется |
|---|---|---|
| Количество классов | ≥ 15 | `evaluate()` |
| Количество свойств | ≥ 10 (Object + Data) | `evaluate()` |
| Количество индивидов | ≥ 20 | `evaluate()` |
| Количество ограничений | ≥ 5 | `evaluate()` |
| Файл `university.owl` сохраняется и читается без ошибок | True | `validation_log.txt` |
| Покрыто competency questions | ≥ 5 | `trace.jsonl` |
