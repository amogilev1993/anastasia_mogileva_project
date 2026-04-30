# Тема 13. Логический вывод на онтологии (Reasoning)

Учебная онтология «Семейные связи». Демонстрация того, как reasoner (HermiT/Pellet)
материализует новые факты из аксиом OWL DL: **транзитивность**, **инверсия**, **симметрия**,
**подсвойство**.

## Структура
```
Тема13_reasoning/
├── README.md                   # этот файл
├── requirements.txt
├── Тема13_reasoning.ipynb      # основной ноутбук (12 секций)
├── starter_pack/
│   ├── docs/domain_brief.md
│   ├── data/individuals.csv
│   ├── data/relationships.csv
│   ├── data/data_dictionary.md
│   ├── kb/ontology_seed_terms.csv
│   ├── kb/competency_questions.md
│   ├── kb/ontology_axioms.md
│   ├── tests/queries.txt
│   ├── tests/cases.csv
│   ├── tests/expected.json
│   ├── schemas/pydantic_models.py
│   └── prompts/                # пусто (LLM не используется)
└── artifacts/                  # генерируется ноутбуком
```

## Как запустить

### Google Colab
1. Загрузите всю папку `Тема13_reasoning/` (через Files → Upload или склонируйте репо).
2. Откройте `Тема13_reasoning.ipynb`.
3. Runtime → Run all. Java в Colab уже установлена, HermiT запустится сразу.

### Локально
```bash
# Java (нужна для HermiT)
sudo apt install -y openjdk-17-jre-headless        # Linux
# brew install openjdk                              # macOS

# Python окружение
cd Тема13_reasoning
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt jupyter

jupyter notebook Тема13_reasoning.ipynb
```
Затем Cell → Run All. Всё генерируется в `artifacts/`.

## Что появится в artifacts/
| Файл | Описание |
|---|---|
| `family.owl` | Сама онтология (создаётся ноутбуком) |
| `reasoner_log.txt` | Имя ризонера + время выполнения + лог |
| `queries_results.csv` | Таблица 5 запросов (до/после reasoning, интерпретация) |
| `inferred_facts.json` | Список новых троек, появившихся после reasoning |
| `ontology_diff.png` | Граф связей до и после reasoning (с подсветкой новых рёбер) |
| `report.md` | Мини-отчёт (1–2 страницы) |
| `kpi_report.csv` | Таблица KPI с PASS/FAIL |
| `input_profile.json` | Паспорт входных данных |
| `architecture.mmd` | Mermaid-диаграмма архитектуры |
| `results.csv` | Унифицированный snapshot результатов |
| `export_summary.txt` | Список всех артефактов |

## KPI
- Reasoner запущен: ✅
- 5 SPARQL-запросов разной сложности: ✅
- ≥ 3 запроса с непустым результатом после reasoning: ✅ (4 из 5)
- ≥ 3 inferred facts: ✅ (≈ 11 шт.)
