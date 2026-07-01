# Fake News Analyzer (Django)

A web application that analyzes news headlines and articles for **fake-news indicators** using a transparent, rule-based scoring system — then explains *why* it reached its verdict.

---

## What it does

Paste in a headline (and optional article text) and the analyzer:

1. Scans for **fake-news keywords** (clickbait/sensational terms) → `+2` each
2. Scans for **emotional/exaggeration patterns** (`!!!`, `URGENT`, `MUST SEE`, …) → `+1` each
3. Scans for **reliable-reporting keywords** (`study`, `peer reviewed`, `according to`, …) → `−2` each
4. Classifies the result:

| Score | Verdict |
|---|---|
| 0–2 | Likely Real |
| 3–6 | Suspicious |
| 7+ | Likely Fake |

It then shows a full breakdown of every keyword/pattern that matched, so the classification is explainable rather than a black box.

> This is a **rule-based heuristic classifier**, not a machine-learning model — by design, so the reasoning is fully transparent.

Analyses are saved to the database and viewable on a dashboard.

---

## Run it

```bash
python -m pip install django
python manage.py migrate
python manage.py runserver
# then open http://127.0.0.1:8000
```

---

## Layout

```
analyzer/
  analysis_engine.py   the rule-based scoring system (core logic)
  models.py            NewsAnalysis model (stored results)
  views.py             request handling
  forms.py             input form
  templates/analyzer/  home, analyze, result, dashboard pages
  static/analyzer/     styling
fake_news_project/
  settings.py, urls.py, wsgi.py
manage.py
```

---

## Tech stack

Python 3 · Django · SQLite · HTML/CSS templates
