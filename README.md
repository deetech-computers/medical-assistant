# Disease Prediction Using Machine Learning

Disease Prediction Assistant is a Flask web application that predicts a possible disease from user-selected symptoms. It uses a Decision Tree Classifier trained from a small CSV dataset and includes user accounts, saved diagnosis records, admin monitoring, and activity logging.

The project is for academic prototype use and is not a replacement for professional medical advice.

## Features

- Symptom search and multi-select diagnosis flow
- Review step before prediction
- Decision Tree based disease prediction
- Confidence-style match percentage
- Risk score, severity note, and practical care guidance
- Printable prediction report
- Guest diagnosis support
- User registration and login
- Saved diagnosis history for logged-in users
- Admin dashboard for users, diagnoses, and activity logs
- Admin analytics with charts, filters, pagination, and CSV export
- Centralized configuration, logging, validation, and error handling
- SQLite database for local development

## Tools Used

- Python
- Flask
- Pandas
- Scikit-learn
- Joblib
- SQLite
- SQLAlchemy
- Alembic
- PostgreSQL support
- HTML
- CSS
- JavaScript

## Setup

Open the project folder and install dependencies:

```bash
pip install -r requirements.txt
```

Train the model:

```bash
python model/train_model.py
```

Run the app:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Environment

Copy `.env.example` values into your deployment environment.

Important settings:

```text
FLASK_CONFIG=development
SECRET_KEY=replace-with-a-secure-random-value
DATABASE_PATH=data/medscope.db
DATABASE_URL=
SQLALCHEMY_ECHO=false
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

For production, set `FLASK_CONFIG=production`, provide a secure `SECRET_KEY`, and set `DATABASE_URL` when using PostgreSQL.

PostgreSQL example:

```text
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/database_name
```

## Database

SQLite remains the default development database. SQLAlchemy is now used for models, sessions, and repository queries.

Create or update schema with Alembic:

```bash
alembic upgrade head
```

Seed the default admin account:

```bash
python scripts/seed_database.py
```

## Default Admin

```text
Email: admin@medscope.local
Password: Admin@12345
```

Change this before any public deployment.

## Main Routes

| Route | Method | Purpose |
| --- | --- | --- |
| `/` | GET | Home page |
| `/diagnosis` | GET | Select symptoms |
| `/review` | POST | Review selected symptoms |
| `/predict` | POST | Run prediction |
| `/results` | GET | Results overview or history redirect |
| `/history` | GET | Logged-in user diagnosis records |
| `/about` | GET | Project information |
| `/login` | GET, POST | Login |
| `/register` | GET, POST | Register |
| `/logout` | GET | Logout |
| `/admin/` | GET | Admin dashboard |
| `/admin/users` | GET | Admin user list |
| `/admin/export/diagnoses` | GET | Admin CSV export |

## API Routes

Versioned API endpoints are available under:

```text
/api/v1
```

Common endpoints:

| Route | Method | Purpose |
| --- | --- | --- |
| `/api/v1/health` | GET | Backend health check |
| `/api/v1/symptoms` | GET | Symptom options |
| `/api/v1/predictions` | POST | Run prediction |
| `/api/v1/auth/register` | POST | Register account |
| `/api/v1/auth/login` | POST | Login |
| `/api/v1/auth/logout` | POST | Logout |
| `/api/v1/me` | GET | Current session |
| `/api/v1/history` | GET | Logged-in user history |
| `/api/v1/admin/summary` | GET | Admin summary |
| `/api/v1/admin/analytics` | GET | Admin analytics |

Full API notes are in:

```text
docs/project/API_DOCUMENTATION.md
```

## Folder Structure

```text
medical-diagnosis-assistant/
  app.py
  config.py
  requirements.txt
  data/
  docs/
  database/
  errors/
  migrations/
  model/
  repositories/
  routes/
  services/
  static/
  templates/
  utils/
  validators/
```

## Phase 1 Architecture Work

The app now includes:

- environment-based configuration
- repository layer for database queries
- authentication form validation
- centralized error handlers
- rotating application logs
- deployment-safe `.env.example`
- Git ignore rules for local runtime files

## Phase 3 Database Work

The app now includes:

- SQLAlchemy models for users, diagnoses, and activities
- SQLAlchemy repository queries
- Alembic migration setup
- indexed database columns for common queries
- PostgreSQL-ready `DATABASE_URL` support
- explicit seed command for the default admin user

More details are available in:

```text
docs/project/PHASE_1_ANALYSIS_REPORT.md
docs/architecture/ARCHITECTURE.md
docs/architecture/PROJECT_ROADMAP.md
```
