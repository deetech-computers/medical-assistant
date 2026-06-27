# Master Project Context

## Project Name

Disease Prediction Assistant

## Purpose

The project is an academic healthcare web application that predicts possible diseases from selected symptoms using a trained Decision Tree Classifier. It supports guest use, user accounts, saved diagnosis history, admin monitoring, and activity tracking.

## Current Phase

Phase 3: Database Upgrade is complete.

The next planned phase is Phase 4: Premium UI/UX. That phase should improve the frontend experience without changing backend behavior or retraining the model.

## Non-Negotiable Rules

- Preserve existing functionality.
- Do not remove features.
- Do not retrain the model unless a later phase requires it.
- Keep SQLite active until the database phase.
- Keep the existing interface stable until the UI phase.
- Verify the project after changes.
- Update documentation and changelog after each phase.

## Core Flows

### Diagnosis Flow

```text
/diagnosis
/review
/predict
result page
```

### Account Flow

```text
/register
/login
/history
/logout
```

### Admin Flow

```text
/admin/
/admin/users
```

## Current Technical Stack

- Python
- Flask
- SQLite
- SQLAlchemy
- Alembic
- PostgreSQL support
- Pandas
- Scikit-learn
- Joblib
- Jinja templates
- HTML
- CSS
- JavaScript

## Deployment Direction

The app is being prepared for GitHub, Render, and later frontend deployment planning. Deployment files are planned for a later phase.
