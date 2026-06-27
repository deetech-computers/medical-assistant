# Changelog

All notable project changes are documented here.

## Unreleased

### Added

- Added SQLAlchemy database models for users, diagnoses, and activities.
- Added SQLAlchemy engine and session management.
- Added Alembic migration setup and initial schema migration.
- Added PostgreSQL-ready `DATABASE_URL` support.
- Added database indexes for common query paths.
- Added explicit database seed command.
- Added Phase 3 database summary documentation.
- Added versioned API routes under `/api/v1`.
- Added API health check endpoint.
- Added standardized JSON success and error response helpers.
- Added API authentication endpoints for register, login, logout, and current user.
- Added API endpoints for symptoms, predictions, user history, admin summary, users, diagnoses, and activities.
- Added API request validation helpers.
- Added API documentation.
- Added environment-based configuration for development, testing, and production.
- Added `.env.example` for safe local and deployment configuration.
- Added rotating file logging.
- Added centralized 404 and 500 error handling.
- Added repository layer for users, diagnoses, and activity logs.
- Added form validation helpers for authentication.
- Added Git ignore rules for caches, logs, local databases, and local secrets.
- Added Phase 1 project analysis documentation.

### Changed

- Updated repositories to use SQLAlchemy instead of direct SQLite queries.
- Updated database initialization to create schemas through SQLAlchemy models.
- Updated setup documentation with migration and seed commands.
- Updated app initialization to register the API blueprint.
- Updated activity tracking so automatic page view logging does not include API requests.
- Updated session configuration with safer defaults.
- Updated app initialization to load configuration from `config.py`.
- Updated database access to support configurable database paths.
- Updated authentication, diagnosis, and activity services to use repositories.
- Replaced placeholder architecture and roadmap notes with project-specific documentation.

### Fixed

- Prepared error pages so missing routes and unexpected server errors show friendly responses.

### Security

- Moved the Flask secret key into environment-driven configuration for production use.
