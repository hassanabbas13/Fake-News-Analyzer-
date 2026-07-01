# Fake News Analyzer (Django)

A web application that analyzes news headlines and articles for **fake-news indicators** using a transparent, rule-based scoring system. It then explains *why* it reached its verdict.

## About the Project

The Fake News Analyzer allows users to paste a news headline and article text into a form. The system scans the text for known fake news indicators, emotional language, and credibility markers. Based on what it finds, it calculates a score and classifies the article as Likely Real, Suspicious, or Likely Fake.
This is a rule based heuristic classifier, not a machine learning model. This was a deliberate design choice so the reasoning is fully transparent and explainable rather than a black box. Every analysis shows a full breakdown of the keywords and patterns that matched, so the user knows exactly why the system reached its conclusion.
All analyses are saved to the database and viewable on a dashboard with charts and statistics.

## What it does

Paste in a headline (and optional article text) and the analyzer:

1. It scans for fake news keywords like shocking, miracle, unbelievable and conspiracy. Each match adds 2 points to the score.
2. It scans for emotional and exaggeration patterns like exclamation marks, URGENT, OMG and MUST SEE. Each match adds 1 point.
3. It scans for reliable reporting keywords like study, research, peer reviewed, journal and according to. Each match subtracts 2 points.


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
## Features

The application has four main pages.

1. The Home Page introduces the project and gives users a button to start analyzing news.
2. The Analyze Page has a form where users enter a headline and article text. Once submitted, the system runs the analysis instantly.
3. The Result Page shows the classification with a color coded card. Green means Likely Real, yellow means Suspicious and red means Likely Fake. It also lists exactly which keywords were detected and how the score was calculated.
4. The Dashboard Page displays a pie chart showing the distribution of results, a bar chart of the most commonly detected fake keywords, summary statistics and a table of recent analyses.

## Run it

Make sure Python is installed on your computer. Then open a terminal and run the following commands.

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
