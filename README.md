
# Reddit Sentiment Analysis — Platform Experience for Artists & Listeners

An end-to-end analytics engineering project built to demonstrate production-grade data pipeline skills — ingesting Reddit discussions, scoring sentiment, and surfacing prioritized platform insights through an automated Airflow pipeline and Streamlit dashboard.

> **Context:** Inspired by the SoundCloud ecosystem. Artists and listeners regularly discuss platform experiences on Reddit (r/WeAreTheMusicMakers, r/makinghiphop, r/Music, etc.). This project treats those conversations as a proxy for product feedback — identifying what's broken, what's loved, and what should be fixed first.

---

## What This Project Does

1. **Ingests** Reddit comments and posts via the official Reddit API (PRAW) across artist- and listener-focused subreddits
2. **Cleans & transforms** raw text data using pandas and NLTK
3. **Scores sentiment** at the comment level using TextBlob (positive / negative / neutral)
4. **Stores** structured data locally using DuckDB with SQL models designed to be portable to BigQuery in production
5. **Orchestrates** the full pipeline on a schedule using Apache Airflow DAGs
6. **Visualizes** results in a Streamlit dashboard — surfacing top issues, sentiment trends over time, and a prioritized list of platform fixes

---

## Skills Demonstrated

| Skill | How It's Used |
|---|---|
| **Apache Airflow** | DAG schedules Reddit ingestion, transformation, and sentiment scoring |
| **SQL & DuckDB** | Structured data models, aggregations, and issue prioritization queries |
| **Python & NLP** | PRAW API ingestion, NLTK preprocessing, TextBlob sentiment scoring |
| **Streamlit** | Interactive dashboard with filters by subreddit, date, and sentiment |
| **ETL/ELT Design** | Raw → cleaned → aggregated data layers with clear separation |
| **Git & GitHub** | Version controlled, documented, and publicly reproducible |

---

## Project Structure
```
reddit-sentiment/
├── dags/               # Airflow DAGs for pipeline orchestration
├── data/
│   ├── raw/            # Raw JSON from Reddit API (gitignored)
│   └── cleaned/        # Transformed, analysis-ready data (gitignored)
├── dashboards/         # Streamlit dashboard app
├── notebooks/          # Exploratory analysis and prototyping
├── scripts/            # Ingestion, cleaning, and sentiment scoring scripts
├── .env                # API credentials (gitignored — never committed)
├── .gitignore
└── README.md
```

---

## Tech Stack

- **Python 3.11**
- **PRAW** — Reddit API client
- **pandas** — data wrangling
- **NLTK + TextBlob** — NLP and sentiment analysis
- **DuckDB** — local SQL database (designed to migrate to BigQuery in production)
- **Apache Airflow** — pipeline orchestration
- **Plotly + Streamlit** — interactive dashboard
- **Git + GitHub** — version control

---

## How to Run Locally

### 1. Clone the repo
```
git clone https://github.com/glago66/reddit-sentiment.git
cd reddit-sentiment
```

### 2. Create and activate the conda environment
```
conda create -n reddit-sentiment python=3.11 -y
conda activate reddit-sentiment
pip install -r requirements.txt
```

### 3. Add your Reddit API credentials
Create a `.env` file in the root directory:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=reddit-sentiment-project
```
To get credentials, register a free app at https://www.reddit.com/prefs/apps

### 4. Run the ingestion script
```
python scripts/ingest.py
```

### 5. Launch the dashboard
```
streamlit run dashboards/app.py
```

---

## Architecture
```
Reddit API (PRAW)
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

Gloria L. — https://github.com/glago66

Analytics engineering portfolio project. Open to feedback and contributions.