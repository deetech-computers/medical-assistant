# Changelog

All notable project changes are documented here.

## Unreleased

### Added

- Added environment-based configuration for development, testing, and production.
- Added `.env.example` for safe local and deployment configuration.
- Added rotating file logging.
- Added centralized 404 and 500 error handling.
- Added repository layer for users, diagnoses, and activity logs.
- Added form validation helpers for authentication.
- Added Git ignore rules for caches, logs, local databases, and local secrets.
- Added Phase 1 project analysis documentation.

### Changed

- Updated app initialization to load configuration from `config.py`.
- Updated database access to support configurable database paths.
- Updated authentication, diagnosis, and activity services to use repositories.
- Replaced placeholder architecture and roadmap notes with project-specific documentation.

### Fixed

- Prepared error pages so missing routes and unexpected server errors show friendly responses.

### Security

- Moved the Flask secret key into environment-driven configuration for production use.
