# Medical Diagnosis Assistant Architecture

## Overview

The application is a Flask web system that predicts possible diseases from selected symptoms using a trained Decision Tree Classifier. It includes guest diagnosis, account-based history, admin monitoring, activity logging, and a responsive healthcare dashboard interface.

## Current Runtime Architecture

Browser pages are rendered with Flask and Jinja templates. The backend receives form submissions, validates input, calls service functions, stores records in SQLite, and returns HTML pages.

Flow:

```text
Templates and JavaScript
Routes
Validators
Services
Repositories
SQLAlchemy models and sessions
SQLite or PostgreSQL database
Machine learning predictor
```

## Backend Layers

### Routes

Routes are defined in:

- `routes/main_routes.py`
- `routes/auth_routes.py`
- `routes/admin_routes.py`
- `routes/api_routes.py`

Routes handle page rendering, redirects, and request coordination. Business rules should continue moving into services and validators.

### API

The application exposes a versioned JSON API under:

```text
/api/v1
```

The API supports health checks, symptoms, predictions, authentication, user history, and admin data. JSON responses use a shared success and error envelope from:

```text
utils/api_response.py
```

API request validation helpers live in:

```text
validators/api_validators.py
```

### Services

Services contain application logic:

- `services/auth_service.py`
- `services/prediction_service.py`
- `services/diagnosis_service.py`
- `services/activity_service.py`
- `services/symptom_service.py`
- `services/database_service.py`

### Repositories

Repositories isolate database queries:

- `repositories/user_repository.py`
- `repositories/diagnosis_repository.py`
- `repositories/activity_repository.py`

Repositories use SQLAlchemy sessions and return plain dictionaries to keep templates, services, and API serializers stable.

### Database Models

SQLAlchemy models live in:

```text
database/models.py
```

Session and engine management live in:

```text
database/session.py
```

### Validators

Validation helpers live in:

- `validators/form_validators.py`

The current validators cover login and registration input. Prediction validation is handled by the symptom service.

## Machine Learning Architecture

Training:

```text
data/symptoms_disease_dataset.csv
model/train_model.py
model/diagnosis_model.pkl
```

Prediction:

```text
Selected symptoms
Feature row with 0 and 1 values
DecisionTreeClassifier
Disease and confidence result
```

The model is intentionally unchanged in Phase 1.

## Database Architecture

SQLite remains the default development database. PostgreSQL is supported through `DATABASE_URL`.

Database file:

```text
data/medscope.db
```

Tables:

- `users`
- `diagnoses`
- `activities`

Tables:

- `users`
- `diagnoses`
- `activities`

Important indexes:

- `users.email`
- `users.role`
- `diagnoses.user_id`
- `diagnoses.disease`
- `diagnoses.created_at`
- `activities.user_id`
- `activities.event_type`
- `activities.created_at`

Alembic migrations live in:

```text
migrations/
```

The initial schema migration is:

```text
migrations/versions/20260627_0001_initial_schema.py
```

Configuration supports:

- `DATABASE_PATH` for SQLite
- `DATABASE_URL` for PostgreSQL or another SQLAlchemy-compatible database

## Authentication Flow

Users register or log in through Flask forms. Passwords are hashed with Werkzeug. The session stores `user_id`. Protected routes use decorators in `routes/auth_routes.py`.

Admin access is role-based. A default admin is created when the database is initialized.

## Activity Logging Flow

The application records:

- page views
- login
- logout
- registration
- diagnosis review
- prediction completion

Successful GET page views are tracked by an `after_request` hook in `app.py`.

## Error Handling

Centralized handlers are registered from:

```text
errors/handlers.py
```

The app supports friendly HTML error pages and JSON responses for clients that request JSON.

Routes under `/api/` always receive JSON errors.

## Configuration

Configuration is centralized in:

```text
config.py
```

Supported profiles:

- development
- testing
- production

Environment examples are documented in `.env.example`.

## Logging

Application logging is configured in:

```text
utils/logging_config.py
```

Logs are written to a rotating file path controlled by configuration.

## Deployment Readiness

Phase 1 prepares the app for deployment by adding:

- environment-based configuration
- centralized logging
- error handling
- repository abstraction
- ignored local runtime files
- `.env.example`

Render, Vercel, Docker, and CI/CD files are planned for later deployment phases.
