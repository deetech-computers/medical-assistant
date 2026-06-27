# Disease Prediction Using Machine Learning

Disease Prediction Assistant is a Flask web application that predicts a possible disease from user-selected symptoms. It uses a Decision Tree Classifier trained from a small CSV dataset and includes user accounts, saved diagnosis records, admin monitoring, and activity logging.

The project is for academic prototype use and is not a replacement for professional medical advice.

## Features

- Symptom search and multi-select diagnosis flow
- Review step before prediction
- Decision Tree based disease prediction
- Confidence-style match percentage
- Guest diagnosis support
- User registration and login
- Saved diagnosis history for logged-in users
- Admin dashboard for users, diagnoses, and activity logs
- Centralized configuration, logging, validation, and error handling
- SQLite database for local development

## Tools Used

- Python
- Flask
- Pandas
- Scikit-learn
- Joblib
- SQLite
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
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

For production, set `FLASK_CONFIG=production` and provide a secure `SECRET_KEY`.

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

## Folder Structure

```text
medical-diagnosis-assistant/
  app.py
  config.py
  requirements.txt
  data/
  docs/
  errors/
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

More details are available in:

```text
docs/project/PHASE_1_ANALYSIS_REPORT.md
docs/architecture/ARCHITECTURE.md
docs/architecture/PROJECT_ROADMAP.md
```
