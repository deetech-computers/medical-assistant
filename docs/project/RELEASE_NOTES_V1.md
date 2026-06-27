# Release Notes Version 1.0

## Overview

Disease Prediction Assistant Version 1.0 is an academic healthcare web application for symptom-based disease prediction using a Decision Tree Classifier. It supports guest diagnosis, user accounts, saved records, admin monitoring, analytics, API access, and production deployment preparation.

## Highlights

- Symptom search and multi-select diagnosis workflow.
- Review step before prediction.
- Decision Tree prediction with confidence-style scoring.
- Result report with risk score, severity note, recommendations, and print export.
- Login, registration, and saved diagnosis history.
- Admin dashboard with analytics, filters, pagination, and CSV export.
- Versioned API under `/api/v1`.
- SQLite development database with PostgreSQL deployment support.
- Render, Docker, Procfile, and Vercel-style deployment files.
- Web manifest, favicon, robots, sitemap, and offline fallback.

## Default Local Admin

```text
Email: admin@medscope.local
Password: Admin@12345
```

Change the default credentials before public deployment.

## Recommended Deployment

Use Render with PostgreSQL. The health endpoint is:

```text
/api/v1/health
```

## Known Limits

- The dataset is intentionally small for academic demonstration.
- The result is not a clinical diagnosis.
- Larger deployment should add CSRF protection, rate limiting, and broader automated tests.
