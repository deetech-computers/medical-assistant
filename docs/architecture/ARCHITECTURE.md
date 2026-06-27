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
SQLite database
Machine learning predictor
```

## Backend Layers

### Routes

Routes are defined in:

- `routes/main_routes.py`
- `routes/auth_routes.py`
- `routes/admin_routes.py`

Routes handle page rendering, redirects, and request coordination. Business rules should continue moving into services and validators.

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

This prepares the app for a future SQLAlchemy and PostgreSQL migration without changing the user experience.

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

SQLite remains the active database.

Database file:

```text
data/medscope.db
```

Tables:

- `users`
- `diagnoses`
- `activities`

Configuration now supports an environment-controlled database path.

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
