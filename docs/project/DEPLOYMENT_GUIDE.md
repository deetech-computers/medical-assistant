# Deployment Guide

## Overview

This project is a Flask web application with server-rendered pages, a versioned API, SQLAlchemy database support, and a saved Decision Tree model. The recommended production target is Render with PostgreSQL.

## Required Environment Variables

```text
FLASK_CONFIG=production
SECRET_KEY=replace-with-a-secure-random-value
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/database_name
SQLALCHEMY_ECHO=false
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
SESSION_COOKIE_SECURE=true
SESSION_LIFETIME_SECONDS=7200
```

## Health Check

Use this endpoint for deployment monitoring:

```text
/api/v1/health
```

Expected response:

```json
{
  "success": true,
  "data": {
    "status": "ok"
  }
}
```

## Render Deployment

The repository includes:

```text
render.yaml
```

Render build command:

```bash
pip install -r requirements.txt && python model/train_model.py && alembic upgrade head && python scripts/seed_database.py
```

Render start command:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

Steps:

1. Push the repository to GitHub.
2. Open Render and create a new Blueprint from the repository.
3. Confirm the web service and PostgreSQL database from `render.yaml`.
4. Let Render generate `SECRET_KEY`.
5. Deploy.
6. Open `/api/v1/health`.
7. Log in with the seeded admin account and change credentials before any public use.

## Docker Deployment

Build:

```bash
docker build -t medical-diagnosis-assistant .
```

Run:

```bash
docker run -p 5000:5000 --env-file .env medical-diagnosis-assistant
```

The Docker startup command runs migrations, seeds the default admin account, and starts Gunicorn.

## Procfile Deployment

Platforms that support Procfile can use:

```text
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

Before starting the web process, run:

```bash
alembic upgrade head
python scripts/seed_database.py
```

## Vercel Notes

The repository includes:

```text
vercel.json
```

The app is currently a Flask server-rendered project. Vercel can route requests to the Python app for demonstration, but Render is the preferred production host because the project uses a database, server sessions, model dependencies, and admin workflows.

For a separate frontend on Vercel later, keep the Flask backend on Render and call the `/api/v1` endpoints from the frontend.

## GitHub Repository

Recommended checks before pushing:

```bash
python -m py_compile app.py config.py
python model/train_model.py
alembic upgrade head
python app.py
```

Do not commit local databases, logs, `.env`, or virtual environments.

## Production Checklist

- Set `FLASK_CONFIG=production`.
- Set a strong `SECRET_KEY`.
- Use PostgreSQL through `DATABASE_URL`.
- Keep `SESSION_COOKIE_SECURE=true`.
- Run migrations before serving traffic.
- Seed the default admin only once, then change the password.
- Check `/api/v1/health` after deploy.
- Review logs after first deployment.
