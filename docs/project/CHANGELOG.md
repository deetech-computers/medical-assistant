# Changelog

All notable project changes are documented here.

## Unreleased

### Added

- Added Render deployment configuration.
- Added Docker deployment configuration.
- Added Procfile and Python runtime declaration.
- Added Vercel Python routing configuration.
- Added deployment documentation for local, Render, Docker, Vercel, GitHub, and environment setup.
- Added production WSGI app target.
- Added Phase 7 deployment summary documentation.
- Added admin analytics service for dashboard reports, chart data, filtered records, pagination, and CSV export.
- Added Chart.js dashboard charts for daily predictions, disease analytics, weekly reports, and monthly reports.
- Added admin symptom analytics and report summary cards.
- Added diagnosis search, disease filter, record type filter, date range filters, and page-size control on the admin dashboard.
- Added `/admin/export/diagnoses` CSV export for filtered diagnosis reports.
- Added `/api/v1/admin/analytics` for reusable admin analytics data.
- Added Phase 6 admin analytics summary documentation.
- Added prediction report insights with confidence level, risk score, severity, probability rows, recommendations, care notes, and safety messaging.
- Added richer result report layout with PDF export support through the browser print flow.
- Added saved-record insight summaries for user history.
- Added prediction insight data to the versioned prediction API response.
- Added Phase 5 prediction experience summary documentation.
- Added light and dark theme support with saved user preference.
- Added color mode toggle in the sidebar.
- Added global form loading state behavior.
- Added print action behavior on result pages.
- Added improved home dashboard statistics.
- Added richer records empty state.
- Added results overview workflow preview.
- Added admin users summary cards.
- Added Phase 4 UI summary documentation.
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

- Updated requirements with Gunicorn for production WSGI serving.
- Updated shared visual styling with improved surfaces, focus states, shadows, animation, and responsive behavior.
- Updated sidebar, topbar, cards, forms, and tables for a more polished healthcare dashboard feel.
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
