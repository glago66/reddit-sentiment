# Reddit Sentiment Analysis — Platform Experience for Artists & Listeners

An end-to-end analytics engineering project built to demonstrate production-grade data pipeline skills — ingesting Reddit discussions, scoring sentiment, and surfacing prioritized platform insights through an automated Airflow pipeline and Streamlit dashboard.

> **Context:** Inspired by the SoundCloud ecosystem. Artists and listeners regularly discuss platform experiences on Reddit (r/WeAreTheMusicMakers, r/makinghiphop, r/Music, etc.). This project treats those conversations as a proxy for product feedback — identifying what's broken, what's loved, and what should be fixed first.

---

## Engineering Decisions & Methodology Notes

### Data Source: Pushshift vs Reddit API

**Original approach:** The project was designed to use the Reddit API (PRAW) for live data ingestion.

**What happened:** As of November 2024, Reddit closed self-service API access. New applications require manual approval through Reddit's Responsible Builder Policy, and approvals for non-commercial personal projects are effectively not being granted.

**Decision:** Switched to [Pushshift](https://huggingface.co/datasets/fddemarco/pushshift-reddit-comments), a publicly available archive of historical Reddit data collected since 2015. This is the same dataset used in over 100 peer-reviewed academic research papers.

**Why this is actually better for this project:**
- No API rate limits — access to years of historical data vs the Reddit API's 1000 post limit
- Richer dataset for trend analysis over time
- No credentials required — fully reproducible by anyone who clones this repo
- The ingest script is designed to be swapped back to live API if access is ever granted

**What this demonstrates:** Real-world data engineering requires adapting to infrastructure constraints. The pipeline architecture (ingest → clean → transform → load → visualize) remains identical regardless of data source.

---

## What This Project Does

1. **Ingests** Reddit comments and posts from Pushshift archives — a publicly available dataset of historical Reddit data collected since 2015, covering artist- and listener-focused subreddits
2. **Cleans & transforms** raw text data using pandas and NLTK
3. **Scores sentiment** at the comment level using TextBlob (positive / negative / neutral)
4. **Stores** structured data locally using DuckDB with SQL models designed to be portable to BigQuery in production
5. **Orchestrates** the full pipeline on a schedule using Apache Airflow DAGs
6. **Visualizes** results in a Streamlit dashboard — surfacing top issues, sentiment trends over time, and a prioritized list of platform fixes

---

## Skills Demonstrated

| Skill | How It's Used |
|---|---|
| **Apache Airflow** | DAG schedules ingestion, transformation, and sentiment scoring |
| **SQL & DuckDB** | Structured data models, aggregations, and issue prioritization queries |
| **Python & NLP** | Pushshift data ingestion, NLTK preprocessing, TextBlob sentiment scoring |
| **Streamlit** | Interactive dashboard with filters by subreddit, date, and sentiment |
| **ETL/ELT Design** | Raw → cleaned → aggregated data layers with clear separation |
| **Git & GitHub** | Version controlled, documented, and publicly reproducible |

---

## Project Structure

```
reddit-sentiment/
├── dags/               # Airflow DAGs for pipeline orchestration
├── data/
│   ├── raw/            # Raw Pushshift .zst files (gitignored)
│   └── cleaned/        # Transformed, analysis-ready data (gitignored)
├── dashboards/         # Streamlit dashboard app
├── notebooks/          # Exploratory analysis and prototyping
├── scripts/            # Ingestion, cleaning, and sentiment scoring scripts
├── .gitignore
└── README.md
```

---

## Tech Stack

- **Python 3.11**
- **Pushshift** — open Reddit data archive (historical comment and post data)
- **pandas** — data wrangling
- **NLTK + TextBlob** — NLP and sentiment analysis
- **DuckDB** — local SQL database (designed to migrate to BigQuery in production)
- **Apache Airflow** — pipeline orchestration
- **Plotly + Streamlit** — interactive dashboard
- **Git + GitHub** — version control

---

## How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/glago66/reddit-sentiment.git
cd reddit-sentiment
```

### 2. Create and activate the conda environment
```bash
conda create -n reddit-sentiment python=3.11 -y
conda activate reddit-sentiment
pip install -r requirements.txt
```

### 3. Download Pushshift data
Download monthly Reddit comment archives from:
https://huggingface.co/datasets/fddemarco/pushshift-reddit-comments

Place `.zst` files in `data/raw/` and run the ingestion script.

### 4. Run the ingestion script
```bash
python scripts/ingest.py
```

### 5. Launch the dashboard
```bash
streamlit run dashboards/app.py
```

---

## Architecture

```
Pushshift Archive (.zst files)
      │
      ▼
 Raw JSON (data/raw/)
      │
      ▼
 Cleaning & NLP (scripts/)
      │
      ▼
 DuckDB SQL Models
      │
      ▼
 Airflow DAG (scheduled)
      │
      ▼
 Streamlit Dashboard
```

---

## Status

🚧 **In Progress** — ingestion and sentiment pipeline complete, dashboard and Airflow DAGs in development.

---

## Author

Gloria L. — [github.com/glago66](https://github.com/glago66)

Analytics engineering portfolio project. Open to feedback and contributions.