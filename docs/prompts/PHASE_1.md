# PHASE 1 — Production Architecture Upgrade

Before writing ANY code, you MUST read the following project documentation completely:

docs/engineering/CODEX_INSTRUCTIONS.md

docs/engineering/SENIOR_ENGINEERING_GUIDELINES.md

docs/engineering/DEVELOPMENT_STANDARDS.md

docs/architecture/ARCHITECTURE.md

docs/architecture/PROJECT_ROADMAP.md

docs/MASTER_PROJECT_CONTEXT.md

These documents are the governing rules for this repository.

Follow them throughout this implementation.

Never violate them unless explicitly instructed.

------------------------------------------------------------

ROLE

You are acting as the Lead Software Architect and Senior Software Engineer.

Your responsibility is to transform this project into production-quality software without breaking any existing functionality.

This is an architecture improvement phase.

Do NOT redesign the UI yet.

Do NOT remove any features.

Everything must continue working exactly as before.

------------------------------------------------------------

PRIMARY OBJECTIVES

1. Analyze the existing project completely.

Understand:

- folder structure
- authentication
- prediction flow
- templates
- admin dashboard
- activity logging
- machine learning model
- database usage

Document your findings before making changes.

------------------------------------------------------------

2. Improve the project architecture.

Refactor into a clean modular architecture.

Suggested structure:

backend/

app/

routes/

services/

repositories/

models/

validators/

middleware/

utils/

config/

ml/

frontend/

templates/

components/

layouts/

static/

------------------------------------------------------------

3. Separate responsibilities.

Routes

↓

Validation

↓

Services

↓

Repositories

↓

Database

Business logic should NOT remain inside routes.

------------------------------------------------------------

4. Configuration

Create production-ready configuration.

Implement:

Development configuration

Production configuration

Testing configuration

Environment variable support

Create:

.env.example

Move secrets into environment variables.

------------------------------------------------------------

5. Logging

Implement centralized logging.

Log:

authentication

prediction requests

errors

warnings

admin actions

application startup

------------------------------------------------------------

6. Error Handling

Create centralized error handling.

Provide:

consistent JSON errors

friendly HTML errors

404 page

500 page

logging for unexpected exceptions

------------------------------------------------------------

7. Validation

Improve validation.

Validate:

forms

API requests

user input

prediction requests

authentication

------------------------------------------------------------

8. Database Preparation

Do NOT migrate to PostgreSQL yet.

Instead:

abstract database access

prepare models

prepare repository layer

ensure SQLite continues working

make PostgreSQL migration easy during Phase 3.

------------------------------------------------------------

9. Documentation

Update:

README

Architecture

Comments

Function documentation

------------------------------------------------------------

10. Deployment Preparation

Prepare project for:

GitHub

Render

Vercel

without changing deployment yet.

------------------------------------------------------------

11. Code Quality

Improve:

naming

formatting

comments

duplicate logic

function size

module organization

maintainability

readability

------------------------------------------------------------

NON-NEGOTIABLE RULES

Do NOT remove features.

Do NOT change user experience.

Do NOT redesign pages.

Do NOT retrain the ML model.

Do NOT migrate databases.

Do NOT introduce breaking changes.

Maintain backward compatibility.

------------------------------------------------------------

QUALITY CHECKLIST

Before considering Phase 1 complete:

✔ Project builds successfully

✔ Project runs successfully

✔ Existing features still work

✔ No broken routes

✔ No broken templates

✔ Authentication works

✔ Prediction works

✔ History works

✔ Admin dashboard works

✔ Activity logging works

✔ No lint errors

✔ No syntax errors

✔ Documentation updated

------------------------------------------------------------

DELIVERABLES

Provide:

1. Architecture summary

2. Folder structure (before vs after)

3. Files modified

4. Files added

5. Technical decisions

6. Future recommendations

7. Deployment notes

8. Risks identified

9. Commit message

10. Git commands

------------------------------------------------------------

AFTER COMPLETING

1. Run the application.

2. Fix every detected issue.

3. Verify all existing functionality.

4. Update CHANGELOG.md.

5. Commit changes using a professional commit message.

6. Push changes to the GitHub repository.

STOP after Phase 1.

Do NOT begin Phase 2 until instructed.