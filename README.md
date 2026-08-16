# AI Job Agent

A LangGraph + LangChain + Firecrawl job-search automation MVP.

## Features

- Resume PDF parsing
- AI candidate profile extraction
- AI-generated job search queries
- Firecrawl web job discovery
- Job deduplication
- Resume/job matching
- Match scoring and missing-skill analysis
- SQLite persistence
- Application status tracking
- Streamlit dashboard
- Google Sheets export
- Gmail daily report
- APScheduler daily execution
- GitHub Actions workflow

## Setup

```bash
uv sync
cp .env.example .env
```

Put your resume at:

```text
uploads/resume.pdf
```

Add API keys to `.env`.

Initialize/test:

```bash
uv run python -m app.main
```

Dashboard:

```bash
uv run streamlit run app/dashboard.py
```

Scheduler:

```bash
uv run python -m app.scheduler
```

## Google Sheets

Create a Google service account, enable Sheets/Drive APIs, download its JSON credentials to:

```text
credentials/google-service-account.json
```

Share the target Google Sheet with the service-account email and set `GOOGLE_SHEET_ID`.

## Gmail

Use Google OAuth to create a Gmail token with the `gmail.send` scope. Put the resulting authorized-user JSON at:

```text
credentials/gmail-token.json
```

Set `DAILY_REPORT_EMAIL`.

## Important

This project is an automation foundation. Review job listings and application details before applying. Do not put secrets, credentials, or your private resume into Git.
